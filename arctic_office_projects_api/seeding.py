from datetime import date
# noinspection PyPackageRequirements
from typing import Dict, Optional, List

from psycopg2.extras import DateRange
# noinspection PyPackageRequirements
from sqlalchemy import exists
# noinspection PyPackageRequirements
from sqlalchemy.sql import func
from faker import Faker

from arctic_office_projects_api import db
from arctic_office_projects_api.models import Project, ProjectCountry, Person, Organisation, Grant, GrantStatus, \
    GrantCurrency, Participant, ParticipantRole, Allocation
from arctic_office_projects_api.main.utils import generate_neutral_id
from arctic_office_projects_api.main.faker.providers.project import Provider as ProjectProvider
from arctic_office_projects_api.main.faker.providers.person import Provider as PersonProvider
from arctic_office_projects_api.main.faker.providers.profile import Provider as ProfileProvider
from arctic_office_projects_api.main.faker.providers.grant import Provider as GrantProvider, GrantType, UKRICouncil
from arctic_office_projects_api.main.faker.providers.organisation import Provider as OrganisationProvider

faker = Faker('en_GB')
faker.add_provider(ProjectProvider)
faker.add_provider(PersonProvider)
faker.add_provider(ProfileProvider)
faker.add_provider(GrantProvider)
faker.add_provider(OrganisationProvider)

