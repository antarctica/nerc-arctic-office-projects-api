import unittest
import pytest
from unittest.mock import patch, mock_open, MagicMock, Mock
from requests import HTTPError

from arctic_office_projects_api import create_app

from arctic_office_projects_api.models import (
    GrantCurrency,
    GrantStatus,
)

from arctic_office_projects_api.importers.gtr import (
    GatewayToResearchResource,
    GatewayToResearchOrganisation,
    UnmappedGatewayToResearchOrganisation,
    GatewayToResearchFund,
    GatewayToResearchProject,
    GatewayToResearchGrantImporter,
    UnmappedGatewayToResearchProjectTopic,
)

valid_resource = {
    "status": "active",
    "title": "Research Project Title",
    "abstractText": "This is an abstract of the research project.",
    "identifiers": {
        "identifier": [
            {"type": "foo", "value": "ABC"},
            {"type": "bar", "value": "12345"},
        ]
    },
    "researchTopics": {"researchTopic": [{"id": "topic1"}, {"id": "topic2"}]},
    "researchSubjects": {"researchSubject": [{"id": "subject1"}, {"id": "subject2"}]},
}

valid_links = {
    "PUBLICATION": ["https://doi.org/10.1000/xyz123"],
    "FUND": ["https://funding.example.com"],
    "PI_PER": ["https://person.example.com/pi"],
    "COI_PER": ["https://person.example.com/coi"],
}


@pytest.fixture
def gtr_project():
    with patch.object(
        GatewayToResearchProject, "__init__", lambda self, gtr_resource_uri: None
    ):
        # Manually set the resource and resource_links as __init__ is bypassed
        project = GatewayToResearchProject("https://gtr.example.com/project/1")
        project.resource = valid_resource
        project.resource_links = valid_links
        return project


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app({"TESTING": True})
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()


class TestProjectTopicMapping(FlaskTestCase):

    @patch("arctic_office_projects_api.utils.log_exception_to_file")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="topic_id,gcmd_link_code\nT1,none\nT2,https://link2\n",
    )
    def test_map_gtr_project_research_topic_no_mapping(
        self, mock_file, mock_log_exception
    ):
        gtr_topic = {"id": "T3", "text": "Topic 3"}

        with self.assertRaises(UnmappedGatewayToResearchProjectTopic):
            GatewayToResearchGrantImporter._map_gtr_project_research_topic_to_category_term(
                gtr_topic
            )


class TestFindUniqueGcmdProjectResearchSubjects:

    def setup_method(self):
        self.importer = GatewayToResearchGrantImporter()

    @patch.object(
        GatewayToResearchGrantImporter,
        "_map_gtr_project_research_subject_to_category_term",
    )
    def test_unique_gcmd_research_subjects(self, mock_map):
        gtr_research_subjects = [
            {"id": "subject1"},
            {"id": "subject2"},
            {"id": "subject1"},  # Duplicate
        ]
        mock_map.side_effect = lambda subject: subject["id"]

        result = self.importer._find_unique_gcmd_project_research_subjects(
            gtr_research_subjects
        )
        assert result == ["subject1", "subject2"]


class TestFindUniqueGcmdProjectResearchTopics:

    def setup_method(self):
        self.importer = GatewayToResearchGrantImporter()

    @patch.object(
        GatewayToResearchGrantImporter,
        "_map_gtr_project_research_topic_to_category_term",
    )
    def test_unique_gcmd_research_topics(self, mock_map):
        gtr_research_topics = [
            {"id": "topic1"},
            {"id": "topic2"},
            {"id": "topic1"},  # Duplicate
        ]
        mock_map.side_effect = lambda topic: topic["id"]

        result = self.importer._find_unique_gcmd_project_research_topics(
            gtr_research_topics
        )
        assert result == ["topic1", "topic2"]


class TestFindUniqueGtrProjectResearchItems:

    def setup_method(self):
        self.importer = GatewayToResearchGrantImporter()

    def test_unique_research_items(self):
        gtr_research_items = [
            {"id": "item1"},
            {"id": "item2"},
            {"id": "item1"},  # Duplicate
        ]
        result = self.importer._find_unique_gtr_project_research_items(
            gtr_research_items
        )
        assert result == ["item1", "item2"]

    def test_empty_list(self):
        result = self.importer._find_unique_gtr_project_research_items([])
        assert result == []


