import requests
import csv

from datetime import date, datetime, timezone
from typing import Dict, Optional, List
from urllib.parse import quote as url_encode

from click import echo, style
from flask import current_app as app
from psycopg2.extras import DateRange
from requests import HTTPError

# noinspection PyPackageRequirements
from sqlalchemy import exists, and_
from sqlalchemy_utils import Ltree

from arctic_office_projects_api.errors import AppException
from arctic_office_projects_api.extensions import db
from arctic_office_projects_api.utils import generate_neutral_id, log_exception_to_file
from arctic_office_projects_api.models import (
    Categorisation,
    CategoryScheme,
    CategoryTerm,
    Grant,
    GrantStatus,
    GrantCurrency,
    Organisation,
    Project,
    Allocation,
    Person,
    Participant,
    ParticipantRole,
)


# Exceptions
class UnmappedGatewayToResearchOrganisation(AppException):
    title = "Unmapped Gateway to Research organisation"
    detail = "A Gateway to Research organisation has not been mapped to an application Organisation via a GRID ID"


class UnmappedGatewayToResearchPerson(AppException):
    title = "Unmapped Gateway to Research person"
    detail = "A Gateway to Research person has not been mapped to an application Person via a ORCID iD"


class UnmappedGatewayToResearchProjectTopic(AppException):
    title = "Unmapped Gateway to Research topic"
    detail = (
        "A Gateway to Research topic has not been mapped to an application category term via a "
        "scheme identifier"
    )


class UnmappedGatewayToResearchProjectSubject(AppException):
    title = "Unmapped Gateway to Research subject"
    detail = (
        "A Gateway to Research subject has not been mapped to an application category term via a "
        "scheme identifier"
    )


class GatewayToResearchResource:
    """
    Represents the API response for a GTR resource

    These have a common structure with each resource identified by a UUID and containing a collection of attributes,
    including a 'links' attribute. This is a list of links to other resources with a 'rel' attribute indicating its
    type/person (e.g. a publication or a person).
    """

    def __init__(self, gtr_resource_uri: str):
        """
        :type gtr_resource_uri: str
        :param gtr_resource_uri: URI of a Gateway to Research resource
        """
        self.resource = self._fetch(gtr_resource_uri=gtr_resource_uri)
        self.resource_uri = gtr_resource_uri
        self.resource_links = self._process_resource_links()

    @staticmethod
    def _fetch(gtr_resource_uri: str) -> Optional[dict]:
        """
        Fetches a GTR resource from the GTR API

        :type gtr_resource_uri: str
        :param gtr_resource_uri: URI of a Gateway to Research resource

        :rtype dict
        :return GTR API response body - typically a resource
        """
        try:
            gtr_resource_response = requests.get(
                url=gtr_resource_uri,
                headers={"accept": "application/vnd.rcuk.gtr.json-v7"},
                timeout=100,
            )
            gtr_resource_response.raise_for_status()
            return gtr_resource_response.json()
        except (HTTPError, KeyError, ValueError) as e:
            raise e

    def _process_resource_links(self) -> Dict[str, List[str]]:
        """
        Organises links in a GTR response by their 'rel' property (type)

        Links in a GTR response are a unstructured list, with each item containing a URI and 'rel' attribute describing
        it's type/purpose (i.e. publication or person).

        Typically when these links are used, only links of a specific 'rel' are useful. This method converts the links
        list into a dict of links indexed by 'rel'.

        E.g.

        [
            {'uri': 'https://www.example.com/foo1', 'rel': 'foo'},
            {'uri': 'https://www.example.com/foo2', 'rel': 'foo'},
            {'uri': 'https://www.example.com/bar1', 'rel': 'bar'}
        ]

        Becomes:

        {
            'foo': [
                {'uri': 'https://www.example.com/foo1', 'rel': 'foo'},
                {'uri': 'https://www.example.com/foo2', 'rel': 'foo'}
            ],
            'bar': [
                {'uri': 'https://www.example.com/bar1', 'rel': 'bar'}
            ]
        }

        :rtype dict
        :returns links in a GTR resource indexed by their 'rel' property
        """

        if "links" not in self.resource:
            raise KeyError("Links element not in GTR resource")
        if "link" not in self.resource["links"]:
            raise KeyError("Links list element not in GTR resource")

        links = {}
        for link in self.resource["links"]["link"]:

            if "rel" not in link:
                raise KeyError("Rel type not in GTR resource link")
            if "href" not in link:
                raise KeyError("Href not in GTR resource link")
            if link["rel"] not in links.keys():
                links[link["rel"]] = []

            # Remove http://internal-gtr-tomcat-alb-611010599.eu-west-2.elb.amazonaws.com:8080
            # Replace with https://gtr.ukri.org

            link_href = link["href"]

            link_base_url = link["href"].split(":")
            if (
                link_base_url[1] == "//internal-gtr-tomcat-alb-611010599.eu-west-2.elb.amazonaws.com"
            ):
                link_href = link["href"].replace(
                    "http://internal-gtr-tomcat-alb-611010599.eu-west-2.elb.amazonaws.com:8080",
                    "https://gtr.ukri.org",
                )

            links[link["rel"]].append(link_href)

        return links