static_resources = {
    'projects': {
        '01DB2ECBP24NHYV5KZQG2N3FS2': {
            'id': '01DB2ECBP24NHYV5KZQG2N3FS2',
            'title': 'Example project 1',
            'acronym': 'EXPRO1',
            'abstract': 'This project is used as an example, for demonstration or testing purposes. '
                        'The contents of this project, and resources it relates to, will not change. \n'
                        'This example project (1) is a project with a single PI and single CoI belonging to the same '
                        'organisation. It is also associated with a single grant and funder. The people, grants and '
                        'organisations related to this project will not be related to another project. This project '
                        'has an acronym, abstract, website and country property. The project duration is in the past.'
                        '\n The remainder of this abstract is padding text to give a realistic abstract length.\n'
                        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eget lorem eleifend turpis '
                        'vestibulum sollicitudin. Curabitur libero nulla, maximus ut facilisis et, maximus quis dolor. '
                        'Nunc ut malesuada felis. Sed volutpat et lectus vitae convallis. Class aptent taciti sociosqu '
                        'ad litora torquent per conubia nostra, per inceptos himenaeos. Fusce ullamcorper nec ante ut '
                        'vulputate. Praesent ultricies mattis dolor quis ultrices. Ut sagittis scelerisque leo '
                        'fringilla malesuada. Donec euismod tincidunt purus vel commodo. \n Aenean volutpat libero '
                        'quis imperdiet tincidunt. Proin iaculis eros at turpis laoreet molestie. Quisque '
                        'pellentesque, lorem id ornare fermentum, nunc urna ultrices libero, eget tempor ipsum lectus '
                        'sollicitudin nibh. Sed sit amet vestibulum nulla. Vivamus dictum, dui id consectetur mattis, '
                        'sapien erat tristique nulla, at lobortis enim nibh eu orci. Curabitur eu purus porttitor, '
                        'rhoncus libero sed, mattis tellus. Praesent ullamcorper tincidunt ex. Vivamus lectus urna, '
                        'dignissim sit amet efficitur a, malesuada at nisi \n. Curabitur auctor ut libero ac pharetra. '
                        'Nunc rutrum facilisis felis, ac rhoncus lorem pulvinar quis. In felis neque, mollis nec '
                        'sagittis feugiat, finibus maximus mauris. Nullam varius, risus id scelerisque tempor, justo '
                        'purus malesuada nulla, eu sagittis purus arcu eget justo. Orci varius natoque penatibus et '
                        'magnis dis parturient montes, nascetur ridiculus mus. Fusce vel pretium augue. Pellentesque '
                        'eu semper odio. Suspendisse congue varius est, et euismod justo accumsan sed. Etiam nec '
                        'scelerisque risus, sed tempus ante. Proin fringilla leo urna, eget pulvinar leo placerat et. '
                        '\n Etiam mollis lacus ut sapien elementum, sed volutpat dui faucibus. Fusce ligula risus, '
                        'tempor at justo ac, tincidunt finibus magna. Duis eget sapien et nibh tincidunt faucibus. '
                        'Duis tempus tincidunt leo. Aenean sit amet cursus ex. Etiam eget finibus nulla, a rutrum '
                        'turpis. Proin imperdiet, augue consectetur varius varius, lectus elit egestas velit, '
                        'ullamcorper pulvinar dolor felis at leo. Cras nec est ut est efficitur pulvinar nec vel nisi. '
                        'Nullam sed elit eu ante finibus volutpat. Nam id diam a urna rutrum dictum. \n Pellentesque '
                        'habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Integer '
                        'accumsan et mi eu sagittis. Ut id nulla at quam efficitur molestie. Donec viverra ex vitae '
                        'mauris ullamcorper elementum. Proin sed felis enim. Suspendisse potenti. Integer malesuada '
                        'interdum mi, ornare semper lorem tempus condimentum. Cras sodales risus quis nibh fermentum '
                        'volutpat. Sed vel tincidunt lectus.',
            'website': 'https://www.example.com',
            'publications': [
                'https://doi.org/10.5555/76559541',
                'https://doi.org/10.5555/97727778',
                'https://doi.org/10.5555/79026270'
            ],
            'duration': DateRange(date(2012, 3, 1), date(2015, 10, 1)),
            'country': ProjectCountry.SJM,
        },
        '01DB2ECBP2DXX8VN7S7AYJBGBT': {
            'id': '01DB2ECBP2DXX8VN7S7AYJBGBT',
            'title': 'Example project 2',
            'acronym': None,
            'abstract': 'This project is used as an example, for demonstration or testing purposes.'
                        'The contents of this project, and resources it relates to, will not change.'
                        'This example project (2) has a single PI, organisation, grant and funder. The resources '
                        'related to this project will also relate to other projects. This project does not have an '
                        'acronym, website, publication or country property. The project duration is in the present. \n '
                        'No padding text is added to this abstract.',
            'website': None,
            'publications': [],
            'duration': DateRange(date(2012, 3, 1), date(2055, 10, 1)),
            'country': None
        },
        '01DB2ECBP2MB2Z9K1BSK5BND0V': {
            'id': '01DB2ECBP2MB2Z9K1BSK5BND0V',
            'title': 'Example project 3',
            'acronym': 'EXPRO3',
            'abstract': 'This project is used as an example, for demonstration or testing purposes.'
                        'The contents of this project, and resources it relates to, will not change.'
                        'This example project (3) has a single PI and multiple CoIs belonging to different '
                        'organisations. It is also associated with a single grant and funder. The resources related to '
                        'this project will also relate to other projects. This project has an acronym and country '
                        'properties, it does not have a website or publications. The project duration is in the future'
                        '. \n The remainder of this abstract is padding text to give a realistic abstract length. \n'
                        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eget lorem eleifend turpis '
                        'vestibulum sollicitudin. Curabitur libero nulla, maximus ut facilisis et, maximus quis dolor. '
                        'Nunc ut malesuada felis. Sed volutpat et lectus vitae convallis. Class aptent taciti sociosqu '
                        'ad litora torquent per conubia nostra, per inceptos himenaeos. Fusce ullamcorper nec ante ut '
                        'vulputate. Praesent ultricies mattis dolor quis ultrices. Ut sagittis scelerisque leo '
                        'fringilla malesuada. Donec euismod tincidunt purus vel commodo. \n Aenean volutpat libero '
                        'quis imperdiet tincidunt. Proin iaculis eros at turpis laoreet molestie. Quisque '
                        'pellentesque, lorem id ornare fermentum, nunc urna ultrices libero, eget tempor ipsum lectus '
                        'sollicitudin nibh. Sed sit amet vestibulum nulla. Vivamus dictum, dui id consectetur mattis, '
                        'sapien erat tristique nulla, at lobortis enim nibh eu orci. Curabitur eu purus porttitor, '
                        'rhoncus libero sed, mattis tellus. Praesent ullamcorper tincidunt ex. Vivamus lectus urna, '
                        'dignissim sit amet efficitur a, malesuada at nisi \n. Curabitur auctor ut libero ac pharetra. '
                        'Nunc rutrum facilisis felis, ac rhoncus lorem pulvinar quis. In felis neque, mollis nec '
                        'sagittis feugiat, finibus maximus mauris. Nullam varius, risus id scelerisque tempor, justo '
                        'purus malesuada nulla, eu sagittis purus arcu eget justo. Orci varius natoque penatibus et '
                        'magnis dis parturient montes, nascetur ridiculus mus. Fusce vel pretium augue. Pellentesque '
                        'eu semper odio. Suspendisse congue varius est, et euismod justo accumsan sed. Etiam nec '
                        'scelerisque risus, sed tempus ante. Proin fringilla leo urna, eget pulvinar leo placerat et. '
                        '\n Etiam mollis lacus ut sapien elementum, sed volutpat dui faucibus. Fusce ligula risus, '
                        'tempor at justo ac, tincidunt finibus magna. Duis eget sapien et nibh tincidunt faucibus. '
                        'Duis tempus tincidunt leo. Aenean sit amet cursus ex. Etiam eget finibus nulla, a rutrum '
                        'turpis. Proin imperdiet, augue consectetur varius varius, lectus elit egestas velit, '
                        'ullamcorper pulvinar dolor felis at leo. Cras nec est ut est efficitur pulvinar nec vel nisi. '
                        'Nullam sed elit eu ante finibus volutpat. Nam id diam a urna rutrum dictum. \n Pellentesque '
                        'habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Integer '
                        'accumsan et mi eu sagittis. Ut id nulla at quam efficitur molestie. Donec viverra ex vitae '
                        'mauris ullamcorper elementum. Proin sed felis enim. Suspendisse potenti. Integer malesuada '
                        'interdum mi, ornare semper lorem tempus condimentum. Cras sodales risus quis nibh fermentum '
                        'volutpat. Sed vel tincidunt lectus.',
            'website': None,
            'publications': [],
            'duration': DateRange(date(2052, 3, 1), date(2055, 10, 1)),
            'country': ProjectCountry.SJM
        }
    },
    'people': {
        '01DB2ECBP2MFB0DH3EF3PH74R0': {
            'id': '01DB2ECBP2MFB0DH3EF3PH74R0',
            'first_name': 'Constance',
            'last_name': 'Watson',
            'orcid_id': 'https://sandbox.orcid.org/0000-0001-8373-6934',
            'logo_url': 'https://cdn.web.bas.ac.uk/bas-registers-service/v1/sample-avatars/conwat/conwat-256.jpg',
            'organisation_nid': '01DB2ECBP3WZDP4PES64XKXJ1A'
        },
        '01DB2ECBP25PVTVVGT9YT7CKSB': {
            'id': '01DB2ECBP25PVTVVGT9YT7CKSB',
            'first_name': 'John',
            'last_name': 'Cinnamon',
            'orcid_id': 'https://sandbox.orcid.org/0000-0001-5652-1129',
            'logo_url': 'https://cdn.web.bas.ac.uk/bas-registers-service/v1/sample-avatars/cinjo/cinjo-256.jpg',
            'organisation_nid': '01DB2ECBP3VF45F1N4XEBF83FE'
        },
        '01DB2ECBP38X26APJ2DNPJERYH': {
            'id': '01DB2ECBP38X26APJ2DNPJERYH',
            'first_name': 'R',
            'last_name': 'Harrison',
            'orcid_id': None,
            'logo_url': None,
            'organisation_nid': '01DB2ECBP3VF45F1N4XEBF83FE'
        },
        '01DB2ECBP3T8V7RD9YW2WA69F1': {
            'id': '01DB2ECBP3T8V7RD9YW2WA69F1',
            'first_name': 'Stewart',
            'last_name': 'Freeman',
            'orcid_id': 'https://fake.orcid.org/0000-0001-0294-4767',
            'logo_url': None,
            'organisation_nid': '01DB2ECBP3DRACYX8PSJBG7A8G'
        },
        '01DB2ECBP3PKST1WFTYR83JSKN': {
            'id': '01DB2ECBP3PKST1WFTYR83JSKN',
            'first_name': 'Rebecca',
            'last_name': 'Ward',
            'orcid_id': 'https://fake.orcid.org/0000-0001-2746-1492',
            'logo_url': None,
            'organisation_nid': '01DB2ECBP3DRACYX8PSJBG7A8G'
        },
        '01DB2ECBP383XV1746WZ48Z87T': {
            'id': '01DB2ECBP383XV1746WZ48Z87T',
            'first_name': 'Howard',
            'last_name': 'Dark',
            'orcid_id': 'https://fake.orcid.org/0000-0002-2995-29632',
            'logo_url': None,
            'organisation_nid': '01DB2ECBP3JRA4T9FGFFBWJBCM'
        }
    },
    'organisations': {
        '01DB2ECBP3WZDP4PES64XKXJ1A': {
            'id': '01DB2ECBP3WZDP4PES64XKXJ1A',
            'grid_identifier': 'XE-EXAMPLE-grid.5500.1',
            'name': 'Example Organisation 1',
            'acronym': 'EXORG1',
            'website': 'https://www.example.com',
            'logo_url': 'https://placeimg.com/256/256/arch'
        },
        '01DB2ECBP3VF45F1N4XEBF83FE': {
            'id': '01DB2ECBP3VF45F1N4XEBF83FE',
            'grid_identifier': None,
            'name': 'Example Organisation 2',
            'acronym': None,
            'website': None,
            'logo_url': None
        },
        '01DB2ECBP3DRACYX8PSJBG7A8G': {
            'id': '01DB2ECBP3DRACYX8PSJBG7A8G',
            'grid_identifier': 'XE-EXAMPLE-grid.5500.3',
            'name': 'Example Organisation 3',
            'acronym': 'EXORG3',
            'website': 'https://www.example.com',
            'logo_url': 'https://placeimg.com/256/256/arch'
        },
        '01DB2ECBP3JRA4T9FGFFBWJBCM': {
            'id': '01DB2ECBP3JRA4T9FGFFBWJBCM',
            'grid_identifier': 'XE-EXAMPLE-grid.5500.4',
            'name': 'Example Organisation 4',
            'acronym': 'EXORG4',
            'website': 'https://www.example.com',
            'logo_url': 'https://placeimg.com/256/256/arch'
        },
        '01DB2ECBP3A13RJ6QEZFN26ZEP': {
            'id': '01DB2ECBP3A13RJ6QEZFN26ZEP',
            'grid_identifier': 'XE-EXAMPLE-grid.5501.1',
            'name': 'Example Funder Organisation 1',
            'acronym': 'EXFUNDORG1',
            'website': 'https://www.example.com',
            'logo_url': 'https://placeimg.com/256/256/arch'
        },
        '01DB2ECBP3YQE4394T0Q97TPP2': {
            'id': '01DB2ECBP3YQE4394T0Q97TPP2',
            'grid_identifier': 'XE-EXAMPLE-grid.5501.2',
            'name': 'Example Funder Organisation 2',
            'acronym': 'EXFUNDORG2',
            'website': 'https://www.example.com',
            'logo_url': 'https://placeimg.com/256/256/arch'
        }
    },
    'grants': {
        '01DB2ECBP3XQ4B8Z5DW7W963YD': {
            'id': '01DB2ECBP3XQ4B8Z5DW7W963YD',
            'reference': 'EX-GRANT-0001',
            'title': 'Example grant 1',
            'abstract': 'This grant is used as an example, for demonstration or testing purposes. '
                        'The contents of this grant, and resources it relates to, will not change. \n'
                        'This example grant (1) is a grant with a single project and funder. The project and '
                        'organisations related to this grant will not be related to another grant. This grant has an '
                        'abstract, website and publications. The grant is closed and occurs in the past. \n'
                        'The remainder of this abstract is padding text to give a realistic abstract length.\n'
                        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eget lorem eleifend turpis '
                        'vestibulum sollicitudin. Curabitur libero nulla, maximus ut facilisis et, maximus quis dolor. '
                        'Nunc ut malesuada felis. Sed volutpat et lectus vitae convallis. Class aptent taciti sociosqu '
                        'ad litora torquent per conubia nostra, per inceptos himenaeos. Fusce ullamcorper nec ante ut '
                        'vulputate. Praesent ultricies mattis dolor quis ultrices. Ut sagittis scelerisque leo '
                        'fringilla malesuada. Donec euismod tincidunt purus vel commodo. \n Aenean volutpat libero '
                        'quis imperdiet tincidunt. Proin iaculis eros at turpis laoreet molestie. Quisque '
                        'pellentesque, lorem id ornare fermentum, nunc urna ultrices libero, eget tempor ipsum lectus '
                        'sollicitudin nibh. Sed sit amet vestibulum nulla. Vivamus dictum, dui id consectetur mattis, '
                        'sapien erat tristique nulla, at lobortis enim nibh eu orci. Curabitur eu purus porttitor, '
                        'rhoncus libero sed, mattis tellus. Praesent ullamcorper tincidunt ex. Vivamus lectus urna, '
                        'dignissim sit amet efficitur a, malesuada at nisi \n. Curabitur auctor ut libero ac pharetra. '
                        'Nunc rutrum facilisis felis, ac rhoncus lorem pulvinar quis. In felis neque, mollis nec '
                        'sagittis feugiat, finibus maximus mauris. Nullam varius, risus id scelerisque tempor, justo '
                        'purus malesuada nulla, eu sagittis purus arcu eget justo. Orci varius natoque penatibus et '
                        'magnis dis parturient montes, nascetur ridiculus mus. Fusce vel pretium augue. Pellentesque '
                        'eu semper odio. Suspendisse congue varius est, et euismod justo accumsan sed. Etiam nec '
                        'scelerisque risus, sed tempus ante. Proin fringilla leo urna, eget pulvinar leo placerat et. '
                        '\n Etiam mollis lacus ut sapien elementum, sed volutpat dui faucibus. Fusce ligula risus, '
                        'tempor at justo ac, tincidunt finibus magna. Duis eget sapien et nibh tincidunt faucibus. '
                        'Duis tempus tincidunt leo. Aenean sit amet cursus ex. Etiam eget finibus nulla, a rutrum '
                        'turpis. Proin imperdiet, augue consectetur varius varius, lectus elit egestas velit, '
                        'ullamcorper pulvinar dolor felis at leo. Cras nec est ut est efficitur pulvinar nec vel nisi. '
                        'Nullam sed elit eu ante finibus volutpat. Nam id diam a urna rutrum dictum. \n Pellentesque '
                        'habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Integer '
                        'accumsan et mi eu sagittis. Ut id nulla at quam efficitur molestie. Donec viverra ex vitae '
                        'mauris ullamcorper elementum. Proin sed felis enim. Suspendisse potenti. Integer malesuada '
                        'interdum mi, ornare semper lorem tempus condimentum. Cras sodales risus quis nibh fermentum '
                        'volutpat. Sed vel tincidunt lectus.',
            'website': 'https://www.example.com',
            'publications': [
                'https://doi.org/10.5555/15822411',
                'https://doi.org/10.5555/45284431',
                'https://doi.org/10.5555/59959290'
            ],
            'duration': DateRange(date(2012, 3, 1), date(2015, 10, 1)),
            'status': GrantStatus.Closed,
            'total_funds': 120000,
            'total_funds_currency': GrantCurrency.GBP,
            'organisation_nid': '01DB2ECBP3A13RJ6QEZFN26ZEP'
        },
        '01DB2ECBP3DJ512HM1409ZNDHW': {
            'id': '01DB2ECBP3DJ512HM1409ZNDHW',
            'reference': 'EX-GRANT-0002',
            'title': 'Example grant 2',
            'abstract': 'This grant is used as an example, for demonstration or testing purposes. '
                        'The contents of this grant, and resources it relates to, will not change. \n'
                        'This example grant (2) is a grant with a single project and funder. The project and '
                        'organisations related to this grant will also relate to other grants. This grant does not '
                        'have a website, publications or total funding amount. The grant is active and occurs in the '
                        'present. \n'
                        'No padding text is added to this abstract.',
            'website': None,
            'publications': [],
            'duration': DateRange(date(2012, 3, 1), date(2055, 10, 1)),
            'status': GrantStatus.Active,
            'total_funds': None,
            'total_funds_currency': None,
            'organisation_nid': '01DB2ECBP3YQE4394T0Q97TPP2'
        },
        '01DB2ECBP3S0PJ4PND3XTVGX25': {
            'id': '01DB2ECBP3S0PJ4PND3XTVGX25',
            'reference': 'EX-GRANT-0003',
            'title': 'Example grant 3',
            'abstract': 'This grant is used as an example, for demonstration or testing purposes. '
                        'The contents of this grant, and resources it relates to, will not change. \n'
                        'This example grant (3) is a grant with a single project and funder. The project and '
                        'organisations related to this grant will also relate to other grants. This grant has an '
                        'abstract and total funding amount, it does not have a website or publications. The grant is '
                        'approved and occurs in the future. \n'
                        'The remainder of this abstract is padding text to give a realistic abstract length.\n'
                        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eget lorem eleifend turpis '
                        'vestibulum sollicitudin. Curabitur libero nulla, maximus ut facilisis et, maximus quis dolor. '
                        'Nunc ut malesuada felis. Sed volutpat et lectus vitae convallis. Class aptent taciti sociosqu '
                        'ad litora torquent per conubia nostra, per inceptos himenaeos. Fusce ullamcorper nec ante ut '
                        'vulputate. Praesent ultricies mattis dolor quis ultrices. Ut sagittis scelerisque leo '
                        'fringilla malesuada. Donec euismod tincidunt purus vel commodo. \n Aenean volutpat libero '
                        'quis imperdiet tincidunt. Proin iaculis eros at turpis laoreet molestie. Quisque '
                        'pellentesque, lorem id ornare fermentum, nunc urna ultrices libero, eget tempor ipsum lectus '
                        'sollicitudin nibh. Sed sit amet vestibulum nulla. Vivamus dictum, dui id consectetur mattis, '
                        'sapien erat tristique nulla, at lobortis enim nibh eu orci. Curabitur eu purus porttitor, '
                        'rhoncus libero sed, mattis tellus. Praesent ullamcorper tincidunt ex. Vivamus lectus urna, '
                        'dignissim sit amet efficitur a, malesuada at nisi \n. Curabitur auctor ut libero ac pharetra. '
                        'Nunc rutrum facilisis felis, ac rhoncus lorem pulvinar quis. In felis neque, mollis nec '
                        'sagittis feugiat, finibus maximus mauris. Nullam varius, risus id scelerisque tempor, justo '
                        'purus malesuada nulla, eu sagittis purus arcu eget justo. Orci varius natoque penatibus et '
                        'magnis dis parturient montes, nascetur ridiculus mus. Fusce vel pretium augue. Pellentesque '
                        'eu semper odio. Suspendisse congue varius est, et euismod justo accumsan sed. Etiam nec '
                        'scelerisque risus, sed tempus ante. Proin fringilla leo urna, eget pulvinar leo placerat et. '
                        '\n Etiam mollis lacus ut sapien elementum, sed volutpat dui faucibus. Fusce ligula risus, '
                        'tempor at justo ac, tincidunt finibus magna. Duis eget sapien et nibh tincidunt faucibus. '
                        'Duis tempus tincidunt leo. Aenean sit amet cursus ex. Etiam eget finibus nulla, a rutrum '
                        'turpis. Proin imperdiet, augue consectetur varius varius, lectus elit egestas velit, '
                        'ullamcorper pulvinar dolor felis at leo. Cras nec est ut est efficitur pulvinar nec vel nisi. '
                        'Nullam sed elit eu ante finibus volutpat. Nam id diam a urna rutrum dictum. \n Pellentesque '
                        'habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Integer '
                        'accumsan et mi eu sagittis. Ut id nulla at quam efficitur molestie. Donec viverra ex vitae '
                        'mauris ullamcorper elementum. Proin sed felis enim. Suspendisse potenti. Integer malesuada '
                        'interdum mi, ornare semper lorem tempus condimentum. Cras sodales risus quis nibh fermentum '
                        'volutpat. Sed vel tincidunt lectus.',
            'website': None,
            'publications': [],
            'duration': DateRange(date(2052, 3, 1), date(2055, 10, 1)),
            'status': GrantStatus.Approved,
            'total_funds': 2000000,
            'total_funds_currency': GrantCurrency.EUR,
            'organisation_nid': '01DB2ECBP3YQE4394T0Q97TPP2'
        }
    },
    "participants": {
        '01DB2ECBP3622SPB5PS3J8W4XF': {
            'id': '01DB2ECBP3622SPB5PS3J8W4XF',
            'role': ParticipantRole.InvestigationRole_PrincipleInvestigator,
            'project_nid': '01DB2ECBP24NHYV5KZQG2N3FS2',
            'person_nid': '01DB2ECBP2MFB0DH3EF3PH74R0'
        },
        '01DB2ECBP3VQGDYMW1CRPJ0VGP': {
            'id': '01DB2ECBP3VQGDYMW1CRPJ0VGP',
            'role': ParticipantRole.InvestigationRole_CoInvestigator,
            'project_nid': '01DB2ECBP24NHYV5KZQG2N3FS2',
            'person_nid': '01DB2ECBP25PVTVVGT9YT7CKSB'
        },
        '01DB2ECBP32H2EZCGKSSV9J4R4': {
            'id': '01DB2ECBP32H2EZCGKSSV9J4R4',
            'role': ParticipantRole.InvestigationRole_PrincipleInvestigator,
            'project_nid': '01DB2ECBP2DXX8VN7S7AYJBGBT',
            'person_nid': '01DB2ECBP38X26APJ2DNPJERYH'
        },
        '01DB2ECBP3016QXHEAVVT77Z1W': {
            'id': '01DB2ECBP3016QXHEAVVT77Z1W',
            'role': ParticipantRole.InvestigationRole_PrincipleInvestigator,
            'project_nid': '01DB2ECBP2MB2Z9K1BSK5BND0V',
            'person_nid': '01DB2ECBP3T8V7RD9YW2WA69F1'
        },
        '01DB2ECBP355YQTDW80GS5R8E7': {
            'id': '01DB2ECBP355YQTDW80GS5R8E7',
            'role': ParticipantRole.InvestigationRole_CoInvestigator,
            'project_nid': '01DB2ECBP2MB2Z9K1BSK5BND0V',
            'person_nid': '01DB2ECBP38X26APJ2DNPJERYH'
        },
        '01DB2ECBP3Z4Z3R0XTDVR6AKC2': {
            'id': '01DB2ECBP3Z4Z3R0XTDVR6AKC2',
            'role': ParticipantRole.InvestigationRole_CoInvestigator,
            'project_nid': '01DB2ECBP2MB2Z9K1BSK5BND0V',
            'person_nid': '01DB2ECBP3PKST1WFTYR83JSKN'
        },
        '01DB2ECBP3VNTNJK30E8D36X3K': {
            'id': '01DB2ECBP3VNTNJK30E8D36X3K',
            'role': ParticipantRole.InvestigationRole_CoInvestigator,
            'project_nid': '01DB2ECBP2MB2Z9K1BSK5BND0V',
            'person_nid': '01DB2ECBP383XV1746WZ48Z87T'
        }
    },
    "allocations": {
        '01DB2ECBP35AT5WBG092J5GDQ9': {
            'id': '01DB2ECBP35AT5WBG092J5GDQ9',
            'project_nid': '01DB2ECBP24NHYV5KZQG2N3FS2',
            'grant_nid': '01DB2ECBP3XQ4B8Z5DW7W963YD'
        },
        '01DB2ECBP355B1K0573GPN851M': {
            'id': '01DB2ECBP355B1K0573GPN851M',
            'project_nid': '01DB2ECBP2DXX8VN7S7AYJBGBT',
            'grant_nid': '01DB2ECBP3DJ512HM1409ZNDHW'
        },
        '01DB2ECBP3GETAEV6PT70TZJM9': {
            'id': '01DB2ECBP3GETAEV6PT70TZJM9',
            'project_nid': '01DB2ECBP2MB2Z9K1BSK5BND0V',
            'grant_nid': '01DB2ECBP3S0PJ4PND3XTVGX25'
        }
    }
}


