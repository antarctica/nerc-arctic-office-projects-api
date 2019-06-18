from datetime import date, datetime, timezone
from typing import Dict, Optional, List
from urllib.parse import quote as url_encode

import requests

from psycopg2.extras import DateRange
from requests import HTTPError
# noinspection PyPackageRequirements
from sqlalchemy import exists

from arctic_office_projects_api.errors import AppException
from arctic_office_projects_api.extensions import db
from arctic_office_projects_api.utils import generate_neutral_id
from arctic_office_projects_api.models import CategoryTerm, Grant, GrantStatus, GrantCurrency, Organisation, Project, \
    Allocation, Person, Participant, ParticipantRole, Categorisation


# Exceptions


class UnmappedGatewayToResearchOrganisation(AppException):
    title = 'Unmapped Gateway to Research organisation'
    detail = 'A Gateway to Research organisation has not been mapped to an application Organisation via a GRID ID'


class UnmappedGatewayToResearchPerson(AppException):
    title = 'Unmapped Gateway to Research person'
    detail = 'A Gateway to Research person has not been mapped to an application Person via a ORCID iD'


class UnmappedGatewayToResearchProjectCategory(AppException):
    title = 'Unmapped Gateway to Research category or topic'
    detail = 'A Gateway to Research category or topic has not been mapped to an application category term via a ' \
             'scheme identifier'