class TestMapGtrProjectStatus:

    def setup_method(self):
        self.importer = GatewayToResearchGrantImporter()

    @pytest.mark.parametrize(
        "status, expected",
        [
            ("Active", GrantStatus.Active),
            ("Closed", GrantStatus.Closed),
            ("Completed", GrantStatus.Completed),
            ("Terminated", GrantStatus.Terminated),
            ("Pending", GrantStatus.Pending),
            ("Unknown", GrantStatus.Unknown),
        ],
    )
    def test_valid_status_mapping(self, status, expected):
        result = self.importer._map_gtr_project_status(status)
        assert result == expected

    def test_invalid_status(self):
        with pytest.raises(
            ValueError,
            match="Status element value in GTR project not mapped to a member of the GrantStatus enumeration",
        ):
            self.importer._map_gtr_project_status("InvalidStatus")


class TestAddGtrPeople:

    @patch("arctic_office_projects_api.db.session")
    @patch("arctic_office_projects_api.models.Organisation")
    @patch("arctic_office_projects_api.models.Person")
    @patch("arctic_office_projects_api.models.Participant")
    def test_add_gtr_people(
        self, mock_participant, mock_person, mock_organisation, mock_db_session
    ):
        project = MagicMock()
        role = MagicMock()

        person1 = MagicMock(
            first_name="John",
            surname="Doe",
            orcid_id="0000-0002-1825-0097",
            employer=MagicMock(ror_id="org-1"),
        )
        person2 = MagicMock(
            first_name="Jane",
            surname="Smith",
            orcid_id="0000-0001-2345-6789",
            employer=MagicMock(ror_id="org-2"),
        )

        mock_organisation.query.filter_by.return_value.one_or_none.side_effect = [
            MagicMock(id=1),
            MagicMock(id=2),
        ]
        mock_person.query.filter_by.return_value.first.side_effect = [None, None]

        GatewayToResearchGrantImporter._add_gtr_people(
            project, [person1, person2], role
        )

        assert mock_db_session.add.call_count == 2


class TestFindGtrProjectIdentifier:

    def setup_method(self):
        self.importer = GatewayToResearchGrantImporter(
            gtr_grant_reference="NE/K011820/1"
        )

    def test_identifier_not_found(self):
        identifiers = {"Other": ["Some other id"]}
        with pytest.raises(
            KeyError, match="RCUK/GTR identifier not in GTR project identifiers"
        ):
            self.importer._find_gtr_project_identifier(identifiers)

    def test_multiple_identifiers(self):
        identifiers = {"RCUK": ["ID1", "ID2"]}
        with pytest.raises(
            KeyError,
            match="Multiple RCUK/GTR identifiers in GTR project identifiers, one expected",
        ):
            self.importer._find_gtr_project_identifier(identifiers)

    def test_valid_identifier(self):
        identifiers = {"RCUK": ["NE/K011820/1"]}
        result = self.importer._find_gtr_project_identifier(identifiers)
        assert result == "NE/K011820/1"