def seed_predictable_test_resources():
    """
    Creates a series of resources for use in tests where all values and relationships are controlled and remain the same

    This method creates and persists model instances for each test resource.
    """
    try:
        # Organisations
        for organisation in static_resources['organisations'].values():
            if not db.session.query(exists().where(Organisation.neutral_id == organisation['id'])).scalar():
                organisation_resource = Organisation(
                    neutral_id=organisation['id'],
                    name=organisation['name']
                )
                db.session.add(organisation_resource)
                if organisation['grid_identifier'] is not None:
                    organisation_resource.grid_identifier = organisation['grid_identifier']
                if organisation['acronym'] is not None:
                    organisation_resource.acronym = organisation['acronym']
                if organisation['website'] is not None:
                    organisation_resource.website = organisation['website']
                if organisation['logo_url'] is not None:
                    organisation_resource.logo_url = organisation['logo_url']

        # Projects
        for project in static_resources['projects'].values():
            if not db.session.query(exists().where(Project.neutral_id == project['id'])).scalar():
                project_resource = Project(
                    neutral_id=project['id'],
                    title=project['title'],
                    abstract=project['abstract'],
                    access_duration=DateRange(project['duration'].lower, None),
                    project_duration=project['duration'],
                )
                db.session.add(project_resource)
                if project['acronym'] is not None:
                    project_resource.acronym = project['acronym']
                if project['website'] is not None:
                    project_resource.website = project['website']
                if len(project['publications']) > 0:
                    project_resource.publications = project['publications']
                if project['country'] is not None:
                    project_resource.country = project['country']

        # People
        for person in static_resources['people'].values():
            if not db.session.query(exists().where(Person.neutral_id == person['id'])).scalar():
                person_resource = Person(
                    neutral_id=person['id'],
                    organisation=Organisation.query.filter_by(neutral_id=person['organisation_nid']).one()
                )
                db.session.add(person_resource)
                if person['first_name'] is not None:
                    person_resource.first_name = person['first_name']
                if person['last_name'] is not None:
                    person_resource.last_name = person['last_name']
                if person['orcid_id'] is not None:
                    person_resource.orcid_id = person['orcid_id']
                if person['logo_url'] is not None:
                    person_resource.logo_url = person['logo_url']

        # Grants
        for grant in static_resources['grants'].values():
            if not db.session.query(exists().where(Grant.neutral_id == grant['id'])).scalar():
                grant_resource = Grant(
                    neutral_id=grant['id'],
                    reference=grant['reference'],
                    title=grant['title'],
                    duration=grant['duration'],
                    status=grant['status'],
                    funder=Organisation.query.filter_by(neutral_id=grant['organisation_nid']).one()
                )
                db.session.add(grant_resource)
                if grant['abstract'] is not None:
                    grant_resource.abstract = grant['abstract']
                if grant['website'] is not None:
                    grant_resource.website = grant['website']
                if len(grant['publications']) > 0:
                    grant_resource.publications = grant['publications']
                if grant['total_funds'] is not None:
                    grant_resource.total_funds = grant['total_funds']
                if grant['total_funds_currency'] is not None:
                    grant_resource.total_funds_currency = grant['total_funds_currency']

        # Participants
        for participant in static_resources['participants'].values():
            if not db.session.query(exists().where(Participant.neutral_id == participant['id'])).scalar():
                participant_resource = Participant(
                    neutral_id=participant['id'],
                    project=Project.query.filter_by(neutral_id=participant['project_nid']).one(),
                    person=Person.query.filter_by(neutral_id=participant['person_nid']).one(),
                    role=participant['role']
                )
                db.session.add(participant_resource)

        # Allocations
        for allocation in static_resources['allocations'].values():
            if not db.session.query(exists().where(Allocation.neutral_id == allocation['id'])).scalar():
                allocation_resource = Allocation(
                    neutral_id=allocation['id'],
                    project=Project.query.filter_by(neutral_id=allocation['project_nid']).one(),
                    grant=Grant.query.filter_by(neutral_id=allocation['grant_nid']).one()
                )
                db.session.add(allocation_resource)

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # Remove any added, but non-committed, entities
        db.session.flush()
        raise e