class GatewayToResearchOrganisation(GatewayToResearchResource):
    """
    Represents the API response for a series of GTR resources that all represent an organisation as an entity

    This class is intended to hold any common functionality shared by these related classes.
    """

    def __init__(self, gtr_resource_uri: str):
        """
        :type gtr_resource_uri: str
        :param gtr_resource_uri: URI of a Gateway to Research resource
        """
        super().__init__(gtr_resource_uri)

        if "name" not in self.resource:
            raise KeyError("Name element not in GTR organisation")
        self.name = self.resource["name"]

        self.ror_id = self._map_to_ror()

    def _ror_dict(resource_uri) -> str:

        csv_file = "/usr/src/app/arctic_office_projects_api/bulk_importer/csvs/project_organisations.csv"

        gtr_path = "http://gtr.ukri.org/gtr/api/organisations/"
        _ror_list = []

        try:
            with open(csv_file, "r", newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                next(reader, None)  # skip the headers
                for row in reader:
                    _ror_dict = {
                        "organisation_uri": gtr_path + row["organisation_id"],
                        "ror_uri": row["organisation_ror"],
                    }
                    _ror_list.append(_ror_dict)

        except FileNotFoundError:
            print(f"File not found: {csv_file}")
        except KeyError as e:
            print(f"Missing expected column: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        for ror_item in _ror_list:
            if resource_uri == ror_item["organisation_uri"]:
                return ror_item["ror_uri"]

    def _map_to_ror(self) -> str:
        """
        Organisations in this project are identified by ROR IDs (https://ror.org)

        These mappings are defined in the _ror_dict method.

        :rtype str
        :return for a given GTR resource URI, a corresponding ROR ID as a URI
        """
        _ror_url = GatewayToResearchOrganisation._ror_dict(self.resource_uri)
        if isinstance(_ror_url, str):
            return _ror_url

        raise UnmappedGatewayToResearchOrganisation(
            meta={"gtr_organisation": {"resource_uri": self.resource_uri}}
        )


class GatewayToResearchFunder(GatewayToResearchOrganisation):
    """
    Represents a GTR Funder, associated with a GTR Fund as the funding organisation

    All logic for this resource is defined in it's parent class.
    """

    pass


class GatewayToResearchEmployer(GatewayToResearchOrganisation):
    """
    Represents a GTR Employer, associated with a GTR Person as their host organisation

    All logic for this resource is defined in it's parent class.
    """

    pass


class GatewayToResearchFund(GatewayToResearchResource):
    """
    Represents a GTR Fund, associated with a GTR Project containing funding and duration information for a grant

    GTR Funds are associate with a GTR Funder (funding organisation).
    """

    def __init__(self, gtr_resource_uri: str):
        """
        :type gtr_resource_uri: str
        :param gtr_resource_uri: URI of a Gateway to Research resource
        """
        super().__init__(gtr_resource_uri)

        self.funder = GatewayToResearchFunder(
            gtr_resource_uri=self._find_gtr_funder_link()
        )

        if "start" not in self.resource:
            raise KeyError("Start date element not in GTR fund")
        if "end" not in self.resource:
            raise KeyError("End date element not in GTR fund")

        self.duration = DateRange(
            self._process_gtr_datetime(self.resource["start"]),
            self._process_gtr_datetime(self.resource["end"]),
        )

        if "valuePounds" not in self.resource:
            raise KeyError("ValuePounds element not in GTR fund")
        if "currencyCode" not in self.resource["valuePounds"]:
            raise KeyError("CurrencyCode element not in GTR fund")
        if "amount" not in self.resource["valuePounds"]:
            raise KeyError("Amount element not in GTR fund")

        self.currency = self._map_gtr_fund_currency_code(
            self.resource["valuePounds"]["currencyCode"]
        )
        self.amount = self.resource["valuePounds"]["amount"]

    @staticmethod
    def _map_gtr_fund_currency_code(currency_code: str) -> GrantCurrency:
        """
        Maps a currency type in a GTR fund to a member of the GrantCurrency enumeration used by this project

        :type currency_code: str
        :param currency_code: currency type in a GTR fund

        :rtype GrantCurrency
        :return member of the GrantCurrency enumeration corresponding to the currency type in a GTR fund
        """
        if currency_code == "GBP":
            return GrantCurrency.GBP

        raise ValueError(
            "CurrencyCode element value in GTR fund not mapped to a member of the GrantCurrency "
            "enumeration"
        )

    def _find_gtr_funder_link(self) -> str:
        """
        Gets the resource URI of the GTR Funder resource for a GTR Fund

        I.e. The URI to the funder of a grant.

        If there isn't a single funder resource an appropriate exception is raised instead.

        :rtype str
        :return URI of the GTR Funder resource for a GTR Fund
        """
        if "FUNDER" not in self.resource_links.keys():
            raise KeyError("GTR funder relation not found in GTR fund links")
        if len(self.resource_links["FUNDER"]) == 0:
            raise KeyError("GTR funder relation not found in GTR fund links")
        if len(self.resource_links["FUNDER"]) > 1:
            raise KeyError(
                "Multiple GTR funder identifiers found in GTR fund links, one expected"
            )

        return self.resource_links["FUNDER"][0]

    @staticmethod
    def _process_gtr_datetime(gtr_date: str) -> date:
        """
        Converts a GTR datetime into a Python date object

        Gateway to Research's JSON encoding uses Unix timestamps with milliseconds and which first need correcting and
        then returned as a date, as durations in this project are whole days.

        :type gtr_date: str
        :param gtr_date: GTR datetime

        :rtype date
        :return: GTR datetime encoded as a python date
        """
        timestamp = int(gtr_date) / 1000
        return datetime.fromtimestamp(timestamp, timezone.utc).date()


class GatewayToResearchPerson(GatewayToResearchResource):
    """
    Represents a GTR Person, associated with one or more GTR Projects based on their role

    GTR People are associated with a GTR Employer (host organisation).
    """

    def __init__(self, gtr_resource_uri: str):
        """
        :type gtr_resource_uri: str
        :param gtr_resource_uri: URI of a Gateway to Research resource
        """
        super().__init__(gtr_resource_uri)

        self.employer = GatewayToResearchEmployer(
            gtr_resource_uri=self._find_gtr_employer_link()
        )

        self.first_name = None
        if "firstName" in self.resource:
            self.first_name = self.resource["firstName"]
        self.surname = None
        if "surname" in self.resource:
            self.surname = self.resource["surname"]
        self.orcid_id = None
        if "orcidId" in self.resource:
            if self.resource["orcidId"] is not None:
                self.orcid_id = f"https://orcid.org/{self.resource['orcidId']}"

    def _find_gtr_employer_link(self):
        """
        Gets the resource URI of the GTR Employer resource for a GTR Person

        I.e. The URI to the employer of a person.

        If there isn't a single employer resource an appropriate exception is raised instead.

        :rtype str
        :return URI of the GTR Employer resource for a GTR Person
        """
        if "EMPLOYED" not in self.resource_links.keys():
            raise KeyError("GTR employer relation not found in GTR person links")
        if len(self.resource_links["EMPLOYED"]) == 0:
            raise KeyError("GTR employer relation not found in GTR person links")
        if len(self.resource_links["EMPLOYED"]) > 1:
            raise KeyError(
                "Multiple GTR employer relations found in GTR person links, one expected"
            )

        return self.resource_links["EMPLOYED"][0]

    def _map_id_to_orcid_ids(self):
        """
        People in this project are identified by ORCID iDs (https://www.orcid.org), however these are not always
        available from GTR and no other identifiers are available to automatically determine the ORCID iD of a person
        based on their GTR resource ID.

        In some cases an individual has an ORCID iD, but GTR is not aware of it. In others an individual may not have an
        ORCID iD, or it isn't possible to identify which is theirs.

        In cases where an ORCID iD is known for an individual, but not by GTR, it can be defined manually in this
        method.

        These mappings are currently defined using a simple if statement, but in future a more scalable solution will
        be needed.

        :rtype str
        :return for a given GTR resource URI, a corresponding ORCID iD as a URL
        """

        csv_file = "/usr/src/app/arctic_office_projects_api/bulk_importer/csvs/project_people.csv"
        gtr_person_url = "https://gtr.ukri.org:443/gtr/api/"
        gtr_people_orcid_id_mappings = {}

        try:
            with open(csv_file, "r", newline="") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    key = gtr_person_url + row["gtr_person"]
                    value = row["orcid"]
                    gtr_people_orcid_id_mappings[key] = value
                    gtr_people_orcid_id_mappings.append({key: value})

        except FileNotFoundError:
            print(f"File not found: {csv_file}")
        except Exception as e:
            print(f"An error occurred with persons mapping: {e}")

        if self.resource_uri not in gtr_people_orcid_id_mappings.keys():
            raise UnmappedGatewayToResearchPerson(
                meta={"gtr_person": {"resource_uri": self.resource_uri}}
            )

        self.orcid_id = gtr_people_orcid_id_mappings[self.resource_uri]


class GatewayToResearchPublication(GatewayToResearchResource):
    """
    Represents a GTR Publication, associated with a GTR Project
    """

    def __init__(self, gtr_resource_uri: str):
        """
        :type gtr_resource_uri: str
        :param gtr_resource_uri: URI of a Gateway to Research resource
        """
        super().__init__(gtr_resource_uri)

        if "doi" in self.resource:
            self.doi = self.resource["doi"]
        else:
            self.doi = None


class GatewayToResearchProject(GatewayToResearchResource):
    """
    Represents a GTR Project, which is considered a grant by this project

    GTR projects are associated various other resources, including funding information, publications and people.
    """

    def __init__(self, gtr_resource_uri: str):
        """
        :type gtr_resource_uri: str
        :param gtr_resource_uri: URI of a Gateway to Research resource
        """

        super().__init__(gtr_resource_uri)

        self.identifiers = self._process_identifiers()
        # print(self.identifiers)
        self.research_topics = self._process_research_topics()
        # print(self.research_topics)
        self.research_subjects = self._process_research_subjects()
        # print(self.research_subjects)
        self.publications = self._process_publications()
        # print(self.publications)
        self.fund = GatewayToResearchFund(gtr_resource_uri=self._find_gtr_fund_link())
        # print (self.fund)
        self.principle_investigators = self._process_people(relation="PI_PER")
        self.co_investigators = self._process_people(relation="COI_PER")

        if "status" not in self.resource:
            raise KeyError("Status element not in GTR project")
        self.status = self.resource["status"]
        if "title" not in self.resource:
            raise KeyError("Title element not in GTR project")
        self.title = self.resource["title"]

        self.abstract = None
        if "abstractText" in self.resource:
            self.abstract = self.resource["abstractText"]

    def _process_identifiers(self) -> Dict[str, List[str]]:
        """
        Organises identifiers in a GTR Project by their 'type' property

        Identifiers in a GTR Project are a unstructured list, with each item containing an identifier and 'type'
        attribute describing it's type/authority (i.e. assigned by a funding agency).

        Typically when these identifiers are used, only identifiers of a specific 'type' are useful. This method
        converts the identifiers list into a dict of identifiers indexed by 'type'.

        E.g.

        [
            {'identifier': 'ABC', 'rel': 'foo'},
            {'identifier': 'ABC/1', 'rel': 'foo'},
            {'identifier': '123454932842', 'rel': 'bar'}
        ]

        Becomes:

        {
            'foo': [
                {'identifier': 'ABC', 'rel': 'foo'},
                {'identifier': 'ABC/1', 'rel': 'foo'}
            ],
            'bar': [
                {'identifier': '123454932842', 'rel': 'bar'}
            ]
        }

        :rtype dict
        :returns links in a GTR resource indexed by their 'rel' property
        """
        project_references = {}

        if "identifiers" not in self.resource:
            raise KeyError("Identifiers element not in GTR project")
        if "identifier" not in self.resource["identifiers"]:
            raise KeyError("Identifiers list element not in GTR project")

        for gtr_identifier in self.resource["identifiers"]["identifier"]:
            if "type" not in gtr_identifier:
                raise KeyError("Type attribute not in GTR project identifier")
            if gtr_identifier["type"] not in project_references:
                project_references[gtr_identifier["type"]] = []
            if "value" not in gtr_identifier:
                raise KeyError("Value attribute not in GTR project identifier")

            project_references[gtr_identifier["type"]].append(gtr_identifier["value"])

        return project_references

    def _process_research_topics(self) -> List[dict]:
        """
        Here we process the research topics from the GTR resource into a list

        :rtype list
        :return list of research topic classifications for a GTR project
        """
        gtr_project_topics = []
        if "researchTopics" in self.resource:
            if "researchTopic" in self.resource["researchTopics"]:
                if len(self.resource["researchTopics"]["researchTopic"]) > 0:
                    for gtr_research_topic in self.resource["researchTopics"][
                        "researchTopic"
                    ]:
                        if "id" in gtr_research_topic:
                            gtr_project_topics.append(gtr_research_topic)

        return gtr_project_topics

    def _process_research_subjects(self) -> List[dict]:
        """
        GTR Projects are classified by both 'Subjects' and 'Topics', this project uses
        categories that cover the domains of GTR subjects and topics and therefore don't need to be separate.

        Here we process the research subjects into its own list

        :rtype list
        :return combined list of classifications for a GTR project
        """
        gtr_project_subjects = []
        if "researchSubjects" in self.resource:
            if "researchSubject" in self.resource["researchSubjects"]:
                if len(self.resource["researchSubjects"]["researchSubject"]) > 0:
                    for gtr_research_subject in self.resource["researchSubjects"][
                        "researchSubject"
                    ]:
                        if "id" in gtr_research_subject:
                            gtr_project_subjects.append(gtr_research_subject)

        return gtr_project_subjects

    def _process_publications(self) -> List[str]:
        """
        Fetches each publication associated with a GTR Project

        In GTR, publications a full resource, however in this project, they are just a list of DOIs.

        :rtype list
        :return list of publication DOIs
        """
        publications = []
        if "PUBLICATION" in self.resource_links:
            for publication_uri in self.resource_links["PUBLICATION"]:
                publication = GatewayToResearchPublication(
                    gtr_resource_uri=publication_uri
                )
                publications.append(publication.doi)

        return publications

    def _process_people(self, relation: str) -> List[GatewayToResearchPerson]:
        """
        Fetches people associated with a GTR Project with a given relation

        I.e. Fetches all the Co-Investigator's for a project.

        :rtype list
        :return list of GTR People resources for further processing
        """
        people = []
        if relation in self.resource_links.keys():
            for person in self.resource_links[relation]:
                people.append(GatewayToResearchPerson(gtr_resource_uri=person))
        return people

    def _find_gtr_fund_link(self):
        """
        Gets the resource URI of the GTR Fund resource for a GTR Project

        I.e. The URI to the funding information for a project.

        If there isn't a single fund resource an appropriate exception is raised instead.

        :rtype str
        :return URI of the GTR Funder resource for a GTR Fund
        """

        if "FUND" not in self.resource_links.keys():
            raise KeyError("GTR fund relation not found in GTR project links")
        if len(self.resource_links["FUND"]) == 0:
            raise KeyError("GTR fund relation not found in GTR project links")
        if len(self.resource_links["FUND"]) > 1:
            raise KeyError(
                "Multiple GTR fund identifiers found in GTR project links, one expected"
            )

        return self.resource_links["FUND"][0]


class GatewayToResearchGrantImporter:
    """
    Mechanism to create Projects and associated resources from resources in Gateway to Research

    Some resources, such as people, are effectively 1:1 mappings but with different attribute names. Others, such as
    projects are created by taking attributes from across different GTR resources, either directly or using lookups to
    other resources in this project.

    GTR projects are loosely equivalent to Grants in this project.
    """

    def __init__(
        self,
        gtr_grant_reference: str = None,
        gtr_project_id: str = None,
        lead_project: str = None,
    ):
        """
        :type gtr_grant_reference: str
        :param gtr_grant_reference: Gateway to Research grant reference (e.g. 'NE/K011820/1')
        :type gtr_project_id: str
        :param gtr_grant_reference: Gateway to Research project ID (e.g. '87D5AD44-2123-442B-B186-75C3878471BD')
        :type lead_project: bool
        :param lead_project: Is the project/grant the lead for a split award?
        """
        self.grant_reference = gtr_grant_reference
        self.gtr_project_id = gtr_project_id
        self.lead_project = (
            int(lead_project) if lead_project is not None else 0
        )  # Handle NoneType safely
        self.grant_exists = False

    def exists(self) -> bool:
        """
        Checks whether a Gateway to Research project has previously been imported as a Grant

        :rtype bool
        :return: Whether a GTR project has already been imported as a Grant
        """
        data_exists = db.session.query(
            exists().where(Grant.reference == self.grant_reference)
        ).scalar()

        if data_exists:
            self.grant_exists = True

        return data_exists

    def update(self, gtr_project_id):
        """
        Updates a Gateway to Research project & grant which have previously been imported

        :rtype bool
        :return: Whether a GTR project has already been imported as a Grant
        """

        gtr_project = GatewayToResearchProject(
            gtr_resource_uri=f"https://gtr.ukri.org/gtr/api/projects/{gtr_project_id}"
        )

        # Update the Grant
        grant_db_data = (
            db.session.query(Grant).filter_by(reference=self.grant_reference).first()
        )
        grant_db_data.title = gtr_project.title
        grant_db_data.abstract = gtr_project.abstract
        grant_db_data.status = self._map_gtr_project_status(status=gtr_project.status)
        grant_db_data.duration = gtr_project.fund.duration
        grant_db_data.total_funds_currency = gtr_project.fund.currency
        grant_db_data.total_funds = gtr_project.fund.amount
        grant_db_data.publications = gtr_project.publications
        grant_db_data.lead_project = self.lead_project
        grant_db_data.funder = Organisation.query.filter_by(
            ror_identifier=gtr_project.fund.funder.ror_id
        ).one_or_none()

        # Update the Project
        project_db_data = Project.query.filter_by(
            grant_reference=self.grant_reference
        ).first()
        project_db_data.title = grant_db_data.title
        project_db_data.abstract = grant_db_data.abstract
        project_db_data.project_duration = grant_db_data.duration
        project_db_data.access_duration = DateRange(grant_db_data.duration.lower, None)
        project_db_data.publications = grant_db_data.publications
        project_db_data.lead_project = self.lead_project

        db.session.commit()

    def search(self) -> Optional[str]:
        """
        Given a grant reference, find a single corresponding GTR project resource ID

        If there isn't, an appropriate exception is raised instead

        :rtype str
        :return ID of a GTR project resource
        """
        try:
            gtr_project_response = requests.get(
                url=f'{"https://gtr.ukri.org/gtr/api/projects"}',
                params={"q": url_encode(self.grant_reference), "f": "pro.gr"},
                headers={"accept": "application/vnd.rcuk.gtr.json-v7"},
                timeout=100,
            )
            gtr_project_response.raise_for_status()
            gtr_project_data = gtr_project_response.json()
            if "project" not in gtr_project_data:
                raise KeyError("Project element not in GTR response")
            if len(gtr_project_data["project"]) != 1:
                raise ValueError(
                    "Multiple project elements found in GTR response, only expected one"
                )

            self.gtr_project_id = gtr_project_data["project"][0]["id"]
            return self.gtr_project_id
        except (HTTPError, KeyError, ValueError) as e:
            raise e

    def fetch(self):
        """
        Fetches a given GTR project, and associated resources to create and persist resources in this project

        A series of GTR resources are retrieved and re-arranged into resources in this project. For resources shared
        across this project (i.e. people) suitable checks are made to ensure duplicates are not created.

        Requirements:
            * where Organisations are used (Grant funders and People organisations), these must already exist
            * where Category Terms are used, these must already exist

        Appropriate mappings will also need to be made in:
            * GatewayToResearchOrganisation._map_to_ror_id()
            * GatewayToResearchPerson._map_id_to_orcid_ids()
            * _map_gtr_project_research_topic_to_category_term()
            * _map_gtr_project_research_subject_to_category_term()
        """
        gtr_project = GatewayToResearchProject(
            gtr_resource_uri=f"https://gtr.ukri.org/gtr/api/projects/{self.gtr_project_id}"
        )

        # If the grant exists - update it & the project too
        if self.grant_exists is True:

            project_reference = self._find_gtr_project_identifier(
                identifiers=gtr_project.identifiers
            )

            grant = Grant.query.filter_by(reference=project_reference).first()

            grant.title = gtr_project.title
            grant.abstract = gtr_project.abstract
            grant.status = self._map_gtr_project_status(status=gtr_project.status)
            grant.duration = gtr_project.fund.duration
            grant.total_funds_currency = gtr_project.fund.currency
            grant.total_funds = gtr_project.fund.amount
            grant.publications = gtr_project.publications
            grant.lead_project = self.lead_project
            grant.funder = Organisation.query.filter_by(
                ror_identifier=gtr_project.fund.funder.ror_id
            ).one_or_none()

            allocations = Allocation.query.filter_by(grant_id=grant.id).all()

            for allocation in allocations:
                project = Project.query.filter_by(id=allocation.project_id).first()
                project.title = grant.title
                project.abstract = grant.abstract
                project.project_duration = grant.duration
                project.access_duration = DateRange(grant.duration.lower, None)
                project.publications = grant.publications
                project.lead_project = self.lead_project

        # Otherwise - add the new grant & the new project
        else:
            grant = Grant(
                neutral_id=generate_neutral_id(),
                reference=self._find_gtr_project_identifier(
                    identifiers=gtr_project.identifiers
                ),
                title=gtr_project.title,
                abstract=gtr_project.abstract,
                status=self._map_gtr_project_status(status=gtr_project.status),
                duration=gtr_project.fund.duration,
                total_funds_currency=gtr_project.fund.currency,
                total_funds=gtr_project.fund.amount,
                publications=gtr_project.publications,
                lead_project=self.lead_project,
                funder=Organisation.query.filter_by(
                    ror_identifier=gtr_project.fund.funder.ror_id
                ).one_or_none(),
            )

            project = Project(
                neutral_id=generate_neutral_id(),
                title=grant.title,
                abstract=grant.abstract,
                project_duration=grant.duration,
                access_duration=DateRange(grant.duration.lower, None),
                publications=grant.publications,
                lead_project=self.lead_project,
                grant_reference=self._find_gtr_project_identifier(
                    identifiers=gtr_project.identifiers
                ),
            )

            db.session.add(project)

            db.session.add(
                Allocation(
                    neutral_id=generate_neutral_id(), project=project, grant=grant
                )
            )

        self._save_gtr_category_terms(gtr_project)
        self._link_gtr_category_terms(gtr_project)

        self._add_gtr_people(
            project=project,
            gtr_people=gtr_project.principle_investigators,
            role=ParticipantRole.InvestigationRole_PrincipleInvestigator,
        )
        self._add_gtr_people(
            project=project,
            gtr_people=gtr_project.co_investigators,
            role=ParticipantRole.InvestigationRole_CoInvestigator,
        )

        db.session.commit()

    def _save_gtr_category_terms(self, project):

        gtr_category_path = Ltree("gtr.ukri.org.resources.classificationprojects.html")

        for term in project.research_subjects:
            # If the subjects exist - update them
            if db.session.query(
                exists().where(CategoryTerm.scheme_identifier == term["id"])
            ).scalar():
                research_subject_to_update = CategoryTerm.query.filter_by(
                    scheme_identifier=term["id"]
                ).one()

                research_subject_to_update.scheme_identifier = term["id"]
                research_subject_to_update.name = term["text"]
                research_subject_to_update.path = gtr_category_path
                research_subject_to_update.category_scheme = CategoryScheme.query.filter_by(
                    namespace="https://gtr.ukri.org/resources/classificationlists.html"
                ).one()
                print(
                    "GTR research_subject updated",
                    research_subject_to_update.name,
                    research_subject_to_update.scheme_identifier,
                )
            # Otherwise add them
            else:
                print("Add new category term:", term["text"], term["id"])
                category_term_resource = CategoryTerm(
                    neutral_id=generate_neutral_id(),
                    scheme_identifier=term["id"],
                    name=term["text"],
                    path=gtr_category_path,
                    category_scheme=CategoryScheme.query.filter_by(
                        namespace="https://gtr.ukri.org/resources/classificationlists.html"
                    ).one(),
                )
                print(
                    "GTR research_subject added",
                    category_term_resource.name,
                    category_term_resource.neutral_id,
                )
                db.session.add(category_term_resource)
                db.session.commit()

        for term in project.research_topics:
            # If the topics exist - update them
            if db.session.query(
                exists().where(CategoryTerm.scheme_identifier == term["id"])
            ).scalar():

                research_topic_to_update = CategoryTerm.query.filter_by(
                    scheme_identifier=term["id"]
                ).one()

                research_topic_to_update.scheme_identifier = term["id"]
                research_topic_to_update.name = term["text"]
                research_topic_to_update.path = gtr_category_path
                research_topic_to_update.category_scheme = CategoryScheme.query.filter_by(
                    namespace="https://gtr.ukri.org/resources/classificationlists.html"
                ).one()
                # print("GTR research_topic updated", research_topic_to_update.name, research_subject_to_update.scheme_identifier)
            # Otherwise add them
            else:
                category_term_resource = CategoryTerm(
                    neutral_id=generate_neutral_id(),
                    scheme_identifier=term["id"],
                    name=term["text"],
                    path=gtr_category_path,
                    category_scheme=CategoryScheme.query.filter_by(
                        namespace="https://gtr.ukri.org/resources/classificationlists.html"
                    ).one(),
                )
                print(
                    "GTR research_topic added",
                    category_term_resource.name,
                    category_term_resource.neutral_id,
                )
                db.session.add(category_term_resource)
                db.session.commit()

    def _link_gtr_category_terms(self, project):

        # GTR Research Topics and Subjects
        gtr_topics = self._find_unique_gtr_project_research_items(
            gtr_research_items=project.research_topics
        )
        gtr_subjects = self._find_unique_gtr_project_research_items(
            gtr_research_items=project.research_subjects
        )

        # GCMD Research Topics and Subjects
        gcmd_topics = self._find_unique_gcmd_project_research_topics(
            gtr_research_topics=project.research_topics
        )
        gcmd_subjects = self._find_unique_gcmd_project_research_subjects(
            gtr_research_subjects=project.research_subjects
        )

        # Flatten the processed topics and subjects to dinstinct list of GCMD identifiers

        # GTR Topics
        category_term_scheme_identifiers = list(gtr_topics)
        # GTR Subjects
        category_term_scheme_identifiers.extend(
            x for x in gtr_subjects if x not in category_term_scheme_identifiers
        )
        # GCMD Topics
        category_term_scheme_identifiers.extend(
            x for x in gcmd_topics if x not in category_term_scheme_identifiers
        )
        # GCMD Subjects
        category_term_scheme_identifiers.extend(
            x for x in gcmd_subjects if x not in category_term_scheme_identifiers
        )

        # Get project_id if it exists
        grant = Grant.query.filter_by(reference=self.grant_reference).first()
        allocation = Allocation.query.filter_by(grant_id=grant.id).first()
        project_id = allocation.project_id

        # Get the project
        project = Project.query.filter_by(id=allocation.project_id).first()

        # print("project id: ", project_id)

        project_category_terms = Categorisation.query.filter_by(
            project_id=project_id
        ).all()

        # If terms exist in the database see if they need altering
        # create two lists. 1: exsisting terms. 2: incoming terms.
        if project_category_terms:

            existing_terms = []
            incoming_terms = []

            for project_category_term in project_category_terms:

                category_term = CategoryTerm.query.filter_by(
                    id=project_category_term.category_term_id
                ).one()
                existing_terms.append(category_term.scheme_identifier)

            for category_term_scheme_identifier in category_term_scheme_identifiers:

                incoming_terms.append(category_term_scheme_identifier)

            # Compare the lists for adding
            existing = set(existing_terms)
            missing_in_existing_add = [x for x in incoming_terms if x not in existing]
            for category_term_scheme_identifier in missing_in_existing_add:

                # Save to category terms link table - links cat terms to projects
                db.session.add(
                    Categorisation(
                        neutral_id=generate_neutral_id(),
                        project_id=project_id,
                        category_term=CategoryTerm.query.filter_by(
                            scheme_identifier=category_term_scheme_identifier
                        ).one(),
                    )
                )
                print("linking topic/subject", category_term_scheme_identifier)

            # Compare the lists for removing
            # incoming_terms.pop() # Debug: pop off an incoming record to test if this works.
            incoming = set(incoming_terms)
            missing_in_incoming_remove = [
                x for x in existing_terms if x not in incoming
            ]
            for category_term_scheme_identifier in missing_in_incoming_remove:

                # Remove from category terms link table - unlinks cat terms to projects
                category_term = CategoryTerm.query.filter_by(
                    scheme_identifier=category_term_scheme_identifier
                ).one()

                Categorisation.query.filter_by(
                    category_term_id=category_term.id
                ).delete()
                print("unlinking topic/subject", category_term_scheme_identifier)

        # Otherwise this is a new grant import, so link the categories
        else:
            for category_term_scheme_identifier in category_term_scheme_identifiers:

                # For edge cases where URLs are added instead of category terms
                URL_check = category_term_scheme_identifier.split("/")

                # Save to category terms link table - links projects to category terms
                if category_term_scheme_identifier != "none":
                    if URL_check[0] != "https:":
                        db.session.add(
                            Categorisation(
                                neutral_id=generate_neutral_id(),
                                project=project,
                                category_term=CategoryTerm.query.filter_by(
                                    scheme_identifier=category_term_scheme_identifier
                                ).one(),
                            )
                        )

                        print(
                            "GTR topic/subject link added:",
                            category_term_scheme_identifier,
                        )

    def _find_gtr_project_identifier(self, identifiers: Dict[str, List[str]]) -> str:
        """
        Gets the identifier form a GTR Project corresponding to the grant reference being imported

        If there isn't a single grant identifier, or it does not correspond to the grant reference being imported, an
        appropriate exception is raised instead.

        This should always be true based on how GTR projects are found, but is checked for completeness.

        :rtype str
        :return Identifier from a GTR project resource matching the grant reference being imported
        """
        if "RCUK" not in identifiers.keys():
            raise KeyError("RCUK/GTR identifier not in GTR project identifiers")
        if len(identifiers["RCUK"]) == 0:
            raise KeyError("RCUK/GTR identifier not in GTR project identifiers")
        if len(identifiers["RCUK"]) > 1:
            raise KeyError(
                "Multiple RCUK/GTR identifiers in GTR project identifiers, one expected"
            )

        if identifiers["RCUK"][0] != self.grant_reference:
            raise ValueError(
                f"RCUK/GTR identifier in GTR project identifiers ({identifiers['RCUK'][0]}), doesn't "
                f"match match requested grant reference ({self.grant_reference})"
            )

        return identifiers["RCUK"][0]

    @staticmethod
    def _add_gtr_people(
        project: Project,
        gtr_people: List[GatewayToResearchPerson],
        role: ParticipantRole,
    ):
        """
        Links a project to it's participants

        Participant resources are created for each person associated with a Project in a given role. Existing People
        resources are used where possible, otherwise new resources with associated Organisations as needed.

        Requirements:
            * where Organisations are used (Grant funders and People organisations), these must already exist

        Appropriate mappings will also need to be made in:
            * GatewayToResearchOrganisation._map_to_ror_id()
            * GatewayToResearchPerson._map_id_to_orcid_ids()

        :type project: Project
        :param project: Project resource being created as part of import process
        :type gtr_people: list
        :param gtr_people: list of GTR people resources associated with the GTR project being imported
        :type role: ParticipantRole
        :param role: Member of the ParticipantRole enumeration to apply to Participant resources created
        """
        for person in gtr_people:

            org_id = (
                db.session.query(Organisation.id)
                .filter(Organisation.ror_identifier == person.employer.ror_id)
                .scalar()
            )

            if not db.session.query(
                exists().where(
                    and_(
                        Person.first_name == person.first_name,
                        Person.last_name == person.surname,
                        Person.organisation_id == org_id,
                    )
                )
            ).scalar():
                db.session.add(
                    Person(
                        neutral_id=generate_neutral_id(),
                        first_name=person.first_name,
                        last_name=person.surname,
                        orcid_id=person.orcid_id,
                        organisation=Organisation.query.filter_by(
                            ror_identifier=person.employer.ror_id
                        ).one_or_none(),
                    )
                )

            db.session.add(
                Participant(
                    neutral_id=generate_neutral_id(),
                    role=role,
                    project=project,
                    person=Person.query.filter_by(
                        first_name=person.first_name, last_name=person.surname
                    ).first(),
                )
            )

    @staticmethod
    def _map_gtr_project_status(status: str) -> GrantStatus:
        """
        Maps a status in a GTR project to a member of the GrantStatus enumeration used by this project

        :type status: str
        :param status: status in a GTR project

        :rtype GrantStatus
        :return member of the GrantStatus enumeration corresponding to the status in a GTR project
        """
        if status == "Active":
            return GrantStatus.Active
        elif status == "Closed":
            return GrantStatus.Closed
        elif status == "Completed":
            return GrantStatus.Completed
        elif status == "Terminated":
            return GrantStatus.Terminated
        elif status == "Pending":
            return GrantStatus.Pending
        elif status == "Unknown":
            return GrantStatus.Unknown

        raise ValueError(
            "Status element value in GTR project not mapped to a member of the GrantStatus enumeration"
        )

    def _find_unique_gtr_project_research_items(self, gtr_research_items: list) -> list:
        """
        For a series of GTR project research items, return a distinct list

        If the 'unclassified' category is included, it is silently removed.

        :type gtr_research_items: list
        :param gtr_research_items: list of GTR project research items

        :rtype list
        :return: distinct list of GTR project research items
        """
        category_term_scheme_identifiers = []
        for category in gtr_research_items:
            # print("GTR_item_term", category)
            category_term_scheme_identifier = category["id"]
            if category_term_scheme_identifier is not None:
                if (
                    category_term_scheme_identifier
                    not in category_term_scheme_identifiers
                ):
                    category_term_scheme_identifiers.append(
                        category_term_scheme_identifier
                    )
        return category_term_scheme_identifiers

    def _find_unique_gcmd_project_research_topics(
        self, gtr_research_topics: list
    ) -> list:
        """
        For a series of GTR project research topics, return a distinct list

        If the 'unclassified' category is included, it is silently removed.

        :type gtr_research_topics: list
        :param gtr_research_topics: list of GTR project research topics

        :rtype list
        :return: distinct list of GCMD project research topics
        """
        category_term_scheme_identifiers = []
        for category in gtr_research_topics:
            category_term_scheme_identifier = (
                self._map_gtr_project_research_topic_to_category_term(category)
            )
            if category_term_scheme_identifier is not None:
                if (
                    category_term_scheme_identifier
                    not in category_term_scheme_identifiers
                ):
                    category_term_scheme_identifiers.append(
                        category_term_scheme_identifier
                    )
        return category_term_scheme_identifiers

    def _find_unique_gcmd_project_research_subjects(
        self, gtr_research_subjects: list
    ) -> list:
        """
        For a series of GTR project subjects, return a distinct list

        :type gtr_research_subjects: list
        :param gtr_research_subjects: list of GTR project research subjects

        :rtype list
        :return: distinct list of GCMD project research subjects
        """
        category_term_scheme_identifiers = []
        for category in gtr_research_subjects:
            category_term_scheme_identifier = (
                self._map_gtr_project_research_subject_to_category_term(category)
            )
            if category_term_scheme_identifier is not None:
                if (
                    category_term_scheme_identifier
                    not in category_term_scheme_identifiers
                ):
                    category_term_scheme_identifiers.append(
                        category_term_scheme_identifier
                    )
        return category_term_scheme_identifiers

    @staticmethod
    def _map_gtr_project_research_topic_to_category_term(
        gtr_research_topic: dict,
    ) -> Optional[str]:
        """
        Categories in this project are identified by scheme identifiers (defined by each scheme), however GTR does not
        use a category scheme supported by this project and no other identifier is available to automatically determine
        a corresponding Category based on its GTR research topic ID.

        This mapping therefore needs to be defined manually in this method. Currently this is done using a simple if
        statement, but in future a more scalable solution will be needed.

        :type gtr_research_topic: dict
        :param gtr_research_topic: GTR project research topic

        :rtype str or None
        :return a Category scheme identifier corresponding to a GTR research topic ID, or None if unclassified
        """
        csv_file = "/usr/src/app/arctic_office_projects_api/bulk_importer/csvs/project_topics.csv"
        topics_list = []
        protocol = "https://"

        try:
            with open(csv_file, "r", newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                next(reader, None)  # skip the headers
                for row in reader:
                    key = row["topic_id"]
                    gcmd_code = row["gcmd_link_code"]
                    if gcmd_code and gcmd_code != "none":
                        value = protocol + gcmd_code
                    else:
                        value = "none"
                    topics_list.append({key: value})

        except FileNotFoundError:
            print(f"File not found: {csv_file}")
        except Exception as e:
            print(f"An error occurred with topics mapping: {e}")

        for topic in topics_list:
            for key, value in topic.items():
                # print(f"Checking: {gtr_research_topic['id']} against {key} with value {value}")
                if gtr_research_topic["id"] == key:
                    # print(f"Match found: {key}")
                    if value == "none":
                        return None
                    else:
                        return value

        raise UnmappedGatewayToResearchProjectTopic(
            meta={
                "gtr_research_topic": {
                    "id": gtr_research_topic["id"],
                    "name": gtr_research_topic["text"],
                }
            }
        )

    @staticmethod
    def _map_gtr_project_research_subject_to_category_term(
        gtr_research_subject: dict,
    ) -> Optional[str]:
        """
        Categories in this project are identified by scheme identifiers (defined by each scheme), however GTR does not
        use a category scheme supported by this project and no other identifier is available to automatically determine
        a corresponding Category based on its GTR research subject name.

        This mapping therefore needs to be defined manually in this method. Currently this is done using a simple if
        statement, but in future a more scalable solution will be needed.

        :type gtr_research_subject: dict
        :param gtr_research_subject: GTR project research subject

        :rtype str
        :return a Category scheme identifier corresponding to a GTR research subject name
        """
        psv_file = "/usr/src/app/arctic_office_projects_api/bulk_importer/csvs/project_subjects.psv"
        subjects_list = []
        protocol = "https://"
        try:
            with open(psv_file, "r", newline="") as psv_file:
                reader = csv.DictReader(psv_file, delimiter="|")
                for row in reader:
                    key = row["subject_text"]
                    if row["gcmd_link_code"] != "none":
                        value = protocol + row["gcmd_link_code"]
                    else:
                        value = "none"
                    subjects_list.append({key: value})

        except FileNotFoundError:
            print(f"File not found: {psv_file}")
        except Exception as e:
            print(f"An error occurred with subjects mapping: {e}")

        for subject in subjects_list:
            for key, value in subject.items():
                if gtr_research_subject["text"] == key:
                    # print(value)
                    return value
                raise UnmappedGatewayToResearchProjectSubject(
                    meta={
                        "gtr_research_subject": {
                            "id": gtr_research_subject["id"],
                            "name": gtr_research_subject["text"],
                        }
                    }
                )


def import_gateway_to_research_grant_interactively(
    gtr_grant_reference: str, lead_project: str
):
    """
    Command to import a project/grant from Gateway to Research

    Wraps around the GatewayToResearchGrantImporter class to provide some feedback during import.

    All errors will trigger an exception to be raised with any pending database models to be removed/flushed.

    :type gtr_grant_reference: str
    :param gtr_grant_reference: Gateway to Research grant reference (e.g. 'NE/K011820/1')
    """
    try:
        app.logger.info(
            f"Importing/Updating Gateway to Research (GTR) project with grant reference ({gtr_grant_reference})"
        )
        echo(
            style(
                f"Importing/Updating Gateway to Research (GTR) project with grant reference ({gtr_grant_reference})"
            )
        )
        importer = GatewayToResearchGrantImporter(
            gtr_grant_reference=gtr_grant_reference, lead_project=lead_project
        )

        gtr_project_id = importer.search()

        if importer.exists():
            importer.update(gtr_project_id)
            app.logger.info(
                f"Finished importing/updating GTR project with grant reference ({gtr_grant_reference}"
            )
            echo(
                style(
                    f"Finished importing/Updating GTR project with grant reference ({gtr_grant_reference})",
                    fg="green",
                )
            )
            return True

        if gtr_project_id is None:
            app.logger.error(
                f"Failed importing GTR project with grant reference ({gtr_grant_reference}) - No or "
                f"multiple GTR projects found"
            )
            echo(
                style(
                    f"Failed importing GTR project with grant reference ({gtr_grant_reference}) - No or "
                    f"multiple GTR projects found",
                    fg="red",
                )
            )
            return False
        app.logger.info(
            f"found GTR project for grant reference ({gtr_grant_reference}) - [{gtr_project_id}] - "
            f"Importing"
        )
        echo(
            style(
                f"found GTR project for grant reference ({gtr_grant_reference}) - [{gtr_project_id}] - "
                f"Importing"
            )
        )

        importer.fetch()
        app.logger.info(
            f"Finished importing GTR project with grant reference ({gtr_grant_reference}), imported"
        )
        echo(
            style(
                f"Finished importing GTR project with grant reference ({gtr_grant_reference}), imported",
                fg="green",
            )
        )
    except UnmappedGatewayToResearchOrganisation as e:
        error_msg = f"Grant ref: {gtr_grant_reference} - Unmapped GTR Organisation [{e.meta['gtr_organisation']['resource_uri']}]"
        app.logger.error(error_msg)
        echo(style(error_msg, fg="red"))

        # Log exception details to a file
        log_exception_to_file(error_msg)

    except UnmappedGatewayToResearchPerson as e:
        error_msg = f"Grant ref: {gtr_grant_reference} - Unmapped GTR Person [{e.meta['gtr_person']['resource_uri']}]"
        app.logger.error(error_msg)
        echo(style(error_msg, fg="red"))

        # Log exception details to a file
        log_exception_to_file(error_msg)

    except UnmappedGatewayToResearchProjectTopic as e:
        error_msg = f"Grant ref: {gtr_grant_reference} - Unmapped GTR Topic [{e.meta['gtr_research_topic']['id']}, {e.meta['gtr_research_topic']['name']}]"
        app.logger.error(error_msg)
        echo(style(error_msg, fg="red"))

        # Log exception details to a file
        log_exception_to_file(error_msg)

    except UnmappedGatewayToResearchProjectSubject as e:
        error_msg = f"Grant ref: {gtr_grant_reference} - Unmapped GTR Subject [{e.meta['gtr_research_subject']['id']}, {e.meta['gtr_research_subject']['name']}]"
        app.logger.error(error_msg)
        echo(style(error_msg, fg="red"))

        # Log exception details to a file
        log_exception_to_file(error_msg)

    except Exception as e:
        db.session.rollback()
        # Remove any added, but non-committed, entities
        db.session.flush()
        raise e
