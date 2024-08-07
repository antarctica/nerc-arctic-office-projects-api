from http import HTTPStatus

from arctic_office_projects_api.errors import ApiNotFoundError

from tests.base_test import BaseResourceTestCase


class OrganisationsResourceTestCase(BaseResourceTestCase):
    def test_organisations_list(self):
        expected_payload = {
            "data": [
                {
                    "attributes": {
                        "acronym": "EXORG1",
                        "grid-identifier": "XE-EXAMPLE-grid.5500.1",
                        "ror-identifier": "02b5d8509",
                        "logo-url": "https://placeimg.com/256/256/arch",
                        "name": "Example Organisation 1",
                        "website": "https://www.example.com"
                    },
                    "id": "01DB2ECBP3WZDP4PES64XKXJ1A",
                    "links": {
                        "self": "http://localhost:9001/organisations/01DB2ECBP3WZDP4PES64XKXJ1A"
                    },
                    "relationships": {
                        "grants": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9001/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/grants",
                                "self": "http://localhost:9001/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/grants"
                            }
                        },
                        "people": {
                            "data": [
                                {
                                    "id": "01DB2ECBP2MFB0DH3EF3PH74R0",
                                    "type": "people"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9001/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/people",
                                "self": "http://localhost:9001/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/people"
                            }
                        }
                    },
                    "type": "organisations"
                },
                {
                    "attributes": {
                        "acronym": None,
                        "grid-identifier": None,
                        "ror-identifier": None,
                        "logo-url": None,
                        "name": "Example Organisation 2",
                        "website": None
                    },
                    "id": "01DB2ECBP3VF45F1N4XEBF83FE",
                    "links": {
                        "self": "http://localhost:9001/organisations/01DB2ECBP3VF45F1N4XEBF83FE"
                    },
                    "relationships": {
                        "grants": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9001/organisations/01DB2ECBP3VF45F1N4XEBF83FE/grants",
                                "self": "http://localhost:9001/organisations/01DB2ECBP3VF45F1N4XEBF83FE/relationships/grants"
                            }
                        },
                        "people": {
                            "data": [
                                {
                                    "id": "01DB2ECBP25PVTVVGT9YT7CKSB",
                                    "type": "people"
                                },
                                {
                                    "id": "01DB2ECBP38X26APJ2DNPJERYH",
                                    "type": "people"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9001/organisations/01DB2ECBP3VF45F1N4XEBF83FE/people",
                                "self": "http://localhost:9001/organisations/01DB2ECBP3VF45F1N4XEBF83FE/relationships/people"
                            }
                        }
                    },
                    "type": "organisations"
                }
            ],
            "included": [
                {
                    "attributes": {
                        "avatar-url": "https://cdn.web.bas.ac.uk/bas-registers-service/v1/sample-avatars/conwat/conwat-256.jpg",
                        "first-name": "Constance",
                        "last-name": "Watson",
                        "orcid-id": "https://sandbox.orcid.org/0000-0001-8373-6934"
                    },
                    "id": "01DB2ECBP2MFB0DH3EF3PH74R0",
                    "links": {
                        "self": "http://localhost:9001/people/01DB2ECBP2MFB0DH3EF3PH74R0"
                    },
                    "relationships": {
                        "organisation": {
                            "data": {
                                "id": "01DB2ECBP3WZDP4PES64XKXJ1A",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9001/people/01DB2ECBP2MFB0DH3EF3PH74R0/organisations",
                                "self": "http://localhost:9001/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/organisations"
                            }
                        },
                        "participation": {
                            "data": [
                                {
                                    "id": "01DB2ECBP3622SPB5PS3J8W4XF",
                                    "type": "participants"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9001/people/01DB2ECBP2MFB0DH3EF3PH74R0/participants",
                                "self": "http://localhost:9001/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/participants"
                            }
                        }
                    },
                    "type": "people"
                },
                {
                    "attributes": {
                        "role": {
                            "class": "http://purl.org/spar/scoro/InvestigationRole",
                            "description": "The principle investigator of the research project.",
                            "member": "http://purl.org/spar/scoro/principle-investigator",
                            "title": "principle investigator"
                        }
                    },
                    "id": "01DB2ECBP3622SPB5PS3J8W4XF",
                    "links": {
                        "self": "http://localhost:9001/participants/01DB2ECBP3622SPB5PS3J8W4XF"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01DB2ECBP2MFB0DH3EF3PH74R0",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9001/participants/01DB2ECBP3622SPB5PS3J8W4XF/people",
                                "self": "http://localhost:9001/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9001/participants/01DB2ECBP3622SPB5PS3J8W4XF/projects",
                                "self": "http://localhost:9001/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/projects"
                            }
                        }
                    },
                    "type": "participants"
                },
                {
                    "attributes": {
                        "abstract": "This project is used as an example, for demonstration or testing purposes. The "
                                    "contents of this project, and resources it relates to, will not change. \n This "
                                    "example project (1) is a project with a single PI and single CoI belonging to the "
                                    "same organisation. It is also associated with a single grant and funder. The "
                                    "people, grants and organisations related to this project will not be related to "
                                    "another project. This project has an acronym, abstract, website and country "
                                    "property. The project duration is in the past. \n The remainder of this abstract "
                                    "is padding text to give a realistic abstract length. \n Lorem ipsum dolor sit amet"
                                    ", consectetur adipiscing elit. Maecenas eget lorem eleifend turpis vestibulum "
                                    "sollicitudin. Curabitur libero nulla, maximus ut facilisis et, maximus quis "
                                    "dolor. Nunc ut malesuada felis. Sed volutpat et lectus vitae convallis. Class "
                                    "aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos "
                                    "himenaeos. Fusce ullamcorper nec ante ut vulputate. Praesent ultricies mattis "
                                    "dolor quis ultrices. Ut sagittis scelerisque leo fringilla malesuada. Donec "
                                    "euismod tincidunt purus vel commodo. \n Aenean volutpat libero quis imperdiet "
                                    "tincidunt. Proin iaculis eros at turpis laoreet molestie. Quisque pellentesque, "
                                    "lorem id ornare fermentum, nunc urna ultrices libero, eget tempor ipsum lectus "
                                    "sollicitudin nibh. Sed sit amet vestibulum nulla. Vivamus dictum, dui id "
                                    "consectetur mattis, sapien erat tristique nulla, at lobortis enim nibh eu orci. "
                                    "Curabitur eu purus porttitor, rhoncus libero sed, mattis tellus. Praesent "
                                    "ullamcorper tincidunt ex. Vivamus lectus urna, dignissim sit amet efficitur a, "
                                    "malesuada at nisi. \n Curabitur auctor ut libero ac pharetra. Nunc rutrum "
                                    "facilisis felis, ac rhoncus lorem pulvinar quis. In felis neque, mollis nec "
                                    "sagittis feugiat, finibus maximus mauris. Nullam varius, risus id scelerisque "
                                    "tempor, justo purus malesuada nulla, eu sagittis purus arcu eget justo. Orci "
                                    "varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. "
                                    "Fusce vel pretium augue. Pellentesque eu semper odio. Suspendisse congue varius "
                                    "est, et euismod justo accumsan sed. Etiam nec scelerisque risus, sed tempus ante. "
                                    "Proin fringilla leo urna, eget pulvinar leo placerat et. \n Etiam mollis lacus ut "
                                    "sapien elementum, sed volutpat dui faucibus. Fusce ligula risus, tempor at justo "
                                    "ac, tincidunt finibus magna. Duis eget sapien et nibh tincidunt faucibus. Duis "
                                    "tempus tincidunt leo. Aenean sit amet cursus ex. Etiam eget finibus nulla, a "
                                    "rutrum turpis. Proin imperdiet, augue consectetur varius varius, lectus elit "
                                    "egestas velit, ullamcorper pulvinar dolor felis at leo. Cras nec est ut est "
                                    "efficitur pulvinar nec vel nisi. Nullam sed elit eu ante finibus volutpat. Nam id "
                                    "diam a urna rutrum dictum. \n Pellentesque habitant morbi tristique senectus et "
                                    "netus et malesuada fames ac turpis egestas. Integer accumsan et mi eu sagittis. "
                                    "Ut id nulla at quam efficitur molestie. Donec viverra ex vitae mauris ullamcorper "
                                    "elementum. Proin sed felis enim. Suspendisse potenti. Integer malesuada interdum "
                                    "mi, ornare semper lorem tempus condimentum. Cras sodales risus quis nibh "
                                    "fermentum volutpat. Sed vel tincidunt lectus.",
                        "access-duration": {
                            "end-instant": None,
                            "interval": "2012-03-01/..",
                            "start-instant": "2012-03-01"
                        },
                        "acronym": "EXPRO1",
                        "country": {
                            "iso-3166-alpha3-code": "SJM",
                            "name": "Svalbard and Jan Mayen"
                        },
                        "lead-project": None,
                        "project-duration": {
                            "end-instant": "2015-10-01",
                            "interval": "2012-03-01/2015-10-01",
                            "start-instant": "2012-03-01"
                        },
                        "publications": [
                            "https://doi.org/10.5555/76559541",
                            "https://doi.org/10.5555/97727778",
                            "https://doi.org/10.5555/79026270"
                        ],
                        "title": "Example project 1",
                        "website": "https://www.example.com"
                    },
                    "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                    "links": {
                        "self": "http://localhost:9001/projects/01DB2ECBP24NHYV5KZQG2N3FS2"
                    },
                    "relationships": {
                        "allocations": {
                            "data": [
                                {
                                    "id": "01DB2ECBP35AT5WBG092J5GDQ9",
                                    "type": "allocations"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9001/projects/01DB2ECBP24NHYV5KZQG2N3FS2/allocations",
                                "self": "http://localhost:9001/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/allocations"
                            }
                        },
                        'categorisations': {
                            'data': [
                                {
                                    'id': '01DC6HYAKYAXE7MZMD08QV5JWG',
                                    'type': 'categorisations'
                                }
                            ],
                            'links': {
                                'related': 'http://localhost:9001/projects/01DB2ECBP24NHYV5KZQG2N3FS2/categorisations',
                                'self': 'http://localhost:9001/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/categorisations'
                            }
                        },
                        "participants": {
                            "data": [
                                {
                                    "id": "01DB2ECBP3622SPB5PS3J8W4XF",
                                    "type": "participants"
                                },
                                {
                                    "id": "01DB2ECBP3VQGDYMW1CRPJ0VGP",
                                    "type": "participants"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9001/projects/01DB2ECBP24NHYV5KZQG2N3FS2/participants",
                                "self": "http://localhost:9001/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
                },
                {
                    "attributes": {
                        "avatar-url": "https://cdn.web.bas.ac.uk/bas-registers-service/v1/sample-avatars/cinjo/cinjo-256.jpg",
                        "first-name": "John",
                        "last-name": "Cinnamon",
                        "orcid-id": "https://sandbox.orcid.org/0000-0001-5652-1129"
                    },
                    "id": "01DB2ECBP25PVTVVGT9YT7CKSB",
                    "links": {
                        "self": "http://localhost:9001/people/01DB2ECBP25PVTVVGT9YT7CKSB"
                    },
                    "relationships": {
                        "organisation": {
                            "data": {
                                "id": "01DB2ECBP3VF45F1N4XEBF83FE",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9001/people/01DB2ECBP25PVTVVGT9YT7CKSB/organisations",
                                "self": "http://localhost:9001/people/01DB2ECBP25PVTVVGT9YT7CKSB/relationships/organisations"
                            }
                        },
                        "participation": {
                            "data": [
                                {
                                    "id": "01DB2ECBP3VQGDYMW1CRPJ0VGP",
                                    "type": "participants"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9001/people/01DB2ECBP25PVTVVGT9YT7CKSB/participants",
                                "self": "http://localhost:9001/people/01DB2ECBP25PVTVVGT9YT7CKSB/relationships/participants"
                            }
                        }
                    },
                    "type": "people"
                },
                {
                    "attributes": {
                        "role": {
                            "class": "http://purl.org/spar/scoro/InvestigationRole",
                            "description": "A co-investigator of the research project.",
                            "member": "http://purl.org/spar/scoro/co-investigator",
                            "title": "co-investigator"
                        }
                    },
                    "id": "01DB2ECBP3VQGDYMW1CRPJ0VGP",
                    "links": {
                        "self": "http://localhost:9001/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01DB2ECBP25PVTVVGT9YT7CKSB",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9001/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/people",
                                "self": "http://localhost:9001/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9001/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/projects",
                                "self": "http://localhost:9001/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/relationships/projects"
                            }
                        }
                    },
                    "type": "participants"
                },
                {
                    "attributes": {
                        "avatar-url": None,
                        "first-name": "R",
                        "last-name": "Harrison",
                        "orcid-id": None
                    },
                    "id": "01DB2ECBP38X26APJ2DNPJERYH",
                    "links": {
                        "self": "http://localhost:9001/people/01DB2ECBP38X26APJ2DNPJERYH"
                    },
                    "relationships": {
                        "organisation": {
                            "data": {
                                "id": "01DB2ECBP3VF45F1N4XEBF83FE",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9001/people/01DB2ECBP38X26APJ2DNPJERYH/organisations",
                                "self": "http://localhost:9001/people/01DB2ECBP38X26APJ2DNPJERYH/relationships/organisations"
                            }
                        },
                        "participation": {
                            "data": [
                                {
                                    "id": "01DB2ECBP32H2EZCGKSSV9J4R4",
                                    "type": "participants"
                                },
                                {
                                    "id": "01DB2ECBP355YQTDW80GS5R8E7",
                                    "type": "participants"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9001/people/01DB2ECBP38X26APJ2DNPJERYH/participants",
                                "self": "http://localhost:9001/people/01DB2ECBP38X26APJ2DNPJERYH/relationships/participants"
                            }
                        }
                    },
                    "type": "people"
                },
                {
                    "attributes": {
                        "role": {
                            "class": "http://purl.org/spar/scoro/InvestigationRole",
                            "description": "The principle investigator of the research project.",
                            "member": "http://purl.org/spar/scoro/principle-investigator",
                            "title": "principle investigator"
                        }
                    },
                    "id": "01DB2ECBP32H2EZCGKSSV9J4R4",
                    "links": {
                        "self": "http://localhost:9001/participants/01DB2ECBP32H2EZCGKSSV9J4R4"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01DB2ECBP38X26APJ2DNPJERYH",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9001/participants/01DB2ECBP32H2EZCGKSSV9J4R4/people",
                                "self": "http://localhost:9001/participants/01DB2ECBP32H2EZCGKSSV9J4R4/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP2DXX8VN7S7AYJBGBT",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9001/participants/01DB2ECBP32H2EZCGKSSV9J4R4/projects",
                                "self": "http://localhost:9001/participants/01DB2ECBP32H2EZCGKSSV9J4R4/relationships/projects"
                            }
                        }
                    },
                    "type": "participants"
                },
                {
                    "attributes": {
                        "abstract": "This project is used as an example, for demonstration or testing purposes. The "
                                    "contents of this project, and resources it relates to, will not change. This "
                                    "example project (2) has a single PI, organisation, grant and funder. The "
                                    "resources related to this project will also relate to other projects. This "
                                    "project does not have an acronym, website, publication or country property. The "
                                    "project duration is in the present. \n No padding text is added to this abstract.",
                        "access-duration": {
                            "end-instant": None,
                            "interval": "2012-03-01/..",
                            "start-instant": "2012-03-01"
                        },
                        "acronym": None,
                        "country": None,
                        "lead-project": None,
                        "project-duration": {
                            "end-instant": "2055-10-01",
                            "interval": "2012-03-01/2055-10-01",
                            "start-instant": "2012-03-01"
                        },
                        "publications": None,
                        "title": "Example project 2",
                        "website": None
                    },
                    "id": "01DB2ECBP2DXX8VN7S7AYJBGBT",
                    "links": {
                        "self": "http://localhost:9001/projects/01DB2ECBP2DXX8VN7S7AYJBGBT"
                    },
                    "relationships": {
                        "allocations": {
                            "data": [
                                {
                                    "id": "01DB2ECBP355B1K0573GPN851M",
                                    "type": "allocations"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9001/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/allocations",
                                "self": "http://localhost:9001/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/relationships/allocations"
                            }
                        },
                        'categorisations': {
                            'data': [],
                            'links': {
                                'related': 'http://localhost:9001/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/categorisations',
                                'self': 'http://localhost:9001/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/relationships/categorisations'
                            }
                        },
                        "participants": {
                            "data": [
                                {
                                    "id": "01DB2ECBP32H2EZCGKSSV9J4R4",
                                    "type": "participants"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9001/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/participants",
                                "self": "http://localhost:9001/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
                },
                {
                    "attributes": {
                        "role": {
                            "class": "http://purl.org/spar/scoro/InvestigationRole",
                            "description": "A co-investigator of the research project.",
                            "member": "http://purl.org/spar/scoro/co-investigator",
                            "title": "co-investigator"
                        }
                    },
                    "id": "01DB2ECBP355YQTDW80GS5R8E7",
                    "links": {
                        "self": "http://localhost:9001/participants/01DB2ECBP355YQTDW80GS5R8E7"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01DB2ECBP38X26APJ2DNPJERYH",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9001/participants/01DB2ECBP355YQTDW80GS5R8E7/people",
                                "self": "http://localhost:9001/participants/01DB2ECBP355YQTDW80GS5R8E7/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP2MB2Z9K1BSK5BND0V",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9001/participants/01DB2ECBP355YQTDW80GS5R8E7/projects",
                                "self": "http://localhost:9001/participants/01DB2ECBP355YQTDW80GS5R8E7/relationships/projects"
                            }
                        }
                    },
                    "type": "participants"
                },
                {
                    "attributes": {
                        "abstract": "This project is used as an example, for demonstration or testing purposes. The contents of "
                                    "this project, and resources it relates to, will not change. This example project (3) has a "
                                    "single PI and multiple CoIs belonging to different organisations. It is also associated "
                                    "with a single grant and funder. The resources related to this project will also relate to "
                                    "other projects. This project has an acronym and country properties, it does not have a "
                                    "website or publications. The project duration is in the future. \n The remainder of this "
                                    "abstract is padding text to give a realistic abstract length. \n Lorem ipsum dolor sit "
                                    "amet, consectetur adipiscing elit. Maecenas eget lorem eleifend turpis vestibulum "
                                    "sollicitudin. Curabitur libero nulla, maximus ut facilisis et, maximus quis dolor. Nunc "
                                    "ut malesuada felis. Sed volutpat et lectus vitae convallis. Class aptent taciti sociosqu "
                                    "ad litora torquent per conubia nostra, per inceptos himenaeos. Fusce ullamcorper nec ante "
                                    "ut vulputate. Praesent ultricies mattis dolor quis ultrices. Ut sagittis scelerisque leo "
                                    "fringilla malesuada. Donec euismod tincidunt purus vel commodo. \n Aenean volutpat libero "
                                    "quis imperdiet tincidunt. Proin iaculis eros at turpis laoreet molestie. Quisque "
                                    "pellentesque, lorem id ornare fermentum, nunc urna ultrices libero, eget tempor ipsum "
                                    "lectus sollicitudin nibh. Sed sit amet vestibulum nulla. Vivamus dictum, dui id "
                                    "consectetur mattis, sapien erat tristique nulla, at lobortis enim nibh eu orci. Curabitur "
                                    "eu purus porttitor, rhoncus libero sed, mattis tellus. Praesent ullamcorper tincidunt ex. "
                                    "Vivamus lectus urna, dignissim sit amet efficitur a, malesuada at nisi. \n Curabitur "
                                    "auctor ut libero ac pharetra. Nunc rutrum facilisis felis, ac rhoncus lorem pulvinar "
                                    "quis. In felis neque, mollis nec sagittis feugiat, finibus maximus mauris. Nullam varius, "
                                    "risus id scelerisque tempor, justo purus malesuada nulla, eu sagittis purus arcu eget "
                                    "justo. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus "
                                    "mus. Fusce vel pretium augue. Pellentesque eu semper odio. Suspendisse congue varius est, "
                                    "et euismod justo accumsan sed. Etiam nec scelerisque risus, sed tempus ante. Proin "
                                    "fringilla leo urna, eget pulvinar leo placerat et. \n Etiam mollis lacus ut sapien "
                                    "elementum, sed volutpat dui faucibus. Fusce ligula risus, tempor at justo ac, tincidunt "
                                    "finibus magna. Duis eget sapien et nibh tincidunt faucibus. Duis tempus tincidunt leo. "
                                    "Aenean sit amet cursus ex. Etiam eget finibus nulla, a rutrum turpis. Proin imperdiet, "
                                    "augue consectetur varius varius, lectus elit egestas velit, ullamcorper pulvinar dolor "
                                    "felis at leo. Cras nec est ut est efficitur pulvinar nec vel nisi. Nullam sed elit eu "
                                    "ante finibus volutpat. Nam id diam a urna rutrum dictum. \n Pellentesque habitant morbi "
                                    "tristique senectus et netus et malesuada fames ac turpis egestas. Integer accumsan et mi "
                                    "eu sagittis. Ut id nulla at quam efficitur molestie. Donec viverra ex vitae mauris "
                                    "ullamcorper elementum. Proin sed felis enim. Suspendisse potenti. Integer malesuada "
                                    "interdum mi, ornare semper lorem tempus condimentum. Cras sodales risus quis nibh "
                                    "fermentum volutpat. Sed vel tincidunt lectus.",
                        "access-duration": {
                            "end-instant": None,
                            "interval": "2052-03-01/..",
                            "start-instant": "2052-03-01"
                        },
                        "acronym": "EXPRO3",
                        "country": {
                            "iso-3166-alpha3-code": "SJM",
                            "name": "Svalbard and Jan Mayen"
                        },
                        "lead-project": None,
                        "project-duration": {
                            "end-instant": "2055-10-01",
                            "interval": "2052-03-01/2055-10-01",
                            "start-instant": "2052-03-01"
                        },
                        "publications": None,
                        "title": "Example project 3",
                        "website": None
                    },
                    "id": "01DB2ECBP2MB2Z9K1BSK5BND0V",
                    "links": {
                        "self": "http://localhost:9001/projects/01DB2ECBP2MB2Z9K1BSK5BND0V"
                    },
                    "relationships": {
                        "allocations": {
                            "data": [
                                {
                                    "id": "01DB2ECBP3GETAEV6PT70TZJM9",
                                    "type": "allocations"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9001/projects/01DB2ECBP2MB2Z9K1BSK5BND0V/allocations",
                                "self": "http://localhost:9001/projects/01DB2ECBP2MB2Z9K1BSK5BND0V/relationships/allocations"
                            }
                        },
                        'categorisations': {
                            'data': [
                                {
                                    "id": "01DC6HYAKY9ZEK8NQ1JGDMKCK7",
                                    "type": "categorisations"
                                },
                                {
                                    "id": "01DC6HYAKYMAEWTS5GDWX5P7Y0",
                                    "type": "categorisations"
                                },
                                {
                                    "id": "01DC6HYAKYSC023KCPG5WWQ7PN",
                                    "type": "categorisations"
                                }
                            ],
                            'links': {
                                'related': 'http://localhost:9001/projects/01DB2ECBP2MB2Z9K1BSK5BND0V/categorisations',
                                'self': 'http://localhost:9001/projects/01DB2ECBP2MB2Z9K1BSK5BND0V/relationships/categorisations'
                            }
                        },
                        "participants": {
                            "data": [
                                {
                                    "id": "01DB2ECBP3016QXHEAVVT77Z1W",
                                    "type": "participants"
                                },
                                {
                                    "id": "01DB2ECBP355YQTDW80GS5R8E7",
                                    "type": "participants"
                                },
                                {
                                    "id": "01DB2ECBP3Z4Z3R0XTDVR6AKC2",
                                    "type": "participants"
                                },
                                {
                                    "id": "01DB2ECBP3VNTNJK30E8D36X3K",
                                    "type": "participants"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9001/projects/01DB2ECBP2MB2Z9K1BSK5BND0V/participants",
                                "self": "http://localhost:9001/projects/01DB2ECBP2MB2Z9K1BSK5BND0V/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
                }
            ],
            "links": {
                "first": "http://localhost:9001/organisations?page=1",
                "last": "http://localhost:9001/organisations?page=3",
                "next": "http://localhost:9001/organisations?page=2",
                "prev": None,
                "self": "http://localhost:9001/organisations?page=1"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/organisations',
            base_url='http://localhost:9001',
            headers={'authorization': f"bearer {token}"},
            query_string={
                'page': 1
            }
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertListEqual(json_response['data'], expected_payload['data'])
        self.assertCountEqual(json_response['included'], expected_payload['included'])
        self.assertDictEqual(json_response['links'], expected_payload['links'])

    def test_organisations_detail(self):
        expected_payload = {
            "data": {
                "attributes": {
                    "acronym": "EXORG1",
                    "grid-identifier": "XE-EXAMPLE-grid.5500.1",
                    "ror-identifier": "02b5d8509",
                    "logo-url": "https://placeimg.com/256/256/arch",
                    "name": "Example Organisation 1",
                    "website": "https://www.example.com"
                },
                "id": "01DB2ECBP3WZDP4PES64XKXJ1A",
                "links": {
                    "self": "http://localhost:9001/organisations/01DB2ECBP3WZDP4PES64XKXJ1A"
                },
                "relationships": {
                    "grants": {
                        "data": [],
                        "links": {
                            "related": "http://localhost:9001/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/grants",
                            "self": "http://localhost:9001/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/grants"
                        }
                    },
                    "people": {
                        "data": [
                            {
                                "id": "01DB2ECBP2MFB0DH3EF3PH74R0",
                                "type": "people"
                            }
                        ],
                        "links": {
                            "related": "http://localhost:9001/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/people",
                            "self": "http://localhost:9001/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/people"
                        }
                    }
                },
                "type": "organisations"
            },
            "included": [
                {
                    "attributes": {
                        "avatar-url": "https://cdn.web.bas.ac.uk/bas-registers-service/v1/sample-avatars/conwat/conwat-256.jpg",
                        "first-name": "Constance",
                        "last-name": "Watson",
                        "orcid-id": "https://sandbox.orcid.org/0000-0001-8373-6934"
                    },
                    "id": "01DB2ECBP2MFB0DH3EF3PH74R0",
                    "links": {
                        "self": "http://localhost:9001/people/01DB2ECBP2MFB0DH3EF3PH74R0"
                    },
                    "relationships": {
                        "organisation": {
                            "data": {
                                "id": "01DB2ECBP3WZDP4PES64XKXJ1A",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9001/people/01DB2ECBP2MFB0DH3EF3PH74R0/organisations",
                                "self": "http://localhost:9001/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/organisations"
                            }
                        },
                        "participation": {
                            "data": [
                                {
                                    "id": "01DB2ECBP3622SPB5PS3J8W4XF",
                                    "type": "participants"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9001/people/01DB2ECBP2MFB0DH3EF3PH74R0/participants",
                                "self": "http://localhost:9001/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/participants"
                            }
                        }
                    },
                    "type": "people"
                },
                {
                    "attributes": {
                        "role": {
                            "class": "http://purl.org/spar/scoro/InvestigationRole",
                            "description": "The principle investigator of the research project.",
                            "member": "http://purl.org/spar/scoro/principle-investigator",
                            "title": "principle investigator"
                        }
                    },
                    "id": "01DB2ECBP3622SPB5PS3J8W4XF",
                    "links": {
                        "self": "http://localhost:9001/participants/01DB2ECBP3622SPB5PS3J8W4XF"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01DB2ECBP2MFB0DH3EF3PH74R0",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9001/participants/01DB2ECBP3622SPB5PS3J8W4XF/people",
                                "self": "http://localhost:9001/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9001/participants/01DB2ECBP3622SPB5PS3J8W4XF/projects",
                                "self": "http://localhost:9001/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/projects"
                            }
                        }
                    },
                    "type": "participants"
                },
                {
                    "attributes": {
                        "abstract": "This project is used as an example, for demonstration or testing purposes. The contents "
                                    "of this project, and resources it relates to, will not change. \n This example project (1) "
                                    "is a project with a single PI and single CoI belonging to the same organisation. It is "
                                    "also associated with a single grant and funder. The people, grants and organisations "
                                    "related to this project will not be related to another project. This project has an "
                                    "acronym, abstract, website and country property. The project duration is in the past. \n "
                                    "The remainder of this abstract is padding text to give a realistic abstract length. \n "
                                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eget lorem eleifend "
                                    "turpis vestibulum sollicitudin. Curabitur libero nulla, maximus ut facilisis et, maximus "
                                    "quis dolor. Nunc ut malesuada felis. Sed volutpat et lectus vitae convallis. Class aptent "
                                    "taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Fusce "
                                    "ullamcorper nec ante ut vulputate. Praesent ultricies mattis dolor quis ultrices. Ut "
                                    "sagittis scelerisque leo fringilla malesuada. Donec euismod tincidunt purus vel commodo. "
                                    "\n Aenean volutpat libero quis imperdiet tincidunt. Proin iaculis eros at turpis laoreet "
                                    "molestie. Quisque pellentesque, lorem id ornare fermentum, nunc urna ultrices libero, "
                                    "eget tempor ipsum lectus sollicitudin nibh. Sed sit amet vestibulum nulla. Vivamus "
                                    "dictum, dui id consectetur mattis, sapien erat tristique nulla, at lobortis enim nibh eu "
                                    "orci. Curabitur eu purus porttitor, rhoncus libero sed, mattis tellus. Praesent "
                                    "ullamcorper tincidunt ex. Vivamus lectus urna, dignissim sit amet efficitur a, malesuada "
                                    "at nisi. \n Curabitur auctor ut libero ac pharetra. Nunc rutrum facilisis felis, ac "
                                    "rhoncus lorem pulvinar quis. In felis neque, mollis nec sagittis feugiat, finibus maximus "
                                    "mauris. Nullam varius, risus id scelerisque tempor, justo purus malesuada nulla, eu "
                                    "sagittis purus arcu eget justo. Orci varius natoque penatibus et magnis dis parturient "
                                    "montes, nascetur ridiculus mus. Fusce vel pretium augue. Pellentesque eu semper odio. "
                                    "Suspendisse congue varius est, et euismod justo accumsan sed. Etiam nec scelerisque "
                                    "risus, sed tempus ante. Proin fringilla leo urna, eget pulvinar leo placerat et. \n Etiam "
                                    "mollis lacus ut sapien elementum, sed volutpat dui faucibus. Fusce ligula risus, tempor "
                                    "at justo ac, tincidunt finibus magna. Duis eget sapien et nibh tincidunt faucibus. Duis "
                                    "tempus tincidunt leo. Aenean sit amet cursus ex. Etiam eget finibus nulla, a rutrum "
                                    "turpis. Proin imperdiet, augue consectetur varius varius, lectus elit egestas velit, "
                                    "ullamcorper pulvinar dolor felis at leo. Cras nec est ut est efficitur pulvinar nec vel "
                                    "nisi. Nullam sed elit eu ante finibus volutpat. Nam id diam a urna rutrum dictum. \n "
                                    "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis "
                                    "egestas. Integer accumsan et mi eu sagittis. Ut id nulla at quam efficitur molestie. "
                                    "Donec viverra ex vitae mauris ullamcorper elementum. Proin sed felis enim. Suspendisse "
                                    "potenti. Integer malesuada interdum mi, ornare semper lorem tempus condimentum. Cras "
                                    "sodales risus quis nibh fermentum volutpat. Sed vel tincidunt lectus.",
                        "access-duration": {
                            "end-instant": None,
                            "interval": "2012-03-01/..",
                            "start-instant": "2012-03-01"
                        },
                        "acronym": "EXPRO1",
                        "country": {
                            "iso-3166-alpha3-code": "SJM",
                            "name": "Svalbard and Jan Mayen"
                        },
                        "lead-project": None,
                        "project-duration": {
                            "end-instant": "2015-10-01",
                            "interval": "2012-03-01/2015-10-01",
                            "start-instant": "2012-03-01"
                        },
                        "publications": [
                            "https://doi.org/10.5555/76559541",
                            "https://doi.org/10.5555/97727778",
                            "https://doi.org/10.5555/79026270"
                        ],
                        "title": "Example project 1",
                        "website": "https://www.example.com"
                    },
                    "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                    "links": {
                        "self": "http://localhost:9001/projects/01DB2ECBP24NHYV5KZQG2N3FS2"
                    },
                    "relationships": {
                        "allocations": {
                            "data": [
                                {
                                    "id": "01DB2ECBP35AT5WBG092J5GDQ9",
                                    "type": "allocations"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9001/projects/01DB2ECBP24NHYV5KZQG2N3FS2/allocations",
                                "self": "http://localhost:9001/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/allocations"
                            }
                        },
                        'categorisations': {
                            'data': [
                                {
                                    'id': '01DC6HYAKYAXE7MZMD08QV5JWG',
                                    'type': 'categorisations'
                                }
                            ],
                            'links': {
                                'related': 'http://localhost:9001/projects/01DB2ECBP24NHYV5KZQG2N3FS2/categorisations',
                                'self': 'http://localhost:9001/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/categorisations'
                            }
                        },
                        "participants": {
                            "data": [
                                {
                                    "id": "01DB2ECBP3622SPB5PS3J8W4XF",
                                    "type": "participants"
                                },
                                {
                                    "id": "01DB2ECBP3VQGDYMW1CRPJ0VGP",
                                    "type": "participants"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9001/projects/01DB2ECBP24NHYV5KZQG2N3FS2/participants",
                                "self": "http://localhost:9001/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
                }
            ],
            "links": {
                "self": "http://localhost:9001/organisations/01DB2ECBP3WZDP4PES64XKXJ1A"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/organisations/01DB2ECBP3WZDP4PES64XKXJ1A',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9001'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response['data'], expected_payload['data'])
        self.assertCountEqual(json_response['included'], expected_payload['included'])
        self.assertDictEqual(json_response['links'], expected_payload['links'])

    def test_organisations_single_missing_unknown_id(self):
        error = ApiNotFoundError()
        expected_payload = self.util_prepare_expected_error_payload(error)

        for organisation_id in ['', 'unknown']:
            with self.subTest(organisation_id=organisation_id):
                token = self.util_create_auth_token()
                response = self.client.get(
                    f"/organisations/{organisation_id}",
                    headers={'authorization': f"bearer {token}"},
                    base_url='http://localhost:9001'
                )
                json_response = response.get_json()
                json_response = self.util_prepare_error_response(json_response)
                self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
                self.assertDictEqual(json_response, expected_payload)

    def test_organisations_relationship_grants(self):
        expected_payload = {
            "data": [],
            "links": {
                "related": "http://localhost:9001/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/grants",
                "self": "http://localhost:9001/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/grants"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/grants',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9001'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_organisations_relationship_people(self):
        expected_payload = {
            "data": [
                {
                    "id": "01DB2ECBP2MFB0DH3EF3PH74R0",
                    "type": "people"
                }
            ],
            "links": {
                "related": "http://localhost:9001/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/people",
                "self": "http://localhost:9001/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/people"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/people',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9001'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_organisations_grants(self):
        expected_payload = {
            "data": [],
            "links": {
                "self": "http://localhost:9001/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/grants"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/grants',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9001'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_organisations_people(self):
        expected_payload = {
            "data": [
                {
                    "attributes": {
                        "avatar-url": "https://cdn.web.bas.ac.uk/bas-registers-service/v1/sample-avatars/conwat/conwat-256.jpg",
                        "first-name": "Constance",
                        "last-name": "Watson",
                        "orcid-id": "https://sandbox.orcid.org/0000-0001-8373-6934"
                    },
                    "id": "01DB2ECBP2MFB0DH3EF3PH74R0",
                    "links": {
                        "self": "http://localhost:9001/people/01DB2ECBP2MFB0DH3EF3PH74R0"
                    },
                    "relationships": {
                        "organisation": {
                            "data": {
                                "id": "01DB2ECBP3WZDP4PES64XKXJ1A",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9001/people/01DB2ECBP2MFB0DH3EF3PH74R0/organisations",
                                "self": "http://localhost:9001/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/organisations"
                            }
                        },
                        "participation": {
                            "data": [
                                {
                                    "id": "01DB2ECBP3622SPB5PS3J8W4XF",
                                    "type": "participants"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9001/people/01DB2ECBP2MFB0DH3EF3PH74R0/participants",
                                "self": "http://localhost:9001/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/participants"
                            }
                        }
                    },
                    "type": "people"
                }
            ],
            "links": {
                "self": "http://localhost:9001/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/people"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/people',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9001'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)