# Resources


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
                headers={
                    'accept': 'application/vnd.rcuk.gtr.json-v7'
                }
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
        if 'links' not in self.resource:
            raise KeyError("Links element not in GTR resource")
        if 'link' not in self.resource['links']:
            raise KeyError("Links list element not in GTR resource")

        links = {}
        for link in self.resource['links']['link']:
            if 'rel' not in link:
                raise KeyError("Rel type not in GTR resource link")
            if 'href' not in link:
                raise KeyError("Href not in GTR resource link")
            if link['rel'] not in links.keys():
                links[link['rel']] = []
            links[link['rel']].append(link['href'])

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

        if 'name' not in self.resource:
            raise KeyError('Name element not in GTR organisation')
        self.name = self.resource['name']

        self.grid_id = self._map_to_grid_id()

    def _map_to_grid_id(self) -> str:
        """
        Organisations in this project are identified by GIRD IDs (https://www.grid.ac), however these are not used by
        GTR and no other identifier is available to automatically determine the GIRD ID for an organisation based on its
        GTR resource ID.

        This mapping therefore needs to be defined manually in this method. Currently this is done using a simple if
        statement, but in future a more scalable solution will be needed.

        :rtype str
        :return for a given GTR resource URI, a corresponding GRID ID as a URI
        """
        # Natural Environment Research Council
        if self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/8A03ED41-E67D-4F4A-B5DD-AAFB272B6471':
            return 'https://www.grid.ac/institutes/grid.8682.4'
        # University of Leeds
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/83D87776-5958-42AE-889D-B8AECF16B468':
            return 'https://www.grid.ac/institutes/grid.9909.9'
        # University of Sheffield
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/03D8AFBB-3EA5-4885-B036-BD4F9F4F9849':
            return 'https://www.grid.ac/institutes/grid.11835.3e'
        # Scottish Association For Marine Science
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/1ED25A21-FD91-4EC2-A06F-724F9F2CDC3D':
            return 'https://www.grid.ac/institutes/grid.410415.5'
        # NERC British Antarctic Survey
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/21CFC584-0BCD-450C-B2C1-EFF574194DBF':
            return 'https://www.grid.ac/institutes/grid.478592.5'
        # University of Ulster
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/245EB81A-808F-4697-BAED-263C20266B74':
            return 'https://www.grid.ac/institutes/grid.12641.30'
        # University of Edinburgh
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/2DB7ED73-8E89-457A-A395-FAC12F929C1A':
            return 'https://www.grid.ac/institutes/grid.4305.2'
        # University of Southampton
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/30A429E3-83B7-4E41-99C0-14A144F07DFE':
            return 'https://www.grid.ac/institutes/grid.5491.9'
        # University College London
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/3A5E126D-C175-4730-9B7B-E6D8CF447F83':
            return 'https://www.grid.ac/institutes/grid.83440.3b'
        # University of Oxford
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/3EAE04CA-9D62-4483-B9C4-F91AD9F4C5A9':
            return 'https://www.grid.ac/institutes/grid.4991.5'
        # Imperial College London
        elif self.resource_uri == "https://gtr.ukri.org:443/gtr/api/organisations/46387D84-F71E-4B7D-8C7D-9C288F113510":
            return 'https://www.grid.ac/institutes/grid.7445.2'
        # Durham University
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/46B41008-0EB4-4E28-BBFB-E98366999EC5':
            return 'https://www.grid.ac/institutes/grid.8250.f'
        # National Oceanography Centre
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/4DB630C7-7E13-4610-A1C3-29601903CEE3':
            return 'https://www.grid.ac/institutes/grid.418022.d'
        # NERC Centre for Ecology and Hydrology
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/4FC881BE-799E-459C-A287-2A68170426DA':
            return 'https://www.grid.ac/institutes/grid.494924.6'
        # University of Manchester
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/68D0E3C9-9246-4CFC-B5E9-48584CF82993':
            return 'https://www.grid.ac/institutes/grid.5379.8'
        # Royal Holloway, University of London
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/7A0397DD-E0C6-4EA3-8031-B841D2503C4D':
            return 'https://www.grid.ac/institutes/grid.4970.a'
        # NERC British Geological Survey
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/7ADE0AB2-1050-4241-987D-F3B1C3322E05':
            return 'https://www.grid.ac/institutes/grid.474329.f'
        # University of York
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/8319F78A-DCBD-49F6-BE00-78E1CD75CDA9':
            return 'https://www.grid.ac/institutes/grid.5685.e'
        # University of East Anglia
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/88C5F7F9-8DCC-41C9-BC4F-F37DA01075C7':
            return 'https://www.grid.ac/institutes/grid.8273.e'
        # University of the Highlands and Islands
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/8BA3C264-769F-487E-B61A-2D4CB6A105B6':
            return 'https://www.grid.ac/institutes/grid.23378.3d'
        # University of Dundee
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/90051600-6EF2-4093-BA8C-2B4B6F550895':
            return 'https://www.grid.ac/institutes/grid.8241.f'
        # University of Nottingham
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/936D002F-A8D1-4A93-AE5D-825ED0903D8D':
            return 'https://www.grid.ac/institutes/grid.4563.4'
        # University of Portsmouth
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/955C55E8-783E-4842-BB2C-2D275A3CAF82':
            return 'https://www.grid.ac/institutes/grid.4701.2'
        # University of Exeter
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/961756BF-E31F-4A13-836F-0A09BA02385C':
            return 'https://www.grid.ac/institutes/grid.8391.3'
        # University of Sussex
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/A8967420-49D3-4509-9912-25FB3EC75B74':
            return 'https://www.grid.ac/institutes/grid.12082.39'
        # Leibniz Institute of Freshwater Ecology
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/AB007A2D-2086-4B7A-8539-DBD5836A8503':
            return 'https://www.grid.ac/institutes/grid.419247.d'
        # University of Stirling
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/C7510606-A36F-4725-A89B-9D592374972A':
            return 'https://www.grid.ac/institutes/grid.11918.30'
        # Loughborough University
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/CAA9A40D-0226-4A4F-AC0D-D8299E30A1EF':
            return 'https://www.grid.ac/institutes/grid.6571.5'
        # University of Cambridge
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/D1774113-D5D2-4B7C-A412-66A90FE4B96F':
            return 'https://www.grid.ac/institutes/grid.5335.0'
        # University of Huddersfield
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/DC934AED-9432-4385-AEAF-006EA2369001':
            return 'https://www.grid.ac/institutes/grid.15751.37'
        # University of Reading
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/E89C3602-0FB4-4044-A918-58966B8A10B2':
            return 'https://www.grid.ac/institutes/grid.9435.b'
        # University of Aberdeen
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/F7E13617-2678-475B-99E4-31479C92038D':
            return 'https://www.grid.ac/institutes/grid.7107.1'
        # Bangor University
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/F9F1D136-12E3-4BE4-9668-0C9BC4A7C1BF':
            return 'https://www.grid.ac/institutes/grid.7362.0'

        raise UnmappedGatewayToResearchOrganisation(meta={
            'gtr_organisation': {
                'resource_uri': self.resource_uri,
                'name': self.name
            }
        })


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

        self.funder = GatewayToResearchFunder(gtr_resource_uri=self._find_gtr_funder_link())

        if 'start' not in self.resource:
            raise KeyError('Start date element not in GTR fund')
        if 'end' not in self.resource:
            raise KeyError('End date element not in GTR fund')

        self.duration = DateRange(
            self._process_gtr_datetime(self.resource['start']),
            self._process_gtr_datetime(self.resource['end'])
        )

        if 'valuePounds' not in self.resource:
            raise KeyError('ValuePounds element not in GTR fund')
        if 'currencyCode' not in self.resource['valuePounds']:
            raise KeyError('CurrencyCode element not in GTR fund')
        if 'amount' not in self.resource['valuePounds']:
            raise KeyError('Amount element not in GTR fund')

        self.currency = self._map_gtr_fund_currency_code(self.resource['valuePounds']['currencyCode'])
        self.amount = self.resource['valuePounds']['amount']

    @staticmethod
    def _map_gtr_fund_currency_code(currency_code: str) -> GrantCurrency:
        """
        Maps a currency type in a GTR fund to a member of the GrantCurrency enumeration used by this project

        :type currency_code: str
        :param currency_code: currency type in a GTR fund

        :rtype GrantCurrency
        :return member of the GrantCurrency enumeration corresponding to the currency type in a GTR fund
        """
        if currency_code == 'GBP':
            return GrantCurrency.GBP

        raise ValueError("CurrencyCode element value in GTR fund not mapped to a member of the GrantCurrency "
                         "enumeration")

    def _find_gtr_funder_link(self) -> str:
        """
        Gets the resource URI of the GTR Funder resource for a GTR Fund

        I.e. The URI to the funder of a grant.

        If there isn't a single funder resource an appropriate exception is raised instead.

        :rtype str
        :return URI of the GTR Funder resource for a GTR Fund
        """
        if 'FUNDER' not in self.resource_links.keys():
            raise KeyError("GTR funder relation not found in GTR fund links")
        if len(self.resource_links['FUNDER']) == 0:
            raise KeyError("GTR funder relation not found in GTR fund links")
        if len(self.resource_links['FUNDER']) > 1:
            raise KeyError("Multiple GTR funder identifiers found in GTR fund links, one expected")

        return self.resource_links['FUNDER'][0]

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

        self.employer = GatewayToResearchEmployer(gtr_resource_uri=self._find_gtr_employer_link())

        self.first_name = None
        if 'firstName' in self.resource:
            self.first_name = self.resource['firstName']
        self.surname = None
        if 'surname' in self.resource:
            self.surname = self.resource['surname']
        self.orcid_id = None
        if 'orcidId' in self.resource:
            self.orcid_id = f"https://orcid.org/{self.resource['orcidId']}"
        self._map_id_to_orcid_ids()

    def _find_gtr_employer_link(self):
        """
        Gets the resource URI of the GTR Employer resource for a GTR Person

        I.e. The URI to the employer of a person.

        If there isn't a single employer resource an appropriate exception is raised instead.

        :rtype str
        :return URI of the GTR Funder resource for a GTR Fund
        """
        if 'EMPLOYED' not in self.resource_links.keys():
            raise KeyError("GTR employer relation not found in GTR person links")
        if len(self.resource_links['EMPLOYED']) == 0:
            raise KeyError("GTR employer relation not found in GTR person links")
        if len(self.resource_links['EMPLOYED']) > 1:
            raise KeyError("Multiple GTR employer relations found in GTR person links, one expected")

        return self.resource_links['EMPLOYED'][0]

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
        gtr_people_orcid_id_mappings = {
            # Kenneth Carslaw - Leeds
            "https://gtr.ukri.org:443/gtr/api/persons/00ECDD3F-DE95-4E2C-85C6-A73578A9256E":
                "https://orcid.org/0000-0002-6800-154X",
            # Barbara Brooks
            "https://gtr.ukri.org:443/gtr/api/persons/4B79375A-2E7B-42EB-A981-3EAEE5AD4066":
                'https://orcid.org/0000-0001-8932-9256',
            # Ian Brooks
            "https://gtr.ukri.org:443/gtr/api/persons/BBCB83F2-B5D2-43B9-859E-0DA9CC0F63D5":
                'https://orcid.org/0000-0002-5051-1322',
            # Steven Dobbie [uncertain]
            "https://gtr.ukri.org:443/gtr/api/persons/8DFA8601-00EB-47B4-A565-8F2956F92B41":
                'https://orcid.org/0000-0001-8474-176X',
        }

        if self.resource_uri not in gtr_people_orcid_id_mappings.keys():
            raise UnmappedGatewayToResearchPerson(meta={
                'gtr_person': {
                    'resource_uri': self.resource_uri,
                    'name': f"{self.first_name} {self.surname}"
                }
            })

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

        if 'doi' not in self.resource:
            raise KeyError('DOI element not in GTR publication')
        self.doi = self.resource['doi']


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
        self.categories = self._process_categories()
        self.publications = self._process_publications()
        self.fund = GatewayToResearchFund(gtr_resource_uri=self._find_gtr_fund_link())
        self.principle_investigators = self._process_people(relation='PI_PER')
        self.co_investigators = self._process_people(relation='COI_PER')

        if 'status' not in self.resource:
            raise KeyError("Status element not in GTR project")
        self.status = self.resource['status']
        if 'title' not in self.resource:
            raise KeyError("Title element not in GTR project")
        self.title = self.resource['title']

        self.abstract = None
        if 'abstractText' in self.resource:
            self.abstract = self.resource['abstractText']

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

        if 'identifiers' not in self.resource:
            raise KeyError("Identifiers element not in GTR project")
        if 'identifier' not in self.resource['identifiers']:
            raise KeyError("Identifiers list element not in GTR project")

        for gtr_identifier in self.resource['identifiers']['identifier']:
            if 'type' not in gtr_identifier:
                raise KeyError("Type attribute not in GTR project identifier")
            if gtr_identifier['type'] not in project_references:
                project_references[gtr_identifier['type']] = []
            if 'value' not in gtr_identifier:
                raise KeyError("Value attribute not in GTR project identifier")

            project_references[gtr_identifier['type']].append(gtr_identifier['value'])

        return project_references

    def _process_categories(self) -> List[dict]:
        """
        Merges 'categories' and 'topics' used in projects into a single set of classifications

        GTR Projects are classified by both 'categories' and 'topics' (using free-text terms), this project uses
        categories that cover the domains of GTR categories and topics and therefore don't need to be separate.

        To make mapping 'categories' and 'topics' to categories from this project easier, this method merges both into
        a single list of classifications.

        :rtype list
        :return combined list of classifications for a GTR project
        """
        gtr_project_categories = []
        if 'researchSubjects' in self.resource:
            if 'researchSubject' in self.resource['researchSubjects']:
                if len(self.resource['researchSubjects']['researchSubject']) > 0:
                    for gtr_research_subject in self.resource['researchSubjects']['researchSubject']:
                        if 'id' in gtr_research_subject:
                            gtr_project_categories.append(gtr_research_subject)
        if 'researchTopics' in self.resource:
            if 'researchTopic' in self.resource['researchTopics']:
                if len(self.resource['researchTopics']['researchTopic']) > 0:
                    for gtr_research_topic in self.resource['researchTopics']['researchTopic']:
                        if 'id' in gtr_research_topic:
                            gtr_project_categories.append(gtr_research_topic)

        return gtr_project_categories

    def _process_publications(self) -> List[str]:
        """
        Fetches each publication associated with a GTR Project

        In GTR, publications a full resource, however in this project, they are just a list of DOIs.

        :rtype list
        :return list of publication DOIs
        """
        publications = []
        if 'PUBLICATION' in self.resource_links:
            for publication_uri in self.resource_links['PUBLICATION']:
                publication = GatewayToResearchPublication(gtr_resource_uri=publication_uri)
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
        if 'FUND' not in self.resource_links.keys():
            raise KeyError("GTR fund relation not found in GTR project links")
        if len(self.resource_links['FUND']) == 0:
            raise KeyError("GTR fund relation not found in GTR project links")
        if len(self.resource_links['FUND']) > 1:
            raise KeyError("Multiple GTR fund identifiers found in GTR project links, one expected")

        return self.resource_links['FUND'][0]


