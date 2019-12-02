import requests

from datetime import date, datetime, timezone
from typing import Dict, Optional, List
from urllib.parse import quote as url_encode

from click import echo, style
from flask import current_app as app
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

class UnmappedGatewayToResearchProjectTopic(AppException):
    title = 'Unmapped Gateway to Research topic'
    detail = 'A Gateway to Research topic has not been mapped to an application category term via a ' \
             'scheme identifier'


class UnmappedGatewayToResearchProjectSubject(AppException):
    title = 'Unmapped Gateway to Research subject'
    detail = 'A Gateway to Research subject has not been mapped to an application category term via a ' \
             'scheme identifier'

class GatewayToResearchPublicationWithoutDOI(AppException):
    title = "Gateway to Research publication doesn't have a DOI"
    detail = 'A Gateway to Research publication needs to include a DOI to be valid in this API'


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
        Organisations in this project are identified by GRID IDs (https://www.grid.ac), however these are not used by
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
        # Marine Biological Association
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/309F361A-A8CC-438D-AB70-93C74E1E91C3':
            return 'https://www.grid.ac/institutes/grid.14335.30'
        # University of St Andrews
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/C0E4FAD2-3C8B-410A-B6DF-3B9B9E433060':
            return 'https://www.grid.ac/institutes/grid.11914.3c'
        # Northumbria University
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/EF390CF0-ECD3-47D8-B9A8-7602AF319BEE':
            return 'https://www.grid.ac/institutes/grid.42629.3b'
        # Plymouth Marine Laboratory
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/EEF9EA95-341D-48C2-8A68-B838D35497C8':
            return 'https://www.grid.ac/institutes/grid.22319.3b'
        # Newcastle University
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/5E2B04DD-4A03-45ED-9892-61C5CCB8AC68':
            return 'https://www.grid.ac/institutes/grid.1006.7'
        # Aarhus University
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/CE43EBFA-3FC9-44BC-B6FF-001F11664C46':
            return 'https://www.grid.ac/institutes/grid.7048.b'
        # Lancaster University
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/8A66BFC9-B9A5-48C6-B46C-761D1C13C5DC':
            return 'https://www.grid.ac/institutes/grid.9835.7'
        # University of Strathclyde
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/5BB4F8BF-B4E0-4EAF-9AF5-885E19D64850':
            return 'https://www.grid.ac/institutes/grid.11984.35'
        # Free University of Brussels
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/773AC409-21D1-4CA0-87AA-1769A45D718E':
            return 'https://www.grid.ac/institutes/grid.8767.e'
        # Warwick University
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/B6FB652A-60C3-48DD-9A33-075D1F759B48':
            return 'https://www.grid.ac/institutes/grid.7372.1'
        # Bristol University
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/4A348A76-B2D0-4DDD-804A-CE735A6D3798':
            return 'https://www.grid.ac/institutes/grid.5337.2'
        # Aberystwyth University
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/E4757A6E-7326-472B-9979-B47D77A65446':
            return 'https://www.grid.ac/institutes/grid.8186.7'
        # University of Hull
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/8A0FC07A-04CD-4F7A-9095-1D2E6C1D918F':
            return 'https://www.grid.ac/institutes/grid.9481.4'
        # Essex University
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/ED6A6B32-663C-4A62-A33B-2C6A68E2E102':
            return 'https://www.grid.ac/institutes/grid.8356.8'
        # Queen Mary, University of London
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/D5337A10-AC8A-402A-8164-C5F9CC6B0140':
            return 'https://www.grid.ac/institutes/grid.4868.2'
        # Leicester University
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/AE0A6F70-C175-4550-B08F-74C8790007BB':
            return 'https://www.grid.ac/institutes/grid.9918.9'
        # Open University
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/89E6D9CB-DAF8-40A2-A9EF-B330A5A7FC24':
            return 'https://www.grid.ac/institutes/grid.10837.3d'
        # Scottish Universities Environmental Research Centre
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/BF1F76BF-B87F-4FE0-B1DB-4650F5E99448':
            return 'https://www.grid.ac/institutes/grid.224137.1'
        # Birmingham University
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/A022BD3A-2A7B-4E64-8877-A2E381C4CCB5':
            return 'https://www.grid.ac/institutes/grid.6572.6'
        # The Natural History Museum
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/B2F6103D-47D2-486A-8F7C-C62362BAACD9':
            return 'https://www.grid.ac/institutes/grid.35937.3b'
        # Plymouth University
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/7801F008-7C77-45E7-90E9-4345B47D138E':
            return 'https://www.grid.ac/institutes/grid.11201.33'
        # Glasgow University
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/AE58F21F-3622-4382-97BB-1359BD183E9F':
            return 'https://www.grid.ac/institutes/grid.8756.c'
        # AHRC
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/1291772D-DFCE-493A-AEE7-24F7EEAFE0E9':
            return 'https://www.grid.ac/institutes/grid.426413.6'
        # EPSRC
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/798CB33D-C79E-4578-83F2-72606407192C':
            return 'https://www.grid.ac/institutes/grid.421091.f'
        # ESRC
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/924BE15C-91F2-4AAD-941A-3F338324B6AE':
            return 'https://www.grid.ac/institutes/grid.434257.3'
        # Innovate Uk
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/1DA78802-0659-4398-B40B-7FA41B56BBF3':
            return 'https://www.grid.ac/institutes/grid.423443.6'
        # Cranfield University
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/F45A4578-F962-4EFA-9CC1-9F2FF4F760AE':
            return 'https://www.grid.ac/institutes/grid.12026.37'
        # Unknown
        elif self.resource_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/F0C1AEFB-C222-4BF6-9CA3-8CF628494537':
            return None
        raise UnmappedGatewayToResearchOrganisation(meta={
            'gtr_organisation': {
                'resource_uri': self.resource_uri
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

        self.funder = GatewayToResearchFunder(
            gtr_resource_uri=self._find_gtr_funder_link())

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

        self.currency = self._map_gtr_fund_currency_code(
            self.resource['valuePounds']['currencyCode'])
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
            raise KeyError(
                "Multiple GTR funder identifiers found in GTR fund links, one expected")

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

        self.employer = GatewayToResearchEmployer(
            gtr_resource_uri=self._find_gtr_employer_link())

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
        :return URI of the GTR Employer resource for a GTR Person
        """
        if 'EMPLOYED' not in self.resource_links.keys():
            raise KeyError(
                "GTR employer relation not found in GTR person links")
        if len(self.resource_links['EMPLOYED']) == 0:
            raise KeyError(
                "GTR employer relation not found in GTR person links")
        if len(self.resource_links['EMPLOYED']) > 1:
            raise KeyError(
                "Multiple GTR employer relations found in GTR person links, one expected")

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
            # Barbara Brooks - Leeds
            "https://gtr.ukri.org:443/gtr/api/persons/4B79375A-2E7B-42EB-A981-3EAEE5AD4066":
                'https://orcid.org/0000-0001-8932-9256',
            # Ian Brooks - Leeds
            "https://gtr.ukri.org:443/gtr/api/persons/BBCB83F2-B5D2-43B9-859E-0DA9CC0F63D5":
                'https://orcid.org/0000-0002-5051-1322',
            # Steven Dobbie [uncertain]
            "https://gtr.ukri.org:443/gtr/api/persons/8DFA8601-00EB-47B4-A565-8F2956F92B41":
                'https://orcid.org/0000-0001-8474-176X',
            # David Lowry - Royal Holloway
            "https://gtr.ukri.org:443/gtr/api/persons/01EDB04B-CAAA-477B-AE23-7BA9BA1B4552":
                "https://orcid.org/0000-0002-8535-0346",
            # Sian Henley - Edinburgh
            "https://gtr.ukri.org:443/gtr/api/persons/04DB4916-2E9B-4746-B5AC-CD8FFD98DBAD":
                "https://orcid.org/0000-0003-1221-1983",
            # Finlo Cottier - SAMS
            "https://gtr.ukri.org:443/gtr/api/persons/0AD27E81-D523-48AA-AA6B-C9C3821DF182":
                "https://orcid.org/0000-0002-3068-1754",
            # Rowan Sutton - Reading / NCAS
            "https://gtr.ukri.org:443/gtr/api/persons/0B2C1A4A-6D80-488E-A28A-23D2EB48B7B6":
                "https://orcid.org/0000-0001-8345-8583",
            # Hugh Coe - Manchester
            "https://gtr.ukri.org:443/gtr/api/persons/0C563960-68AC-41EB-8535-4F23806F09AA":
                "https://orcid.org/0000-0002-3264-1713",
            # Peter Langdon - Southampton
            "https://gtr.ukri.org:443/gtr/api/persons/0FB14E60-3A55-4CE1-B476-DDCFDDE621B5":
                "https://orcid.org/0000-0003-2724-2643",
            # Bhavani Narayanaswamy - Highlands & Islands (possibly also SAMS)
            "https://gtr.ukri.org:443/gtr/api/persons/13FA7765-399D-4905-8260-F849DBDE2068":
                "https://orcid.org/0000-0002-5810-9127",
            # Keith Haines - Reading
            "https://gtr.ukri.org:443/gtr/api/persons/1A191F76-65F5-46A6-8E4F-2443B2ED6E31":
                "https://orcid.org/0000-0003-2768-2374",
            # John Adrian Pyle - Cambridge [needs organisation mapping manually]
            "https://gtr.ukri.org:443/gtr/api/persons/1A4B6425-F976-4667-AABF-DBCBBB7C3645":
                "https://orcid.org/0000-0003-3629-9916",
            # Andrew Manning - UEA
            "https://gtr.ukri.org:443/gtr/api/persons/2001E910-8250-41BA-A0B3-103175B8E241":
                "https://orcid.org/0000-0001-6952-7773",
            # David Tappin - BGS
            "https://gtr.ukri.org:443/gtr/api/persons/2A66F565-101A-46A7-A306-2740803946BE":
                "https://orcid.org/0000-0003-3186-8403",
            # Carl Percival - Manchester
            "https://gtr.ukri.org:443/gtr/api/persons/2C40BFD4-78D8-4474-A310-60EEEB4D4367":
                "https://orcid.org/0000-0003-2525-160X",
            # David Marshall - Oxford
            "https://gtr.ukri.org:443/gtr/api/persons/2E94CCB3-6825-4CC3-BF3D-3EF3DC94095E":
                "https://orcid.org/0000-0002-5199-6579",
            # Matthew Piggott - Imperial
            "https://gtr.ukri.org:443/gtr/api/persons/3015433E-450E-4FFC-84C8-A8C98F95C19F":
                "https://orcid.org/0000-0002-7526-6853",
            # Peter Challenor - Exeter
            "https://gtr.ukri.org:443/gtr/api/persons/36A16C19-AD10-4C08-9AA5-2DA6BF1805C1":
                "https://orcid.org/0000-0001-8661-2718",
            # Dan Charman - Exeter
            "https://gtr.ukri.org:443/gtr/api/persons/3AF9853E-C741-4AFA-80A6-D81028DFF965":
                "https://orcid.org/0000-0003-3464-4536",
            # Doerthe Tetzlaff - Leibniz Institute of Freshwater Ecology
            "https://gtr.ukri.org:443/gtr/api/persons/3B2929B5-E2B3-4E97-AA3A-5E50A04E8DBB":
                "https://orcid.org/0000-0002-7183-8674",
            # Lucy Carpenter - York
            "https://gtr.ukri.org:443/gtr/api/persons/3BB1C2AE-A72C-4EE4-BEBC-9A26941B7FC9":
                "https://orcid.org/0000-0002-6257-3950",
            # Thomas Choularton - Manchester [needs organisation mapping manually]
            "https://gtr.ukri.org:443/gtr/api/persons/3CC2AEBF-3922-47F7-82C5-35F9748A3011":
                "https://orcid.org/0000-0002-0409-4329",
            # Kerry Dinsmore - CEH
            "https://gtr.ukri.org:443/gtr/api/persons/3ED15A53-9882-4859-9096-54BFFCF6474D":
                "https://orcid.org/0000-0002-3586-6256",
            # John King - BAS
            "https://gtr.ukri.org:443/gtr/api/persons/3EDDE53B-29D3-4B5B-BAFE-5F6198D2E5F1":
                "https://orcid.org/0000-0003-3315-7568",
            # Jonathan Jackson - OceanLab, University of Aberdeen [needs organisation mapping manually]
            "https://gtr.ukri.org:443/gtr/api/persons/41C3F70F-AA57-4176-AB5C-1A8DD4CEFFF9":
                'https://orcid.org/0000-0001-6387-3114',
            # Helen Johnson - Oxford [check mapping]
            "https://gtr.ukri.org:443/gtr/api/persons/5115097B-0BA3-4A05-A822-7A777FD7EEE5":
                'https://orcid.org/0000-0003-1873-2085',
            # Glenn Carver [Unknown?]
            "https://gtr.ukri.org:443/gtr/api/persons/517CA55C-9F65-4C9F-B6F5-E212FAAA59F1":
                'https://orcid.org/0000-0001-7582-6497',
            # Antonios Zervos - Southampton [check mapping]
            "https://gtr.ukri.org:443/gtr/api/persons/52EF2886-B160-4D84-9338-E49A2F60CD33":
                'http://orcid.org/0000-0002-2662-9320',
            # Iain Hartley - Exeter
            "https://gtr.ukri.org:443/gtr/api/persons/5425E38B-D4A4-4F7D-BC5D-ADEBADE91EAA":
                'https://orcid.org/0000-0002-9183-6617',
            # Paul Connolly - Manchester
            "https://gtr.ukri.org:443/gtr/api/persons/5D9BDBDF-E33A-4CEA-851D-170139511C17":
                'https://orcid.org/0000-0002-3294-7405',
            # Jeffery Priest - Calgary (prev. Southampton)
            "https://gtr.ukri.org:443/gtr/api/persons/650EAE92-D384-4F8F-96C0-8027C839AA5E":
                'https://orcid.org/0000-0001-5639-2101',
            # Benedict Rogers - Manchester
            "https://gtr.ukri.org:443/gtr/api/persons/657FE816-0279-44C6-AE38-AA7296375B10":
                'https://orcid.org/0000-0002-3269-7979',
            # Ed Hawkins - Reading
            "https://gtr.ukri.org:443/gtr/api/persons/65A4C49F-8C74-43F0-BCA3-B06AFE4E859D":
                'https://orcid.org/0000-0001-9477-3677',
            # Martin Gallagher - Manchester
            "https://gtr.ukri.org:443/gtr/api/persons/66F27E10-48BB-4714-9A85-9BCC4090FB65":
                'https://orcid.org/0000-0002-4968-6088',
            # Gareth Phoenix - Sheffield
            "https://gtr.ukri.org:443/gtr/api/persons/67095429-F0EF-47CD-B197-219035F0127D":
                'https://orcid.org/0000-0002-0911-8107',
            # James Dorsey - Manchester
            "https://gtr.ukri.org:443/gtr/api/persons/6A8E4532-EA54-4909-8DEC-1125A79A7FDE":
                'https://orcid.org/0000-0002-1720-9412',
            # Mark Inall - SAMS
            "https://gtr.ukri.org:443/gtr/api/persons/7542AC4E-A691-4B52-92DB-027DB27A247D":
                'https://orcid.org/0000-0002-1624-4275',
            # Sue Dawson - Dundee
            "https://gtr.ukri.org:443/gtr/api/persons/777013B8-E933-4376-9EA6-828D6D17C822":
                'https://orcid.org/0000-0001-8115-4551',
            # Daniel Feltham - Reading
            "https://gtr.ukri.org:443/gtr/api/persons/77F2F26D-01E9-41D8-9FDF-82087A6A1CF1":
                'https://orcid.org/0000-0003-2289-014X',
            # Jens-Arne Subke - Stirling
            "https://gtr.ukri.org:443/gtr/api/persons/79B6AE08-32D0-40C5-991E-369ACB7A6D56":
                'https://orcid.org/0000-0001-9244-639X',
            # Lee Cunningham - Manchester
            "https://gtr.ukri.org:443/gtr/api/persons/79EB4379-F6F4-410C-B31F-BE021E3F0639":
                'http://orcid.org/0000-0002-7686-7490',
            # Alberto Naveira Garabato - Southampton
            "https://gtr.ukri.org:443/gtr/api/persons/828DE68A-0A00-4ACF-B386-584524C563BE":
                'https://orcid.org/0000-0001-6071-605X',
            # Richard Essery - Edinburgh
            "https://gtr.ukri.org:443/gtr/api/persons/86F46246-B5D0-444A-861F-1C71DF678511":
                'http://orcid.org/0000-0003-1756-9095',
            # Jacqueline Hamilton - York
            "https://gtr.ukri.org:443/gtr/api/persons/8C1A67B8-1338-4644-888A-E583BDACF5DF":
                'https://orcid.org/0000-0003-0975-4311',
            # Julian Murton - Sussex
            "https://gtr.ukri.org:443/gtr/api/persons/8D799711-CEB0-4DF1-A534-B10AFF1EAC26":
                'https://orcid.org/0000-0002-9469-5856',
            # Kim Last - SAMS
            "https://gtr.ukri.org:443/gtr/api/persons/90679B1B-37B4-4290-A0F1-777FBACFD849":
                'https://orcid.org/0000-0001-9402-2347',
            # Peter Allison - Imperial
            "https://gtr.ukri.org:443/gtr/api/persons/9296FC3E-797B-4F98-8DD2-F690561F9C90":
                'https://orcid.org/0000-0002-4997-5314',
            # Julian Dowdeswell - SPRI, Cambridge
            "https://gtr.ukri.org:443/gtr/api/persons/9394F178-672F-4841-A7D2-11BAA0F96CA4":
                'https://orcid.org/0000-0003-1369-9482',
            # Matthew Collins - Exeter
            "https://gtr.ukri.org:443/gtr/api/persons/9920CC72-2421-470F-BAD2-F70C4D6F7777":
                'https://orcid.org/0000-0003-3785-6008',
            # Garry Hayman - CEH
            "https://gtr.ukri.org:443/gtr/api/persons/9AE998A7-816E-4351-9152-2EC0794F4F42":
                'http://orcid.org/0000-0003-3825-4156',
            # Emily Shuckburgh - Cambridge (prev. BAS)
            "https://gtr.ukri.org:443/gtr/api/persons/9FD6EE4D-1FA0-4C91-9029-9B8C8ECFF9D0":
                'https://orcid.org/0000-0001-9206-3444',
            # Ian Renfrew - UEA
            "https://gtr.ukri.org:443/gtr/api/persons/A243B3E6-B6CF-49CE-B9CD-95B34AF61D22":
                'https://orcid.org/0000-0001-9379-8215',
            # Euan Nisbet - Royal Holloway
            "https://gtr.ukri.org:443/gtr/api/persons/A39C85BA-D5AA-4B93-9221-A8FF9AFD8D19":
                'https://orcid.org/0000-0001-9379-8215',
            # Byongjun Hwang - Huddersfield
            "https://gtr.ukri.org:443/gtr/api/persons/A745D5F8-8F0A-4F23-B6F7-340B8B83BE04":
                'https://orcid.org/0000-0003-4579-2040',
            # Gordon McFiggans - Manchester
            "https://gtr.ukri.org:443/gtr/api/persons/A757DCA4-11A9-4E31-A909-4178F9A4326C":
                'https://orcid.org/0000-0002-3423-7896',
            # Alistair Dawson [Should be Alastair] - Dundee
            "https://gtr.ukri.org:443/gtr/api/persons/AA1CB5E7-4FA2-4BB1-9207-E3956F7076A3":
                'https://orcid.org/0000-0002-8383-8487',
            # Tom Rippeth - Bangor
            "https://gtr.ukri.org:443/gtr/api/persons/AB6BDE0A-2AE2-47A0-9D67-2251B15C6113":
                'http://orcid.org/0000-0002-9286-0176',
            # Mary Edwards - Southampton
            "https://gtr.ukri.org:443/gtr/api/persons/AB93A48C-73D3-4A83-B629-313E442A0AF9":
                'https://orcid.org/0000-0002-3490-6682',
            # Nicholas Anderson - Loughborough
            "https://gtr.ukri.org:443/gtr/api/persons/B11BBEC7-B32B-4456-A861-B1EAA6C960E3":
                'https://orcid.org/0000-0002-0037-0306',
            # Kevin Horsburgh - NOC
            "https://gtr.ukri.org:443/gtr/api/persons/B17B3FE8-113A-47B9-85C8-E0D3D59EFEB6":
                'https://orcid.org/0000-0003-4803-9919',
            # Jonathan Crosier - Manchester
            "https://gtr.ukri.org:443/gtr/api/persons/B3C9A6AB-1A74-4A47-ADE7-E611573CB913":
                'http://orcid.org/0000-0002-3086-4729',
            # Mathew Williams - Edinburgh
            "https://gtr.ukri.org:443/gtr/api/persons/B5BB39B9-0CFA-4514-8973-73C327F59EFE":
                'https://orcid.org/0000-0001-6117-5208',
            # Philip Wookey - Stirling
            "https://gtr.ukri.org:443/gtr/api/persons/B6D05E2A-9AD1-4761-B846-552D67EF7926":
                'https://orcid.org/0000-0001-5957-6424',
            # Paul Dunlop - Ulster
            "https://gtr.ukri.org:443/gtr/api/persons/B7AB74E8-2DBC-44C0-A1D6-7D838DE08FB6":
                'https://orcid.org/0000-0001-9503-5545',
            # Maria Luneva - NOC
            "https://gtr.ukri.org:443/gtr/api/persons/B7B83DE3-1412-4784-9722-23C818F7683E":
                'https://orcid.org/0000-0003-3240-5427',
            # Suleyman Sami Nalbant - Edinburgh
            "https://gtr.ukri.org:443/gtr/api/persons/B908935E-F993-4EAF-9476-1ABA02A4C616":
                'https://orcid.org/0000-0002-7944-5912',
            # Robert Baxter - Durham
            "https://gtr.ukri.org:443/gtr/api/persons/CDF2B354-9377-4106-B9CB-634C20D4D898":
                'https://orcid.org/0000-0002-7504-6797',
            # Chris Ian Clayton (C R I) - Southampton
            "https://gtr.ukri.org:443/gtr/api/persons/D08E6379-0AB3-40A4-BD55-E73AAC8E2A86":
                'https://orcid.org/0000-0003-0071-8437',
            # Gareth Collins - Imperial
            "https://gtr.ukri.org:443/gtr/api/persons/D11D73BD-AD47-4A9A-979A-DAB6CBAED9CE":
                'https://orcid.org/0000-0002-6087-6149',
            # Peter Stansby - Manchester
            "https://gtr.ukri.org:443/gtr/api/persons/D246DD86-5AD6-49B8-90BA-7061CD202A51":
                'https://orcid.org/0000-0002-3552-0810',
            # Leonard Shaffrey - Reading
            "https://gtr.ukri.org:443/gtr/api/persons/D7395893-00A2-438A-8423-674DDC4AEF22":
                'https://orcid.org/0000-0003-2696-752X',
            # Keith Davidson - SAMS
            "https://gtr.ukri.org:443/gtr/api/persons/DC235160-418A-461C-996D-4AC2A95D3126":
                'https://orcid.org/0000-0001-9269-3227',
            # Peter Talling - Durham
            "https://gtr.ukri.org:443/gtr/api/persons/E186C90F-0312-49F0-9CE8-47E042A5A84F":
                'https://orcid.org/0000-0001-5234-0398',
            # Keith Bower - Manchester
            "https://gtr.ukri.org:443/gtr/api/persons/E58BC862-996B-4456-84DA-CD9EF3F11A76":
                'https://orcid.org/0000-0002-9802-3264',
            # James Hopkins - York
            "https://gtr.ukri.org:443/gtr/api/persons/E90C079C-3E8B-42C0-AAC6-A9610CA3653C":
                'http://orcid.org/0000-0002-0447-2633',
            # David Meldrum - SAMS
            "https://gtr.ukri.org:443/gtr/api/persons/ECB88D53-17E8-4F83-A11F-24B4654A19B3":
                'https://orcid.org/0000-0002-9431-7257',
            # Adrian Martin - Southampton
            "https://gtr.ukri.org:443/gtr/api/persons/EE778812-DC4E-4C32-A19F-764FCAA18AE0":
                'https://orcid.org/0000-0002-1202-8612',
            # James Allan - Manchester
            "https://gtr.ukri.org:443/gtr/api/persons/F011D67C-29CD-4E8E-AFB0-DD8FDEA8F950":
                'http://orcid.org/0000-0001-6492-4876',
            # Suzanne McGowan - Nottingham
            "https://gtr.ukri.org:443/gtr/api/persons/F340DFB4-7E65-4C84-9299-793CD9053628":
                'https://orcid.org/0000-0003-4034-7140',
            # Andrew Shepherd - Leeds
            "https://gtr.ukri.org:443/gtr/api/persons/F37CEAD9-5B33-4B4B-B024-2EFE300DF6F9":
                'https://orcid.org/0000-0002-4914-1299',
            # Walter Distaso - Imperial
            "https://gtr.ukri.org:443/gtr/api/persons/F686AF09-E90E-4339-992A-FB610DFD9A92":
                'https://orcid.org/0000-0002-4122-0160',
            # Sheldon Bacon - NOC
            "https://gtr.ukri.org:443/gtr/api/persons/F99A9B4B-CB30-424B-8584-46AB9B1CD166":
                'https://orcid.org/0000-0002-2471-9373',
            # Ute Skiba - CEH
            "https://gtr.ukri.org:443/gtr/api/persons/FB186100-33CA-4438-BC44-B445A2FC7166":
                'https://orcid.org/0000-0001-8659-6092',
            # Michel Tsamados - UCL
            "https://gtr.ukri.org:443/gtr/api/persons/FFC933A9-265E-4B6F-8CA9-0DA86ADB6976":
                'https://orcid.org/0000-0001-7034-5360'
        }

        if self.resource_uri not in gtr_people_orcid_id_mappings.keys():
            raise UnmappedGatewayToResearchPerson(meta={
                'gtr_person': {
                    'resource_uri': self.resource_uri
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
            raise GatewayToResearchPublicationWithoutDOI(meta={
                'gtr_publication': {
                    'resource_uri': self.resource_uri
                }
            })

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
        self.research_topics = self._process_research_topics()
        self.research_subjects = self._process_research_subjects()
        self.publications = self._process_publications()
        self.fund = GatewayToResearchFund(
            gtr_resource_uri=self._find_gtr_fund_link())
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

            project_references[gtr_identifier['type']].append(
                gtr_identifier['value'])

        return project_references

    def _process_research_topics(self) -> List[dict]:
        """
        Here we process the research topics from the GTR resource into a list

        :rtype list
        :return list of research topic classifications for a GTR project
        """
        gtr_project_topics = []
        if 'researchTopics' in self.resource:
            if 'researchTopic' in self.resource['researchTopics']:
                if len(self.resource['researchTopics']['researchTopic']) > 0:
                    for gtr_research_topic in self.resource['researchTopics']['researchTopic']:
                        if 'id' in gtr_research_topic:
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
        if 'researchSubjects' in self.resource:
            if 'researchSubject' in self.resource['researchSubjects']:
                if len(self.resource['researchSubjects']['researchSubject']) > 0:
                    for gtr_research_subject in self.resource['researchSubjects']['researchSubject']:
                        if 'id' in gtr_research_subject:
                            gtr_project_subjects.append(
                                gtr_research_subject)

        return gtr_project_subjects

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
                publication = GatewayToResearchPublication(
                    gtr_resource_uri=publication_uri)
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
            raise KeyError(
                "Multiple GTR fund identifiers found in GTR project links, one expected")

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
                raise ValueError(
                    "Multiple project elements found in GTR response, only expected one")

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
            * _map_gtr_project_research_topic_to_category_term()
            * _map_gtr_project_research_subject_to_category_term()
        """
        gtr_project = GatewayToResearchProject(
            gtr_resource_uri=f"https://gtr.ukri.org/gtr/api/projects/{self.gtr_project_id}"
        )

        grant = Grant(
            neutral_id=generate_neutral_id(),
            reference=self._find_gtr_project_identifier(
                identifiers=gtr_project.identifiers),
            title=gtr_project.title,
            abstract=gtr_project.abstract,
            status=self._map_gtr_project_status(status=gtr_project.status),
            duration=gtr_project.fund.duration,
            total_funds_currency=gtr_project.fund.currency,
            total_funds=gtr_project.fund.amount,
            publications=gtr_project.publications,
            funder=Organisation.query.filter_by(
                grid_identifier=gtr_project.fund.funder.grid_id).one_or_none()
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

        # Research Topics and Research Subjects
        topics = self._find_unique_gtr_project_research_topics(
            gtr_research_topics=gtr_project.research_topics
        )

        subjects = self._find_unique_gtr_project_research_subjects(
            gtr_research_subjects=gtr_project.research_subjects
        )

        # Flatten the processed topics and subjects to dinstinct list of GCMD identifiers
        category_term_scheme_identifiers = list(topics)
        category_term_scheme_identifiers.extend(
            x for x in subjects if x not in category_term_scheme_identifiers)

        for category_term_scheme_identifier in category_term_scheme_identifiers:
            db.session.add(Categorisation(
                neutral_id=generate_neutral_id(),
                project=project,
                category_term=CategoryTerm.query.filter_by(
                    scheme_identifier=category_term_scheme_identifier).one()
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
            raise KeyError(
                "RCUK/GTR identifier not in GTR project identifiers")
        if len(identifiers['RCUK']) == 0:
            raise KeyError(
                "RCUK/GTR identifier not in GTR project identifiers")
        if len(identifiers['RCUK']) > 1:
            raise KeyError(
                "Multiple RCUK/GTR identifiers in GTR project identifiers, one expected")

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
                raise ValueError(
                    "GTR project person could not be mapped to a Person, no ORCID iD")

            if not db.session.query(exists().where(Person.orcid_id == person.orcid_id)).scalar():
                db.session.add(Person(
                    neutral_id=generate_neutral_id(),
                    first_name=person.first_name,
                    last_name=person.surname,
                    orcid_id=person.orcid_id,
                    organisation=Organisation.query.filter_by(
                        grid_identifier=person.employer.grid_id).one_or_none()
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
        if status == 'Active':
            return GrantStatus.Active
        elif status == 'Closed':
            return GrantStatus.Closed

        raise ValueError(
            "Status element value in GTR project not mapped to a member of the GrantStatus enumeration")

    def _find_unique_gtr_project_research_topics(self, gtr_research_topics: list) -> list:
        """
        For a series of GTR project research topics, return a distinct list

        If the 'unclassified' category is included, it is silently removed.

        :type gtr_research_topics: list
        :param gtr_research_topics: list of GTR project research topics

        :rtype list
        :return: distinct list of GTR project research topics
        """
        category_term_scheme_identifiers = []
        for category in gtr_research_topics:
            category_term_scheme_identifier = self._map_gtr_project_research_topic_to_category_term(
                category)
            if category_term_scheme_identifier is not None:
                if category_term_scheme_identifier not in category_term_scheme_identifiers:
                    category_term_scheme_identifiers.append(
                        category_term_scheme_identifier)
        return category_term_scheme_identifiers

    def _find_unique_gtr_project_research_subjects(self, gtr_research_subjects: list) -> list:
        """
        For a series of GTR project subjects, return a distinct list

        :type gtr_research_subjects: list
        :param gtr_research_subjects: list of GTR project research subjects

        :rtype list
        :return: distinct list of GTR project research subjects
        """
        category_term_scheme_identifiers = []
        for category in gtr_research_subjects:
            category_term_scheme_identifier = self._map_gtr_project_research_subject_to_category_term(
                category)
            if category_term_scheme_identifier is not None:
                if category_term_scheme_identifier not in category_term_scheme_identifiers:
                    category_term_scheme_identifiers.append(
                        category_term_scheme_identifier)
        return category_term_scheme_identifiers

    @staticmethod
    def _map_gtr_project_research_topic_to_category_term(gtr_research_topic: dict) -> Optional[str]:
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
        if gtr_research_topic['id'] == 'E4C03353-6311-43F9-9204-CFC2536D2017':
            return 'https://gcmdservices.gsfc.nasa.gov/kms/concept/c47f6052-634e-40ef-a5ac-13f69f6f4c2a'
        elif gtr_research_topic['id'] == 'C62D281D-F1B9-423D-BDAB-361EC9BE7C68':
            return 'https://gcmdservices.gsfc.nasa.gov/kms/concept/286d2ae0-9d86-4ef0-a2b4-014843a98532'
        elif gtr_research_topic['id'] == 'C29F371D-A988-48F8-BFF5-1657DAB1176F':
            return 'https://gcmdservices.gsfc.nasa.gov/kms/concept/286d2ae0-9d86-4ef0-a2b4-014843a98532'
        elif gtr_research_topic['id'] == 'B01D3878-E7BD-4830-9503-2F54544E809E':
            return 'https://gcmdservices.gsfc.nasa.gov/kms/concept/286d2ae0-9d86-4ef0-a2b4-014843a98532'
        # Community Ecology
        elif gtr_research_topic['id'] == 'F4786876-D9A9-404D-8569-BBC813C73074':
            # COMMUNITY DYNAMICS
            return 'https://gcmdservices.gsfc.nasa.gov/kms/concept/8fb66b46-b998-4412-a541-d2acabdf484b'
        # Biogeochemical Cycles
        elif gtr_research_topic['id'] == '62DCC1BF-B512-4BDB-A0C3-02BC17E15F6B':
            # BIOGEOCHEMICAL CYCLES
            return 'https://gcmdservices.gsfc.nasa.gov/kms/concept/9015e65f-bbae-4855-a4b6-1bfa601752bd'
        # Climate & Climate Change
        elif gtr_research_topic['id'] == 'EE4457DB-92A3-44EA-8D5F-77013CC107E0':
            # CLIMATE INDICATORS
            return 'https://gcmdservices.gsfc.nasa.gov/kms/concept/23703b6b-ee15-4512-b5b2-f441547e2edf'
        # Hydrological Processes
        elif gtr_research_topic['id'] == 'D4F391DF-BCE0-47FA-BED7-78025F16B14D':
            # COASTAL PROCESSES
            return 'https://gcmdservices.gsfc.nasa.gov/kms/concept/b6fd22ab-dca7-4dfa-8812-913453b5695b'
        # Geohazards
        elif gtr_research_topic['id'] == 'BE94F009-26A1-4E5B-B0B3-722A355F282C':
            # NATURAL HAZARDS
            return 'https://gcmdservices.gsfc.nasa.gov/kms/concept/ec0e2762-f57a-4fdc-b395-c8d7d5590d18'
        # Sediment/Sedimentary Processes
        elif gtr_research_topic['id'] == '5537B6B2-9FD6-40FB-B300-64555528D3FF':
            # EROSION/SEDIMENTATION
            return 'https://gcmdservices.gsfc.nasa.gov/kms/concept/a246a8cf-e3f9-4045-af9f-dc97f6fe019a'
        # Environmental Microbiology
        elif gtr_research_topic['id'] == '5B73146D-6DEF-4D88-BE83-FE7B9DB21D62':
            # BIOLOGICAL CLASSIFICATION
            return 'https://gcmdservices.gsfc.nasa.gov/kms/concept/fbec5145-79e6-4ed0-a804-6228aa6daba5'
        # Glacial & Cryospheric Systems
        elif gtr_research_topic['id'] == '07B1BD3F-A7ED-4640-8B09-C1F296DC56BF':
            # GLACIERS/ICE SHEETS
            return 'https://gcmdservices.gsfc.nasa.gov/kms/concept/099ab1ae-f4d2-48cc-be2f-86bd58ffc4ca'
        # Soil science
        elif gtr_research_topic['id'] == '96F70ACB-D35F-416F-9360-4EFD402DFA6B':
            # SOILS
            return 'https://gcmdservices.gsfc.nasa.gov/kms/concept/3526afb8-0dc9-43c7-8ad4-f34f250a1e91'
        # Ecosystem Scale Processes
        elif gtr_research_topic['id'] == '12C7A68B-3922-4925-9C0B-7FACEC921815':
            # ECOSYSTEMS
            return 'https://gcmdservices.gsfc.nasa.gov/kms/concept/f1a25060-330c-4f84-9633-ed59ae8c64bf'
        # Unclassified
        elif gtr_research_topic['id'] == 'D05BC2E0-0345-4A3F-8C3F-775BC42A0819':
            return None

        raise UnmappedGatewayToResearchProjectTopic(meta={
            'gtr_research_topic': {
                'id': gtr_research_topic['id'],
                'name': gtr_research_topic['text']
            }
        })

    @staticmethod
    def _map_gtr_project_research_subject_to_category_term(gtr_research_subject: dict) -> Optional[str]:
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
        if gtr_research_subject['text'] == 'Terrest. & freshwater environ.':
            return 'https://gcmdservices.gsfc.nasa.gov/kms/concept/91c64c46-d040-4daa-b26c-61952fdfaf50'
        elif gtr_research_subject['text'] == 'Ecol, biodivers. & systematics':
            return 'https://gcmdservices.gsfc.nasa.gov/kms/concept/f1a25060-330c-4f84-9633-ed59ae8c64bf'
        elif gtr_research_subject['text'] == 'Marine environments':
            return 'https://gcmdservices.gsfc.nasa.gov/kms/concept/91697b7d-8f2b-4954-850e-61d5f61c867d'
        elif gtr_research_subject['text'] == 'Geosciences':
            return 'https://gcmdservices.gsfc.nasa.gov/kms/concept/2b9ad978-d986-4d63-b477-0f5efc8ace72'
        elif gtr_research_subject['text'] == 'Climate and climate change':
            return 'https://gcmdservices.gsfc.nasa.gov/kms/concept/c47f6052-634e-40ef-a5ac-13f69f6f4c2a'
        elif gtr_research_subject['text'] == 'Atmospheric phys. & chemistry':
            return 'https://gcmdservices.gsfc.nasa.gov/kms/concept/b9c56939-c624-467d-b196-e56a5b660334'

        raise UnmappedGatewayToResearchProjectSubject(meta={
            'gtr_research_subject': {
                'id': gtr_research_subject['id'],
                'name': gtr_research_subject['text']
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
        app.logger.info(
            f"Importing Gateway to Research (GTR) project with grant reference ({gtr_grant_reference})")
        echo(style(
            f"Importing Gateway to Research (GTR) project with grant reference ({gtr_grant_reference})"))
        importer = GatewayToResearchGrantImporter(
            gtr_grant_reference=gtr_grant_reference)
        if importer.exists():
            app.logger.info(f"Finished importing GTR project with grant reference ({gtr_grant_reference}) - Already "
                            f"imported")
            echo(style(f"Finished importing GTR project with grant reference ({gtr_grant_reference}) - Already "
                       f"imported", fg='green'))
            return True

        gtr_project_id = importer.search()
        if gtr_project_id is None:
            app.logger.error(f"Failed importing GTR project with grant reference ({gtr_grant_reference}) - No or "
                             f"multiple GTR projects found")
            echo(style(f"Failed importing GTR project with grant reference ({gtr_grant_reference}) - No or "
                       f"multiple GTR projects found", fg='red'))
            return False
        app.logger.info(f"... found GTR project for grant reference ({gtr_grant_reference}) - [{gtr_project_id}] - "
                        f"Importing")
        echo(style(f"... found GTR project for grant reference ({gtr_grant_reference}) - [{gtr_project_id}] - "
                   f"Importing"))

        importer.fetch()
        app.logger.info(
            f"Finished importing GTR project with grant reference ({gtr_grant_reference}), imported")
        echo(style(
            f"Finished importing GTR project with grant reference ({gtr_grant_reference}), imported", fg='green'
        ))
    except UnmappedGatewayToResearchOrganisation as e:
        app.logger.error(
            f"Unmapped GTR Organisation [{e.meta['gtr_organisation']['resource_uri']}]")
        echo(style(
            f"Unmapped GTR Organisation [{e.meta['gtr_organisation']['resource_uri']}]", fg='red'))
    except UnmappedGatewayToResearchPerson as e:
        app.logger.error(
            f"Unmapped GTR Person [{e.meta['gtr_person']['resource_uri']}]")
        echo(
            style(f"Unmapped GTR Person [{e.meta['gtr_person']['resource_uri']}]", fg='red'))
    except GatewayToResearchPublicationWithoutDOI as e:
        app.logger.error(
            f"GTR Publication has no DOI [{e.meta['gtr_publication']['resource_uri']}]")
        echo(style(
            f"GTR Publication has no DOI [{e.meta['gtr_publication']['resource_uri']}]", fg='red'))
    except UnmappedGatewayToResearchProjectTopic as e:
        app.logger.error(
            f"Unmapped GTR Topic [{e.meta['gtr_research_topic']['id']}, {e.meta['gtr_research_topic']['name']}]")
        echo(style(
            f"Unmapped GTR Topic [{e.meta['gtr_research_topic']['id']}, {e.meta['gtr_research_topic']['name']}]", fg='red'
        ))
    except UnmappedGatewayToResearchProjectSubject as e:
        app.logger.error(
            f"Unmapped GTR Subject [{e.meta['gtr_research_subject']['id']}, {e.meta['gtr_research_subject']['name']}]")
        echo(style(
            f"Unmapped GTR Subject [{e.meta['gtr_research_subject']['id']}, {e.meta['gtr_research_subject']['name']}]", fg='red'
        ))
    except Exception as e:
        db.session.rollback()
        # Remove any added, but non-committed, entities
        db.session.flush()
        raise e