def seed_random_test_resources(count: int = 100):
    """
    Creates a series of resources for use in staging environments where the distribution of resource types, resource
     attributes and relationships between resources are fake but realistic.

     The Faker library is used to generate fake values and decide between different types of resource, for example
     whether a resource is 'small' or 'large' or has an optional related resource.

    This method creates and persists model instances for a variable number of test resources.

    :type count: int
    :param count: number of random test resources to create
    """
    try:
        # some funders are not random and don't need to be made for each test resource
        funders = make_common_funders()

        for i in range(0, count):
            # Project
            project_type = faker.project_type()
            ukri_council = _get_ukri_council(project_type=project_type)
            project_duration = faker.project_duration(project_type)
            project = Project(
                neutral_id=generate_neutral_id(),
                title=faker.title(),
                abstract=faker.abstract(),
                access_duration=DateRange(project_duration.lower, None),
                project_duration=project_duration,
                country=ProjectCountry.SJM
            )
            if faker.has_acronym(project_type):
                project.acronym = faker.acronym()
            if faker.has_website(project_type):
                project.website = faker.uri()
            if faker.has_publications:
                project.publications = faker.publications_list()
            db.session.add(project)

            # Grant(s)
            # Currently assumes 1:1 relationship between project and grant until #22 is addressed
            funder = _get_funder(project_type=project_type, ukri_council=ukri_council, funders=funders)
            grant_type = faker.project_type()
            grant_duration = faker.project_duration(grant_type)
            grant = Grant(
                neutral_id=generate_neutral_id(),
                reference=faker.grant_reference(grant_type, ukri_council),
                title=faker.title(),
                abstract=faker.abstract(),
                duration=grant_duration,
                status=faker.grant_status(grant_duration).name,
                total_funds=faker.total_funds(grant_type),
                total_funds_currency=faker.grant_currency(grant_type).name,
                funder=funder
            )
            if faker.has_acronym(grant_type):
                grant.acronym = faker.acronym()
            if faker.has_website(grant_type):
                grant.website = faker.grant_website(grant_type, grant.reference)
            if faker.has_publications:
                grant.publications = faker.publications_list()
            db.session.add(grant)

            # Participants (PI)
            principle_investigator = _get_principle_investigator()
            db.session.add(Participant(
                neutral_id=generate_neutral_id(),
                project=project,
                person=principle_investigator,
                role=ParticipantRole.InvestigationRole_PrincipleInvestigator
            ))

            # Participants (Co-I)
            project_has_co_investigators = faker.has_co_investigators()
            if project_has_co_investigators:
                co_investigators = _get_co_investigators(principle_investigator=principle_investigator)
                for co_investigator in co_investigators:
                    db.session.add(Participant(
                        neutral_id=generate_neutral_id(),
                        project=project,
                        person=co_investigator,
                        role=ParticipantRole.InvestigationRole_CoInvestigator
                    ))

            # Allocations
            db.session.add(Allocation(
                neutral_id=generate_neutral_id(),
                project=project,
                grant=grant
            ))

            db.session.commit()
    except Exception as e:
        db.session.rollback()
        # Remove any added, but non-committed, entities
        db.session.flush()
        raise e