# Importer


class GatewayToResearchGrantImporter:
    """
    Mechanism to create Projects and associated resources from resources in Gateway to Research

    Some resources, such as people, are effectively 1:1 mappings but with different attribute names. Others, such as
    projects are created by taking attributes from across different GTR resources, either directly or using lookups to
    other resources in this project.

    GTR projects are loosely equivalent to Grants in this project.
    """

    def __init__(self, gtr_grant_reference: str = None, gtr_project_id: str = None):
        """
        :type gtr_grant_reference: str
        :param gtr_grant_reference: Gateway to Research grant reference (e.g. 'NE/K011820/1')
        :type gtr_project_id: str
        :param gtr_grant_reference: Gateway to Research project ID (e.g. '87D5AD44-2123-442B-B186-75C3878471BD')
        """
        self.grant_reference = gtr_grant_reference
        self.gtr_project_id = gtr_project_id

    def exists(self) -> bool:
        """
        Checks whether a Gateway to Research project has previously been imported as a Grant

        :rtype bool
        :return: Whether a GTR project has already been imported as a Grant
        """
        return db.session.query(exists().where(Grant.reference == self.grant_reference)).scalar()

    def search(self) -> Optional[str]:
        """
        Given a grant reference, find a single corresponding GTR project resource ID

        If there isn't, an appropriate exception is raised instead

        :rtype str
        :return ID of a GTR project resource
        """
        try:
            gtr_project_response = requests.get(
                url=f"https://gtr.ukri.org/gtr/api/projects",
                params={
                    'q': url_encode(self.grant_reference),
                    'f': 'pro.gr'
                },
                headers={
                    'accept': 'application/vnd.rcuk.gtr.json-v7'
                }
            )
            gtr_project_response.raise_for_status()
            gtr_project_data = gtr_project_response.json()
            if 'project' not in gtr_project_data:
                raise KeyError("Project element not in GTR response")
            if len(gtr_project_data['project']) != 1:
                raise ValueError("Multiple project elements found in GTR response, only expected one")

            self.gtr_project_id = gtr_project_data['project'][0]['id']
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
            * GatewayToResearchOrganisation._map_to_grid_id()
            * GatewayToResearchPerson._map_id_to_orcid_ids()
            * _map_gtr_project_category_to_category_term()
        """
        gtr_project = GatewayToResearchProject(
            gtr_resource_uri=f"https://gtr.ukri.org/gtr/api/projects/{self.gtr_project_id}"
        )

        grant = Grant(
            neutral_id=generate_neutral_id(),
            reference=self._find_gtr_project_identifier(identifiers=gtr_project.identifiers),
            title=gtr_project.title,
            abstract=gtr_project.abstract,
            status=self._map_gtr_project_status(status=gtr_project.status),
            duration=gtr_project.fund.duration,
            total_funds_currency=gtr_project.fund.currency,
            total_funds=gtr_project.fund.amount,
            publications=gtr_project.publications,
            funder=Organisation.query.filter_by(grid_identifier=gtr_project.fund.funder.grid_id).one()
        )
        db.session.add(grant)

        project = Project(
            neutral_id=generate_neutral_id(),
            title=grant.title,
            abstract=grant.abstract,
            project_duration=grant.duration,
            access_duration=DateRange(grant.duration.lower, None),
            publications=grant.publications
        )
        db.session.add(project)

        db.session.add(Allocation(
            neutral_id=generate_neutral_id(),
            project=project,
            grant=grant
        ))

        category_term_scheme_identifiers = self._find_unique_gtr_project_categories(
            gtr_categories=gtr_project.categories
        )
        for category_term_scheme_identifier in category_term_scheme_identifiers:
            db.session.add(Categorisation(
                neutral_id=generate_neutral_id(),
                project=project,
                category_term=CategoryTerm.query.filter_by(scheme_identifier=category_term_scheme_identifier).one()
            ))

        self._add_gtr_people(
            project=project,
            gtr_people=gtr_project.principle_investigators,
            role=ParticipantRole.InvestigationRole_PrincipleInvestigator
        )
        self._add_gtr_people(
            project=project,
            gtr_people=gtr_project.co_investigators,
            role=ParticipantRole.InvestigationRole_CoInvestigator
        )

        db.session.commit()

    def _find_gtr_project_identifier(self, identifiers: Dict[str, List[str]]) -> str:
        """
        Gets the identifier form a GTR Project corresponding to the grant reference being imported

        If there isn't a single grant identifier, or it does not correspond to the grant reference being imported, an
        appropriate exception is raised instead.

        This should always be true based on how GTR projects are found, but is checked for completeness.

        :rtype str
        :return Identifier from a GTR project resource matching the grant reference being imported
        """
        if 'RCUK' not in identifiers.keys():
            raise KeyError("RCUK/GTR identifier not in GTR project identifiers")
        if len(identifiers['RCUK']) == 0:
            raise KeyError("RCUK/GTR identifier not in GTR project identifiers")
        if len(identifiers['RCUK']) > 1:
            raise KeyError("Multiple RCUK/GTR identifiers in GTR project identifiers, one expected")

        if identifiers['RCUK'][0] != self.grant_reference:
            raise ValueError(f"RCUK/GTR identifier in GTR project identifiers ({identifiers['RCUK'][0]}), doesn't "
                             f"match match requested grant reference ({self.grant_reference})")

        return identifiers['RCUK'][0]

    @staticmethod
    def _add_gtr_people(
        project: Project,
        gtr_people: List[GatewayToResearchPerson],
        role: ParticipantRole
    ):
        """
        Links a project to it's participants

        Participant resources are created for each person associated with a Project in a given role. Existing People
        resources are used where possible, otherwise new resources with associated Organisations as needed.

        Requirements:
            * where Organisations are used (Grant funders and People organisations), these must already exist

        Appropriate mappings will also need to be made in:
            * GatewayToResearchOrganisation._map_to_grid_id()
            * GatewayToResearchPerson._map_id_to_orcid_ids()

        :type project: Project
        :param project: Project resource being created as part of import process
        :type gtr_people: list
        :param gtr_people: list of GTR people resources associated with the GTR project being imported
        :type role: ParticipantRole
        :param role: Member of the ParticipantRole enumeration to apply to Participant resources created
        """
        for person in gtr_people:
            if person.orcid_id is None:
                raise ValueError("GTR project person could not be mapped to a Person, no ORCID iD")

            if not db.session.query(exists().where(Person.orcid_id == person.orcid_id)).scalar():
                db.session.add(Person(
                    neutral_id=generate_neutral_id(),
                    first_name=person.first_name,
                    last_name=person.surname,
                    orcid_id=person.orcid_id,
                    organisation=Organisation.query.filter_by(grid_identifier=person.employer.grid_id).one()
                ))
            db.session.add(Participant(
                neutral_id=generate_neutral_id(),
                role=role,
                project=project,
                person=Person.query.filter_by(orcid_id=person.orcid_id).one()
            ))

    @staticmethod
    def _map_gtr_project_status(status: str) -> GrantStatus:
        """
        Maps a status in a GTR project to a member of the GrantStatus enumeration used by this project

        :type status: str
        :param status: status in a GTR project

        :rtype GrantStatus
        :return member of the GrantStatus enumeration corresponding to the status in a GTR project
        """
        if status == 'Closed':
            return GrantStatus.Closed

        raise ValueError("Status element value in GTR project not mapped to a member of the GrantStatus enumeration")

    def _find_unique_gtr_project_categories(self, gtr_categories: list) -> list:
        """
        For a series of GTR project categories/topics, return a distinct list

        If the 'unclassified' category is included, it is silently removed.

        :type gtr_categories: list
        :param gtr_categories: list of GTR project categories/topics

        :rtype list
        :return: distinct list of GTR project categories/topics
        """
        category_term_scheme_identifiers = []
        for category in gtr_categories:
            category_term_scheme_identifier = self._map_gtr_project_category_to_category_term(category)
            if category_term_scheme_identifier is not None:
                if category_term_scheme_identifier not in category_term_scheme_identifiers:
                    category_term_scheme_identifiers.append(category_term_scheme_identifier)
        return category_term_scheme_identifiers

    @staticmethod
    def _map_gtr_project_category_to_category_term(gtr_category: dict) -> Optional[str]:
        """
        Categories in this project are identified by scheme identifiers (defined by each scheme), however GTR does not
        use a category scheme supported by this project and no other identifier is available to automatically determine
        a corresponding Category based on its GTR category or topic ID.

        This mapping therefore needs to be defined manually in this method. Currently this is done using a simple if
        statement, but in future a more scalable solution will be needed.

        :type gtr_category: dict
        :param gtr_category: GTR project category or topic

        :rtype str or None
        :return a Category scheme identifier corresponding to a GTR category or topic ID, or None if unclassified
        """
        if gtr_category['id'] == 'E4C03353-6311-43F9-9204-CFC2536D2017':
            return 'https://gcmdservices.gsfc.nasa.gov/kms/concept/c47f6052-634e-40ef-a5ac-13f69f6f4c2a'
        elif gtr_category['id'] == 'C62D281D-F1B9-423D-BDAB-361EC9BE7C68':
            return 'https://gcmdservices.gsfc.nasa.gov/kms/concept/286d2ae0-9d86-4ef0-a2b4-014843a98532'
        elif gtr_category['id'] == 'C29F371D-A988-48F8-BFF5-1657DAB1176F':
            return 'https://gcmdservices.gsfc.nasa.gov/kms/concept/286d2ae0-9d86-4ef0-a2b4-014843a98532'
        elif gtr_category['id'] == 'B01D3878-E7BD-4830-9503-2F54544E809E':
            return 'https://gcmdservices.gsfc.nasa.gov/kms/concept/286d2ae0-9d86-4ef0-a2b4-014843a98532'
        # Unclassified
        elif gtr_category['id'] == 'D05BC2E0-0345-4A3F-8C3F-775BC42A0819':
            return None

        raise UnmappedGatewayToResearchProjectCategory(meta={
            'gtr_category': {
                'id': gtr_category['id'],
                'name': gtr_category['text']
            }
        })


def import_gateway_to_research_grant_interactively(gtr_grant_reference: str):
    """
    Command to import a project/grant from Gateway to Research

    Wraps around the GatewayToResearchGrantImporter class to provide some feedback during import.

    All errors will trigger an exception to be raised with any pending database models to be removed/flushed.

    :type gtr_grant_reference: str
    :param gtr_grant_reference: Gateway to Research grant reference (e.g. 'NE/K011820/1')
    """
    try:
        print(f"Importing Gateway to Research (GTR) project with grant reference ({gtr_grant_reference})")

        importer = GatewayToResearchGrantImporter(gtr_grant_reference=gtr_grant_reference)
        if importer.exists():
            print(
                f"Finished importing GTR project with grant reference ({gtr_grant_reference}), already imported")
            return True

        gtr_project_id = importer.search()
        if gtr_project_id is None:
            print(
                f"* Failed importing GTR project with grant reference ({gtr_grant_reference}), no or multiple GTR "
                f"projects found")
            return False
        print(f"... found GTR project for grant reference ({gtr_grant_reference}) - [{gtr_project_id}], importing")

        importer.fetch()
        print(f"Finished importing GTR project with grant reference ({gtr_grant_reference}), imported")
    except Exception as e:
        db.session.rollback()
        # Remove any added, but non-committed, entities
        db.session.flush()
        raise e


# temp
def foo():
    from http import HTTPStatus

    import_gateway_to_research_grant_interactively(gtr_grant_reference='NE/K011820/1')

    return '', HTTPStatus.OK