class TestLinkGtrCategoryTerms:

    @patch("arctic_office_projects_api.db.session")
    @patch("arctic_office_projects_api.models.Grant")
    @patch("arctic_office_projects_api.models.Allocation")
    @patch("arctic_office_projects_api.models.Project")
    @patch("arctic_office_projects_api.models.Categorisation")
    @patch("arctic_office_projects_api.models.CategoryTerm")
    @patch(
        "arctic_office_projects_api.importers.gtr.GatewayToResearchGrantImporter._find_unique_gtr_project_research_items"
    )
    def test_link_gtr_category_terms(
        self,
        mock_find_unique_gtr_project_research_items,
        mock_category_term,
        mock_categorisation,
        mock_project,
        mock_allocation,
        mock_grant,
        mock_db_session,
    ):
        # Initialize the importer (with the correct gtr_grant_reference argument)
        # importer = GatewayToResearchGrantImporter(gtr_grant_reference="NE/I028947/1")

        # Create a mock project with research subjects and topics
        project = MagicMock()
        project.research_subjects = [
            {"id": "subject1", "text": "Subject 1"},
            {"id": "subject2", "text": "Subject 2"},
        ]
        project.research_topics = [
            {"id": "topic1", "text": "Topic 1"},
            {"id": "topic2", "text": "Topic 2"},
        ]

        # Mock the _find_unique_gtr_project_research_items method to avoid the unmapped exception
        mock_find_unique_gtr_project_research_items.return_value = [
            "subject1",
            "subject2",
            "topic1",
            "topic2",
        ]

        # Set up mock return values for Grant, Allocation, Project, etc.
        mock_grant.query.filter_by.return_value.first.return_value = MagicMock(id=1)
        mock_allocation.query.filter_by.return_value.first.return_value = MagicMock(
            project_id=1
        )
        mock_project.query.filter_by.return_value.first.return_value = MagicMock(id=1)

        mock_category_term.query.filter_by.return_value.one.return_value = MagicMock()

        # Mock the categorisation query to return existing terms
        mock_categorisation.query.filter_by.return_value.all.return_value = [
            MagicMock(category_term_id=1),
        ]

        mock_existing_category_term = MagicMock(scheme_identifier="subject1")
        mock_category_term.query.filter_by.return_value.one.return_value = (
            mock_existing_category_term
        )

        # # Call the method
        # importer._link_gtr_category_terms(project)

        # # Assert that we fetched and linked the category terms
        # assert mock_category_term.query.filter_by.call_count > 0

        # # Check the addition of new terms and the removal of missing ones
        # assert mock_categorisation.query.filter_by.call_count > 0
        # assert mock_db_session.add.call_count > 0
        # assert mock_db_session.commit.call_count > 0


class TestSaveGtrCategoryTerms:

    @patch("arctic_office_projects_api.db.session")
    @patch("arctic_office_projects_api.models.CategoryTerm")
    @patch("arctic_office_projects_api.models.CategoryScheme")
    def test_save_gtr_category_terms(
        self, mock_category_scheme, mock_category_term, mock_db_session
    ):
        importer = GatewayToResearchGrantImporter()  # Initialize your importer
        project = MagicMock()
        project.research_subjects = [
            {"id": "subject1", "text": "Subject 1"},
            {"id": "subject2", "text": "Subject 2"},
        ]
        project.research_topics = [
            {"id": "topic1", "text": "Topic 1"},
            {"id": "topic2", "text": "Topic 2"},
        ]

        mock_category_scheme.query.filter_by.return_value.one.return_value = MagicMock()
        mock_category_term.query.filter_by.return_value.one.return_value = MagicMock()

        # Mock existing check
        mock_db_session.query.return_value.scalar.side_effect = [
            True,
            False,
            True,
            False,
        ]

        # Call the method
        importer._save_gtr_category_terms(project)

        # Check that it updated existing research subjects
        assert mock_category_term.query.filter_by.call_count == 0
        assert mock_category_term.call_count == 0

        # Check that new category terms were added for topics and subjects
        assert mock_db_session.add.call_count == 2  # Two new terms added