def make_common_funders() -> Dict[str, Organisation]:
    """
    Creates a series of common funder (Organisations) resources

    When generating fake projects most will be UKRI grants, which will be funded by a UKRI research council.
    Some others will be EU grants, which will be funded by the EU.

    This method creates these funders if they don't already exist.

    :rtype dict
    :return: Dictionary of common funder resources indexed by acronym
    """
    if not db.session.query(exists().where(Organisation.website == 'https://ahrc.ukri.org')).scalar():
        db.session.add(Organisation(
            neutral_id=generate_neutral_id(),
            grid_identifier=faker.grid_id(),
            name='Arts and Humanities Research Council',
            acronym='AHRC',
            website='https://ahrc.ukri.org',
            logo_url='https://placeimg.com/256/256/arch'
        ))
    ahrc = Organisation.query.filter_by(website='https://ahrc.ukri.org').one()

    if not db.session.query(exists().where(Organisation.website == 'https://bbsrc.ukri.org')).scalar():
        db.session.add(Organisation(
            neutral_id=generate_neutral_id(),
            grid_identifier=faker.grid_id(),
            name='Biotechnology and Biological Sciences Research Council',
            acronym='BBSRC',
            website='https://bbsrc.ukri.org',
            logo_url='https://placeimg.com/256/256/arch'
        ))
    bbsrc = Organisation.query.filter_by(website='https://bbsrc.ukri.org').one()

    if not db.session.query(exists().where(Organisation.website == 'https://esrc.ukri.org')).scalar():
        db.session.add(Organisation(
            neutral_id=generate_neutral_id(),
            grid_identifier=faker.grid_id(),
            name='Economic and Social Research Council',
            acronym='ESRC',
            website='https://esrc.ukri.org',
            logo_url='https://placeimg.com/256/256/arch'
        ))
    esrc = Organisation.query.filter_by(website='https://esrc.ukri.org').one()

    if not db.session.query(exists().where(Organisation.website == 'https://epsrc.ukri.org')).scalar():
        db.session.add(Organisation(
            neutral_id=generate_neutral_id(),
            grid_identifier=faker.grid_id(),
            name='Engineering and Physical Sciences Research Council',
            acronym='EPSRC',
            website='https://epsrc.ukri.org',
            logo_url='https://placeimg.com/256/256/arch'
        ))
    epsrc = Organisation.query.filter_by(website='https://epsrc.ukri.org').one()

    if not db.session.query(exists().where(Organisation.website == 'https://mrc.ukri.org')).scalar():
        db.session.add(Organisation(
            neutral_id=generate_neutral_id(),
            grid_identifier=faker.grid_id(),
            name='Medical Research Council',
            acronym='MRC',
            website='https://mrc.ukri.org',
            logo_url='https://placeimg.com/256/256/arch'
        ))
    mrc = Organisation.query.filter_by(website='https://mrc.ukri.org').one()

    if not db.session.query(exists().where(Organisation.website == 'https://nerc.ukri.org')).scalar():
        db.session.add(Organisation(
            neutral_id=generate_neutral_id(),
            grid_identifier=faker.grid_id(),
            name='Natural Environment Research Council',
            acronym='NERC',
            website='https://nerc.ukri.org',
            logo_url='https://placeimg.com/256/256/arch'
        ))
    nerc = Organisation.query.filter_by(website='https://nerc.ukri.org').one()

    if not db.session.query(exists().where(Organisation.website == 'https://stfc.ukri.org')).scalar():
        db.session.add(Organisation(
            neutral_id=generate_neutral_id(),
            grid_identifier=faker.grid_id(),
            name='Science and Technology Facilities Council',
            acronym='STFC',
            website='https://stfc.ukri.org',
            logo_url='https://placeimg.com/256/256/arch'
        ))
    stfc = Organisation.query.filter_by(website='https://stfc.ukri.org').one()

    if not db.session.query(exists().where(Organisation.website == 'https://europa.eu')).scalar():
        db.session.add(Organisation(
            neutral_id=generate_neutral_id(),
            grid_identifier=faker.grid_id(),
            name='European Union',
            acronym='EU',
            website='https://europa.eu',
            logo_url='https://placeimg.com/256/256/arch'
        ))
    eu = Organisation.query.filter_by(website='https://europa.eu').one()

    return {
        'AHRC': ahrc,
        'BBSRC': bbsrc,
        'ESRC': esrc,
        'EPSRC': epsrc,
        'MRC': mrc,
        'NERC': nerc,
        'STFC': stfc,
        'EU': eu
    }


