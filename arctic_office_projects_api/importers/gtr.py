import requests

from datetime import date, datetime, timezone
from typing import Dict, Optional, List
from urllib.parse import quote as url_encode

from click import echo, style
from psycopg2.extras import DateRange
from requests import HTTPError
# noinspection PyPackageRequirements
from sqlalchemy import exists, and_
from sqlalchemy_utils import Ltree

from arctic_office_projects_api.errors import AppException
from arctic_office_projects_api.extensions import db
from arctic_office_projects_api.utils import generate_neutral_id
from arctic_office_projects_api.models import CategoryScheme, CategoryTerm, Grant, GrantStatus, GrantCurrency, Organisation, Project, \
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

            # Remove http://internal-gtr-tomcat-alb-611010599.eu-west-2.elb.amazonaws.com:8080
            # Replace with https://gtr.ukri.org

            link_href = link['href']

            link_base_url = link['href'].split(":")
            if link_base_url[1] == "//internal-gtr-tomcat-alb-611010599.eu-west-2.elb.amazonaws.com":
                link_href = link['href'].replace(
                    "http://internal-gtr-tomcat-alb-611010599.eu-west-2.elb.amazonaws.com:8080",
                    "https://gtr.ukri.org"
                )

            links[link['rel']].append(link_href)

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

        self.ror_id = self._map_to_ror()

    def _ror_dict(resource_uri) -> str:

        ror_dict = {
            # Natural Environment Research Council
            "https://gtr.ukri.org/gtr/api/organisations/8A03ED41-E67D-4F4A-B5DD-AAFB272B6471": "https://api.ror.org/organizations?query=02b5d8509",
            # University of Leeds
            "https://gtr.ukri.org/gtr/api/organisations/83D87776-5958-42AE-889D-B8AECF16B468": "https://api.ror.org/organizations?query=024mrxd33",
            # University of Sheffield
            "https://gtr.ukri.org/gtr/api/organisations/03D8AFBB-3EA5-4885-B036-BD4F9F4F9849": "https://api.ror.org/organizations?query=05krs5044",
            # Scottish Association For Marine Science
            "https://gtr.ukri.org/gtr/api/organisations/1ED25A21-FD91-4EC2-A06F-724F9F2CDC3D": "https://api.ror.org/organizations?query=04ke6ht85",
            # NERC British Antarctic Survey
            "https://gtr.ukri.org/gtr/api/organisations/21CFC584-0BCD-450C-B2C1-EFF574194DBF": "https://api.ror.org/organizations?query=01rhff309",
            # University of Ulster
            "https://gtr.ukri.org/gtr/api/organisations/245EB81A-808F-4697-BAED-263C20266B74": "https://api.ror.org/organizations?query=01yp9g959",
            # University of Edinburgh
            "https://gtr.ukri.org/gtr/api/organisations/2DB7ED73-8E89-457A-A395-FAC12F929C1A": "https://api.ror.org/organizations?query=01nrxwf90",
            # University of Southampton
            "https://gtr.ukri.org/gtr/api/organisations/30A429E3-83B7-4E41-99C0-14A144F07DFE": "https://api.ror.org/organizations?query=01ryk1543",
            # University College London
            "https://gtr.ukri.org/gtr/api/organisations/3A5E126D-C175-4730-9B7B-E6D8CF447F83": "https://api.ror.org/organizations?query=02jx3x895",
            # University of Oxford
            "https://gtr.ukri.org/gtr/api/organisations/3EAE04CA-9D62-4483-B9C4-F91AD9F4C5A9": "https://api.ror.org/organizations?query=052gg0110",
            # Imperial College London
            "https://gtr.ukri.org/gtr/api/organisations/46387D84-F71E-4B7D-8C7D-9C288F113510": "https://api.ror.org/organizations?query=041kmwe10",
            # Durham University
            "https://gtr.ukri.org/gtr/api/organisations/46B41008-0EB4-4E28-BBFB-E98366999EC5": "https://api.ror.org/organizations?query=01v29qb04",
            # National Oceanography Centre 1
            "https://gtr.ukri.org/gtr/api/organisations/4DB630C7-7E13-4610-A1C3-29601903CEE3": "https://api.ror.org/organizations?query=00874hx02",
            # National Oceanography Centre 2
            "https://gtr.ukri.org/gtr/api/organisations/333FAC7F-030F-4A9C-87FD-78DB66107E58": "https://api.ror.org/organizations?query=00874hx02",
            # NERC Centre for Ecology and Hydrology
            "https://gtr.ukri.org/gtr/api/organisations/4FC881BE-799E-459C-A287-2A68170426DA": "https://api.ror.org/organizations?query=00pggkr55",
            # UK Ctr for Ecology & Hydrology fr 011219
            "https://gtr.ukri.org/gtr/api/organisations/2431A6E2-13D5-40AB-A58A-AC75E6A3654E": "https://api.ror.org/organizations?query=00pggkr55",
            # University of Manchester
            "https://gtr.ukri.org/gtr/api/organisations/68D0E3C9-9246-4CFC-B5E9-48584CF82993": "https://api.ror.org/organizations?query=027m9bs27",
            # Royal Holloway, University of London
            "https://gtr.ukri.org/gtr/api/organisations/7A0397DD-E0C6-4EA3-8031-B841D2503C4D": "https://api.ror.org/organizations?query=04g2vpn86",
            # NERC British Geological Survey
            "https://gtr.ukri.org/gtr/api/organisations/7ADE0AB2-1050-4241-987D-F3B1C3322E05": "https://api.ror.org/organizations?query=04a7gbp98",
            # University of York
            "https://gtr.ukri.org/gtr/api/organisations/8319F78A-DCBD-49F6-BE00-78E1CD75CDA9": "https://api.ror.org/organizations?query=04m01e293",
            # University of East Anglia
            "https://gtr.ukri.org/gtr/api/organisations/88C5F7F9-8DCC-41C9-BC4F-F37DA01075C7": "https://api.ror.org/organizations?query=026k5mg93",
            # University of the Highlands and Islands
            "https://gtr.ukri.org/gtr/api/organisations/8BA3C264-769F-487E-B61A-2D4CB6A105B6": "https://api.ror.org/organizations?query=02s08xt61",
            # University of Dundee
            "https://gtr.ukri.org/gtr/api/organisations/90051600-6EF2-4093-BA8C-2B4B6F550895": "https://api.ror.org/organizations?query=03h2bxq36",
            # University of Nottingham
            "https://gtr.ukri.org/gtr/api/organisations/936D002F-A8D1-4A93-AE5D-825ED0903D8D": "https://api.ror.org/organizations?query=01ee9ar58",
            # University of Portsmouth
            "https://gtr.ukri.org/gtr/api/organisations/955C55E8-783E-4842-BB2C-2D275A3CAF82": "https://api.ror.org/organizations?query=03ykbk197",
            # University of Exeter
            "https://gtr.ukri.org/gtr/api/organisations/961756BF-E31F-4A13-836F-0A09BA02385C": "https://api.ror.org/organizations?query=03yghzc09",
            # University of Sussex
            "https://gtr.ukri.org/gtr/api/organisations/A8967420-49D3-4509-9912-25FB3EC75B74": "https://api.ror.org/organizations?query=00ayhx656",
            # Leibniz Institute of Freshwater Ecology
            "https://gtr.ukri.org/gtr/api/organisations/AB007A2D-2086-4B7A-8539-DBD5836A8503": "https://api.ror.org/organizations?query=01nftxb06",
            # University of Stirling
            "https://gtr.ukri.org/gtr/api/organisations/C7510606-A36F-4725-A89B-9D592374972A": "https://api.ror.org/organizations?query=045wgfr59",
            # Loughborough University
            "https://gtr.ukri.org/gtr/api/organisations/CAA9A40D-0226-4A4F-AC0D-D8299E30A1EF": "https://api.ror.org/organizations?query=04vg4w365",
            # University of Cambridge
            "https://gtr.ukri.org/gtr/api/organisations/D1774113-D5D2-4B7C-A412-66A90FE4B96F": "https://api.ror.org/organizations?query=013meh722",
            # University of Huddersfield
            "https://gtr.ukri.org/gtr/api/organisations/DC934AED-9432-4385-AEAF-006EA2369001": "https://api.ror.org/organizations?query=05t1h8f27",
            # University of Reading
            "https://gtr.ukri.org/gtr/api/organisations/E89C3602-0FB4-4044-A918-58966B8A10B2": "https://api.ror.org/organizations?query=05v62cm79",
            # University of Aberdeen
            "https://gtr.ukri.org/gtr/api/organisations/F7E13617-2678-475B-99E4-31479C92038D": "https://api.ror.org/organizations?query=016476m91",
            # Bangor University
            "https://gtr.ukri.org/gtr/api/organisations/F9F1D136-12E3-4BE4-9668-0C9BC4A7C1BF": "https://api.ror.org/organizations?query=006jb1a24",
            # Marine Biological Association
            "https://gtr.ukri.org/gtr/api/organisations/309F361A-A8CC-438D-AB70-93C74E1E91C3": "https://api.ror.org/organizations?query=046dg4z72",
            # University of St Andrews
            "https://gtr.ukri.org/gtr/api/organisations/C0E4FAD2-3C8B-410A-B6DF-3B9B9E433060": "https://api.ror.org/organizations?query=02wn5qz54",
            # Northumbria University
            "https://gtr.ukri.org/gtr/api/organisations/EF390CF0-ECD3-47D8-B9A8-7602AF319BEE": "https://api.ror.org/organizations?query=049e6bc10",
            # Plymouth Marine Laboratory
            "https://gtr.ukri.org/gtr/api/organisations/EEF9EA95-341D-48C2-8A68-B838D35497C8": "https://api.ror.org/organizations?query=05av9mn02",
            # Newcastle University
            "https://gtr.ukri.org/gtr/api/organisations/5E2B04DD-4A03-45ED-9892-61C5CCB8AC68": "https://api.ror.org/organizations?query=01kj2bm70",
            # Aarhus University
            "https://gtr.ukri.org/gtr/api/organisations/CE43EBFA-3FC9-44BC-B6FF-001F11664C46": "https://api.ror.org/organizations?query=01aj84f44",
            # Lancaster University 1
            "https://gtr.ukri.org/gtr/api/organisations/8A66BFC9-B9A5-48C6-B46C-761D1C13C5DC": "https://api.ror.org/organizations?query=04f2nsd36",
            # Lancaster University 2
            "https://gtr.ukri.org/gtr/api/organisations/44160F04-5CBF-4E8E-A6C6-C0EF61A5865C": "https://api.ror.org/organizations?query=04f2nsd36",
            # University of Strathclyde
            "https://gtr.ukri.org/gtr/api/organisations/5BB4F8BF-B4E0-4EAF-9AF5-885E19D64850": "https://api.ror.org/organizations?query=00n3w3b69",
            # Free University of Brussels
            "https://gtr.ukri.org/gtr/api/organisations/773AC409-21D1-4CA0-87AA-1769A45D718E": "https://api.ror.org/organizations?query=02vpfbn76",
            # Warwick University
            "https://gtr.ukri.org/gtr/api/organisations/B6FB652A-60C3-48DD-9A33-075D1F759B48": "https://api.ror.org/organizations?query=01a77tt86",
            # Bristol University
            "https://gtr.ukri.org/gtr/api/organisations/4A348A76-B2D0-4DDD-804A-CE735A6D3798": "https://api.ror.org/organizations?query=0524sp257",
            # Aberystwyth University
            "https://gtr.ukri.org/gtr/api/organisations/E4757A6E-7326-472B-9979-B47D77A65446": "https://api.ror.org/organizations?query=015m2p889",
            # University of Hull
            "https://gtr.ukri.org/gtr/api/organisations/8A0FC07A-04CD-4F7A-9095-1D2E6C1D918F": "https://api.ror.org/organizations?query=04nkhwh30",
            # Essex University
            "https://gtr.ukri.org/gtr/api/organisations/ED6A6B32-663C-4A62-A33B-2C6A68E2E102": "https://api.ror.org/organizations?query=02nkf1q06",
            # Queen Mary, University of London
            "https://gtr.ukri.org/gtr/api/organisations/D5337A10-AC8A-402A-8164-C5F9CC6B0140": "https://api.ror.org/organizations?query=026zzn846",
            # Leicester University - 1
            "https://gtr.ukri.org/gtr/api/organisations/AE0A6F70-C175-4550-B08F-74C8790007BB": "https://api.ror.org/organizations?query=04h699437",
            # Leicester University - 2
            "https://gtr.ukri.org/gtr/api/organisations/C842A34F-18F7-454D-A259-FED802368496": "https://api.ror.org/organizations?query=04h699437",
            # Open University
            "https://gtr.ukri.org/gtr/api/organisations/89E6D9CB-DAF8-40A2-A9EF-B330A5A7FC24": "https://api.ror.org/organizations?query=02rv3w387",
            # Scottish Universities Environmental Research Centre
            "https://gtr.ukri.org/gtr/api/organisations/BF1F76BF-B87F-4FE0-B1DB-4650F5E99448": "https://api.ror.org/organizations?query=05jfq2w07",
            # Birmingham University 1
            "https://gtr.ukri.org/gtr/api/organisations/A022BD3A-2A7B-4E64-8877-A2E381C4CCB5": "https://api.ror.org/organizations?query=03angcq70",
            # Birmingham University 2
            "https://gtr.ukri.org/gtr/api/organisations/818CD6C9-61EE-41F2-9F37-0C7A8F43E25D": "https://api.ror.org/organizations?query=03angcq70",
            # The Natural History Museum
            "https://gtr.ukri.org/gtr/api/organisations/B2F6103D-47D2-486A-8F7C-C62362BAACD9": "https://api.ror.org/organizations?query=039zvsn29",
            # Plymouth University
            "https://gtr.ukri.org/gtr/api/organisations/7801F008-7C77-45E7-90E9-4345B47D138E": "https://api.ror.org/organizations?query=008n7pv89",
            # Glasgow University
            "https://gtr.ukri.org/gtr/api/organisations/AE58F21F-3622-4382-97BB-1359BD183E9F": "https://api.ror.org/organizations?query=00vtgdb53",
            # Cranfield University
            "https://gtr.ukri.org/gtr/api/organisations/F45A4578-F962-4EFA-9CC1-9F2FF4F760AE": "https://api.ror.org/organizations?query=05cncd958",
            # University of Liverpool
            "https://gtr.ukri.org/gtr/api/organisations/A0A585E0-6B0D-4643-A3A6-47943B4CBFEF": "https://api.ror.org/organizations?query=04xs57h96",
            # University of Lincoln
            "https://gtr.ukri.org/gtr/api/organisations/D64641C7-D9A6-4B41-9C8F-03F7396CB8DA": "https://api.ror.org/organizations?query=03yeq9x20",
            # Cardiff University
            "https://gtr.ukri.org/gtr/api/organisations/9C10D78F-6430-4CA7-9528-B96B0762A4C6": "https://api.ror.org/organizations?query=03kk7td41",
            # University of Abertay Dundee
            "https://gtr.ukri.org/gtr/api/organisations/544242A5-6640-4FD5-87C5-348557ED5307": "https://api.ror.org/organizations?query=04mwwnx67",
            # Free University of Brussels
            "https://gtr.ukri.org/gtr/api/organisations/FCD90BB9-BD1C-43D4-98EE-AE74283911E3": "https://api.ror.org/organizations?query=02vpfbn76",
            # Florida State University
            "https://gtr.ukri.org/gtr/api/organisations/B916CBD5-C485-400E-9973-216992E6F5DE": "https://api.ror.org/organizations?query=05g3dte14",
            # Manchester Metropolitan University
            "https://gtr.ukri.org/gtr/api/organisations/E594FDB4-DD6F-441F-90D6-C423A2916446": "https://api.ror.org/organizations?query=02hstj355",
            # Swansea University
            "https://gtr.ukri.org/gtr/api/organisations/AB307619-D4FA-427E-A042-09DBEBA84669": "https://api.ror.org/organizations?query=053fq8t95",
            # Higher School of Economics
            "https://gtr.ukri.org/gtr/api/organisations/7412B9A7-B073-4FA6-8710-19D1427488FB": "https://api.ror.org/organizations?query=055f7t516",
            # National Research Centre for Geosciences
            "https://gtr.ukri.org/gtr/api/organisations/8A4899C8-DF2F-44BC-8431-43C3785C02F7": "https://api.ror.org/organizations?query=00kn43d12",
            # University of Oslo
            "https://gtr.ukri.org/gtr/api/organisations/E30B7145-0051-47F4-B2D6-C93EE14B8568": "https://api.ror.org/organizations?query=01xtthb56",
            # British Trust for Ornithology
            "https://gtr.ukri.org/gtr/api/organisations/A8BE8EF6-CDA2-41D4-A52B-B66A41997D1D": "https://api.ror.org/organizations?query=03w54w620",
            # University of the West of England
            "https://gtr.ukri.org/gtr/api/organisations/2A80FFDA-3B8B-43BA-80C3-3AA850B49BA1": "https://api.ror.org/organizations?query=02nwg5t34",
            # Southampton Solent University
            "https://gtr.ukri.org/gtr/api/organisations/DD18D9A8-0FE2-4857-A405-7F41C183F65D": "https://api.ror.org/organizations?query=05xydav19",
            # Earlham Institute
            "https://gtr.ukri.org/gtr/api/organisations/B7B056A3-95CE-4F90-9F31-708B4612610D": "https://api.ror.org/organizations?query=018cxtf62",
            # Queen's University of Belfast
            "https://gtr.ukri.org/gtr/api/organisations/EC23DA53-CA73-4104-A3F6-2A9523484E69": "https://api.ror.org/organizations?query=00hswnk62",
            # Anglia Ruskin University
            "https://gtr.ukri.org/gtr/api/organisations/56F19F82-4654-46D6-891A-EA80CBC02587": "https://api.ror.org/organizations?query=0009t4v78",
            # Netherlands Inst of Ecology
            "https://gtr.ukri.org/gtr/api/organisations/223D9435-B6F9-4997-850B-DEEBCECC793B": "https://api.ror.org/organizations?query=01g25jp36",
            # King's College London
            "https://gtr.ukri.org/gtr/api/organisations/318B5D98-4CB4-4B10-A876-08FC93071A56": "https://api.ror.org/organizations?query=0220mzb33",
            # AHRC
            "https://gtr.ukri.org/gtr/api/organisations/1291772D-DFCE-493A-AEE7-24F7EEAFE0E9": "https://api.ror.org/organizations?query=0505m1554",
            # EPSRC
            "https://gtr.ukri.org/gtr/api/organisations/798CB33D-C79E-4578-83F2-72606407192C": "https://api.ror.org/organizations?query=0439y7842",
            # ESRC
            "https://gtr.ukri.org/gtr/api/organisations/924BE15C-91F2-4AAD-941A-3F338324B6AE": "https://api.ror.org/organizations?query=03n0ht308",
            # BBSRC
            "https://gtr.ukri.org/gtr/api/organisations/2512EF1C-401B-4222-9869-A770D4C5FAC7": "https://api.ror.org/organizations?query=00cwqg982",
            # Innovate Uk 1
            "https://gtr.ukri.org/gtr/api/organisations/1DA78802-0659-4398-B40B-7FA41B56BBF3": "https://api.ror.org/organizations?query=05ar5fy68",
            # Innovate Uk 2
            "https://gtr.ukri.org/gtr/api/organisations/E18E2F0F-AC7D-4E02-9559-669F7C8FEC74": "https://api.ror.org/organizations?query=05ar5fy68",
            # Innovate Uk 3
            "https://gtr.ukri.org/gtr/api/organisations/052C4F5E-74CA-4A1D-B771-82891497D8F5": "https://api.ror.org/organizations?query=05ar5fy68",
            # James Hutton Institute
            "https://gtr.ukri.org/gtr/api/organisations/326B6518-42F3-4CE4-B7C6-8494C6105BF1": "https://api.ror.org/organizations?query=03rzp5127",
            # University of Groningen
            "https://gtr.ukri.org/gtr/api/organisations/326EF7F4-5944-472D-BC94-2CA4484AEE74": "https://api.ror.org/organizations?query=012p63287",
            # Unknown
            "https://gtr.ukri.org/gtr/api/organisations/F0C1AEFB-C222-4BF6-9CA3-8CF628494537": "https://api.ror.org/organizations",
        }

        for ror in ror_dict:
            if resource_uri == ror:
                ror_value = ror_dict.get(ror)
                return ror_value

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
                'https://orcid.org/0000-0001-7034-5360',
            # Heather Alison Bouman - Oxford University
            "https://gtr.ukri.org:443/gtr/api/persons/CD9B1E18-1AA3-4E18-9A3F-C2DE79CBBCEB":
            'https://orcid.org/0000-0002-7407-9431',
            # Bart Egidius Van Dongen - Manchester University
            "https://gtr.ukri.org:443/gtr/api/persons/8FCE53A8-0C21-4162-93B1-7424EC08763C":
            'https://orcid.org/0000-0003-1189-142X',
            # Raja Ganeshram - University of Edinburgh
            "https://gtr.ukri.org:443/gtr/api/persons/89874E4D-902B-4B2B-873D-A95B4CFF4738":
            'https://orcid.org/0000-0002-5150-1310',
            # Geraint Andrew Tarling - BAS
            "https://gtr.ukri.org:443/gtr/api/persons/138BADBE-2FB1-4D7C-9444-DBD7AC82DF43":
            'https://orcid.org/0000-0002-3753-5899',
            # Daniel J Mayor - NOC
            "https://gtr.ukri.org:443/gtr/api/persons/1486F06E-695A-4E98-BD9B-9045254B3FEA":
            'https://orcid.org/0000-0002-1295-0041',
            # Yueng-Djern Lenn - Bangor
            "https://gtr.ukri.org:443/gtr/api/persons/E532D67A-59BE-41CC-8BE8-94DD3E8CCAFE":
            'https://orcid.org/0000-0001-6031-523X',
            # Joanne Hopkins - NOC
            "https://gtr.ukri.org:443/gtr/api/persons/EBE6F4FC-967E-4E29-9E61-A6076895BE04":
            'http://orcid.org/0000-0003-1504-3671',
            # Martin Solan - Southampton
            "https://gtr.ukri.org:443/gtr/api/persons/AFFB5A85-DAC7-48F2-AE07-952481073BAA":
            'https://orcid.org/0000-0001-9924-5574',
            # Ben Andrew Ward - Southampton
            "https://gtr.ukri.org:443/gtr/api/persons/50444B9C-4782-4135-AC0C-5DE9E7444A05":
            'https://orcid.org/0000-0003-1290-8270',
            # Ryan Reynolds Neely - Leeds
            "https://gtr.ukri.org:443/gtr/api/persons/622343F7-063E-4E4F-AD2B-3ABB95CB1590":
            'https://orcid.org/0000-0003-4560-4812',
            # Markus Michael Frey - BAS
            "https://gtr.ukri.org:443/gtr/api/persons/35CC6C9B-37C1-4791-BA52-EAA4FCC23D16":
            'https://orcid.org/0000-0003-0535-0416',
            # Julienne Stroeve - UCL
            "https://gtr.ukri.org:443/gtr/api/persons/7E95FFC4-B5D5-493A-B5A4-CC6B1BCEB7F6":
            'https://orcid.org/0000-0001-7316-8320',
            # Jeremy Charles Ely - Sheffield
            "https://gtr.ukri.org:443/gtr/api/persons/94CC9220-726B-4738-BF99-DF8E758765BC":
            'https://orcid.org/0000-0003-4007-1500',
            # Thomas John Bracegirdle - BAS
            "https://gtr.ukri.org:443/gtr/api/persons/BD3F03BA-8E5A-4084-9A84-62CD0928FE3F":
            'https://orcid.org/0000-0002-8868-4739',
            # Beth Scott - Aberdeen
            "https://gtr.ukri.org:443/gtr/api/persons/840DC5C3-017A-4AD7-9515-563BD0E71163":
            'https://orcid.org/0000-0001-5412-3952',
            # Andrew Jonathan Hodson - UNIS, Norway
            "https://gtr.ukri.org:443/gtr/api/persons/2C27EE95-AC89-423A-B4CA-F75604790961":
            'https://orcid.org/0000-0002-1255-7987',
            # Samraat Pawar - Imperial College London
            "https://gtr.ukri.org:443/gtr/api/persons/0C503344-7D14-4C36-9F3F-73223A796985":
            'https://orcid.org/0000-0001-8375-5684',
            # Margaret Jane Yelland - NOC
            "https://gtr.ukri.org:443/gtr/api/persons/E014B362-8B27-4EE7-9B2B-0EE6BA42C13E":
            'https://orcid.org/0000-0002-0936-4957',
            # Angus Ian Best - NOC
            "https://gtr.ukri.org:443/gtr/api/persons/3D956DF3-1C35-45B6-ADC2-22D310FE63D5":
            'https://orcid.org/0000-0001-9558-4261',
            # James Scourse - Exeter
            "https://gtr.ukri.org:443/gtr/api/persons/D4224C78-EC26-41C3-AFF0-6E687034DFA6":
            'https://orcid.org/0000-0003-2658-8730',
            # Paul Halloran - Exeter
            "https://gtr.ukri.org:443/gtr/api/persons/1A22F476-2DF1-46F4-838E-F576D2C603C7":
            'https://orcid.org/0000-0002-9227-0678',
            # Sarah Chadburn - Exeter
            "https://gtr.ukri.org:443/gtr/api/persons/41C00C6E-1017-4261-902E-898252080D2B":
            'https://orcid.org/0000-0003-1320-315X',
            # Jennifer Gill - UEA
            "https://gtr.ukri.org:443/gtr/api/persons/ED8FB31C-8D9B-4384-9320-262E20AEE07A":
            'https://orcid.org/0000-0002-2649-1325',
            # Andras Sobester - Southampton
            "https://gtr.ukri.org:443/gtr/api/persons/542E05E7-780C-4750-96D4-22AD3E78FBF7":
            'https://orcid.org/0000-0002-8997-4375',
            # James Screen - Exeter
            "https://gtr.ukri.org:443/gtr/api/persons/9B340BDB-C0A9-4BEA-8013-7178B4978BF7":
            'https://orcid.org/0000-0003-1728-783X',
            # Angela Victorina Gallego-Sala - Exeter
            "https://gtr.ukri.org:443/gtr/api/persons/B2C5E020-7032-4D4A-8474-6C6AE44DDF28":
            'https://orcid.org/0000-0002-7483-7773',
            # Simon Frederick Tett - Edinburgh
            "https://gtr.ukri.org:443/gtr/api/persons/3316451E-01DB-4ADD-AE44-25A575ED22C1":
            'https://orcid.org/0000-0001-7526-560X',
            # Alastair Lewis - NCAS, York
            "https://gtr.ukri.org:443/gtr/api/persons/E7265890-DFAA-4CF4-8181-48515950E2FA":
            'https://orcid.org/0000-0002-4075-3651',
            # Thomas Mock - UEA
            "https://gtr.ukri.org:443/gtr/api/persons/B8A0D322-8B6B-48A9-A8B5-1AA3780A89E9":
            'https://orcid.org/0000-0001-9604-0362',
            # Walter Oechel - San Diegoa State University, USA
            "https://gtr.ukri.org:443/gtr/api/persons/943FEA7C-8F21-4565-B579-8359A7C3CCA1":
            'https://orcid.org/0000-0002-3504-026X',
            # Tina Van De Flierdt - Imperial; College London
            "https://gtr.ukri.org:443/gtr/api/persons/3FCFA10D-A17B-4B7B-B342-2EC2293B96A2":
            'https://orcid.org/0000-0001-7176-9755',
            # Lorna Street - Edinburgh
            "https://gtr.ukri.org:443/gtr/api/persons/335CF8E0-B236-4424-B60B-7536788288C7":
            'http://orcid.org/0000-0001-9570-7479',
            # Amber Luella Annett - Southampton
            "https://gtr.ukri.org:443/gtr/api/persons/3C206F0C-E636-4D86-86B7-61F959148559":
            'https://orcid.org/0000-0002-3730-2438',
            # Rhodri Jerrett - Manchester
            "https://gtr.ukri.org:443/gtr/api/persons/676F942D-1AFE-436D-B60F-C50F23E355AD":
            'https://orcid.org/0000-0002-1412-3808',
            # Louise Claire Sime - BAS
            "https://gtr.ukri.org:443/gtr/api/persons/482B3DAB-CBF4-4FC9-BBC3-80C333D3E2C0":
            'https://orcid.org/0000-0002-9093-7926',
            # John Campbell Maclennan - Cambridge
            "https://gtr.ukri.org:443/gtr/api/persons/8DDB527E-9C3C-49EE-B6AE-1BDBDCB8DD97":
            'https://orcid.org/0000-0001-6857-9600',
            # Julie Prytulak - Durham University
            "https://gtr.ukri.org:443/gtr/api/persons/675A3847-2195-41F2-80C1-7DDD4509A8D1":
            'http://orcid.org/0000-0001-5269-1059',
            # Emanuel Ulrich Gloor - Leeds
            "https://gtr.ukri.org:443/gtr/api/persons/5DABD8C4-83A4-4AB3-93C9-DB49DC66ABFA":
            'https://orcid.org/0000-0002-9384-6341',
            # Andrew Watson - Exeter
            "https://gtr.ukri.org:443/gtr/api/persons/42391614-350E-4783-9FBF-46F9D67CC682":
            'http://orcid.org/0000-0002-9654-8147',
            # Claire Reeves - Open Univeristy
            "https://gtr.ukri.org:443/gtr/api/persons/26C13F6D-9648-4662-90FA-24F16B9515E7":
            'https://orcid.org/0000-0002-2493-2123',
            # Paul Palmer - Edinburgh
            "https://gtr.ukri.org:443/gtr/api/persons/F64F8711-B1DE-406B-B648-5A427216B839":
            'https://orcid.org/0000-0002-1487-0969',
            # Steven James Woolnough - Reading
            "https://gtr.ukri.org:443/gtr/api/persons/510BA244-9342-4BBD-AEA9-CB0DA2B6842B":
            'https://orcid.org/0000-0003-0500-8514',
            # Erin Louise McClymont - Durham University
            "https://gtr.ukri.org:443/gtr/api/persons/8930E0D3-F48C-49D1-810E-EA0B8B569206":
            'https://orcid.org/0000-0003-1562-8768',
            # Nicholas Pappas Klingaman - Reading
            "https://gtr.ukri.org:443/gtr/api/persons/01F74E77-6453-48B3-9CCD-F19D3F29BF8C":
            'https://orcid.org/0000-0002-2927-9303',
            # Amanda Claire Maycock - Leeds
            "https://gtr.ukri.org:443/gtr/api/persons/0131E012-F028-4F23-889E-587792EF1723":
            'https://orcid.org/0000-0002-6614-1127',
            # Anja Schmidt - Cambridge University
            "https://gtr.ukri.org:443/gtr/api/persons/222750E9-004A-41D2-B3C1-342CE9BDDCC5":
            'http://orcid.org/0000-0001-8759-2843',
            # Mike Burton - Manchester
            "https://gtr.ukri.org:443/gtr/api/persons/DC538BAF-E35A-4C0E-BE47-78691A21429C":
            'http://orcid.org/0000-0003-3779-4812',
            # Tamsin Alice Mather - Oxford
            "https://gtr.ukri.org:443/gtr/api/persons/1FCEBE77-7EA1-4CAD-914A-96ECC07349C5":
            'https://orcid.org/0000-0003-4259-7303',
            # David Johnson - Manchester
            "https://gtr.ukri.org:443/gtr/api/persons/BEB94C7B-24AE-4C04-9D7E-49BEBEDF3D10":
            'https://orcid.org/0000-0003-2299-2525'
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

        if 'doi' in self.resource:
            self.doi = self.resource['doi']
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
        self.fund = GatewayToResearchFund(
            gtr_resource_uri=self._find_gtr_fund_link())
        # print (self.fund)
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

    def __init__(self, gtr_grant_reference: str = None, gtr_project_id: str = None, lead_project: str = None):
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
        self.lead_project = int(lead_project)

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
            lead_project=self.lead_project,
            funder=Organisation.query.filter_by(
                ror_identifier=gtr_project.fund.funder.ror_id).one_or_none()
        )
        db.session.add(grant)

        project = Project(
            neutral_id=generate_neutral_id(),
            title=grant.title,
            abstract=grant.abstract,
            project_duration=grant.duration,
            access_duration=DateRange(grant.duration.lower, None),
            publications=grant.publications,
            lead_project=self.lead_project
        )
        db.session.add(project)

        db.session.add(Allocation(
            neutral_id=generate_neutral_id(),
            project=project,
            grant=grant
        ))

        self._save_gtr_category_terms(gtr_project)

        # GTR Research Topics and Subjects
        gtr_topics = self._find_unique_gtr_project_research_items(
            gtr_research_items=gtr_project.research_topics
        )

        gtr_subjects = self._find_unique_gtr_project_research_items(
            gtr_research_items=gtr_project.research_subjects
        )

        # GCMD Research Topics and Subjects
        gcmd_topics = self._find_unique_gcmd_project_research_topics(
            gtr_research_topics=gtr_project.research_topics
        )

        gcmd_subjects = self._find_unique_gcmd_project_research_subjects(
            gtr_research_subjects=gtr_project.research_subjects
        )

        # Flatten the processed topics and subjects to dinstinct list of GCMD identifiers
        # GTR Topics
        category_term_scheme_identifiers = list(gtr_topics)
        # GTR Subjects
        category_term_scheme_identifiers.extend(
            x for x in gtr_subjects if x not in category_term_scheme_identifiers)
        # GCMD Topics
        category_term_scheme_identifiers.extend(
            x for x in gcmd_topics if x not in category_term_scheme_identifiers)
        # GCMD Subjects
        category_term_scheme_identifiers.extend(
            x for x in gcmd_subjects if x not in category_term_scheme_identifiers)

        for category_term_scheme_identifier in category_term_scheme_identifiers:

            # Save to category terms link table
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

    def _save_gtr_category_terms(self, project):

        gtr_category_path = Ltree("gtr.ukri.org.resources.classificationprojects.html")

        for term in project.research_subjects:
            if db.session.query(exists().where(CategoryTerm.scheme_identifier == term['id'])).scalar():
                print("Skipping, GTR Category already imported")
                continue

            category_term_resource = CategoryTerm(
                neutral_id=generate_neutral_id(),
                scheme_identifier=term['id'],
                name=term['text'],
                path=gtr_category_path,
                category_scheme=CategoryScheme.query.filter_by(
                    namespace="https://gtr.ukri.org/resources/classificationlists.html"
                ).one()
            )
            db.session.add(category_term_resource)

        for term in project.research_topics:
            if db.session.query(exists().where(CategoryTerm.scheme_identifier == term['id'])).scalar():
                print("Skipping, GTR Category already imported")
                continue

            category_term_resource = CategoryTerm(
                neutral_id=generate_neutral_id(),
                scheme_identifier=term['id'],
                name=term['text'],
                path=gtr_category_path,
                category_scheme=CategoryScheme.query.filter_by(
                    namespace="https://gtr.ukri.org/resources/classificationlists.html"
                ).one()
            )
            db.session.add(category_term_resource)

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

            org_id = db.session.query(Organisation.id).filter(Organisation.ror_identifier == person.employer.ror_id).scalar()

            if not db.session.query(exists().where(and_(
                Person.first_name == person.first_name,
                Person.last_name == person.surname,
                Person.organisation_id == org_id
            ))).scalar():
                db.session.add(Person(
                    neutral_id=generate_neutral_id(),
                    first_name=person.first_name,
                    last_name=person.surname,
                    orcid_id=person.orcid_id,
                    organisation=Organisation.query.filter_by(
                        ror_identifier=person.employer.ror_id).one_or_none()
                ))

            db.session.add(Participant(
                neutral_id=generate_neutral_id(),
                role=role,
                project=project,
                person=Person.query.filter_by(first_name=person.first_name, last_name=person.surname).first()
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
            category_term_scheme_identifier = category['id']
            if category_term_scheme_identifier is not None:
                if category_term_scheme_identifier not in category_term_scheme_identifiers:
                    category_term_scheme_identifiers.append(
                        category_term_scheme_identifier)
        return category_term_scheme_identifiers

    def _find_unique_gcmd_project_research_topics(self, gtr_research_topics: list) -> list:
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
            category_term_scheme_identifier = self._map_gtr_project_research_topic_to_category_term(
                category)
            if category_term_scheme_identifier is not None:
                if category_term_scheme_identifier not in category_term_scheme_identifiers:
                    category_term_scheme_identifiers.append(
                        category_term_scheme_identifier)
        return category_term_scheme_identifiers

    def _find_unique_gcmd_project_research_subjects(self, gtr_research_subjects: list) -> list:
        """
        For a series of GTR project subjects, return a distinct list

        :type gtr_research_subjects: list
        :param gtr_research_subjects: list of GTR project research subjects

        :rtype list
        :return: distinct list of GCMD project research subjects
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
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/c47f6052-634e-40ef-a5ac-13f69f6f4c2a'
        elif gtr_research_topic['id'] == 'C62D281D-F1B9-423D-BDAB-361EC9BE7C68':
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/286d2ae0-9d86-4ef0-a2b4-014843a98532'
        elif gtr_research_topic['id'] == 'C29F371D-A988-48F8-BFF5-1657DAB1176F':
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/286d2ae0-9d86-4ef0-a2b4-014843a98532'
        elif gtr_research_topic['id'] == 'B01D3878-E7BD-4830-9503-2F54544E809E':
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/286d2ae0-9d86-4ef0-a2b4-014843a98532'
        # Community Ecology
        elif gtr_research_topic['id'] == 'F4786876-D9A9-404D-8569-BBC813C73074':
            # COMMUNITY DYNAMICS
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/8fb66b46-b998-4412-a541-d2acabdf484b'
        # Biogeochemical Cycles
        elif gtr_research_topic['id'] == '62DCC1BF-B512-4BDB-A0C3-02BC17E15F6B':
            # BIOGEOCHEMICAL CYCLES
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/9015e65f-bbae-4855-a4b6-1bfa601752bd'
        # Climate & Climate Change
        elif gtr_research_topic['id'] == 'EE4457DB-92A3-44EA-8D5F-77013CC107E0':
            # CLIMATE INDICATORS
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/23703b6b-ee15-4512-b5b2-f441547e2edf'
        # Hydrological Processes
        elif gtr_research_topic['id'] == 'D4F391DF-BCE0-47FA-BED7-78025F16B14D':
            # TERRESTRIAL HYDROSPHERE
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/885735f3-121e-4ca0-ac8b-f37dbc972f03'
        # Geohazards
        elif gtr_research_topic['id'] == 'BE94F009-26A1-4E5B-B0B3-722A355F282C':
            # NATURAL HAZARDS
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/ec0e2762-f57a-4fdc-b395-c8d7d5590d18'
        # Sediment/Sedimentary Processes
        elif gtr_research_topic['id'] == '5537B6B2-9FD6-40FB-B300-64555528D3FF':
            # EROSION/SEDIMENTATION
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/a246a8cf-e3f9-4045-af9f-dc97f6fe019a'
        # Environmental Microbiology
        elif gtr_research_topic['id'] == '5B73146D-6DEF-4D88-BE83-FE7B9DB21D62':
            # BIOLOGICAL CLASSIFICATION
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/fbec5145-79e6-4ed0-a804-6228aa6daba5'
        # Glacial & Cryospheric Systems
        elif gtr_research_topic['id'] == '07B1BD3F-A7ED-4640-8B09-C1F296DC56BF':
            # GLACIERS/ICE SHEETS
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/099ab1ae-f4d2-48cc-be2f-86bd58ffc4ca'
        # Soil science
        elif gtr_research_topic['id'] == '96F70ACB-D35F-416F-9360-4EFD402DFA6B':
            # SOILS
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/3526afb8-0dc9-43c7-8ad4-f34f250a1e91'
        # Ecosystem Scale Processes
        elif gtr_research_topic['id'] == '12C7A68B-3922-4925-9C0B-7FACEC921815':
            # ECOSYSTEMS
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/f1a25060-330c-4f84-9633-ed59ae8c64bf'
        # Tropospheric Processes
        elif gtr_research_topic['id'] == 'AE661B5A-7390-4AD2-BCF2-D611CB668BD1':
            # ATMOSPHERE
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/c47f6052-634e-40ef-a5ac-13f69f6f4c2a'
        # Population Ecology
        elif gtr_research_topic['id'] == 'DE30777A-E4A8-486B-875D-58CC92FD5525':
            # BIOLOGICAL CLASSIFICATION
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/fbec5145-79e6-4ed0-a804-6228aa6daba5'
        # Ocean Circulation
        elif gtr_research_topic['id'] == '723BA0F8-3ECD-4E2A-A39E-44936EAC1517':
            # OCEAN CIRCULATION
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/a031952d-9f00-4ba5-9966-5f87ab9dfdd4'
        # Land - Atmosphere Interactions
        elif gtr_research_topic['id'] == 'E94BED75-343A-47C8-BEA1-E1E927732B34':
            # ATMOSPHERE
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/c47f6052-634e-40ef-a5ac-13f69f6f4c2a'
        # Remote Sensing & Earth Obs.
        elif gtr_research_topic['id'] == '4504C6B4-D825-4F14-B0D3-7931AC636B71':
            # SPECTRAL/ENGINEERING
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/83150c54-5da8-4ee8-9579-19b95a8dc10c'
        # Regional & Extreme Weather
        elif gtr_research_topic['id'] == '396591D1-8226-43A9-991D-8E0D265D99D0':
            # EXTREME WEATHER
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/b29b46ad-f05f-4144-b965-5f606ce96963'
        # Palaeoenvironments
        elif gtr_research_topic['id'] == '7DCAF586-72E2-4881-9251-E72F38AF1CA4':
            # PALAEOCLIMATE
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/c7245882-84a1-4192-acfa-a758b5b9c151'
        # Earth & environmental
        elif gtr_research_topic['id'] == '4237918D-61A8-47E0-91EE-65E98661A88B':
            # HUMAN DIMENSION/ENVIRONMENTAL IMPACTS
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/3f4cfc81-7745-43d9-b313-f68cdf72359b'
        # Behavioural Ecology
        elif gtr_research_topic['id'] == '685A8D5E-BD8A-4D8D-BAC5-607439217156':
            # ECOLOGICAL DYNAMICS
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/6bef0291-a9ca-4832-bbb4-80459dc1493f'
        # Environmental Genomics
        elif gtr_research_topic['id'] == 'DE7203EB-4721-41C9-BB3C-539A8F6E8049':
            # BIOLOGICAL CLASSIFICATION
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/fbec5145-79e6-4ed0-a804-6228aa6daba5'
        # Conservation Ecology
        elif gtr_research_topic['id'] == '5020ECC8-E0E8-434D-BDD5-663A9C04EFA2':
            # CONSERVATION
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/40869a25-edea-4438-80f9-47c9e6910b9b'
        # Radiative Processes & Effects
        elif gtr_research_topic['id'] == '45964B78-B4F7-4098-996B-49505C85B744':
            # SURFACE RADIATIVE PROPERTIES
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/cb5cc628-a1b5-459e-934f-881153a937b8'
        # Large Scale Dynamics/Transport
        elif gtr_research_topic['id'] == '59CF5FB3-F46B-448B-AECF-47852750EF3C':
            # OCEANS
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/91697b7d-8f2b-4954-850e-61d5f61c867d'
        # Land - Ocean Interactions
        elif gtr_research_topic['id'] == 'B945AA77-44D5-467F-9B53-2EE3C3F550B1':
            # COASTAL PROCESSES
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/b6fd22ab-dca7-4dfa-8812-913453b5695b'
        # Mantle & Core Processes
        elif gtr_research_topic['id'] == 'C6842010-EC71-44DF-B79C-64B1BA9B3BDE':
            # TECTONICS
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/1e17c8d3-81d0-473c-8f24-d2a4ea52b6b9'
        # Quaternary Science
        elif gtr_research_topic['id'] == 'E32742C9-DE22-4776-82B4-444177FA03AD':
            # SOLID EARTH
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/2b9ad978-d986-4d63-b477-0f5efc8ace72'
        # Stratospheric Processes
        elif gtr_research_topic['id'] == 'A8A9F791-62D5-4B6F-90EB-2F6F8813D700':
            # ATMOSPHERE
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/c47f6052-634e-40ef-a5ac-13f69f6f4c2a'
        # Volcanic Processes
        elif gtr_research_topic['id'] == '052183D5-AB83-4C5E-97FA-7B0C1D4AF3FA':
            # VOLCANIC ACTIVITY
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/1faaede0-2cd6-4447-b28b-0a28d9e2d067'
        # Agricultural systems
        elif gtr_research_topic['id'] == '794345CD-A1D5-4984-ADDD-088BCF41822F':
            # AGRICULTURE
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/a956d045-3b12-441c-8a18-fac7d33b2b4e'
        # Earth Surface Processes
        elif gtr_research_topic['id'] == '47491D28-C3A9-416A-8459-3ECC0715B776':
            # GEOMORPHIC LANDFORMS/PROCESSES
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/d35b9ba5-d018-48a5-8f0d-92b9c55b3279'
        # Technol. for Environ. Appl.
        elif gtr_research_topic['id'] == '98C0D11F-5C27-40CE-A895-54E4C61784B1':
            # EARTH SCIENCE SERVICES
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/894f9116-ae3c-40b6-981d-5113de961710'
        # Responses to environment
        elif gtr_research_topic['id'] == '8717CFA9-D46B-41A5-8971-BF4431B68E29':
            # CLIMATE INDICIATORS
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/23703b6b-ee15-4512-b5b2-f441547e2edf'
        # Metabolomics / Metabonomics
        elif gtr_research_topic['id'] == '9F673176-B1B7-47C8-9D0F-DEC4A0410F7C':
            # BIOLOGICAL CLASSIFICATION
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/fbec5145-79e6-4ed0-a804-6228aa6daba5'
        # Biochemistry & physiology
        elif gtr_research_topic['id'] == '649031FD-C21E-42D9-AC12-41ACA59CC11C':
            # ANIMAL PHYSIOLOGY AND BIOCHEMISTRY
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/f9cdf3ae-fe8b-4a19-a946-a8c8780d7894'
        # Prehistoric Archaeology
        elif gtr_research_topic['id'] == '14AE809A-4116-46B5-ABF7-DF8BCE2BF069':
            # PALEOCLIMATE
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/c7245882-84a1-4192-acfa-a758b5b9c151'
        # Water Quality
        elif gtr_research_topic['id'] == '99C0726F-47B0-4500-8B73-4DD0C60E31DF':
            # WATER QUALITY
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/1ee8a323-f0ba-4a21-b597-50890c527c8e'
        # Plant physiology
        elif gtr_research_topic['id'] == '15080F45-1EA3-41B4-BC23-C49CB918FBC4':
            # PLANTS
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/0b4081fa-5233-4484-bc82-706976defa0e'
        # Carbon Capture & Storage
        elif gtr_research_topic['id'] == 'B5705566-FCD9-4E90-A1F6-458BBDED816E':
            # CARBON CAPTURE AND STORAGE
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/e8c24822-7d2d-48c6-9dca-df3860e9bd63'
        # Survey & Monitoring
        elif gtr_research_topic['id'] == '189E1F60-BF95-405D-A6F0-62BBD78E2DD5':
            # EARTH SCIENCE SERVICES
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/894f9116-ae3c-40b6-981d-5113de961710'
        # Environment & Health
        elif gtr_research_topic['id'] == '86884005-D98A-4391-95D8-913141C39F7C':
            # HEALTH ADVISORIES
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/370eba54-962b-4e59-9686-86d5c5ab9c88'
        # Systematics & Taxonomy
        elif gtr_research_topic['id'] == '2CF6994C-A1AE-435B-853C-2C228927BC9E':
            # BIOLOGICAL CLASSIFICATION
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/fbec5145-79e6-4ed0-a804-6228aa6daba5'
        # Crop protection
        elif gtr_research_topic['id'] == '6F3E4891-E3E8-4568-94D8-075A0552DE90':
            # AGRICULTURAL PLANT SCIENCE
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/25be3b9a-9d4c-4b5b-8d24-b1f519913d90'
        # Earth Resources
        elif gtr_research_topic['id'] == '859194A3-8EE1-41D7-90C5-DA2999B93E8E':
            # SOLID EARTH
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/2b9ad978-d986-4d63-b477-0f5efc8ace72'
        # Atmospheric Kinetics
        elif gtr_research_topic['id'] == '62E0966C-A067-4075-B244-33F1F4DD4B1E':
            # ATMOSPHERE
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/c47f6052-634e-40ef-a5ac-13f69f6f4c2a'
        # Environmental Physiology
        elif gtr_research_topic['id'] == '6CA01F47-BDE6-46F1-8679-A31D5317A885':
            # AGRICULTURE
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/a956d045-3b12-441c-8a18-fac7d33b2b4e'
        # Transport Geography
        elif gtr_research_topic['id'] == '0C5394E1-D713-4507-8021-0A9785789545':
            # TRANSPORTATION
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/37a6c8e2-f2ac-48a4-a4fa-d80f700f68db'
        # Accelerator R&D
        elif gtr_research_topic['id'] == 'BF8C9667-2697-4493-8519-7787831D008B':
            # EARTH SCIENCE SERVICES
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/894f9116-ae3c-40b6-981d-5113de961710'
        # Properties Of Earth Materials
        elif gtr_research_topic['id'] == '9C0F9DC0-329C-4C09-B439-E4335EA8F916':
            # SOLID EARTH
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/2b9ad978-d986-4d63-b477-0f5efc8ace72'
        # Technology and method dev
        elif gtr_research_topic['id'] == '80A9D6C5-792D-4DD9-9138-BEC1BB556AA9':
            # EARTH SCIENCE SERVICES
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/894f9116-ae3c-40b6-981d-5113de961710'
        # Upper Atmos Process & Geospace
        elif gtr_research_topic['id'] == '4CF6D0C3-CF9C-4067-9466-B9FC16647C21':
            # ATMOSPHERE
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/c47f6052-634e-40ef-a5ac-13f69f6f4c2a'
        # RF & Microwave Technology
        elif gtr_research_topic['id'] == 'CEDD6868-376B-45CB-BAB7-5AD38D089AC0':
            # MICROWAVE
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/66700628-2b62-4466-999e-faeb15ca4da5'
        # Museum & Gallery Studies
        elif gtr_research_topic['id'] == '51073B72-B972-4034-A0A1-87A6B0DCD198':
            # RECREATIONAL ACTIVITIES
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/9ee8acad-458e-45c1-a1d5-9b1649c82ea7'
        # Socio Legal Studies
        elif gtr_research_topic['id'] == 'B75590D5-E385-45F1-B6D0-CC3EDEFDE67D':
            # SOCIOECONOMICS
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/a96e6cd6-0f35-491d-8198-7551d03e1cbc'
        # Scandinavian studies
        elif gtr_research_topic['id'] == '80990855-5789-4612-9DC4-701464F66874':
            # HUMAN SETTLEMENTS
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/fee25cad-7ffe-4ee2-a6f2-8116b8a0a707'
        # Animal behaviour
        elif gtr_research_topic['id'] == '790AD28C-6380-4025-83C2-6881B93C4602':
            # ANIMAL ECOLOGY AND BEHAVIOR
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/5d1b53b2-7d69-4b7c-903f-d8cf29430f93'
        # Theoretical biology
        elif gtr_research_topic['id'] == '4A6E5CEB-ACA3-4301-98AD-C7EC310948FD':
            # BIOLOGICAL CLASSIFICATION
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/fbec5145-79e6-4ed0-a804-6228aa6daba5'
        # Pollution
        elif gtr_research_topic['id'] == 'DC6B2467-35B6-4997-9582-1BF957B82697':
            # EMISSIONS
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/2a60df4a-a0d7-4e4b-b02a-372a083f0170'
        # Animal organisms
        elif gtr_research_topic['id'] == '4A2A69ED-37ED-4980-91A7-E54B4F6A9BC6':
            # BIOLOGICAL CLASSIFICATION
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/fbec5145-79e6-4ed0-a804-6228aa6daba5'
        # Diet & health
        elif gtr_research_topic['id'] == '446B7E7F-04EB-4121-9CC6-9171277E00DA':
            # PUBLIC HEALTH
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/da2c70fd-d92b-45be-b159-b2c10cb387c6'
        # Extremophiles
        elif gtr_research_topic['id'] == '6E4BDD5C-C98C-4B33-B870-6A3A366BEE58':
            # BIOLOGICAL CLASSIFICATION
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/fbec5145-79e6-4ed0-a804-6228aa6daba5'
        # Plant responses to environment
        elif gtr_research_topic['id'] == 'AE2D53CC-F199-452E-A1FE-B63F4222D636':
            # LAND SURFACE/AGRICULTURE INDICATORS
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/112e71ec-c0a1-49a8-82d7-bcb317b45860'
        # Population Genetics/Evolution
        elif gtr_research_topic['id'] == 'A4209D5A-2E41-4290-9D1A-3172C1F48962':
            # SPECIES/POPULATION INTERACTIONS
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/58f39353-7e1c-4884-9501-376cd0377fbf'
        # Water Engineering
        elif gtr_research_topic['id'] == '19789484-D6B8-4965-AD25-309DD43054A0':
            # ENVIRONMENTAL ENGINEERING
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/596225b7-2cd8-4638-bb75-23bfb491aeb1'
        # Research Approaches
        elif gtr_research_topic['id'] == '0fde38f8-b9a4-453f-827e-ba161dd12c78':
            # ADMINISTRATIVE SCIENCES
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/fbf13798-2bcd-4ae7-99f9-a4b69dd425c1'
        # Plant developmental biology
        elif gtr_research_topic['id'] == '023A4090-7FA5-4AFE-9071-DCC99F0221C4':
            # PLANT BIOLOGY
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/ec5f63cf-d6d6-4af9-8b52-52b9450a5df4'
        # Med.Instrument.Device& Equip.
        elif gtr_research_topic['id'] == '16595C3C-600D-4AD2-B394-16E06F96495F':
            # In Situ/Laboratory Instruments
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/ff564c87-78f2-47eb-a857-a4bdc0a71ae5'
        # Mathematical Aspects of OR
        elif gtr_research_topic['id'] == 'F0F2F1A7-287A-4B6F-AA0E-74A55BB4DEE4':
            # MATHEMATICS
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/c94e9340-2fe5-4254-bcbd-8d8aaed45f6e'
        # Community Art inc A & H
        elif gtr_research_topic['id'] == '62F4842F-55F4-41C6-A77A-572005E91429':
            # FINE ARTS
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/ae0ade63-4d8b-4908-9821-a2ec0bec85bc'
        # Optical Devices & Subsystems
        elif gtr_research_topic['id'] == '66CE6BAB-875D-4F4D-B415-F93CA7A2C4CA':
            # Earth Remote Sensing Instruments
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/6015ef7b-f3bd-49e1-9193-cc23db566b69'
        # Imperial/Colonial History
        elif gtr_research_topic['id'] == '319D6F57-4306-40E8-9F0A-84D514AAF7FC':
            # SOCIAL SCIENCES
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/89ea7131-263f-4642-bbb5-09c65457ef3d'
        # Analytical Science
        elif gtr_research_topic['id'] == '98EA7556-1427-44F9-84F3-BF99B7207302':
            return None
        # Animal & human physiology
        elif gtr_research_topic['id'] == 'E793F7FE-614C-4A45-83A0-BE79B172092C':
            return None
        # Assess/Remediate Contamination
        elif gtr_research_topic['id'] == '4A635FDF-4DC1-48AB-A010-04619A0042EF':
            return None
        # Civil Engineering Materials
        elif gtr_research_topic['id'] == '0F0B5443-BE5E-4DB6-823E-B7E33EE35922':
            return None
        # Continuum Mechanics
        elif gtr_research_topic['id'] == '02B9E893-AC2F-436D-BF88-28E1AC827F5D':
            return None
        # Cultural History
        elif gtr_research_topic['id'] == 'ACF80B6E-2900-42FE-9B9B-C84E295EA0AC':
            return None
        # Endocrinology
        elif gtr_research_topic['id'] == '3646DA55-FE51-4E44-A8FA-E8E83A4CCBA4':
            return None
        # Energy - Conventional
        elif gtr_research_topic['id'] == 'FFAA021A-6F31-43D9-8517-EA79D1E71F54':
            return None
        # Environmental Informatics
        elif gtr_research_topic['id'] == 'F63617E9-02B7-41EA-AD68-B2D597237394':
            return None
        # Exploration Technology
        elif gtr_research_topic['id'] == 'DF27EB97-39D5-4F5C-8F07-21BBABBF9422':
            return None
        # Geography and Development
        elif gtr_research_topic['id'] == '78369800-A95E-49BC-94E7-8659E5C2EFEF':
            return None
        # Historical Geography
        elif gtr_research_topic['id'] == '2D6754CC-B7DE-45FB-BB9D-CE7AA05892D0':
            return None
        # Omic sciences & technologies
        elif gtr_research_topic['id'] == '9BDF80E2-029E-4505-B7EE-DB0FA633E483':
            return None
        # Solar & Solar-Terrestrial Phys
        elif gtr_research_topic['id'] == 'DAA4C99D-BD30-4A55-B416-7AFE780BB7B8':
            return None
        # Spatial Planning
        elif gtr_research_topic['id'] == 'AF20B57E-E40B-45BC-85C8-DDC6F4777697':
            return None
        # Materials Characterisation
        elif gtr_research_topic['id'] == '561091A1-9FC9-4508-B1B2-2F3623E1FC9D':
            return None
        # Evolution & populations
        elif gtr_research_topic['id'] == '62F9C365-02D0-4623-9A73-8CA09DA0FFF2':
            return None
        # Atoms & Ions
        elif gtr_research_topic['id'] == '4D22A081-A665-4EAE-8542-CB1050A44B55':
            return None
        # Cultural Geography
        elif gtr_research_topic['id'] == '8990E5FE-B44F-4A5B-8FDE-0610A5BE98C4':
            return None
        # International Law
        elif gtr_research_topic['id'] == 'EC0E734E-D9A1-463E-AB7A-CCB02E877E10':
            return None
        # History of Sci./Med./Technol.
        elif gtr_research_topic['id'] == 'E5E4CBFA-1AC0-405D-A6EC-46A5C0B6704F':
            return None
        # Mathematical Analysis
        elif gtr_research_topic['id'] == '04D8FF87-2CFC-44E7-A7DF-47E10C813E05':
            return None
        # Ecotoxicology
        elif gtr_research_topic['id'] == '6A654DB9-716E-4BAC-867B-E1CE45A994F6':
            return None
        # Tectonic Processes
        elif gtr_research_topic['id'] == '401A9A9F-83DF-48FD-B108-C4CC7FB7572C':
            return None
        # Epigenetics
        elif gtr_research_topic['id'] == 'B6EF57B2-8ACD-48E6-9B45-98507446B053':
            return None
        # Applied Arts HTP
        elif gtr_research_topic['id'] == '287497FB-DD4A-44CC-AC13-DBAFADC9AD82':
            return None
        # Environmental Geography
        elif gtr_research_topic['id'] == 'F6DEB3C9-18A0-4A06-87C5-8C347DF98C60':
            return None
        # Social Anthropology
        elif gtr_research_topic['id'] == '020361E1-B8CA-49FD-9149-27D31D21C7A3':
            return None
        # Regional Geography
        elif gtr_research_topic['id'] == '8DA0F0DB-E15C-4A3D-ADD9-E08898CE6475':
            return None
        # Cultural Studies
        elif gtr_research_topic['id'] == 'ABBA5192-0B16-4BC8-8B3F-3A48625872F0':
            return None
        # Ground Engineering
        elif gtr_research_topic['id'] == '5AAD42DB-C6CB-4B09-8555-8ECA565B6B59':
            return None
        # Earth Engineering
        elif gtr_research_topic['id'] == 'DEEA5CB1-59E6-4D82-92D6-DB74E180E6F7':
            return None
        # Water Engineering
        elif gtr_research_topic['id'] == '19789484-D6B8-4965-AD25-309DD43054A0':
            return None
        # Research approaches
        elif gtr_research_topic['id'] == '63F3D26F-05D5-477D-9F77-C6C8AC47C7DD':
            return None
        # Plant developmental biology
        elif gtr_research_topic['id'] == '023A4090-7FA5-4AFE-9071-DCC99F0221C4':
            return None
        # Energy Efficiency
        elif gtr_research_topic['id'] == 'BE7CEC14-3FA2-49BC-89EE-062447C269C1':
            return None
        # Genomics
        elif gtr_research_topic['id'] == '4661C82D-F66E-4672-BA82-7C12180BBDF7':
            return None
        # Instrumentation Eng. & Dev.
        elif gtr_research_topic['id'] == 'F78E4567-DD59-4364-9D1F-0A778996E941':
            return None
        # Coastal & Waterway Engineering
        elif gtr_research_topic['id'] == '44BF93F5-71F4-42EF-A39B-8A0F09C7DDD1':
            return None
        # Construction Ops & Management
        elif gtr_research_topic['id'] == 'F58B1665-2CA2-473F-9805-357FD6CC4529':
            return None
        # Social Geography
        elif gtr_research_topic['id'] == '1AB3F721-B2D1-4875-A568-E7F49B4465E9':
            return None
        # Animal Diseases
        elif gtr_research_topic['id'] == 'A502D25A-BB70-4F74-844D-32A2BAD075A5':
            return None
        # Cultural and Anthrop Geography
        elif gtr_research_topic['id'] == '4CB391BE-87E7-4006-A2C5-43ED9DBA773C':
            return None
        # Energy - Marine & Hydropower
        elif gtr_research_topic['id'] == '6BCCE8AB-CBA5-4D28-9682-5236FE9D0668':
            return None
        # Operations Management
        elif gtr_research_topic['id'] == 'BDA5E012-C5EA-48C7-B1D8-594821FDC78E':
            return None
        # Transport Ops & Management
        elif gtr_research_topic['id'] == '748617DE-4AB0-42C9-9514-B22ECFBE05E1':
            return None
        # Social Policy
        elif gtr_research_topic['id'] == '12179D88-04B3-47E9-89E1-B5EE8F895227':
            return None
        # Management & Business Studies
        elif gtr_research_topic['id'] == '5E9AA4EC-49E3-4D6A-B545-79DA07CE39E0':
            return None
        # SStatistics & Appl. Probability
        elif gtr_research_topic['id'] == '62309876-5C71-411C-B1A7-1B2907AFB5A8':
            return None
        # Wind Power
        elif gtr_research_topic['id'] == 'A006DA8C-29E9-4AF4-85F5-6736BE80583D':
            return None
        # Environmental Engineering
        elif gtr_research_topic['id'] == '97FC8337-8E84-46A6-ACF2-A6047DA8C582':
            return None
        # Oceanic Studies
        elif gtr_research_topic['id'] == 'BF1A1580-BC3D-4008-855B-67221E5AC026':
            return None
        # Solar Technology
        elif gtr_research_topic['id'] == '1175C1D0-52DD-4F11-A1B8-E080CABC3609':
            return None
        # Energy Storage
        elif gtr_research_topic['id'] == '97AD4D1C-4499-4C7E-AF8A-FE9EFE56E306':
            return None
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
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/91c64c46-d040-4daa-b26c-61952fdfaf50'
        elif gtr_research_subject['text'] == 'Ecol, biodivers. & systematics':
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/f1a25060-330c-4f84-9633-ed59ae8c64bf'
        elif gtr_research_subject['text'] == 'Marine environments':
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/91697b7d-8f2b-4954-850e-61d5f61c867d'
        elif gtr_research_subject['text'] == 'Geosciences':
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/2b9ad978-d986-4d63-b477-0f5efc8ace72'
        elif gtr_research_subject['text'] == 'Climate and climate change':
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/c47f6052-634e-40ef-a5ac-13f69f6f4c2a'
        elif gtr_research_subject['text'] == 'Atmospheric phys. & chemistry':
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/b9c56939-c624-467d-b196-e56a5b660334'
        elif gtr_research_subject['text'] == 'Climate & Climate Change':
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/c47f6052-634e-40ef-a5ac-13f69f6f4c2a'
        elif gtr_research_subject['text'] == 'Microbial sciences':
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/fbec5145-79e6-4ed0-a804-6228aa6daba5'
        elif gtr_research_subject['text'] == 'Tools, technologies & methods':
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/83150c54-5da8-4ee8-9579-19b95a8dc10c'
        elif gtr_research_subject['text'] == 'Agri-environmental science':
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/a956d045-3b12-441c-8a18-fac7d33b2b4e'
        elif gtr_research_subject['text'] == 'Archaeology':
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/bf703f22-9775-460d-86bd-149aaef1acde'
        elif gtr_research_subject['text'] == 'Plant & crop science':
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/f1c35c74-0b10-46de-9c06-efeda92d383a'
        elif gtr_research_subject['text'] == 'Human Geography':
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/fb93d937-c17c-45d0-a9e3-ca5c8a800ca8'
        elif gtr_research_subject['text'] == 'Info. & commun. Technol.':
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/d4313915-2d24-424c-a171-30ee9a6f4bb5'
        elif gtr_research_subject['text'] == 'Medical & health interface':
            return 'https://gcmd.earthdata.nasa.gov/kms/concept/da2c70fd-d92b-45be-b159-b2c10cb387c6'
        elif gtr_research_subject['text'] == 'Biomolecules & biochemistry':
            return None
        elif gtr_research_subject['text'] == 'Facility Development':
            return None
        elif gtr_research_subject['text'] == 'Instrument. sensor & detectors':
            return None
        elif gtr_research_subject['text'] == 'Omic sciences & technologies':
            return None
        elif gtr_research_subject['text'] == 'Pollution, waste & resources':
            return None
        elif gtr_research_subject['text'] == 'Animal Science':
            return None
        elif gtr_research_subject['text'] == 'Chemical measurement':
            return None
        elif gtr_research_subject['text'] == 'Planetary science':
            return None
        elif gtr_research_subject['text'] == 'Energy':
            return None
        elif gtr_research_subject['text'] == 'Genetics & development':
            return None
        elif gtr_research_subject['text'] == 'Mathematical sciences':
            return None
        elif gtr_research_subject['text'] == 'Food science & nutrition':
            return None
        elif gtr_research_subject['text'] == 'Environmental planning':
            return None
        elif gtr_research_subject['text'] == 'Civil eng. & built environment':
            return None
        elif gtr_research_subject['text'] == 'History':
            return None
        elif gtr_research_subject['text'] == 'Materials sciences':
            return None
        elif gtr_research_subject['text'] == 'Atomic & molecular physics':
            return None
        elif gtr_research_subject['text'] == 'Law & legal studies':
            return None
        elif gtr_research_subject['text'] == 'Solar & terrestrial physics':
            return None
        elif gtr_research_subject['text'] == 'Social Anthropology':
            return None
        elif gtr_research_subject['text'] == 'Sociology':
            return None
        elif gtr_research_subject['text'] == 'Visual arts':
            return None
        elif gtr_research_subject['text'] == 'Cultural & museum studies':
            return None
        elif gtr_research_subject['text'] == 'Development studies':
            return None
        elif gtr_research_subject['text'] == 'Transport Ops & Management':
            return None
        elif gtr_research_subject['text'] == 'Social Policy':
            return None
        elif gtr_research_subject['text'] == 'Science-Based Archaeology':
            return None
        elif gtr_research_subject['text'] == 'Solar Technology':
            return None
        elif gtr_research_subject['text'] == 'Cultural and Anthrop Geography':
            return None
        elif gtr_research_subject['text'] == 'Social Geography':
            return None
        elif gtr_research_subject['text'] == 'Construction Ops & Management':
            return None
        elif gtr_research_subject['text'] == 'Animal Diseases':
            return None
        elif gtr_research_subject['text'] == 'Operations Management':
            return None
        elif gtr_research_subject['text'] == 'Management & Business Studies':
            return None
        elif gtr_research_subject['text'] == 'Statistics & Appl. Probability':
            return None
        elif gtr_research_subject['text'] == 'Wind Power':
            return None
        elif gtr_research_subject['text'] == 'Energy Storage':
            return None
        elif gtr_research_subject['text'] == 'Environmental Engineering':
            return None

        raise UnmappedGatewayToResearchProjectSubject(meta={
            'gtr_research_subject': {
                'id': gtr_research_subject['id'],
                'name': gtr_research_subject['text']
            }
        })


def import_gateway_to_research_grant_interactively(gtr_grant_reference: str, lead_project: str):
    """
    Command to import a project/grant from Gateway to Research

    Wraps around the GatewayToResearchGrantImporter class to provide some feedback during import.

    All errors will trigger an exception to be raised with any pending database models to be removed/flushed.

    :type gtr_grant_reference: str
    :param gtr_grant_reference: Gateway to Research grant reference (e.g. 'NE/K011820/1')
    """
    try:
        # app.logger.info(
        #     f"Importing Gateway to Research (GTR) project with grant reference ({gtr_grant_reference})")
        echo(style(
            f"Importing Gateway to Research (GTR) project with grant reference ({gtr_grant_reference})"))
        importer = GatewayToResearchGrantImporter(
            gtr_grant_reference=gtr_grant_reference, lead_project=lead_project)

        if importer.exists():
            # app.logger.info(f"Finished importing GTR project with grant reference ({gtr_grant_reference}) - Already "
            #                 f"imported")
            echo(style(f"Finished importing GTR project with grant reference ({gtr_grant_reference}) - Already "
                       f"imported", fg='green'))
            return True

        gtr_project_id = importer.search()

        if gtr_project_id is None:
            # app.logger.error(f"Failed importing GTR project with grant reference ({gtr_grant_reference}) - No or "
            #                  f"multiple GTR projects found")
            echo(style(f"Failed importing GTR project with grant reference ({gtr_grant_reference}) - No or "
                       f"multiple GTR projects found", fg='red'))
            return False
        # app.logger.info(f"... found GTR project for grant reference ({gtr_grant_reference}) - [{gtr_project_id}] - "
        #                 f"Importing")
        echo(style(f"... found GTR project for grant reference ({gtr_grant_reference}) - [{gtr_project_id}] - "
                   f"Importing"))

        importer.fetch()
        # app.logger.info(
        #     f"Finished importing GTR project with grant reference ({gtr_grant_reference}), imported")
        echo(style(
            f"Finished importing GTR project with grant reference ({gtr_grant_reference}), imported", fg='green'
        ))
    except UnmappedGatewayToResearchOrganisation as e:
        # app.logger.error(
        #     f"Unmapped GTR Organisation [{e.meta['gtr_organisation']['resource_uri']}]")
        echo(style(
            f"Unmapped GTR Organisation [{e.meta['gtr_organisation']['resource_uri']}]", fg='red'))
    except UnmappedGatewayToResearchPerson as e:
        # app.logger.error(
        #     f"Unmapped GTR Person [{e.meta['gtr_person']['resource_uri']}]")
        echo(
            style(f"Unmapped GTR Person [{e.meta['gtr_person']['resource_uri']}]", fg='red'))
    except UnmappedGatewayToResearchProjectTopic as e:
        # app.logger.error(
        #     f"Unmapped GTR Topic [{e.meta['gtr_research_topic']['id']}, {e.meta['gtr_research_topic']['name']}]")
        echo(style(
            f"Unmapped GTR Topic [{e.meta['gtr_research_topic']['id']}, {e.meta['gtr_research_topic']['name']}]", fg='red'
        ))
    except UnmappedGatewayToResearchProjectSubject as e:
        # app.logger.error(
        #     f"Unmapped GTR Subject [{e.meta['gtr_research_subject']['id']}, {e.meta['gtr_research_subject']['name']}]")
        echo(style(
            f"Unmapped GTR Subject [{e.meta['gtr_research_subject']['id']}, {e.meta['gtr_research_subject']['name']}]", fg='red'
        ))
    except Exception as e:
        db.session.rollback()
        # Remove any added, but non-committed, entities
        db.session.flush()
        raise e