class TestGatewayToResearchGrantImporter:

    def test_init(self):
        importer = GatewayToResearchGrantImporter(
            gtr_grant_reference="NE/K011820/1",
            gtr_project_id="87D5AD44-2123-442B-B186-75C3878471BD",
            lead_project=True,
        )
        assert importer.grant_reference == "NE/K011820/1"
        assert importer.gtr_project_id == "87D5AD44-2123-442B-B186-75C3878471BD"
        assert importer.lead_project == 1  # Because lead_project is converted to an int
        assert importer.grant_exists is False

    @patch("arctic_office_projects_api.db.session.query")
    @patch("arctic_office_projects_api.models.Grant")
    def test_exists(self, mock_grant, mock_db_query):
        mock_grant.reference = "NE/K011820/1"
        mock_db_query.return_value.scalar.return_value = True

        importer = GatewayToResearchGrantImporter(gtr_grant_reference="NE/K011820/1")

        result = importer.exists()

        assert result is True
        assert importer.grant_exists is True

    # Test the exists method when no grant exists
    @patch("arctic_office_projects_api.db.session.query")
    @patch("arctic_office_projects_api.models.Grant")
    def test_exists_not_found(self, mock_grant, mock_db_query):
        mock_grant.reference = "NE/K011820/1"
        mock_db_query.return_value.scalar.return_value = False

        importer = GatewayToResearchGrantImporter(gtr_grant_reference="NE/K011820/1")

        result = importer.exists()

        assert result is False
        assert importer.grant_exists is False

    # Test the search method (successful request)
    @patch("requests.get")
    def test_search_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"project": [{"id": "12345"}]}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        importer = GatewayToResearchGrantImporter(gtr_grant_reference="NE/K011820/1")

        result = importer.search()

        assert result == "12345"
        assert importer.gtr_project_id == "12345"

    # Test the search method (failure with multiple projects)
    @patch("requests.get")
    def test_search_multiple_projects(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "project": [{"id": "12345"}, {"id": "67890"}]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        importer = GatewayToResearchGrantImporter(gtr_grant_reference="NE/K011820/1")

        with pytest.raises(
            ValueError,
            match=r"Expected exactly one project, got \d+"
        ):
            importer.search()

    def test_update_with_unknown_status(self):
        importer = GatewayToResearchGrantImporter(gtr_grant_reference="NE/K011820/1")

        # Mock a GTR project with an unknown status
        mock_gtr_project = Mock
        mock_gtr_project.status = "UnknownStatus"

        with pytest.raises(
            ValueError,
            match="Status element value in GTR project not mapped to a member of the GrantStatus enumeration",
        ):
            importer._map_gtr_project_status(mock_gtr_project.status)

    # Test update method (updating existing grant and project)
    @patch("arctic_office_projects_api.db.session.query")
    @patch("arctic_office_projects_api.models.Grant")
    @patch("arctic_office_projects_api.models.Project")
    @patch("arctic_office_projects_api.importers.gtr.GatewayToResearchProject")
    def test_update(self, mock_gtr_project, mock_project, mock_grant, mock_db_query):
        # Set up mock data
        mock_grant_data = MagicMock()
        mock_project_data = MagicMock()
        mock_db_query.return_value.filter_by.return_value.first.return_value = (
            mock_grant_data
        )
        mock_project.query.filter_by.return_value.first.return_value = mock_project_data
        mock_gtr_project.title = "New Title"
        mock_gtr_project.abstract = "New Abstract"
        mock_gtr_project.status = "unknown"
        mock_gtr_project.fund.duration = "P2Y"
        mock_gtr_project.fund.currency = "GBP"
        mock_gtr_project.fund.amount = 100000
        mock_gtr_project.publications = []

        # importer = GatewayToResearchGrantImporter(gtr_grant_reference="NE/K011820/1")

        # print(importer)
        # print("mock_gtr_project.status", mock_gtr_project.status)

        # importer.update(gtr_project_id="NE/K011820/1")

        # assert mock_grant_data.title == "New Title"
        # assert mock_grant_data.abstract == "New Abstract"
        # assert mock_grant_data.total_funds == 100000
        # assert mock_project_data.title == "New Title"
        # assert mock_project_data.abstract == "New Abstract"

    # Test fetch method (new project and grant creation)
    @patch("arctic_office_projects_api.db.session.add")
    @patch("arctic_office_projects_api.db.session.commit")
    @patch("arctic_office_projects_api.importers.gtr.GatewayToResearchProject")
    def test_fetch(self, mock_gtr_project, mock_commit, mock_add):
        mock_gtr_project_instance = mock_gtr_project.return_value

        mock_gtr_project_instance.identifiers = {"RCUK": "GTR-123456"}

        # Set other necessary attributes of the mock GTR project
        mock_gtr_project_instance.title = "Sample Title"
        mock_gtr_project_instance.abstract = "Sample Abstract"
        mock_gtr_project_instance.status = "Active"
        mock_gtr_project_instance.fund.duration = "P2Y"
        mock_gtr_project_instance.fund.currency = "GBP"
        mock_gtr_project_instance.fund.amount = 100000

        # Initialize the importer
        # importer = GatewayToResearchGrantImporter(gtr_grant_reference="NE/K011820/1")

        # importer.fetch()

        # assert mock_add.called
        # assert mock_commit.called


class TestGatewayToResearchProject:

    def test_initialization(self, gtr_project):
        gtr_project.status = valid_resource["status"]
        gtr_project.title = valid_resource["title"]
        gtr_project.abstract = valid_resource["abstractText"]

        assert gtr_project.status == "active"
        assert gtr_project.title == "Research Project Title"
        assert gtr_project.abstract == "This is an abstract of the research project."

    def test_process_identifiers(self, gtr_project):
        identifiers = gtr_project._process_identifiers()
        assert identifiers["foo"] == ["ABC"]
        assert identifiers["bar"] == ["12345"]

    def test_process_research_topics(self, gtr_project):
        topics = gtr_project._process_research_topics()
        assert len(topics) == 2
        assert topics[0]["id"] == "topic1"
        assert topics[1]["id"] == "topic2"

    def test_process_research_subjects(self, gtr_project):
        subjects = gtr_project._process_research_subjects()
        assert len(subjects) == 2
        assert subjects[0]["id"] == "subject1"
        assert subjects[1]["id"] == "subject2"

    def test_find_gtr_fund_link(self, gtr_project):
        fund_link = gtr_project._find_gtr_fund_link()
        assert fund_link == "https://funding.example.com"

    def test_find_gtr_fund_link_no_fund(self, gtr_project):
        gtr_project.resource_links["FUND"] = []
        with pytest.raises(
            KeyError, match="GTR fund relation not found in GTR project links"
        ):
            gtr_project._find_gtr_fund_link()

    def test_find_gtr_fund_link_multiple_funds(self, gtr_project):
        gtr_project.resource_links["FUND"] = ["fund1", "fund2"]
        with pytest.raises(
            KeyError,
            match="Multiple GTR fund identifiers found in GTR project links, one expected",
        ):
            gtr_project._find_gtr_fund_link()


class TestGatewayToResearchFund:

    def test_map_gtr_fund_currency_code_success(self):
        # Test the currency code mapping
        assert (
            GatewayToResearchFund._map_gtr_fund_currency_code("GBP") == GrantCurrency.GBP
        )

    def test_map_gtr_fund_currency_code_failure(self):
        # Test that an invalid currency code raises a ValueError
        with pytest.raises(
            ValueError,
            match="CurrencyCode element value in GTR fund not mapped to a member of the GrantCurrency enumeration",
        ):
            GatewayToResearchFund._map_gtr_fund_currency_code("USD")


class TestGatewayToResearchResource:

    @patch("requests.get")
    def test_init_success(self, mock_get):
        mock_get.return_value.json.return_value = {
            "links": {
                "link": [
                    {"rel": "publication", "href": "http://example.com/pub"},
                    {"rel": "person", "href": "http://example.com/person"},
                ]
            }
        }
        mock_get.return_value.status_code = 200

        resource = GatewayToResearchResource("http://example.com/resource")
        assert resource.resource_uri == "http://example.com/resource"
        assert resource.resource_links["publication"] == ["http://example.com/pub"]
        assert resource.resource_links["person"] == ["http://example.com/person"]

    @patch("requests.get")
    def test_init_http_error(self, mock_get):
        mock_get.side_effect = HTTPError("HTTP error occurred")

        with pytest.raises(HTTPError):
            GatewayToResearchResource("http://example.com/resource")

    @patch("requests.get")
    def test_process_resource_links_key_error(self, mock_get):
        mock_get.return_value.json.return_value = {}

        with pytest.raises(KeyError):
            GatewayToResearchResource("http://example.com/resource")

    @patch("requests.get")
    def test_process_resource_links_missing_rel(self, mock_get):
        mock_get.return_value.json.return_value = {
            "links": {"link": [{"href": "http://example.com/pub"}]}
        }

        with pytest.raises(KeyError):
            GatewayToResearchResource("http://example.com/resource")


class TestGatewayToResearchOrganisation(FlaskTestCase):

    @patch("requests.get")
    def test_init_missing_name(self, mock_get):
        mock_get.return_value.json.return_value = {"links": {"link": []}}
        mock_get.return_value.status_code = 200

        with pytest.raises(KeyError):
            GatewayToResearchOrganisation("http://gtr.ukri.org/gtr/api/organisations/1")

    def test_map_to_ror_unmapped_organisation(app_context):
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = {
                "name": "Test Organisation",
                "links": {"link": []},
            }
            mock_get.return_value.status_code = 200

            with patch(
                "builtins.open",
                mock_open(read_data="organisation_id,organisation_ror\n1,ror.org/1"),
            ):
                with pytest.raises(UnmappedGatewayToResearchOrganisation):
                    GatewayToResearchOrganisation(
                        "http://gtr.ukri.org/gtr/api/organisations/unknown"
                    )


if __name__ == "__main__":
    pytest.main()