def _get_ukri_council(project_type: GrantType) -> Optional[UKRICouncil]:
    """
    Returns the acronym of the funder for fake projects funded by a UKRI grant

    :type project_type: GrantType
    :param project_type: Member of the GrantType enumeration

    :rtype UKRICouncil
    :return: an Organisation model if a project is funded by a UKRI grant, otherwise None
    """
    if project_type is GrantType.UKRI_STANDARD_GRANT or project_type is GrantType.UKRI_LARGE_GRANT:
        return UKRICouncil[faker.grant_funder(project_type)]

    return None


def _get_funder(
    project_type: GrantType,
    ukri_council: Optional[UKRICouncil],
    funders: Dict[str, Organisation]
) -> Organisation:
    """
    Returns the funder (Organisation) resource for a fake project's grant

    For fake projects funded by a UKRI grant, the appropriate UKRI research council is returned.

    For fake projects funded by an EU grant, the EU funder is returned.

    For fake projects funded by an 'other' grant, a fake, random, funder is returned. At least 3 fake funders will be
    generated, after which an existing fake funder will be used.

    :type project_type: GrantType
    :param project_type: Member of the GrantType enumeration
    :type ukri_council: UKRICouncil
    :param ukri_council: an Organisation model if a project is funded by a UKRI grant, otherwise None
    :type funders: dict
    :param funders: Dictionary of common funder resources indexed by acronym

    :rtype Organisation
    :return: Organisation model instance for use as a funder for a grant in a fake project
    """
    if project_type is GrantType.UKRI_STANDARD_GRANT or project_type is GrantType.UKRI_LARGE_GRANT:
        return funders[ukri_council.name]

    funder_identifier = faker.grant_funder(project_type)

    if project_type is GrantType.EU_STANDARD_GRANT:
        return funders[funder_identifier]

    if project_type is GrantType.OTHER:
        non_other_funders = list(static_resources['organisations'].keys())
        for funder in funders.values():
            non_other_funders.append(funder.neutral_id)

        if funder_identifier is not None \
                and Organisation.query.filter(Organisation.neutral_id.notin_(non_other_funders)).count() >= 3:
            return Organisation.query.filter(Organisation.neutral_id.notin_(non_other_funders)).\
                order_by(func.random()).first()

        funder_organisation = Organisation(
            neutral_id=generate_neutral_id(),
            grid_identifier=faker.grid_id(),
            name=faker.company(),
            acronym=faker.acronym(),
            website=faker.uri(),
            logo_url='https://placeimg.com/256/256/arch'
        )
        db.session.add(funder_organisation)
        return funder_organisation


def _get_principle_investigator() -> Person:
    """
    Returns the Person resource for a fake project's principle investigator

    At least 3 fake People will be generated, after which a new or existing fake person will be used.

    :rtype Person
    :return: Person model instance for use as the principle investigator for a fake project
    """
    if faker.has_existing_principle_investigator() \
            and Person.query.filter(Person.neutral_id.notin_(static_resources['people'].keys())).count() >= 3:
        return Person.query.filter(Person.neutral_id.notin_(static_resources['people'].keys())). \
            order_by(func.random()).first()

    principle_investigator_organisation = _get_investigator_organisation()
    principle_investigator_person = Person(
        neutral_id=generate_neutral_id(),
        organisation=principle_investigator_organisation
    )
    if faker.has_orcid_id():
        principle_investigator_person.orcid_id = faker.orcid_id()
    if faker.male_or_female() == 'male':
        principle_investigator_person.first_name = faker.first_name_male(),
        principle_investigator_person.last_name = faker.last_name_male()
        if faker.has_avatar():
            principle_investigator_person.logo_url = faker.avatar_male()
    else:
        principle_investigator_person.first_name = faker.first_name_female(),
        principle_investigator_person.last_name = faker.last_name_female()
        if faker.has_avatar():
            principle_investigator_person.logo_url = faker.avatar_female()
    db.session.add(principle_investigator_person)

    return principle_investigator_person


def _get_investigator_organisation() -> Organisation:
    """
    Returns an Organisation for use as the organisation for a person associated with a fake project as a investigator

    At least 3 fake Organisations will be generated, after which a new or existing fake organisation will be used.

    :rtype Organisation
    :return: Organisation model instance for use as the organisation for a fake person resource
    """
    if faker.has_existing_principle_investigator_organisation() \
            and Organisation.query.filter(Organisation.neutral_id.notin_(
                static_resources['organisations'].keys()
            )).count() >= 3:
        return Organisation.query.filter(Organisation.neutral_id.notin_(static_resources['organisations'].keys())). \
            order_by(func.random()).first()

    principle_investigator_organisation = Organisation(
        neutral_id=generate_neutral_id(),
        grid_identifier=faker.grid_id(),
        name=faker.company(),
        acronym=faker.acronym(),
        website=faker.uri(),
        logo_url='https://placeimg.com/256/256/arch'
    )
    db.session.add(principle_investigator_organisation)

    return principle_investigator_organisation


def _get_co_investigators(principle_investigator: Person) -> List[Person]:
    """
    Returns a series of Person resources for a fake project's co-investigators

    A project may not have any co-investigators - where it does, at least 3 fake People will be generated, after which
    a new or existing fake person will be used (excluding the project's principle investigator).

    :type principle_investigator: Person
    :param principle_investigator: Person model instance used as the principle investigator for a fake project

    :rtype list
    :return: List of Person model instance for use as co-investigators for a fake project
    """
    co_investigators_count = faker.co_investigator_count()
    new_co_investigators_count = _get_new_co_investigator_count(
        co_investigators_count=co_investigators_count,
        principle_investigator=principle_investigator
    )

    for new_co_investigator in range(1, new_co_investigators_count):
        co_investigator_organisation = _get_investigator_organisation()

        co_investigator_person = Person(
            neutral_id=generate_neutral_id(),
            organisation=co_investigator_organisation
        )
        if faker.has_orcid_id():
            co_investigator_person.orcid_id = faker.orcid_id()
        if faker.male_or_female() == 'male':
            co_investigator_person.first_name = faker.first_name_male(),
            co_investigator_person.last_name = faker.last_name_male()
            if faker.has_avatar():
                co_investigator_person.logo_url = faker.avatar_male()
        else:
            co_investigator_person.first_name = faker.first_name_female(),
            co_investigator_person.last_name = faker.last_name_female()
            if faker.has_avatar():
                co_investigator_person.logo_url = faker.avatar_female()
        db.session.add(co_investigator_person)

    ineligible_investigators = list(static_resources['people'].keys())
    ineligible_investigators.append(principle_investigator.neutral_id)
    return Person.query.filter(Person.neutral_id.notin_(ineligible_investigators)).order_by(func.random())\
        .limit(co_investigators_count)


def _get_new_co_investigator_count(co_investigators_count: int, principle_investigator: Person) -> int:
    """
    Determines he number of new co-investigators needed for a fake project

    A proportion of the co-investigators for each project may be created as new resources. This method will ensure
    there are at least 10 people (across all projects), regardless of this proportion.

    :type co_investigators_count: int
    :param co_investigators_count: total number of co-investigators a fake project has
    :type principle_investigator: Person
    :param principle_investigator: Person model instance used as the principle investigator for a fake project

    :rtype int
    :return: the number of co-investigators in a fake project that should be created as new resources
    """
    new_co_investigators_count = 0

    for co_investigator in range(1, co_investigators_count):
        if not faker.has_existing_co_investigator():
            new_co_investigators_count = new_co_investigators_count + 1

    ineligible_investigators = list(static_resources['people'].keys())
    ineligible_investigators.append(principle_investigator.neutral_id)
    available_investigators = Person.query.filter(Person.neutral_id.notin_(ineligible_investigators)).count()

    if available_investigators < co_investigators_count:
        new_co_investigators_count = new_co_investigators_count + (co_investigators_count - available_investigators)

    investigators = Person.query.filter(Person.neutral_id.notin_(static_resources['people'].keys())).count()
    if investigators <= 10:
        initial_co_investigators_count = co_investigators_count - new_co_investigators_count
        if initial_co_investigators_count >= 10:
            return new_co_investigators_count + (10 - investigators)
        return new_co_investigators_count + initial_co_investigators_count

    return new_co_investigators_count
