from http import HTTPStatus

from flask_migrate import Config, upgrade, downgrade, Migrate

from arctic_office_projects_api.meta.errors import ApiNotFoundError
from arctic_office_projects_api import db
from arctic_office_projects_api.seeding import seed_predictable_test_resources
from tests.base_test import BaseTestCase


class MainBlueprintTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        with self.app.app_context():
            # Migrate and seed database
            config = Config("migrations/alembic.ini")
            config.set_main_option("script_location", "migrations")
            Migrate(self.app, db)
            upgrade()
            seed_predictable_test_resources()
            db.session.commit()

    def tearDown(self):
        db.session.remove()
        with self.app.app_context():
            # Rollback all DB migrations
            downgrade(revision='base')

        super().tearDown()

    def test_index(self):
        response = self.client.get(
            '/',
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('meta', json_response.keys())
        self.assertIn('summary', json_response['meta'].keys())
        self.assertEqual(
            'This API is used to record details of projects related to the NERC Arctic Office - '
            'https://www.arctic.ac.uk',
            json_response['meta']['summary']
        )

    def test_projects_list(self):
        expected_payload = {
            "data": [
                {
                    "attributes": {
                        "abstract": "This project is used as an example, for demonstration or testing purposes. The "
                                    "contents of this project, and resources it relates to, will not change. \n This "
                                    "example project (1) is a project with a single PI and single CoI belonging to the "
                                    "same organisation. It is also associated with a single grant and funder. The "
                                    "people, grants and organisations related to this project will not be related to "
                                    "another project. This project has an acronym, abstract, website and country "
                                    "property. The project duration is in the past. \n The remainder of this abstract "
                                    "is padding text to give a realistic abstract length. \n Lorem ipsum dolor sit amet, "
                                    "consectetur adipiscing elit. Maecenas eget lorem eleifend turpis vestibulum "
                                    "sollicitudin. Curabitur libero nulla, maximus ut facilisis et, maximus quis dolor."
                                    " Nunc ut malesuada felis. Sed volutpat et lectus vitae convallis. Class aptent "
                                    "taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. "
                                    "Fusce ullamcorper nec ante ut vulputate. Praesent ultricies mattis dolor quis "
                                    "ultrices. Ut sagittis scelerisque leo fringilla malesuada. Donec euismod "
                                    "tincidunt purus vel commodo. \n Aenean volutpat libero quis imperdiet tincidunt. "
                                    "Proin iaculis eros at turpis laoreet molestie. Quisque pellentesque, lorem id "
                                    "ornare fermentum, nunc urna ultrices libero, eget tempor ipsum lectus "
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
                        "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/allocations",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/allocations"
                            }
                        },
                        "categorisations": {
                            "data": [
                                {
                                    "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                                    "type": "categorisations"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/categorisations",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/categorisations"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/participants",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
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
                        "self": "http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/allocations",
                                "self": "http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/relationships/allocations"
                            }
                        },
                        "categorisations": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/categorisations",
                                "self": "http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/relationships/categorisations"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/participants",
                                "self": "http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
                }
            ],
            "included": [
                {
                    "id": "01DB2ECBP35AT5WBG092J5GDQ9",
                    "links": {
                        "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9"
                    },
                    "relationships": {
                        "grant": {
                            "data": {
                                "id": "01DB2ECBP3XQ4B8Z5DW7W963YD",
                                "type": "grants"
                            },
                            "links": {
                                "related": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/grants",
                                "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/relationships/grants"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/projects",
                                "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/relationships/projects"
                            }
                        }
                    },
                    "type": "allocations"
                },
                {
                    "attributes": {
                        "abstract": "This grant is used as an example, for demonstration or testing purposes. The "
                                    "contents of this grant, and resources it relates to, will not change. \n This "
                                    "example grant (1) is a grant with a single project and funder. The project and "
                                    "organisations related to this grant will not be related to another grant. This "
                                    "grant has an abstract, website and publications. The grant is closed and occurs "
                                    "in the past. \n The remainder of this abstract is padding text to give a realistic "
                                    "abstract length. \n Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                                    "Maecenas eget lorem eleifend turpis vestibulum sollicitudin. Curabitur libero "
                                    "nulla, maximus ut facilisis et, maximus quis dolor. Nunc ut malesuada felis. Sed "
                                    "volutpat et lectus vitae convallis. Class aptent taciti sociosqu ad litora "
                                    "torquent per conubia nostra, per inceptos himenaeos. Fusce ullamcorper nec ante "
                                    "ut vulputate. Praesent ultricies mattis dolor quis ultrices. Ut sagittis "
                                    "scelerisque leo fringilla malesuada. Donec euismod tincidunt purus vel commodo. "
                                    "\n Aenean volutpat libero quis imperdiet tincidunt. Proin iaculis eros at turpis "
                                    "laoreet molestie. Quisque pellentesque, lorem id ornare fermentum, nunc urna "
                                    "ultrices libero, eget tempor ipsum lectus sollicitudin nibh. Sed sit amet "
                                    "vestibulum nulla. Vivamus dictum, dui id consectetur mattis, sapien erat "
                                    "tristique nulla, at lobortis enim nibh eu orci. Curabitur eu purus porttitor, "
                                    "rhoncus libero sed, mattis tellus. Praesent ullamcorper tincidunt ex. Vivamus "
                                    "lectus urna, dignissim sit amet efficitur a, malesuada at nisi. \n Curabitur "
                                    "auctor ut libero ac pharetra. Nunc rutrum facilisis felis, ac rhoncus lorem "
                                    "pulvinar quis. In felis neque, mollis nec sagittis feugiat, finibus maximus "
                                    "mauris. Nullam varius, risus id scelerisque tempor, justo purus malesuada nulla, "
                                    "eu sagittis purus arcu eget justo. Orci varius natoque penatibus et magnis dis "
                                    "parturient montes, nascetur ridiculus mus. Fusce vel pretium augue. Pellentesque "
                                    "eu semper odio. Suspendisse congue varius est, et euismod justo accumsan sed. "
                                    "Etiam nec scelerisque risus, sed tempus ante. Proin fringilla leo urna, eget "
                                    "pulvinar leo placerat et. \n Etiam mollis lacus ut sapien elementum, sed volutpat "
                                    "dui faucibus. Fusce ligula risus, tempor at justo ac, tincidunt finibus magna. "
                                    "Duis eget sapien et nibh tincidunt faucibus. Duis tempus tincidunt leo. Aenean "
                                    "sit amet cursus ex. Etiam eget finibus nulla, a rutrum turpis. Proin imperdiet, "
                                    "augue consectetur varius varius, lectus elit egestas velit, ullamcorper pulvinar "
                                    "dolor felis at leo. Cras nec est ut est efficitur pulvinar nec vel nisi. Nullam "
                                    "sed elit eu ante finibus volutpat. Nam id diam a urna rutrum dictum. \n "
                                    "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac "
                                    "turpis egestas. Integer accumsan et mi eu sagittis. Ut id nulla at quam efficitur "
                                    "molestie. Donec viverra ex vitae mauris ullamcorper elementum. Proin sed felis "
                                    "enim. Suspendisse potenti. Integer malesuada interdum mi, ornare semper lorem "
                                    "tempus condimentum. Cras sodales risus quis nibh fermentum volutpat. Sed vel "
                                    "tincidunt lectus.",
                        "duration": {
                            "end-instant": "2015-10-01",
                            "interval": "2012-03-01/2015-10-01",
                            "start-instant": "2012-03-01"
                        },
                        "publications": [
                            "https://doi.org/10.5555/15822411",
                            "https://doi.org/10.5555/45284431",
                            "https://doi.org/10.5555/59959290"
                        ],
                        "reference": "EX-GRANT-0001",
                        "status": "closed",
                        "title": "Example grant 1",
                        "total-funds": {
                            "currency": {
                                "iso-4217-code": "GBP",
                                "major-symbol": "\u00a3"
                            },
                            "value": 120000.00
                        },
                        "website": "https://www.example.com"
                    },
                    "id": "01DB2ECBP3XQ4B8Z5DW7W963YD",
                    "links": {
                        "self": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD"
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
                                "related": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/allocations",
                                "self": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/relationships/allocations"
                            }
                        },
                        "funder": {
                            "data": {
                                "id": "01DB2ECBP3A13RJ6QEZFN26ZEP",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/organisations",
                                "self": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/relationships/organisations"
                            }
                        }
                    },
                    "type": "grants"
                },
                {
                    "attributes": {
                        "acronym": "EXFUNDORG1",
                        "grid-identifier": "XE-EXAMPLE-grid.5501.1",
                        "logo-url": "https://placeimg.com/256/256/arch",
                        "name": "Example Funder Organisation 1",
                        "website": "https://www.example.com"
                    },
                    "id": "01DB2ECBP3A13RJ6QEZFN26ZEP",
                    "links": {
                        "self": "http://localhost:9000/organisations/01DB2ECBP3A13RJ6QEZFN26ZEP"
                    },
                    "relationships": {
                        "grants": {
                            "data": [
                                {
                                    "id": "01DB2ECBP3XQ4B8Z5DW7W963YD",
                                    "type": "grants"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/organisations/01DB2ECBP3A13RJ6QEZFN26ZEP/grants",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3A13RJ6QEZFN26ZEP/relationships/grants"
                            }
                        },
                        "people": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/organisations/01DB2ECBP3A13RJ6QEZFN26ZEP/people",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3A13RJ6QEZFN26ZEP/relationships/people"
                            }
                        }
                    },
                    "type": "organisations"
                },
                {
                    "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                    "links": {
                        "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG"
                    },
                    "relationships": {
                        "category": {
                            "data": {
                                "id": "01DC6HYAKX53S13HCN2SBN4333",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/categories",
                                "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/relationships/categories"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/projects",
                                "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/relationships/projects"
                            }
                        }
                    },
                    "type": "categorisations"
                },
                {
                    "attributes": {
                        "aliases": [
                            "Third Term"
                        ],
                        'concept': 'https://www.example.com/category-scheme-1/category-term-4',
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The "
                            "contents of this term, and resources it relates to, will not change. \n This term (3) is "
                            "a third level term with a second level term as a parent (2) and no child terms."
                        ],
                        "examples": [
                            "Example category term 3 - example"
                        ],
                        "notation": "1.2.3",
                        "notes": [
                            "Example category term 3 - note"
                        ],
                        'scheme': 'https://www.example.com/category-scheme-1',
                        "scope-notes": [
                            "Example category term 3 - scope note"
                        ],
                        "title": "Example Category Term: Level 3"
                    },
                    "id": "01DC6HYAKX53S13HCN2SBN4333",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [
                                {
                                    "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                                    "type": "categorisations"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": {
                                "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                },
                {
                    "attributes": {
                        "aliases": [
                            "Second Term"
                        ],
                        'concept': 'https://www.example.com/category-scheme-1/category-term-3',
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The "
                            "contents of this term, and resources it relates to, will not change. \n This term (2) is "
                            "a second level term with a first level term as a parent (1) and a single child term (3)."
                        ],
                        "examples": [
                            "Example category term 2 - example"
                        ],
                        "notation": "1.2",
                        "notes": [
                            "Example category term 2 - note"
                        ],
                        'scheme': 'https://www.example.com/category-scheme-1',
                        "scope-notes": [
                            "Example category term 2 - scope note"
                        ],
                        "title": "Example Category Term: Level 2"
                    },
                    "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": {
                                "id": "01DC6HYAKX5NT8WBYWASQ9ENC8",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                },
                {
                    "attributes": {
                        "acronym": "EXCATSCH1",
                        "description": "This category scheme is used as an example, for demonstration or testing "
                                       "purposes. The terms in this scheme, and resources they relates to, will not "
                                       "change.",
                        "name": "Example Category Scheme 1",
                        "revision": "2019-05-28",
                        "version": "1.0"
                    },
                    "id": "01DC6HYAKXG8FCN63D7DH06W84",
                    "links": {
                        "self": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84"
                    },
                    "relationships": {
                        "categories": {
                            "data": [
                                {
                                    "id": "01DC6HYAKX993ZK6YHCVWAE169",
                                    "type": "categories"
                                },
                                {
                                    "id": "01DC6HYAKX5NT8WBYWASQ9ENC8",
                                    "type": "categories"
                                },
                                {
                                    "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                                    "type": "categories"
                                },
                                {
                                    "id": "01DC6HYAKX53S13HCN2SBN4333",
                                    "type": "categories"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84/categories",
                                "self": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84/relationships/categories"
                            }
                        }
                    },
                    "type": "category-schemes"
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
                        "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01DB2ECBP2MFB0DH3EF3PH74R0",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/people",
                                "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/projects",
                                "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/projects"
                            }
                        }
                    },
                    "type": "participants"
                },
                {
                    "attributes": {
                        "avatar-url": "https://cdn.web.bas.ac.uk/bas-registers-service/v1/sample-avatars/conwat/conwat-256.jpg",
                        "first-name": "Constance",
                        "last-name": "Watson",
                        "orcid-id": "https://sandbox.orcid.org/0000-0001-8373-6934"
                    },
                    "id": "01DB2ECBP2MFB0DH3EF3PH74R0",
                    "links": {
                        "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0"
                    },
                    "relationships": {
                        "organisation": {
                            "data": {
                                "id": "01DB2ECBP3WZDP4PES64XKXJ1A",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/organisations",
                                "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/organisations"
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
                                "related": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/participants",
                                "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/participants"
                            }
                        }
                    },
                    "type": "people"
                },
                {
                    "attributes": {
                        "acronym": "EXORG1",
                        "grid-identifier": "XE-EXAMPLE-grid.5500.1",
                        "logo-url": "https://placeimg.com/256/256/arch",
                        "name": "Example Organisation 1",
                        "website": "https://www.example.com"
                    },
                    "id": "01DB2ECBP3WZDP4PES64XKXJ1A",
                    "links": {
                        "self": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A"
                    },
                    "relationships": {
                        "grants": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/grants",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/grants"
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
                                "related": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/people",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/people"
                            }
                        }
                    },
                    "type": "organisations"
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
                        "self": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01DB2ECBP25PVTVVGT9YT7CKSB",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/people",
                                "self": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/projects",
                                "self": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/relationships/projects"
                            }
                        }
                    },
                    "type": "participants"
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
                        "self": "http://localhost:9000/people/01DB2ECBP25PVTVVGT9YT7CKSB"
                    },
                    "relationships": {
                        "organisation": {
                            "data": {
                                "id": "01DB2ECBP3VF45F1N4XEBF83FE",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9000/people/01DB2ECBP25PVTVVGT9YT7CKSB/organisations",
                                "self": "http://localhost:9000/people/01DB2ECBP25PVTVVGT9YT7CKSB/relationships/organisations"
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
                                "related": "http://localhost:9000/people/01DB2ECBP25PVTVVGT9YT7CKSB/participants",
                                "self": "http://localhost:9000/people/01DB2ECBP25PVTVVGT9YT7CKSB/relationships/participants"
                            }
                        }
                    },
                    "type": "people"
                },
                {
                    "attributes": {
                        "acronym": None,
                        "grid-identifier": None,
                        "logo-url": None,
                        "name": "Example Organisation 2",
                        "website": None
                    },
                    "id": "01DB2ECBP3VF45F1N4XEBF83FE",
                    "links": {
                        "self": "http://localhost:9000/organisations/01DB2ECBP3VF45F1N4XEBF83FE"
                    },
                    "relationships": {
                        "grants": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/organisations/01DB2ECBP3VF45F1N4XEBF83FE/grants",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3VF45F1N4XEBF83FE/relationships/grants"
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
                                "related": "http://localhost:9000/organisations/01DB2ECBP3VF45F1N4XEBF83FE/people",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3VF45F1N4XEBF83FE/relationships/people"
                            }
                        }
                    },
                    "type": "organisations"
                },
                {
                    "id": "01DB2ECBP355B1K0573GPN851M",
                    "links": {
                        "self": "http://localhost:9000/allocations/01DB2ECBP355B1K0573GPN851M"
                    },
                    "relationships": {
                        "grant": {
                            "data": {
                                "id": "01DB2ECBP3DJ512HM1409ZNDHW",
                                "type": "grants"
                            },
                            "links": {
                                "related": "http://localhost:9000/allocations/01DB2ECBP355B1K0573GPN851M/grants",
                                "self": "http://localhost:9000/allocations/01DB2ECBP355B1K0573GPN851M/relationships/grants"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP2DXX8VN7S7AYJBGBT",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/allocations/01DB2ECBP355B1K0573GPN851M/projects",
                                "self": "http://localhost:9000/allocations/01DB2ECBP355B1K0573GPN851M/relationships/projects"
                            }
                        }
                    },
                    "type": "allocations"
                },
                {
                    "attributes": {
                        "abstract": "This grant is used as an example, for demonstration or testing purposes. The "
                                    "contents of this grant, and resources it relates to, will not change. \n This "
                                    "example grant (2) is a grant with a single project and funder. The project and "
                                    "organisations related to this grant will also relate to other grants. This grant "
                                    "does not have a website, publications or total funding amount. The grant is "
                                    "active and occurs in the present. \n No padding text is added to this abstract.",
                        "duration": {
                            "end-instant": "2055-10-01",
                            "interval": "2012-03-01/2055-10-01",
                            "start-instant": "2012-03-01"
                        },
                        "publications": None,
                        "reference": "EX-GRANT-0002",
                        "status": "active",
                        "title": "Example grant 2",
                        "total-funds": None,
                        "website": None
                    },
                    "id": "01DB2ECBP3DJ512HM1409ZNDHW",
                    "links": {
                        "self": "http://localhost:9000/grants/01DB2ECBP3DJ512HM1409ZNDHW"
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
                                "related": "http://localhost:9000/grants/01DB2ECBP3DJ512HM1409ZNDHW/allocations",
                                "self": "http://localhost:9000/grants/01DB2ECBP3DJ512HM1409ZNDHW/relationships/allocations"
                            }
                        },
                        "funder": {
                            "data": {
                                "id": "01DB2ECBP3YQE4394T0Q97TPP2",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9000/grants/01DB2ECBP3DJ512HM1409ZNDHW/organisations",
                                "self": "http://localhost:9000/grants/01DB2ECBP3DJ512HM1409ZNDHW/relationships/organisations"
                            }
                        }
                    },
                    "type": "grants"
                },
                {
                    "attributes": {
                        "acronym": "EXFUNDORG2",
                        "grid-identifier": "XE-EXAMPLE-grid.5501.2",
                        "logo-url": "https://placeimg.com/256/256/arch",
                        "name": "Example Funder Organisation 2",
                        "website": "https://www.example.com"
                    },
                    "id": "01DB2ECBP3YQE4394T0Q97TPP2",
                    "links": {
                        "self": "http://localhost:9000/organisations/01DB2ECBP3YQE4394T0Q97TPP2"
                    },
                    "relationships": {
                        "grants": {
                            "data": [
                                {
                                    "id": "01DB2ECBP3DJ512HM1409ZNDHW",
                                    "type": "grants"
                                },
                                {
                                    "id": "01DB2ECBP3S0PJ4PND3XTVGX25",
                                    "type": "grants"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/organisations/01DB2ECBP3YQE4394T0Q97TPP2/grants",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3YQE4394T0Q97TPP2/relationships/grants"
                            }
                        },
                        "people": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/organisations/01DB2ECBP3YQE4394T0Q97TPP2/people",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3YQE4394T0Q97TPP2/relationships/people"
                            }
                        }
                    },
                    "type": "organisations"
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
                        "self": "http://localhost:9000/participants/01DB2ECBP32H2EZCGKSSV9J4R4"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01DB2ECBP38X26APJ2DNPJERYH",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP32H2EZCGKSSV9J4R4/people",
                                "self": "http://localhost:9000/participants/01DB2ECBP32H2EZCGKSSV9J4R4/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP2DXX8VN7S7AYJBGBT",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP32H2EZCGKSSV9J4R4/projects",
                                "self": "http://localhost:9000/participants/01DB2ECBP32H2EZCGKSSV9J4R4/relationships/projects"
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
                        "self": "http://localhost:9000/people/01DB2ECBP38X26APJ2DNPJERYH"
                    },
                    "relationships": {
                        "organisation": {
                            "data": {
                                "id": "01DB2ECBP3VF45F1N4XEBF83FE",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9000/people/01DB2ECBP38X26APJ2DNPJERYH/organisations",
                                "self": "http://localhost:9000/people/01DB2ECBP38X26APJ2DNPJERYH/relationships/organisations"
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
                                "related": "http://localhost:9000/people/01DB2ECBP38X26APJ2DNPJERYH/participants",
                                "self": "http://localhost:9000/people/01DB2ECBP38X26APJ2DNPJERYH/relationships/participants"
                            }
                        }
                    },
                    "type": "people"
                }
            ],
            "links": {
                "first": "http://localhost:9000/projects?page=1",
                "last": "http://localhost:9000/projects?page=2",
                "next": "http://localhost:9000/projects?page=2",
                "prev": None,
                "self": "http://localhost:9000/projects?page=1"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/projects',
            base_url='http://localhost:9000',
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

    def test_projects_detail(self):
        expected_payload = {
            "data": {
                "attributes": {
                    "abstract": "This project is used as an example, for demonstration or testing purposes. The "
                                "contents of "
                                "this project, and resources it relates to, will not change. \n This example project "
                                "(1) is a project with a single PI and single CoI belonging to the same organisation. "
                                "It is also associated with a single grant and funder. The people, grants and "
                                "organisations related to this project will not be related to another project. This "
                                "project has an acronym, abstract, website and country property. The project duration "
                                "is in the past. \n The remainder of this abstract is padding text to give a realistic "
                                "abstract length. \n Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas "
                                "eget lorem eleifend turpis vestibulum sollicitudin. Curabitur libero nulla, maximus "
                                "ut facilisis et, maximus quis dolor. Nunc ut malesuada felis. Sed volutpat et lectus "
                                "vitae convallis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, "
                                "per inceptos himenaeos. Fusce ullamcorper nec ante ut vulputate. Praesent ultricies "
                                "mattis dolor quis ultrices. Ut sagittis scelerisque leo fringilla malesuada. Donec "
                                "euismod tincidunt purus vel commodo. \n Aenean volutpat libero quis imperdiet "
                                "tincidunt. Proin iaculis eros at turpis laoreet molestie. Quisque pellentesque, lorem "
                                "id ornare fermentum, nunc urna ultrices libero, eget tempor ipsum lectus sollicitudin "
                                "nibh. Sed sit amet vestibulum nulla. Vivamus dictum, dui id consectetur mattis, "
                                "sapien erat tristique nulla, at lobortis enim nibh eu orci. Curabitur eu purus "
                                "porttitor, rhoncus libero sed, mattis tellus. Praesent ullamcorper tincidunt ex. "
                                "Vivamus lectus urna, dignissim sit amet efficitur a, malesuada at nisi. \n Curabitur "
                                "auctor ut libero ac pharetra. Nunc rutrum facilisis felis, ac rhoncus lorem pulvinar "
                                "quis. In felis neque, mollis nec sagittis feugiat, finibus maximus mauris. Nullam "
                                "varius, risus id scelerisque tempor, justo purus malesuada nulla, eu sagittis purus "
                                "arcu eget justo. Orci varius natoque penatibus et magnis dis parturient montes, "
                                "nascetur ridiculus mus. Fusce vel pretium augue. Pellentesque eu semper odio. "
                                "Suspendisse congue varius est, et euismod justo accumsan sed. Etiam nec scelerisque "
                                "risus, sed tempus ante. Proin fringilla leo urna, eget pulvinar leo placerat et. \n "
                                "Etiam mollis lacus ut sapien elementum, sed volutpat dui faucibus. Fusce ligula "
                                "risus, tempor at justo ac, tincidunt finibus magna. Duis eget sapien et nibh "
                                "tincidunt faucibus. Duis tempus tincidunt leo. Aenean sit amet cursus ex. Etiam eget "
                                "finibus nulla, a rutrum turpis. Proin imperdiet, augue consectetur varius varius, "
                                "lectus elit egestas velit, ullamcorper pulvinar dolor felis at leo. Cras nec est ut "
                                "est efficitur pulvinar nec vel nisi. Nullam sed elit eu ante finibus volutpat. Nam id "
                                "diam a urna rutrum dictum. \n Pellentesque habitant morbi tristique senectus et netus "
                                "et malesuada fames ac turpis egestas. Integer accumsan et mi eu sagittis. Ut id nulla "
                                "at quam efficitur molestie. Donec viverra ex vitae mauris ullamcorper elementum. "
                                "Proin sed felis enim. Suspendisse potenti. Integer malesuada interdum mi, ornare "
                                "semper lorem tempus condimentum. Cras sodales risus quis nibh fermentum volutpat. Sed "
                                "vel tincidunt lectus.",
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
                    "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2"
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
                            "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/allocations",
                            "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/allocations"
                        }
                    },
                    "categorisations": {
                        "data": [
                            {
                                "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                                "type": "categorisations"
                            }
                        ],
                        "links": {
                            "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/categorisations",
                            "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/categorisations"
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
                            "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/participants",
                            "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/participants"
                        }
                    }
                },
                "type": "projects"
            },
            "included": [
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
                        "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01DB2ECBP2MFB0DH3EF3PH74R0",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/people",
                                "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/projects",
                                "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/projects"
                            }
                        }
                    },
                    "type": "participants"
                },
                {
                    "attributes": {
                        "avatar-url": "https://cdn.web.bas.ac.uk/bas-registers-service/v1/sample-avatars/conwat/conwat-256.jpg",
                        "first-name": "Constance",
                        "last-name": "Watson",
                        "orcid-id": "https://sandbox.orcid.org/0000-0001-8373-6934"
                    },
                    "id": "01DB2ECBP2MFB0DH3EF3PH74R0",
                    "links": {
                        "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0"
                    },
                    "relationships": {
                        "organisation": {
                            "data": {
                                "id": "01DB2ECBP3WZDP4PES64XKXJ1A",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/organisations",
                                "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/organisations"
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
                                "related": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/participants",
                                "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/participants"
                            }
                        }
                    },
                    "type": "people"
                },
                {
                    "attributes": {
                        "acronym": "EXORG1",
                        "grid-identifier": "XE-EXAMPLE-grid.5500.1",
                        "logo-url": "https://placeimg.com/256/256/arch",
                        "name": "Example Organisation 1",
                        "website": "https://www.example.com"
                    },
                    "id": "01DB2ECBP3WZDP4PES64XKXJ1A",
                    "links": {
                        "self": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A"
                    },
                    "relationships": {
                        "grants": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/grants",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/grants"
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
                                "related": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/people",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/people"
                            }
                        }
                    },
                    "type": "organisations"
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
                        "self": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01DB2ECBP25PVTVVGT9YT7CKSB",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/people",
                                "self": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/projects",
                                "self": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/relationships/projects"
                            }
                        }
                    },
                    "type": "participants"
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
                        "self": "http://localhost:9000/people/01DB2ECBP25PVTVVGT9YT7CKSB"
                    },
                    "relationships": {
                        "organisation": {
                            "data": {
                                "id": "01DB2ECBP3VF45F1N4XEBF83FE",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9000/people/01DB2ECBP25PVTVVGT9YT7CKSB/organisations",
                                "self": "http://localhost:9000/people/01DB2ECBP25PVTVVGT9YT7CKSB/relationships/organisations"
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
                                "related": "http://localhost:9000/people/01DB2ECBP25PVTVVGT9YT7CKSB/participants",
                                "self": "http://localhost:9000/people/01DB2ECBP25PVTVVGT9YT7CKSB/relationships/participants"
                            }
                        }
                    },
                    "type": "people"
                },
                {
                    "attributes": {
                        "acronym": None,
                        "grid-identifier": None,
                        "logo-url": None,
                        "name": "Example Organisation 2",
                        "website": None
                    },
                    "id": "01DB2ECBP3VF45F1N4XEBF83FE",
                    "links": {
                        "self": "http://localhost:9000/organisations/01DB2ECBP3VF45F1N4XEBF83FE"
                    },
                    "relationships": {
                        "grants": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/organisations/01DB2ECBP3VF45F1N4XEBF83FE/grants",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3VF45F1N4XEBF83FE/relationships/grants"
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
                                "related": "http://localhost:9000/organisations/01DB2ECBP3VF45F1N4XEBF83FE/people",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3VF45F1N4XEBF83FE/relationships/people"
                            }
                        }
                    },
                    "type": "organisations"
                },
                {
                    "id": "01DB2ECBP35AT5WBG092J5GDQ9",
                    "links": {
                        "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9"
                    },
                    "relationships": {
                        "grant": {
                            "data": {
                                "id": "01DB2ECBP3XQ4B8Z5DW7W963YD",
                                "type": "grants"
                            },
                            "links": {
                                "related": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/grants",
                                "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/relationships/grants"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/projects",
                                "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/relationships/projects"
                            }
                        }
                    },
                    "type": "allocations"
                },
                {
                    "attributes": {
                        "abstract": "This grant is used as an example, for demonstration or testing purposes. The contents of "
                                    "this grant, and resources it relates to, will not change. \n This example grant (1) is a "
                                    "grant with a single project and funder. The project and organisations related to this "
                                    "grant will not be related to another grant. This grant has an abstract, website and "
                                    "publications. The grant is closed and occurs in the past. \n The remainder of this "
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
                        "duration": {
                            "end-instant": "2015-10-01",
                            "interval": "2012-03-01/2015-10-01",
                            "start-instant": "2012-03-01"
                        },
                        "publications": [
                            "https://doi.org/10.5555/15822411",
                            "https://doi.org/10.5555/45284431",
                            "https://doi.org/10.5555/59959290"
                        ],
                        "reference": "EX-GRANT-0001",
                        "status": "closed",
                        "title": "Example grant 1",
                        "total-funds": {
                            "currency": {
                                "iso-4217-code": "GBP",
                                "major-symbol": "\u00a3"
                            },
                            "value": 120000.00
                        },
                        "website": "https://www.example.com"
                    },
                    "id": "01DB2ECBP3XQ4B8Z5DW7W963YD",
                    "links": {
                        "self": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD"
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
                                "related": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/allocations",
                                "self": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/relationships/allocations"
                            }
                        },
                        "funder": {
                            "data": {
                                "id": "01DB2ECBP3A13RJ6QEZFN26ZEP",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/organisations",
                                "self": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/relationships/organisations"
                            }
                        }
                    },
                    "type": "grants"
                },
                {
                    "attributes": {
                        "acronym": "EXFUNDORG1",
                        "grid-identifier": "XE-EXAMPLE-grid.5501.1",
                        "logo-url": "https://placeimg.com/256/256/arch",
                        "name": "Example Funder Organisation 1",
                        "website": "https://www.example.com"
                    },
                    "id": "01DB2ECBP3A13RJ6QEZFN26ZEP",
                    "links": {
                        "self": "http://localhost:9000/organisations/01DB2ECBP3A13RJ6QEZFN26ZEP"
                    },
                    "relationships": {
                        "grants": {
                            "data": [
                                {
                                    "id": "01DB2ECBP3XQ4B8Z5DW7W963YD",
                                    "type": "grants"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/organisations/01DB2ECBP3A13RJ6QEZFN26ZEP/grants",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3A13RJ6QEZFN26ZEP/relationships/grants"
                            }
                        },
                        "people": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/organisations/01DB2ECBP3A13RJ6QEZFN26ZEP/people",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3A13RJ6QEZFN26ZEP/relationships/people"
                            }
                        }
                    },
                    "type": "organisations"
                },
                {
                    "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                    "links": {
                        "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG"
                    },
                    "relationships": {
                        "category": {
                            "data": {
                                "id": "01DC6HYAKX53S13HCN2SBN4333",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/categories",
                                "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/relationships/categories"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/projects",
                                "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/relationships/projects"
                            }
                        }
                    },
                    "type": "categorisations"
                },
                {
                    "attributes": {
                        "aliases": [
                            "Third Term"
                        ],
                        'concept': 'https://www.example.com/category-scheme-1/category-term-4',
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The "
                            "contents of this term, and resources it relates to, will not change. \n This term (3) is "
                            "a third level term with a second level term as a parent (2) and no child terms."
                        ],
                        "examples": [
                            "Example category term 3 - example"
                        ],
                        "notation": "1.2.3",
                        "notes": [
                            "Example category term 3 - note"
                        ],
                        'scheme': 'https://www.example.com/category-scheme-1',
                        "scope-notes": [
                            "Example category term 3 - scope note"
                        ],
                        "title": "Example Category Term: Level 3"
                    },
                    "id": "01DC6HYAKX53S13HCN2SBN4333",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [
                                {
                                    "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                                    "type": "categorisations"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": {
                                "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                },
                {
                    "attributes": {
                        "aliases": [
                            "Second Term"
                        ],
                        'concept': 'https://www.example.com/category-scheme-1/category-term-3',
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The "
                            "contents of this term, and resources it relates to, will not change. \n This term (2) is "
                            "a second level term with a first level term as a parent (1) and a single child term (3)."
                        ],
                        "examples": [
                            "Example category term 2 - example"
                        ],
                        "notation": "1.2",
                        "notes": [
                            "Example category term 2 - note"
                        ],
                        'scheme': 'https://www.example.com/category-scheme-1',
                        "scope-notes": [
                            "Example category term 2 - scope note"
                        ],
                        "title": "Example Category Term: Level 2"
                    },
                    "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": {
                                "id": "01DC6HYAKX5NT8WBYWASQ9ENC8",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                },
                {
                    "attributes": {
                        "acronym": "EXCATSCH1",
                        "description": "This category scheme is used as an example, for demonstration or testing "
                                       "purposes. The terms in this scheme, and resources they relates to, will not "
                                       "change.",
                        "name": "Example Category Scheme 1",
                        "revision": "2019-05-28",
                        "version": "1.0"
                    },
                    "id": "01DC6HYAKXG8FCN63D7DH06W84",
                    "links": {
                        "self": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84"
                    },
                    "relationships": {
                        "categories": {
                            "data": [
                                {
                                    "id": "01DC6HYAKX993ZK6YHCVWAE169",
                                    "type": "categories"
                                },
                                {
                                    "id": "01DC6HYAKX5NT8WBYWASQ9ENC8",
                                    "type": "categories"
                                },
                                {
                                    "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                                    "type": "categories"
                                },
                                {
                                    "id": "01DC6HYAKX53S13HCN2SBN4333",
                                    "type": "categories"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84/categories",
                                "self": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84/relationships/categories"
                            }
                        }
                    },
                    "type": "category-schemes"
                }
            ],
            "links": {
                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/projects/01DB2ECBP24NHYV5KZQG2N3FS2',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response['data'], expected_payload['data'])
        self.assertCountEqual(json_response['included'], expected_payload['included'])
        self.assertDictEqual(json_response['links'], expected_payload['links'])

    def test_projects_single_missing_unknown_id(self):
        error = ApiNotFoundError()
        expected_payload = self.util_prepare_expected_error_payload(error)

        for project_id in ['', 'unknown']:
            with self.subTest(project_id=project_id):
                token = self.util_create_auth_token()
                response = self.client.get(
                    f"/projects/{project_id}",
                    headers={'authorization': f"bearer {token}"},
                    base_url='http://localhost:9000'
                )
                json_response = response.get_json()
                json_response = self.util_prepare_error_response(json_response)
                self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
                self.assertDictEqual(json_response, expected_payload)

    def test_projects_relationship_allocations(self):
        expected_payload = {
            "data": [
                {
                    "id": "01DB2ECBP35AT5WBG092J5GDQ9",
                    "type": "allocations"
                }
            ],
            "links": {
                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/allocations",
                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/allocations"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/allocations',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_projects_relationship_participants(self):
        expected_payload = {
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
                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/participants",
                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/participants"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/participants',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_projects_relationship_categorisations(self):
        expected_payload = {
            "data": [
                {
                    "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                    "type": "categorisations"
                }
            ],
            "links": {
                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/categorisations",
                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/categorisations"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/categorisations',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_projects_allocations(self):
        expected_payload = {
            "data": [
                {
                    "id": "01DB2ECBP35AT5WBG092J5GDQ9",
                    "links": {
                        "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9"
                    },
                    "relationships": {
                        "grant": {
                            "data": {
                                "id": "01DB2ECBP3XQ4B8Z5DW7W963YD",
                                "type": "grants"
                            },
                            "links": {
                                "related": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/grants",
                                "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/relationships/grants"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/projects",
                                "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/relationships/projects"
                            }
                        }
                    },
                    "type": "allocations"
                }
            ],
            "links": {
                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/allocations"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/projects/01DB2ECBP24NHYV5KZQG2N3FS2/allocations',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_projects_participants(self):
        expected_payload = {
            "data": [
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
                        "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01DB2ECBP2MFB0DH3EF3PH74R0",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/people",
                                "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/projects",
                                "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/projects"
                            }
                        }
                    },
                    "type": "participants"
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
                        "self": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01DB2ECBP25PVTVVGT9YT7CKSB",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/people",
                                "self": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/projects",
                                "self": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/relationships/projects"
                            }
                        }
                    },
                    "type": "participants"
                }
            ],
            "links": {
                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/participants"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/projects/01DB2ECBP24NHYV5KZQG2N3FS2/participants',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_projects_categorisations(self):
        expected_payload = {
            "data": [
                {
                    "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                    "links": {
                        "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG"
                    },
                    "relationships": {
                        "category": {
                            "data": {
                                "id": "01DC6HYAKX53S13HCN2SBN4333",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/categories",
                                "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/relationships/categories"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/projects",
                                "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/relationships/projects"
                            }
                        }
                    },
                    "type": "categorisations"
                }
            ],
            "links": {
                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/categorisations"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/projects/01DB2ECBP24NHYV5KZQG2N3FS2/categorisations',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_participants_list(self):
        expected_payload = {
            "data": [
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
                        "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01DB2ECBP2MFB0DH3EF3PH74R0",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/people",
                                "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/projects",
                                "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/projects"
                            }
                        }
                    },
                    "type": "participants"
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
                        "self": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01DB2ECBP25PVTVVGT9YT7CKSB",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/people",
                                "self": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/projects",
                                "self": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/relationships/projects"
                            }
                        }
                    },
                    "type": "participants"
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
                        "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0"
                    },
                    "relationships": {
                        "organisation": {
                            "data": {
                                "id": "01DB2ECBP3WZDP4PES64XKXJ1A",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/organisations",
                                "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/organisations"
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
                                "related": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/participants",
                                "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/participants"
                            }
                        }
                    },
                    "type": "people"
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
                                    "rhoncus lorem pulvinar quis. In felis neque, mollis nec sagittis feugiat, finibus "
                                    "maximus mauris. Nullam varius, risus id scelerisque tempor, justo purus malesuada nulla, "
                                    "eu sagittis purus arcu eget justo. Orci varius natoque penatibus et magnis dis "
                                    "parturient montes, nascetur ridiculus mus. Fusce vel pretium augue. Pellentesque eu "
                                    "semper odio. Suspendisse congue varius est, et euismod justo accumsan sed. Etiam nec "
                                    "scelerisque risus, sed tempus ante. Proin fringilla leo urna, eget pulvinar leo placerat "
                                    "et. \n Etiam mollis lacus ut sapien elementum, sed volutpat dui faucibus. Fusce ligula "
                                    "risus, tempor at justo ac, tincidunt finibus magna. Duis eget sapien et nibh tincidunt "
                                    "faucibus. Duis tempus tincidunt leo. Aenean sit amet cursus ex. Etiam eget finibus "
                                    "nulla, a rutrum turpis. Proin imperdiet, augue consectetur varius varius, lectus elit "
                                    "egestas velit, ullamcorper pulvinar dolor felis at leo. Cras nec est ut est efficitur "
                                    "pulvinar nec vel nisi. Nullam sed elit eu ante finibus volutpat. Nam id diam a urna "
                                    "rutrum dictum. \n Pellentesque habitant morbi tristique senectus et netus et malesuada "
                                    "fames ac turpis egestas. Integer accumsan et mi eu sagittis. Ut id nulla at quam "
                                    "efficitur molestie. Donec viverra ex vitae mauris ullamcorper elementum. Proin sed felis "
                                    "enim. Suspendisse potenti. Integer malesuada interdum mi, ornare semper lorem tempus "
                                    "condimentum. Cras sodales risus quis nibh fermentum volutpat. Sed vel tincidunt lectus.",
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
                        "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/allocations",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/allocations"
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
                                'related': 'http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/categorisations',
                                'self': 'http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/categorisations'
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/participants",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/participants"
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
                        "self": "http://localhost:9000/people/01DB2ECBP25PVTVVGT9YT7CKSB"
                    },
                    "relationships": {
                        "organisation": {
                            "data": {
                                "id": "01DB2ECBP3VF45F1N4XEBF83FE",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9000/people/01DB2ECBP25PVTVVGT9YT7CKSB/organisations",
                                "self": "http://localhost:9000/people/01DB2ECBP25PVTVVGT9YT7CKSB/relationships/organisations"
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
                                "related": "http://localhost:9000/people/01DB2ECBP25PVTVVGT9YT7CKSB/participants",
                                "self": "http://localhost:9000/people/01DB2ECBP25PVTVVGT9YT7CKSB/relationships/participants"
                            }
                        }
                    },
                    "type": "people"
                }
            ],
            "links": {
                "first": "http://localhost:9000/participants?page=1",
                "last": "http://localhost:9000/participants?page=4",
                "next": "http://localhost:9000/participants?page=2",
                "prev": None,
                "self": "http://localhost:9000/participants?page=1"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/participants',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertListEqual(json_response['data'], expected_payload['data'])
        self.assertCountEqual(json_response['included'], expected_payload['included'])
        self.assertDictEqual(json_response['links'], expected_payload['links'])

    def test_participants_detail(self):
        expected_payload = {
            "data": {
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
                    "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF"
                },
                "relationships": {
                    "person": {
                        "data": {
                            "id": "01DB2ECBP2MFB0DH3EF3PH74R0",
                            "type": "people"
                        },
                        "links": {
                            "related": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/people",
                            "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/people"
                        }
                    },
                    "project": {
                        "data": {
                            "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                            "type": "projects"
                        },
                        "links": {
                            "related": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/projects",
                            "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/projects"
                        }
                    }
                },
                "type": "participants"
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
                        "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0"
                    },
                    "relationships": {
                        "organisation": {
                            "data": {
                                "id": "01DB2ECBP3WZDP4PES64XKXJ1A",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/organisations",
                                "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/organisations"
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
                                "related": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/participants",
                                "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/participants"
                            }
                        }
                    },
                    "type": "people"
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
                                    "risus, sed tempus ante. Proin fringilla leo urna, eget pulvinar leo placerat et. \n "
                                    "Etiam mollis lacus ut sapien elementum, sed volutpat dui faucibus. Fusce ligula risus, "
                                    "tempor at justo ac, tincidunt finibus magna. Duis eget sapien et nibh tincidunt faucibus. "
                                    "Duis tempus tincidunt leo. Aenean sit amet cursus ex. Etiam eget finibus nulla, a rutrum "
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
                        "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/allocations",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/allocations"
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
                                'related': 'http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/categorisations',
                                'self': 'http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/categorisations'
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/participants",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
                }
            ],
            "links": {
                "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/participants/01DB2ECBP3622SPB5PS3J8W4XF',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response['data'], expected_payload['data'])
        self.assertCountEqual(json_response['included'], expected_payload['included'])
        self.assertDictEqual(json_response['links'], expected_payload['links'])

    def test_participants_single_missing_unknown_id(self):
        error = ApiNotFoundError()
        expected_payload = self.util_prepare_expected_error_payload(error)

        for participant_id in ['', 'unknown']:
            with self.subTest(participant_id=participant_id):
                token = self.util_create_auth_token()
                response = self.client.get(
                    f"/participants/{participant_id}",
                    headers={'authorization': f"bearer {token}"},
                    base_url='http://localhost:9000'
                )
                json_response = response.get_json()
                json_response = self.util_prepare_error_response(json_response)
                self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
                self.assertDictEqual(json_response, expected_payload)

    def test_participants_relationship_projects(self):
        expected_payload = {
            "data": {
                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                "type": "projects"
            },
            "links": {
                "related": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/projects",
                "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/projects"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/projects',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_participants_relationship_people(self):
        expected_payload = {
            "data": {
                "id": "01DB2ECBP2MFB0DH3EF3PH74R0",
                "type": "people"
            },
            "links": {
                "related": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/people",
                "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/people"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/people',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_participants_projects(self):
        expected_payload = {
            "data": {
                "attributes": {
                    "abstract": "This project is used as an example, for demonstration or testing purposes. The contents of "
                                "this project, and resources it relates to, will not change. \n This example project (1) is a "
                                "project with a single PI and single CoI belonging to the same organisation. It is also "
                                "associated with a single grant and funder. The people, grants and organisations related to "
                                "this project will not be related to another project. This project has an acronym, abstract, "
                                "website and country property. The project duration is in the past. \n The remainder of this "
                                "abstract is padding text to give a realistic abstract length. \n Lorem ipsum dolor sit amet, "
                                "consectetur adipiscing elit. Maecenas eget lorem eleifend turpis vestibulum sollicitudin. "
                                "Curabitur libero nulla, maximus ut facilisis et, maximus quis dolor. Nunc ut malesuada "
                                "felis. Sed volutpat et lectus vitae convallis. Class aptent taciti sociosqu ad litora "
                                "torquent per conubia nostra, per inceptos himenaeos. Fusce ullamcorper nec ante ut "
                                "vulputate. Praesent ultricies mattis dolor quis ultrices. Ut sagittis scelerisque leo "
                                "fringilla malesuada. Donec euismod tincidunt purus vel commodo. \n Aenean volutpat libero "
                                "quis imperdiet tincidunt. Proin iaculis eros at turpis laoreet molestie. Quisque "
                                "pellentesque, lorem id ornare fermentum, nunc urna ultrices libero, eget tempor ipsum "
                                "lectus sollicitudin nibh. Sed sit amet vestibulum nulla. Vivamus dictum, dui id consectetur "
                                "mattis, sapien erat tristique nulla, at lobortis enim nibh eu orci. Curabitur eu purus "
                                "porttitor, rhoncus libero sed, mattis tellus. Praesent ullamcorper tincidunt ex. Vivamus "
                                "lectus urna, dignissim sit amet efficitur a, malesuada at nisi. \n Curabitur auctor ut "
                                "libero ac pharetra. Nunc rutrum facilisis felis, ac rhoncus lorem pulvinar quis. In felis "
                                "neque, mollis nec sagittis feugiat, finibus maximus mauris. Nullam varius, risus id "
                                "scelerisque tempor, justo purus malesuada nulla, eu sagittis purus arcu eget justo. Orci "
                                "varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Fusce "
                                "vel pretium augue. Pellentesque eu semper odio. Suspendisse congue varius est, et euismod "
                                "justo accumsan sed. Etiam nec scelerisque risus, sed tempus ante. Proin fringilla leo urna, "
                                "eget pulvinar leo placerat et. \n Etiam mollis lacus ut sapien elementum, sed volutpat dui "
                                "faucibus. Fusce ligula risus, tempor at justo ac, tincidunt finibus magna. Duis eget sapien "
                                "et nibh tincidunt faucibus. Duis tempus tincidunt leo. Aenean sit amet cursus ex. Etiam "
                                "eget finibus nulla, a rutrum turpis. Proin imperdiet, augue consectetur varius varius, "
                                "lectus elit egestas velit, ullamcorper pulvinar dolor felis at leo. Cras nec est ut est "
                                "efficitur pulvinar nec vel nisi. Nullam sed elit eu ante finibus volutpat. Nam id diam a "
                                "urna rutrum dictum. \n Pellentesque habitant morbi tristique senectus et netus et malesuada "
                                "fames ac turpis egestas. Integer accumsan et mi eu sagittis. Ut id nulla at quam efficitur "
                                "molestie. Donec viverra ex vitae mauris ullamcorper elementum. Proin sed felis enim. "
                                "Suspendisse potenti. Integer malesuada interdum mi, ornare semper lorem tempus condimentum. "
                                "Cras sodales risus quis nibh fermentum volutpat. Sed vel tincidunt lectus.",
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
                    "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2"
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
                            "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/allocations",
                            "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/allocations"
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
                            'related': 'http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/categorisations',
                            'self': 'http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/categorisations'
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
                            "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/participants",
                            "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/participants"
                        }
                    }
                },
                "type": "projects"
            },
            "links": {
                "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/projects"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/participants/01DB2ECBP3622SPB5PS3J8W4XF/projects',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_participants_people(self):
        expected_payload = {
            "data": {
                "attributes": {
                    "avatar-url": "https://cdn.web.bas.ac.uk/bas-registers-service/v1/sample-avatars/conwat/conwat-256.jpg",
                    "first-name": "Constance",
                    "last-name": "Watson",
                    "orcid-id": "https://sandbox.orcid.org/0000-0001-8373-6934"
                },
                "id": "01DB2ECBP2MFB0DH3EF3PH74R0",
                "links": {
                    "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0"
                },
                "relationships": {
                    "organisation": {
                        "data": {
                            "id": "01DB2ECBP3WZDP4PES64XKXJ1A",
                            "type": "organisations"
                        },
                        "links": {
                            "related": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/organisations",
                            "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/organisations"
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
                            "related": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/participants",
                            "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/participants"
                        }
                    }
                },
                "type": "people"
            },
            "links": {
                "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/people"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/participants/01DB2ECBP3622SPB5PS3J8W4XF/people',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_people_list(self):
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
                        "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0"
                    },
                    "relationships": {
                        "organisation": {
                            "data": {
                                "id": "01DB2ECBP3WZDP4PES64XKXJ1A",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/organisations",
                                "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/organisations"
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
                                "related": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/participants",
                                "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/participants"
                            }
                        }
                    },
                    "type": "people"
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
                        "self": "http://localhost:9000/people/01DB2ECBP25PVTVVGT9YT7CKSB"
                    },
                    "relationships": {
                        "organisation": {
                            "data": {
                                "id": "01DB2ECBP3VF45F1N4XEBF83FE",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9000/people/01DB2ECBP25PVTVVGT9YT7CKSB/organisations",
                                "self": "http://localhost:9000/people/01DB2ECBP25PVTVVGT9YT7CKSB/relationships/organisations"
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
                                "related": "http://localhost:9000/people/01DB2ECBP25PVTVVGT9YT7CKSB/participants",
                                "self": "http://localhost:9000/people/01DB2ECBP25PVTVVGT9YT7CKSB/relationships/participants"
                            }
                        }
                    },
                    "type": "people"
                }
            ],
            "included": [
                {
                    "attributes": {
                        "acronym": "EXORG1",
                        "grid-identifier": "XE-EXAMPLE-grid.5500.1",
                        "logo-url": "https://placeimg.com/256/256/arch",
                        "name": "Example Organisation 1",
                        "website": "https://www.example.com"
                    },
                    "id": "01DB2ECBP3WZDP4PES64XKXJ1A",
                    "links": {
                        "self": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A"
                    },
                    "relationships": {
                        "grants": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/grants",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/grants"
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
                                "related": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/people",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/people"
                            }
                        }
                    },
                    "type": "organisations"
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
                        "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01DB2ECBP2MFB0DH3EF3PH74R0",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/people",
                                "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/projects",
                                "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/projects"
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
                        "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/allocations",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/allocations"
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
                                'related': 'http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/categorisations',
                                'self': 'http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/categorisations'
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/participants",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
                },
                {
                    "attributes": {
                        "acronym": None,
                        "grid-identifier": None,
                        "logo-url": None,
                        "name": "Example Organisation 2",
                        "website": None
                    },
                    "id": "01DB2ECBP3VF45F1N4XEBF83FE",
                    "links": {
                        "self": "http://localhost:9000/organisations/01DB2ECBP3VF45F1N4XEBF83FE"
                    },
                    "relationships": {
                        "grants": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/organisations/01DB2ECBP3VF45F1N4XEBF83FE/grants",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3VF45F1N4XEBF83FE/relationships/grants"
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
                                "related": "http://localhost:9000/organisations/01DB2ECBP3VF45F1N4XEBF83FE/people",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3VF45F1N4XEBF83FE/relationships/people"
                            }
                        }
                    },
                    "type": "organisations"
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
                        "self": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01DB2ECBP25PVTVVGT9YT7CKSB",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/people",
                                "self": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/projects",
                                "self": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/relationships/projects"
                            }
                        }
                    },
                    "type": "participants"
                }
            ],
            "links": {
                "first": "http://localhost:9000/people?page=1",
                "last": "http://localhost:9000/people?page=3",
                "next": "http://localhost:9000/people?page=2",
                "prev": None,
                "self": "http://localhost:9000/people?page=1"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/people',
            base_url='http://localhost:9000',
            headers={'authorization': f"bearer {token}"},
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertListEqual(json_response['data'], expected_payload['data'])
        self.assertCountEqual(json_response['included'], expected_payload['included'])
        self.assertDictEqual(json_response['links'], expected_payload['links'])

    def test_people_detail(self):
        expected_payload = {
            "data": {
                "attributes": {
                    "avatar-url": "https://cdn.web.bas.ac.uk/bas-registers-service/v1/sample-avatars/conwat/conwat-256.jpg",
                    "first-name": "Constance",
                    "last-name": "Watson",
                    "orcid-id": "https://sandbox.orcid.org/0000-0001-8373-6934"
                },
                "id": "01DB2ECBP2MFB0DH3EF3PH74R0",
                "links": {
                    "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0"
                },
                "relationships": {
                    "organisation": {
                        "data": {
                            "id": "01DB2ECBP3WZDP4PES64XKXJ1A",
                            "type": "organisations"
                        },
                        "links": {
                            "related": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/organisations",
                            "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/organisations"
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
                            "related": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/participants",
                            "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/participants"
                        }
                    }
                },
                "type": "people"
            },
            "included": [
                {
                    "attributes": {
                        "acronym": "EXORG1",
                        "grid-identifier": "XE-EXAMPLE-grid.5500.1",
                        "logo-url": "https://placeimg.com/256/256/arch",
                        "name": "Example Organisation 1",
                        "website": "https://www.example.com"
                    },
                    "id": "01DB2ECBP3WZDP4PES64XKXJ1A",
                    "links": {
                        "self": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A"
                    },
                    "relationships": {
                        "grants": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/grants",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/grants"
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
                                "related": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/people",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/people"
                            }
                        }
                    },
                    "type": "organisations"
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
                        "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01DB2ECBP2MFB0DH3EF3PH74R0",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/people",
                                "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/projects",
                                "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/projects"
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
                        "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/allocations",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/allocations"
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
                                'related': 'http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/categorisations',
                                'self': 'http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/categorisations'
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/participants",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
                }
            ],
            "links": {
                "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/people/01DB2ECBP2MFB0DH3EF3PH74R0',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response['data'], expected_payload['data'])
        self.assertCountEqual(json_response['included'], expected_payload['included'])
        self.assertDictEqual(json_response['links'], expected_payload['links'])

    def test_people_single_missing_unknown_id(self):
        error = ApiNotFoundError()
        expected_payload = self.util_prepare_expected_error_payload(error)

        for person_id in ['', 'unknown']:
            with self.subTest(person_id=person_id):
                token = self.util_create_auth_token()
                response = self.client.get(
                    f"/people/{person_id}",
                    base_url='http://localhost:9000',
                    headers={'authorization': f"bearer {token}"},
                )
                json_response = response.get_json()
                json_response = self.util_prepare_error_response(json_response)
                self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
                self.assertDictEqual(json_response, expected_payload)

    def test_people_relationship_organisations(self):
        expected_payload = {
            "data": {
                "id": "01DB2ECBP3WZDP4PES64XKXJ1A",
                "type": "organisations"
            },
            "links": {
                "related": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/organisations",
                "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/organisations"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/organisations',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_people_relationship_participants(self):
        expected_payload = {
            "data": [
                {
                    "id": "01DB2ECBP3622SPB5PS3J8W4XF",
                    "type": "participants"
                }
            ],
            "links": {
                "related": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/participants",
                "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/participants"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/participants',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_people_participants(self):
        expected_payload = {
            "data": [
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
                        "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01DB2ECBP2MFB0DH3EF3PH74R0",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/people",
                                "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/projects",
                                "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/projects"
                            }
                        }
                    },
                    "type": "participants"
                }
            ],
            "links": {
                "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/participants"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/people/01DB2ECBP2MFB0DH3EF3PH74R0/participants',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_people_organisations(self):
        expected_payload = {
            "data": {
                "attributes": {
                    "acronym": "EXORG1",
                    "grid-identifier": "XE-EXAMPLE-grid.5500.1",
                    "logo-url": "https://placeimg.com/256/256/arch",
                    "name": "Example Organisation 1",
                    "website": "https://www.example.com"
                },
                "id": "01DB2ECBP3WZDP4PES64XKXJ1A",
                "links": {
                    "self": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A"
                },
                "relationships": {
                    "grants": {
                        "data": [],
                        "links": {
                            "related": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/grants",
                            "self": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/grants"
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
                            "related": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/people",
                            "self": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/people"
                        }
                    }
                },
                "type": "organisations"
            },
            "links": {
                "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/organisations"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/people/01DB2ECBP2MFB0DH3EF3PH74R0/organisations',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_grants_list(self):
        expected_payload = {
            "data": [
                {
                    "attributes": {
                        "abstract": "This grant is used as an example, for demonstration or testing purposes. The contents of "
                                    "this grant, and resources it relates to, will not change. \n This example grant (1) is a "
                                    "grant with a single project and funder. The project and organisations related to this "
                                    "grant will not be related to another grant. This grant has an abstract, website and "
                                    "publications. The grant is closed and occurs in the past. \n The remainder of this "
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
                        "duration": {
                            "end-instant": "2015-10-01",
                            "interval": "2012-03-01/2015-10-01",
                            "start-instant": "2012-03-01"
                        },
                        "publications": [
                            "https://doi.org/10.5555/15822411",
                            "https://doi.org/10.5555/45284431",
                            "https://doi.org/10.5555/59959290"
                        ],
                        "reference": "EX-GRANT-0001",
                        "status": "closed",
                        "title": "Example grant 1",
                        "total-funds": {
                            "currency": {
                                "iso-4217-code": "GBP",
                                "major-symbol": "\u00a3"
                            },
                            "value": 120000.00
                        },
                        "website": "https://www.example.com"
                    },
                    "id": "01DB2ECBP3XQ4B8Z5DW7W963YD",
                    "links": {
                        "self": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD"
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
                                "related": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/allocations",
                                "self": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/relationships/allocations"
                            }
                        },
                        "funder": {
                            "data": {
                                "id": "01DB2ECBP3A13RJ6QEZFN26ZEP",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/organisations",
                                "self": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/relationships/organisations"
                            }
                        }
                    },
                    "type": "grants"
                },
                {
                    "attributes": {
                        "abstract": "This grant is used as an example, for demonstration or testing purposes. The "
                                    "contents of this grant, and resources it relates to, will not change. \n This "
                                    "example grant (2) is a grant with a single project and funder. The project and "
                                    "organisations related to this grant will also relate to other grants. This grant "
                                    "does not have a website, publications or total funding amount. The grant is "
                                    "active and occurs in the present. \n No padding text is added to this abstract.",
                        "duration": {
                            "end-instant": "2055-10-01",
                            "interval": "2012-03-01/2055-10-01",
                            "start-instant": "2012-03-01"
                        },
                        "publications": None,
                        "reference": "EX-GRANT-0002",
                        "status": "active",
                        "title": "Example grant 2",
                        "total-funds": None,
                        "website": None
                    },
                    "id": "01DB2ECBP3DJ512HM1409ZNDHW",
                    "links": {
                        "self": "http://localhost:9000/grants/01DB2ECBP3DJ512HM1409ZNDHW"
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
                                "related": "http://localhost:9000/grants/01DB2ECBP3DJ512HM1409ZNDHW/allocations",
                                "self": "http://localhost:9000/grants/01DB2ECBP3DJ512HM1409ZNDHW/relationships/allocations"
                            }
                        },
                        "funder": {
                            "data": {
                                "id": "01DB2ECBP3YQE4394T0Q97TPP2",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9000/grants/01DB2ECBP3DJ512HM1409ZNDHW/organisations",
                                "self": "http://localhost:9000/grants/01DB2ECBP3DJ512HM1409ZNDHW/relationships/organisations"
                            }
                        }
                    },
                    "type": "grants"
                }
            ],
            "included": [
                {
                    "id": "01DB2ECBP35AT5WBG092J5GDQ9",
                    "links": {
                        "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9"
                    },
                    "relationships": {
                        "grant": {
                            "data": {
                                "id": "01DB2ECBP3XQ4B8Z5DW7W963YD",
                                "type": "grants"
                            },
                            "links": {
                                "related": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/grants",
                                "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/relationships/grants"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/projects",
                                "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/relationships/projects"
                            }
                        }
                    },
                    "type": "allocations"
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
                                    "risus, sed tempus ante. Proin fringilla leo urna, eget pulvinar leo placerat et. \n "
                                    "Etiam mollis lacus ut sapien elementum, sed volutpat dui faucibus. Fusce ligula risus, "
                                    "tempor at justo ac, tincidunt finibus magna. Duis eget sapien et nibh tincidunt faucibus. "
                                    "Duis tempus tincidunt leo. Aenean sit amet cursus ex. Etiam eget finibus nulla, a rutrum "
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
                        "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/allocations",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/allocations"
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
                                'related': 'http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/categorisations',
                                'self': 'http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/categorisations'
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/participants",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
                },
                {
                    "attributes": {
                        "acronym": "EXFUNDORG1",
                        "grid-identifier": "XE-EXAMPLE-grid.5501.1",
                        "logo-url": "https://placeimg.com/256/256/arch",
                        "name": "Example Funder Organisation 1",
                        "website": "https://www.example.com"
                    },
                    "id": "01DB2ECBP3A13RJ6QEZFN26ZEP",
                    "links": {
                        "self": "http://localhost:9000/organisations/01DB2ECBP3A13RJ6QEZFN26ZEP"
                    },
                    "relationships": {
                        "grants": {
                            "data": [
                                {
                                    "id": "01DB2ECBP3XQ4B8Z5DW7W963YD",
                                    "type": "grants"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/organisations/01DB2ECBP3A13RJ6QEZFN26ZEP/grants",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3A13RJ6QEZFN26ZEP/relationships/grants"
                            }
                        },
                        "people": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/organisations/01DB2ECBP3A13RJ6QEZFN26ZEP/people",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3A13RJ6QEZFN26ZEP/relationships/people"
                            }
                        }
                    },
                    "type": "organisations"
                },
                {
                    "id": "01DB2ECBP355B1K0573GPN851M",
                    "links": {
                        "self": "http://localhost:9000/allocations/01DB2ECBP355B1K0573GPN851M"
                    },
                    "relationships": {
                        "grant": {
                            "data": {
                                "id": "01DB2ECBP3DJ512HM1409ZNDHW",
                                "type": "grants"
                            },
                            "links": {
                                "related": "http://localhost:9000/allocations/01DB2ECBP355B1K0573GPN851M/grants",
                                "self": "http://localhost:9000/allocations/01DB2ECBP355B1K0573GPN851M/relationships/grants"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP2DXX8VN7S7AYJBGBT",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/allocations/01DB2ECBP355B1K0573GPN851M/projects",
                                "self": "http://localhost:9000/allocations/01DB2ECBP355B1K0573GPN851M/relationships/projects"
                            }
                        }
                    },
                    "type": "allocations"
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
                        "self": "http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/allocations",
                                "self": "http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/relationships/allocations"
                            }
                        },
                        'categorisations': {
                            'data': [],
                            'links': {
                                'related': 'http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/categorisations',
                                'self': 'http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/relationships/categorisations'
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
                                "related": "http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/participants",
                                "self": "http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
                },
                {
                    "attributes": {
                        "acronym": "EXFUNDORG2",
                        "grid-identifier": "XE-EXAMPLE-grid.5501.2",
                        "logo-url": "https://placeimg.com/256/256/arch",
                        "name": "Example Funder Organisation 2",
                        "website": "https://www.example.com"
                    },
                    "id": "01DB2ECBP3YQE4394T0Q97TPP2",
                    "links": {
                        "self": "http://localhost:9000/organisations/01DB2ECBP3YQE4394T0Q97TPP2"
                    },
                    "relationships": {
                        "grants": {
                            "data": [
                                {
                                    "id": "01DB2ECBP3DJ512HM1409ZNDHW",
                                    "type": "grants"
                                },
                                {
                                    "id": "01DB2ECBP3S0PJ4PND3XTVGX25",
                                    "type": "grants"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/organisations/01DB2ECBP3YQE4394T0Q97TPP2/grants",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3YQE4394T0Q97TPP2/relationships/grants"
                            }
                        },
                        "people": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/organisations/01DB2ECBP3YQE4394T0Q97TPP2/people",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3YQE4394T0Q97TPP2/relationships/people"
                            }
                        }
                    },
                    "type": "organisations"
                }
            ],
            "links": {
                "first": "http://localhost:9000/grants?page=1",
                "last": "http://localhost:9000/grants?page=2",
                "next": "http://localhost:9000/grants?page=2",
                "prev": None,
                "self": "http://localhost:9000/grants?page=1"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/grants',
            base_url='http://localhost:9000',
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

    def test_grants_detail(self):
        expected_payload = {
            "data": {
                "attributes": {
                    "abstract": "This grant is used as an example, for demonstration or testing purposes. The contents of "
                                "this grant, and resources it relates to, will not change. \n This example grant (1) is a "
                                "grant with a single project and funder. The project and organisations related to this grant "
                                "will not be related to another grant. This grant has an abstract, website and publications. "
                                "The grant is closed and occurs in the past. \n The remainder of this abstract is padding "
                                "text to give a realistic abstract length. \n Lorem ipsum dolor sit amet, consectetur "
                                "adipiscing elit. Maecenas eget lorem eleifend turpis vestibulum sollicitudin. Curabitur "
                                "libero nulla, maximus ut facilisis et, maximus quis dolor. Nunc ut malesuada felis. Sed "
                                "volutpat et lectus vitae convallis. Class aptent taciti sociosqu ad litora torquent per "
                                "conubia nostra, per inceptos himenaeos. Fusce ullamcorper nec ante ut vulputate. Praesent "
                                "ultricies mattis dolor quis ultrices. Ut sagittis scelerisque leo fringilla malesuada. "
                                "Donec euismod tincidunt purus vel commodo. \n Aenean volutpat libero quis imperdiet "
                                "tincidunt. Proin iaculis eros at turpis laoreet molestie. Quisque pellentesque, lorem id "
                                "ornare fermentum, nunc urna ultrices libero, eget tempor ipsum lectus sollicitudin nibh. "
                                "Sed sit amet vestibulum nulla. Vivamus dictum, dui id consectetur mattis, sapien erat "
                                "tristique nulla, at lobortis enim nibh eu orci. Curabitur eu purus porttitor, rhoncus "
                                "libero sed, mattis tellus. Praesent ullamcorper tincidunt ex. Vivamus lectus urna, "
                                "dignissim sit amet efficitur a, malesuada at nisi. \n Curabitur auctor ut libero ac "
                                "pharetra. Nunc rutrum facilisis felis, ac rhoncus lorem pulvinar quis. In felis neque, "
                                "mollis nec sagittis feugiat, finibus maximus mauris. Nullam varius, risus id scelerisque "
                                "tempor, justo purus malesuada nulla, eu sagittis purus arcu eget justo. Orci varius "
                                "natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Fusce vel "
                                "pretium augue. Pellentesque eu semper odio. Suspendisse congue varius est, et euismod "
                                "justo accumsan sed. Etiam nec scelerisque risus, sed tempus ante. Proin fringilla leo urna, "
                                "eget pulvinar leo placerat et. \n Etiam mollis lacus ut sapien elementum, sed volutpat dui "
                                "faucibus. Fusce ligula risus, tempor at justo ac, tincidunt finibus magna. Duis eget sapien "
                                "et nibh tincidunt faucibus. Duis tempus tincidunt leo. Aenean sit amet cursus ex. Etiam "
                                "eget finibus nulla, a rutrum turpis. Proin imperdiet, augue consectetur varius varius, "
                                "lectus elit egestas velit, ullamcorper pulvinar dolor felis at leo. Cras nec est ut est "
                                "efficitur pulvinar nec vel nisi. Nullam sed elit eu ante finibus volutpat. Nam id diam a "
                                "urna rutrum dictum. \n Pellentesque habitant morbi tristique senectus et netus et malesuada "
                                "fames ac turpis egestas. Integer accumsan et mi eu sagittis. Ut id nulla at quam efficitur "
                                "molestie. Donec viverra ex vitae mauris ullamcorper elementum. Proin sed felis enim. "
                                "Suspendisse potenti. Integer malesuada interdum mi, ornare semper lorem tempus condimentum. "
                                "Cras sodales risus quis nibh fermentum volutpat. Sed vel tincidunt lectus.",
                    "duration": {
                        "end-instant": "2015-10-01",
                        "interval": "2012-03-01/2015-10-01",
                        "start-instant": "2012-03-01"
                    },
                    "publications": [
                        "https://doi.org/10.5555/15822411",
                        "https://doi.org/10.5555/45284431",
                        "https://doi.org/10.5555/59959290"
                    ],
                    "reference": "EX-GRANT-0001",
                    "status": "closed",
                    "title": "Example grant 1",
                    "total-funds": {
                        "currency": {
                            "iso-4217-code": "GBP",
                            "major-symbol": "\u00a3"
                        },
                        "value": 120000.00
                    },
                    "website": "https://www.example.com"
                },
                "id": "01DB2ECBP3XQ4B8Z5DW7W963YD",
                "links": {
                    "self": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD"
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
                            "related": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/allocations",
                            "self": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/relationships/allocations"
                        }
                    },
                    "funder": {
                        "data": {
                            "id": "01DB2ECBP3A13RJ6QEZFN26ZEP",
                            "type": "organisations"
                        },
                        "links": {
                            "related": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/organisations",
                            "self": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/relationships/organisations"
                        }
                    }
                },
                "type": "grants"
            },
            "included": [
                {
                    "id": "01DB2ECBP35AT5WBG092J5GDQ9",
                    "links": {
                        "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9"
                    },
                    "relationships": {
                        "grant": {
                            "data": {
                                "id": "01DB2ECBP3XQ4B8Z5DW7W963YD",
                                "type": "grants"
                            },
                            "links": {
                                "related": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/grants",
                                "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/relationships/grants"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/projects",
                                "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/relationships/projects"
                            }
                        }
                    },
                    "type": "allocations"
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
                                    "is padding text to give a realistic abstract length. \n Lorem ipsum dolor sit amet, "
                                    "consectetur adipiscing elit. Maecenas eget lorem eleifend turpis vestibulum "
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
                        "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/allocations",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/allocations"
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
                                'related': 'http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/categorisations',
                                'self': 'http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/categorisations'
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/participants",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
                },
                {
                    "attributes": {
                        "acronym": "EXFUNDORG1",
                        "grid-identifier": "XE-EXAMPLE-grid.5501.1",
                        "logo-url": "https://placeimg.com/256/256/arch",
                        "name": "Example Funder Organisation 1",
                        "website": "https://www.example.com"
                    },
                    "id": "01DB2ECBP3A13RJ6QEZFN26ZEP",
                    "links": {
                        "self": "http://localhost:9000/organisations/01DB2ECBP3A13RJ6QEZFN26ZEP"
                    },
                    "relationships": {
                        "grants": {
                            "data": [
                                {
                                    "id": "01DB2ECBP3XQ4B8Z5DW7W963YD",
                                    "type": "grants"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/organisations/01DB2ECBP3A13RJ6QEZFN26ZEP/grants",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3A13RJ6QEZFN26ZEP/relationships/grants"
                            }
                        },
                        "people": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/organisations/01DB2ECBP3A13RJ6QEZFN26ZEP/people",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3A13RJ6QEZFN26ZEP/relationships/people"
                            }
                        }
                    },
                    "type": "organisations"
                }
            ],
            "links": {
                "self": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/grants/01DB2ECBP3XQ4B8Z5DW7W963YD',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response['data'], expected_payload['data'])
        self.assertCountEqual(json_response['included'], expected_payload['included'])
        self.assertDictEqual(json_response['links'], expected_payload['links'])

    def test_grants_single_missing_unknown_id(self):
        error = ApiNotFoundError()
        expected_payload = self.util_prepare_expected_error_payload(error)

        for grant_id in ['', 'unknown']:
            with self.subTest(grant_id=grant_id):
                token = self.util_create_auth_token()
                response = self.client.get(
                    f"/grants/{grant_id}",
                    headers={'authorization': f"bearer {token}"},
                    base_url='http://localhost:9000'
                )
                json_response = response.get_json()
                json_response = self.util_prepare_error_response(json_response)
                self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
                self.assertDictEqual(json_response, expected_payload)

    def test_grants_relationship_allocations(self):
        expected_payload = {
            "data": [
                {
                    "id": "01DB2ECBP35AT5WBG092J5GDQ9",
                    "type": "allocations"
                }
            ],
            "links": {
                "related": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/allocations",
                "self": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/relationships/allocations"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/relationships/allocations',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_grants_relationship_organisations(self):
        expected_payload = {
            "data": {
                "id": "01DB2ECBP3A13RJ6QEZFN26ZEP",
                "type": "organisations"
            },
            "links": {
                "related": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/organisations",
                "self": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/relationships/organisations"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/relationships/organisations',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_grants_allocations(self):
        expected_payload = {
            "data": [
                {
                    "id": "01DB2ECBP35AT5WBG092J5GDQ9",
                    "links": {
                        "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9"
                    },
                    "relationships": {
                        "grant": {
                            "data": {
                                "id": "01DB2ECBP3XQ4B8Z5DW7W963YD",
                                "type": "grants"
                            },
                            "links": {
                                "related": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/grants",
                                "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/relationships/grants"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/projects",
                                "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/relationships/projects"
                            }
                        }
                    },
                    "type": "allocations"
                }
            ],
            "links": {
                "self": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/allocations"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/allocations',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_grants_organisations(self):
        expected_payload = {
            "data": {
                "attributes": {
                    "acronym": "EXFUNDORG1",
                    "grid-identifier": "XE-EXAMPLE-grid.5501.1",
                    "logo-url": "https://placeimg.com/256/256/arch",
                    "name": "Example Funder Organisation 1",
                    "website": "https://www.example.com"
                },
                "id": "01DB2ECBP3A13RJ6QEZFN26ZEP",
                "links": {
                    "self": "http://localhost:9000/organisations/01DB2ECBP3A13RJ6QEZFN26ZEP"
                },
                "relationships": {
                    "grants": {
                        "data": [
                            {
                                "id": "01DB2ECBP3XQ4B8Z5DW7W963YD",
                                "type": "grants"
                            }
                        ],
                        "links": {
                            "related": "http://localhost:9000/organisations/01DB2ECBP3A13RJ6QEZFN26ZEP/grants",
                            "self": "http://localhost:9000/organisations/01DB2ECBP3A13RJ6QEZFN26ZEP/relationships/grants"
                        }
                    },
                    "people": {
                        "data": [],
                        "links": {
                            "related": "http://localhost:9000/organisations/01DB2ECBP3A13RJ6QEZFN26ZEP/people",
                            "self": "http://localhost:9000/organisations/01DB2ECBP3A13RJ6QEZFN26ZEP/relationships/people"
                        }
                    }
                },
                "type": "organisations"
            },
            "links": {
                "self": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/organisations"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/organisations',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_allocations_list(self):
        expected_payload = {
            "data": [
                {
                    "id": "01DB2ECBP35AT5WBG092J5GDQ9",
                    "links": {
                        "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9"
                    },
                    "relationships": {
                        "grant": {
                            "data": {
                                "id": "01DB2ECBP3XQ4B8Z5DW7W963YD",
                                "type": "grants"
                            },
                            "links": {
                                "related": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/grants",
                                "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/relationships/grants"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/projects",
                                "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/relationships/projects"
                            }
                        }
                    },
                    "type": "allocations"
                },
                {
                    "id": "01DB2ECBP355B1K0573GPN851M",
                    "links": {
                        "self": "http://localhost:9000/allocations/01DB2ECBP355B1K0573GPN851M"
                    },
                    "relationships": {
                        "grant": {
                            "data": {
                                "id": "01DB2ECBP3DJ512HM1409ZNDHW",
                                "type": "grants"
                            },
                            "links": {
                                "related": "http://localhost:9000/allocations/01DB2ECBP355B1K0573GPN851M/grants",
                                "self": "http://localhost:9000/allocations/01DB2ECBP355B1K0573GPN851M/relationships/grants"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP2DXX8VN7S7AYJBGBT",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/allocations/01DB2ECBP355B1K0573GPN851M/projects",
                                "self": "http://localhost:9000/allocations/01DB2ECBP355B1K0573GPN851M/relationships/projects"
                            }
                        }
                    },
                    "type": "allocations"
                }
            ],
            "included": [
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
                        "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/allocations",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/allocations"
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
                                'related': 'http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/categorisations',
                                'self': 'http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/categorisations'
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/participants",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
                },
                {
                    "attributes": {
                        "abstract": "This grant is used as an example, for demonstration or testing purposes. The contents of "
                                    "this grant, and resources it relates to, will not change. \n This example grant (1) is a "
                                    "grant with a single project and funder. The project and organisations related to this "
                                    "grant will not be related to another grant. This grant has an abstract, website and "
                                    "publications. The grant is closed and occurs in the past. \n The remainder of this "
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
                        "duration": {
                            "end-instant": "2015-10-01",
                            "interval": "2012-03-01/2015-10-01",
                            "start-instant": "2012-03-01"
                        },
                        "publications": [
                            "https://doi.org/10.5555/15822411",
                            "https://doi.org/10.5555/45284431",
                            "https://doi.org/10.5555/59959290"
                        ],
                        "reference": "EX-GRANT-0001",
                        "status": "closed",
                        "title": "Example grant 1",
                        "total-funds": {
                            "currency": {
                                "iso-4217-code": "GBP",
                                "major-symbol": "\u00a3"
                            },
                            "value": 120000.00
                        },
                        "website": "https://www.example.com"
                    },
                    "id": "01DB2ECBP3XQ4B8Z5DW7W963YD",
                    "links": {
                        "self": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD"
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
                                "related": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/allocations",
                                "self": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/relationships/allocations"
                            }
                        },
                        "funder": {
                            "data": {
                                "id": "01DB2ECBP3A13RJ6QEZFN26ZEP",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/organisations",
                                "self": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/relationships/organisations"
                            }
                        }
                    },
                    "type": "grants"
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
                        "self": "http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/allocations",
                                "self": "http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/relationships/allocations"
                            }
                        },
                        'categorisations': {
                            'data': [],
                            'links': {
                                'related': 'http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/categorisations',
                                'self': 'http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/relationships/categorisations'
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
                                "related": "http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/participants",
                                "self": "http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
                },
                {
                    "attributes": {
                        "abstract": "This grant is used as an example, for demonstration or testing purposes. The contents of "
                                    "this grant, and resources it relates to, will not change. \n This example grant (2) is a "
                                    "grant with a single project and funder. The project and organisations related to this "
                                    "grant will also relate to other grants. This grant does not have a website, publications "
                                    "or total funding amount. The grant is active and occurs in the present. \n No padding "
                                    "text is added to this abstract.",
                        "duration": {
                            "end-instant": "2055-10-01",
                            "interval": "2012-03-01/2055-10-01",
                            "start-instant": "2012-03-01"
                        },
                        "publications": None,
                        "reference": "EX-GRANT-0002",
                        "status": "active",
                        "title": "Example grant 2",
                        "total-funds": None,
                        "website": None
                    },
                    "id": "01DB2ECBP3DJ512HM1409ZNDHW",
                    "links": {
                        "self": "http://localhost:9000/grants/01DB2ECBP3DJ512HM1409ZNDHW"
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
                                "related": "http://localhost:9000/grants/01DB2ECBP3DJ512HM1409ZNDHW/allocations",
                                "self": "http://localhost:9000/grants/01DB2ECBP3DJ512HM1409ZNDHW/relationships/allocations"
                            }
                        },
                        "funder": {
                            "data": {
                                "id": "01DB2ECBP3YQE4394T0Q97TPP2",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9000/grants/01DB2ECBP3DJ512HM1409ZNDHW/organisations",
                                "self": "http://localhost:9000/grants/01DB2ECBP3DJ512HM1409ZNDHW/relationships/organisations"
                            }
                        }
                    },
                    "type": "grants"
                }
            ],
            "links": {
                "first": "http://localhost:9000/allocations?page=1",
                "last": "http://localhost:9000/allocations?page=2",
                "next": "http://localhost:9000/allocations?page=2",
                "prev": None,
                "self": "http://localhost:9000/allocations?page=1"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/allocations',
            base_url='http://localhost:9000',
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

    def test_allocations_detail(self):
        expected_payload = {
            "data": {
                "id": "01DB2ECBP35AT5WBG092J5GDQ9",
                "links": {
                    "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9"
                },
                "relationships": {
                    "grant": {
                        "data": {
                            "id": "01DB2ECBP3XQ4B8Z5DW7W963YD",
                            "type": "grants"
                        },
                        "links": {
                            "related": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/grants",
                            "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/relationships/grants"
                        }
                    },
                    "project": {
                        "data": {
                            "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                            "type": "projects"
                        },
                        "links": {
                            "related": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/projects",
                            "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/relationships/projects"
                        }
                    }
                },
                "type": "allocations"
            },
            "included": [
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
                        "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/allocations",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/allocations"
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
                                'related': 'http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/categorisations',
                                'self': 'http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/categorisations'
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/participants",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
                },
                {
                    "attributes": {
                        "abstract": "This grant is used as an example, for demonstration or testing purposes. The contents of "
                                    "this grant, and resources it relates to, will not change. \n This example grant (1) is a "
                                    "grant with a single project and funder. The project and organisations related to this "
                                    "grant will not be related to another grant. This grant has an abstract, website and "
                                    "publications. The grant is closed and occurs in the past. \n The remainder of this "
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
                        "duration": {
                            "end-instant": "2015-10-01",
                            "interval": "2012-03-01/2015-10-01",
                            "start-instant": "2012-03-01"
                        },
                        "publications": [
                            "https://doi.org/10.5555/15822411",
                            "https://doi.org/10.5555/45284431",
                            "https://doi.org/10.5555/59959290"
                        ],
                        "reference": "EX-GRANT-0001",
                        "status": "closed",
                        "title": "Example grant 1",
                        "total-funds": {
                            "currency": {
                                "iso-4217-code": "GBP",
                                "major-symbol": "\u00a3"
                            },
                            "value": 120000.00
                        },
                        "website": "https://www.example.com"
                    },
                    "id": "01DB2ECBP3XQ4B8Z5DW7W963YD",
                    "links": {
                        "self": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD"
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
                                "related": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/allocations",
                                "self": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/relationships/allocations"
                            }
                        },
                        "funder": {
                            "data": {
                                "id": "01DB2ECBP3A13RJ6QEZFN26ZEP",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/organisations",
                                "self": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/relationships/organisations"
                            }
                        }
                    },
                    "type": "grants"
                }
            ],
            "links": {
                "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/allocations/01DB2ECBP35AT5WBG092J5GDQ9',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response['data'], expected_payload['data'])
        self.assertCountEqual(json_response['included'], expected_payload['included'])
        self.assertDictEqual(json_response['links'], expected_payload['links'])

    def test_allocations_single_missing_unknown_id(self):
        error = ApiNotFoundError()
        expected_payload = self.util_prepare_expected_error_payload(error)

        for allocation_id in ['', 'unknown']:
            with self.subTest(allocation_id=allocation_id):
                token = self.util_create_auth_token()
                response = self.client.get(
                    f"/allocations/{allocation_id}",
                    headers={'authorization': f"bearer {token}"},
                    base_url='http://localhost:9000'
                )
                json_response = response.get_json()
                json_response = self.util_prepare_error_response(json_response)
                self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
                self.assertDictEqual(json_response, expected_payload)

    def test_allocations_relationship_grants(self):
        expected_payload = {
            "data": {
                "id": "01DB2ECBP3XQ4B8Z5DW7W963YD",
                "type": "grants"
            },
            "links": {
                "related": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/grants",
                "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/relationships/grants"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/allocations/01DB2ECBP35AT5WBG092J5GDQ9/relationships/grants',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_allocations_relationship_projects(self):
        expected_payload = {
            "data": {
                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                "type": "projects"
            },
            "links": {
                "related": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/projects",
                "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/relationships/projects"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/allocations/01DB2ECBP35AT5WBG092J5GDQ9/relationships/projects',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_allocations_grants(self):
        expected_payload = {
            "data": {
                "attributes": {
                    "abstract": "This grant is used as an example, for demonstration or testing purposes. The contents of "
                                "this grant, and resources it relates to, will not change. \n This example grant (1) is a "
                                "grant with a single project and funder. The project and organisations related to this grant "
                                "will not be related to another grant. This grant has an abstract, website and publications. "
                                "The grant is closed and occurs in the past. \n The remainder of this abstract is padding "
                                "text to give a realistic abstract length. \n Lorem ipsum dolor sit amet, consectetur "
                                "adipiscing elit. Maecenas eget lorem eleifend turpis vestibulum sollicitudin. Curabitur "
                                "libero nulla, maximus ut facilisis et, maximus quis dolor. Nunc ut malesuada felis. Sed "
                                "volutpat et lectus vitae convallis. Class aptent taciti sociosqu ad litora torquent per "
                                "conubia nostra, per inceptos himenaeos. Fusce ullamcorper nec ante ut vulputate. Praesent "
                                "ultricies mattis dolor quis ultrices. Ut sagittis scelerisque leo fringilla malesuada. "
                                "Donec euismod tincidunt purus vel commodo. \n Aenean volutpat libero quis imperdiet "
                                "tincidunt. Proin iaculis eros at turpis laoreet molestie. Quisque pellentesque, lorem id "
                                "ornare fermentum, nunc urna ultrices libero, eget tempor ipsum lectus sollicitudin nibh. "
                                "Sed sit amet vestibulum nulla. Vivamus dictum, dui id consectetur mattis, sapien erat "
                                "tristique nulla, at lobortis enim nibh eu orci. Curabitur eu purus porttitor, rhoncus "
                                "libero sed, mattis tellus. Praesent ullamcorper tincidunt ex. Vivamus lectus urna, "
                                "dignissim sit amet efficitur a, malesuada at nisi. \n Curabitur auctor ut libero ac "
                                "pharetra. Nunc rutrum facilisis felis, ac rhoncus lorem pulvinar quis. In felis neque, "
                                "mollis nec sagittis feugiat, finibus maximus mauris. Nullam varius, risus id scelerisque "
                                "tempor, justo purus malesuada nulla, eu sagittis purus arcu eget justo. Orci varius natoque "
                                "penatibus et magnis dis parturient montes, nascetur ridiculus mus. Fusce vel pretium augue. "
                                "Pellentesque eu semper odio. Suspendisse congue varius est, et euismod justo accumsan sed. "
                                "Etiam nec scelerisque risus, sed tempus ante. Proin fringilla leo urna, eget pulvinar leo "
                                "placerat et. \n Etiam mollis lacus ut sapien elementum, sed volutpat dui faucibus. Fusce "
                                "ligula risus, tempor at justo ac, tincidunt finibus magna. Duis eget sapien et nibh "
                                "tincidunt faucibus. Duis tempus tincidunt leo. Aenean sit amet cursus ex. Etiam eget "
                                "finibus nulla, a rutrum turpis. Proin imperdiet, augue consectetur varius varius, lectus "
                                "elit egestas velit, ullamcorper pulvinar dolor felis at leo. Cras nec est ut est efficitur "
                                "pulvinar nec vel nisi. Nullam sed elit eu ante finibus volutpat. Nam id diam a urna rutrum "
                                "dictum. \n Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac "
                                "turpis egestas. Integer accumsan et mi eu sagittis. Ut id nulla at quam efficitur molestie. "
                                "Donec viverra ex vitae mauris ullamcorper elementum. Proin sed felis enim. Suspendisse "
                                "potenti. Integer malesuada interdum mi, ornare semper lorem tempus condimentum. Cras "
                                "sodales risus quis nibh fermentum volutpat. Sed vel tincidunt lectus.",
                    "duration": {
                        "end-instant": "2015-10-01",
                        "interval": "2012-03-01/2015-10-01",
                        "start-instant": "2012-03-01"
                    },
                    "publications": [
                        "https://doi.org/10.5555/15822411",
                        "https://doi.org/10.5555/45284431",
                        "https://doi.org/10.5555/59959290"
                    ],
                    "reference": "EX-GRANT-0001",
                    "status": "closed",
                    "title": "Example grant 1",
                    "total-funds": {
                        "currency": {
                            "iso-4217-code": "GBP",
                            "major-symbol": "\u00a3"
                        },
                        "value": 120000.00
                    },
                    "website": "https://www.example.com"
                },
                "id": "01DB2ECBP3XQ4B8Z5DW7W963YD",
                "links": {
                    "self": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD"
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
                            "related": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/allocations",
                            "self": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/relationships/allocations"
                        }
                    },
                    "funder": {
                        "data": {
                            "id": "01DB2ECBP3A13RJ6QEZFN26ZEP",
                            "type": "organisations"
                        },
                        "links": {
                            "related": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/organisations",
                            "self": "http://localhost:9000/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/relationships/organisations"
                        }
                    }
                },
                "type": "grants"
            },
            "links": {
                "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/grants"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/allocations/01DB2ECBP35AT5WBG092J5GDQ9/grants',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_allocations_projects(self):
        expected_payload = {
            "data": {
                "attributes": {
                    "abstract": "This project is used as an example, for demonstration or testing purposes. The contents of "
                                "this project, and resources it relates to, will not change. \n This example project (1) is a "
                                "project with a single PI and single CoI belonging to the same organisation. It is also "
                                "associated with a single grant and funder. The people, grants and organisations related to "
                                "this project will not be related to another project. This project has an acronym, abstract, "
                                "website and country property. The project duration is in the past. \n The remainder of this "
                                "abstract is padding text to give a realistic abstract length. \n Lorem ipsum dolor sit amet, "
                                "consectetur adipiscing elit. Maecenas eget lorem eleifend turpis vestibulum sollicitudin. "
                                "Curabitur libero nulla, maximus ut facilisis et, maximus quis dolor. Nunc ut malesuada "
                                "felis. Sed volutpat et lectus vitae convallis. Class aptent taciti sociosqu ad litora "
                                "torquent per conubia nostra, per inceptos himenaeos. Fusce ullamcorper nec ante ut "
                                "vulputate. Praesent ultricies mattis dolor quis ultrices. Ut sagittis scelerisque leo "
                                "fringilla malesuada. Donec euismod tincidunt purus vel commodo. \n Aenean volutpat libero "
                                "quis imperdiet tincidunt. Proin iaculis eros at turpis laoreet molestie. Quisque "
                                "pellentesque, lorem id ornare fermentum, nunc urna ultrices libero, eget tempor ipsum "
                                "lectus sollicitudin nibh. Sed sit amet vestibulum nulla. Vivamus dictum, dui id consectetur "
                                "mattis, sapien erat tristique nulla, at lobortis enim nibh eu orci. Curabitur eu purus "
                                "porttitor, rhoncus libero sed, mattis tellus. Praesent ullamcorper tincidunt ex. Vivamus "
                                "lectus urna, dignissim sit amet efficitur a, malesuada at nisi. \n Curabitur auctor ut "
                                "libero ac pharetra. Nunc rutrum facilisis felis, ac rhoncus lorem pulvinar quis. In felis "
                                "neque, mollis nec sagittis feugiat, finibus maximus mauris. Nullam varius, risus id "
                                "scelerisque tempor, justo purus malesuada nulla, eu sagittis purus arcu eget justo. Orci "
                                "varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Fusce vel "
                                "pretium augue. Pellentesque eu semper odio. Suspendisse congue varius est, et euismod justo "
                                "accumsan sed. Etiam nec scelerisque risus, sed tempus ante. Proin fringilla leo urna, eget "
                                "pulvinar leo placerat et. \n Etiam mollis lacus ut sapien elementum, sed volutpat dui "
                                "faucibus. Fusce ligula risus, tempor at justo ac, tincidunt finibus magna. Duis eget sapien "
                                "et nibh tincidunt faucibus. Duis tempus tincidunt leo. Aenean sit amet cursus ex. Etiam "
                                "eget finibus nulla, a rutrum turpis. Proin imperdiet, augue consectetur varius varius, "
                                "lectus elit egestas velit, ullamcorper pulvinar dolor felis at leo. Cras nec est ut est "
                                "efficitur pulvinar nec vel nisi. Nullam sed elit eu ante finibus volutpat. Nam id diam a "
                                "urna rutrum dictum. \n Pellentesque habitant morbi tristique senectus et netus et malesuada "
                                "fames ac turpis egestas. Integer accumsan et mi eu sagittis. Ut id nulla at quam efficitur "
                                "molestie. Donec viverra ex vitae mauris ullamcorper elementum. Proin sed felis enim. "
                                "Suspendisse potenti. Integer malesuada interdum mi, ornare semper lorem tempus condimentum. "
                                "Cras sodales risus quis nibh fermentum volutpat. Sed vel tincidunt lectus.",
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
                    "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2"
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
                            "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/allocations",
                            "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/allocations"
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
                            'related': 'http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/categorisations',
                            'self': 'http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/categorisations'
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
                            "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/participants",
                            "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/participants"
                        }
                    }
                },
                "type": "projects"
            },
            "links": {
                "self": "http://localhost:9000/allocations/01DB2ECBP35AT5WBG092J5GDQ9/projects"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/allocations/01DB2ECBP35AT5WBG092J5GDQ9/projects',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_organisations_list(self):
        expected_payload = {
            "data": [
                {
                    "attributes": {
                        "acronym": "EXORG1",
                        "grid-identifier": "XE-EXAMPLE-grid.5500.1",
                        "logo-url": "https://placeimg.com/256/256/arch",
                        "name": "Example Organisation 1",
                        "website": "https://www.example.com"
                    },
                    "id": "01DB2ECBP3WZDP4PES64XKXJ1A",
                    "links": {
                        "self": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A"
                    },
                    "relationships": {
                        "grants": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/grants",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/grants"
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
                                "related": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/people",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/people"
                            }
                        }
                    },
                    "type": "organisations"
                },
                {
                    "attributes": {
                        "acronym": None,
                        "grid-identifier": None,
                        "logo-url": None,
                        "name": "Example Organisation 2",
                        "website": None
                    },
                    "id": "01DB2ECBP3VF45F1N4XEBF83FE",
                    "links": {
                        "self": "http://localhost:9000/organisations/01DB2ECBP3VF45F1N4XEBF83FE"
                    },
                    "relationships": {
                        "grants": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/organisations/01DB2ECBP3VF45F1N4XEBF83FE/grants",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3VF45F1N4XEBF83FE/relationships/grants"
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
                                "related": "http://localhost:9000/organisations/01DB2ECBP3VF45F1N4XEBF83FE/people",
                                "self": "http://localhost:9000/organisations/01DB2ECBP3VF45F1N4XEBF83FE/relationships/people"
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
                        "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0"
                    },
                    "relationships": {
                        "organisation": {
                            "data": {
                                "id": "01DB2ECBP3WZDP4PES64XKXJ1A",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/organisations",
                                "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/organisations"
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
                                "related": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/participants",
                                "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/participants"
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
                        "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01DB2ECBP2MFB0DH3EF3PH74R0",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/people",
                                "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/projects",
                                "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/projects"
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
                        "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/allocations",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/allocations"
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
                                'related': 'http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/categorisations',
                                'self': 'http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/categorisations'
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/participants",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/participants"
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
                        "self": "http://localhost:9000/people/01DB2ECBP25PVTVVGT9YT7CKSB"
                    },
                    "relationships": {
                        "organisation": {
                            "data": {
                                "id": "01DB2ECBP3VF45F1N4XEBF83FE",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9000/people/01DB2ECBP25PVTVVGT9YT7CKSB/organisations",
                                "self": "http://localhost:9000/people/01DB2ECBP25PVTVVGT9YT7CKSB/relationships/organisations"
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
                                "related": "http://localhost:9000/people/01DB2ECBP25PVTVVGT9YT7CKSB/participants",
                                "self": "http://localhost:9000/people/01DB2ECBP25PVTVVGT9YT7CKSB/relationships/participants"
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
                        "self": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01DB2ECBP25PVTVVGT9YT7CKSB",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/people",
                                "self": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/projects",
                                "self": "http://localhost:9000/participants/01DB2ECBP3VQGDYMW1CRPJ0VGP/relationships/projects"
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
                        "self": "http://localhost:9000/people/01DB2ECBP38X26APJ2DNPJERYH"
                    },
                    "relationships": {
                        "organisation": {
                            "data": {
                                "id": "01DB2ECBP3VF45F1N4XEBF83FE",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9000/people/01DB2ECBP38X26APJ2DNPJERYH/organisations",
                                "self": "http://localhost:9000/people/01DB2ECBP38X26APJ2DNPJERYH/relationships/organisations"
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
                                "related": "http://localhost:9000/people/01DB2ECBP38X26APJ2DNPJERYH/participants",
                                "self": "http://localhost:9000/people/01DB2ECBP38X26APJ2DNPJERYH/relationships/participants"
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
                        "self": "http://localhost:9000/participants/01DB2ECBP32H2EZCGKSSV9J4R4"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01DB2ECBP38X26APJ2DNPJERYH",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP32H2EZCGKSSV9J4R4/people",
                                "self": "http://localhost:9000/participants/01DB2ECBP32H2EZCGKSSV9J4R4/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP2DXX8VN7S7AYJBGBT",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP32H2EZCGKSSV9J4R4/projects",
                                "self": "http://localhost:9000/participants/01DB2ECBP32H2EZCGKSSV9J4R4/relationships/projects"
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
                        "self": "http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/allocations",
                                "self": "http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/relationships/allocations"
                            }
                        },
                        'categorisations': {
                            'data': [],
                            'links': {
                                'related': 'http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/categorisations',
                                'self': 'http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/relationships/categorisations'
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
                                "related": "http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/participants",
                                "self": "http://localhost:9000/projects/01DB2ECBP2DXX8VN7S7AYJBGBT/relationships/participants"
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
                        "self": "http://localhost:9000/participants/01DB2ECBP355YQTDW80GS5R8E7"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01DB2ECBP38X26APJ2DNPJERYH",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP355YQTDW80GS5R8E7/people",
                                "self": "http://localhost:9000/participants/01DB2ECBP355YQTDW80GS5R8E7/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP2MB2Z9K1BSK5BND0V",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP355YQTDW80GS5R8E7/projects",
                                "self": "http://localhost:9000/participants/01DB2ECBP355YQTDW80GS5R8E7/relationships/projects"
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
                        "self": "http://localhost:9000/projects/01DB2ECBP2MB2Z9K1BSK5BND0V"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP2MB2Z9K1BSK5BND0V/allocations",
                                "self": "http://localhost:9000/projects/01DB2ECBP2MB2Z9K1BSK5BND0V/relationships/allocations"
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
                                'related': 'http://localhost:9000/projects/01DB2ECBP2MB2Z9K1BSK5BND0V/categorisations',
                                'self': 'http://localhost:9000/projects/01DB2ECBP2MB2Z9K1BSK5BND0V/relationships/categorisations'
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
                                "related": "http://localhost:9000/projects/01DB2ECBP2MB2Z9K1BSK5BND0V/participants",
                                "self": "http://localhost:9000/projects/01DB2ECBP2MB2Z9K1BSK5BND0V/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
                }
            ],
            "links": {
                "first": "http://localhost:9000/organisations?page=1",
                "last": "http://localhost:9000/organisations?page=3",
                "next": "http://localhost:9000/organisations?page=2",
                "prev": None,
                "self": "http://localhost:9000/organisations?page=1"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/organisations',
            base_url='http://localhost:9000',
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
                    "logo-url": "https://placeimg.com/256/256/arch",
                    "name": "Example Organisation 1",
                    "website": "https://www.example.com"
                },
                "id": "01DB2ECBP3WZDP4PES64XKXJ1A",
                "links": {
                    "self": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A"
                },
                "relationships": {
                    "grants": {
                        "data": [],
                        "links": {
                            "related": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/grants",
                            "self": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/grants"
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
                            "related": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/people",
                            "self": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/people"
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
                        "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0"
                    },
                    "relationships": {
                        "organisation": {
                            "data": {
                                "id": "01DB2ECBP3WZDP4PES64XKXJ1A",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/organisations",
                                "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/organisations"
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
                                "related": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/participants",
                                "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/participants"
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
                        "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01DB2ECBP2MFB0DH3EF3PH74R0",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/people",
                                "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/projects",
                                "self": "http://localhost:9000/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/projects"
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
                        "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/allocations",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/allocations"
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
                                'related': 'http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/categorisations',
                                'self': 'http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/categorisations'
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/participants",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
                }
            ],
            "links": {
                "self": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/organisations/01DB2ECBP3WZDP4PES64XKXJ1A',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
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
                    base_url='http://localhost:9000'
                )
                json_response = response.get_json()
                json_response = self.util_prepare_error_response(json_response)
                self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
                self.assertDictEqual(json_response, expected_payload)

    def test_organisations_relationship_grants(self):
        expected_payload = {
            "data": [],
            "links": {
                "related": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/grants",
                "self": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/grants"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/grants',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
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
                "related": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/people",
                "self": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/people"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/people',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_organisations_grants(self):
        expected_payload = {
            "data": [],
            "links": {
                "self": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/grants"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/grants',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
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
                        "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0"
                    },
                    "relationships": {
                        "organisation": {
                            "data": {
                                "id": "01DB2ECBP3WZDP4PES64XKXJ1A",
                                "type": "organisations"
                            },
                            "links": {
                                "related": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/organisations",
                                "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/organisations"
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
                                "related": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/participants",
                                "self": "http://localhost:9000/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/participants"
                            }
                        }
                    },
                    "type": "people"
                }
            ],
            "links": {
                "self": "http://localhost:9000/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/people"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/people',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_category_scheme_list(self):
        expected_payload = {
            "data": [
                {
                    "attributes": {
                        "acronym": "EXCATSCH1",
                        "description": "This category scheme is used as an example, for demonstration or testing purposes. The terms in this scheme, and resources they relates to, will not change.",
                        "name": "Example Category Scheme 1",
                        "revision": "2019-05-28",
                        "version": "1.0"
                    },
                    "id": "01DC6HYAKXG8FCN63D7DH06W84",
                    "links": {
                        "self": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84"
                    },
                    "relationships": {
                        "categories": {
                            "data": [
                                {
                                    "id": "01DC6HYAKX993ZK6YHCVWAE169",
                                    "type": "categories"
                                },
                                {
                                    "id": "01DC6HYAKX5NT8WBYWASQ9ENC8",
                                    "type": "categories"
                                },
                                {
                                    "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                                    "type": "categories"
                                },
                                {
                                    "id": "01DC6HYAKX53S13HCN2SBN4333",
                                    "type": "categories"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84/categories",
                                "self": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84/relationships/categories"
                            }
                        }
                    },
                    "type": "category-schemes"
                },
                {
                    "attributes": {
                        "acronym": None,
                        "description": None,
                        "name": "Example Category Scheme 2",
                        "revision": None,
                        "version": None
                    },
                    "id": "01DC6HYAKXMK47A45KCHZBH0CQ",
                    "links": {
                        "self": "http://localhost:9000/category-schemes/01DC6HYAKXMK47A45KCHZBH0CQ"
                    },
                    "relationships": {
                        "categories": {
                            "data": [
                                {
                                    "id": "01DC6HYAKXY0JT6583RCXTJY3Q",
                                    "type": "categories"
                                },
                                {
                                    "id": "01DC6HYAKXK6PMXX2TTTFTK5B4",
                                    "type": "categories"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/category-schemes/01DC6HYAKXMK47A45KCHZBH0CQ/categories",
                                "self": "http://localhost:9000/category-schemes/01DC6HYAKXMK47A45KCHZBH0CQ/relationships/categories"
                            }
                        }
                    },
                    "type": "category-schemes"
                }
            ],
            "included": [
                {
                    "attributes": {
                        "aliases": [
                            "ROOT"
                        ],
                        "concept": "https://www.example.com/category-scheme-1/category-term-1",
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The contents of this term, and resources it relates to, will not change. \n This term (0) is the root term with a single child term (1)."
                        ],
                        "examples": [
                            "Example root category term - example"
                        ],
                        "notation": "0",
                        "notes": [
                            "Example root category term - note"
                        ],
                        "scheme": "https://www.example.com/category-scheme-1",
                        "scope-notes": [
                            "Example root category term - scope note"
                        ],
                        "title": "Example Category Term: 0"
                    },
                    "id": "01DC6HYAKX993ZK6YHCVWAE169",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": None,
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                },
                {
                    "attributes": {
                        "aliases": [
                            "First Term"
                        ],
                        "concept": "https://www.example.com/category-scheme-1/category-term-2",
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The contents of this term, and resources it relates to, will not change. \n This term (1) is a first level term with the root term (0) as a parent and a single child term (2)."
                        ],
                        "examples": [
                            "Example category term 1 - example"
                        ],
                        "notation": "1",
                        "notes": [
                            "Example category term 1 - note"
                        ],
                        "scheme": "https://www.example.com/category-scheme-1",
                        "scope-notes": [
                            "Example category term 1 - scope note"
                        ],
                        "title": "Example Category Term: Level 1"
                    },
                    "id": "01DC6HYAKX5NT8WBYWASQ9ENC8",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": {
                                "id": "01DC6HYAKX993ZK6YHCVWAE169",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                },
                {
                    "attributes": {
                        "aliases": [
                            "Second Term"
                        ],
                        "concept": "https://www.example.com/category-scheme-1/category-term-3",
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The contents of this term, and resources it relates to, will not change. \n This term (2) is a second level term with a first level term as a parent (1) and a single child term (3)."
                        ],
                        "examples": [
                            "Example category term 2 - example"
                        ],
                        "notation": "1.2",
                        "notes": [
                            "Example category term 2 - note"
                        ],
                        "scheme": "https://www.example.com/category-scheme-1",
                        "scope-notes": [
                            "Example category term 2 - scope note"
                        ],
                        "title": "Example Category Term: Level 2"
                    },
                    "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": {
                                "id": "01DC6HYAKX5NT8WBYWASQ9ENC8",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                },
                {
                    "attributes": {
                        "aliases": [
                            "Third Term"
                        ],
                        "concept": "https://www.example.com/category-scheme-1/category-term-4",
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The contents of this term, and resources it relates to, will not change. \n This term (3) is a third level term with a second level term as a parent (2) and no child terms."
                        ],
                        "examples": [
                            "Example category term 3 - example"
                        ],
                        "notation": "1.2.3",
                        "notes": [
                            "Example category term 3 - note"
                        ],
                        "scheme": "https://www.example.com/category-scheme-1",
                        "scope-notes": [
                            "Example category term 3 - scope note"
                        ],
                        "title": "Example Category Term: Level 3"
                    },
                    "id": "01DC6HYAKX53S13HCN2SBN4333",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [
                                {
                                    "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                                    "type": "categorisations"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": {
                                "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                },
                {
                    "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                    "links": {
                        "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG"
                    },
                    "relationships": {
                        "category": {
                            "data": {
                                "id": "01DC6HYAKX53S13HCN2SBN4333",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/categories",
                                "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/relationships/categories"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/projects",
                                "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/relationships/projects"
                            }
                        }
                    },
                    "type": "categorisations"
                },
                {
                    "attributes": {
                        "abstract": "This project is used as an example, for demonstration or testing purposes. The contents of this project, and resources it relates to, will not change. \n This example project (1) is a project with a single PI and single CoI belonging to the same organisation. It is also associated with a single grant and funder. The people, grants and organisations related to this project will not be related to another project. This project has an acronym, abstract, website and country property. The project duration is in the past. \n The remainder of this abstract is padding text to give a realistic abstract length. \n Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eget lorem eleifend turpis vestibulum sollicitudin. Curabitur libero nulla, maximus ut facilisis et, maximus quis dolor. Nunc ut malesuada felis. Sed volutpat et lectus vitae convallis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Fusce ullamcorper nec ante ut vulputate. Praesent ultricies mattis dolor quis ultrices. Ut sagittis scelerisque leo fringilla malesuada. Donec euismod tincidunt purus vel commodo. \n Aenean volutpat libero quis imperdiet tincidunt. Proin iaculis eros at turpis laoreet molestie. Quisque pellentesque, lorem id ornare fermentum, nunc urna ultrices libero, eget tempor ipsum lectus sollicitudin nibh. Sed sit amet vestibulum nulla. Vivamus dictum, dui id consectetur mattis, sapien erat tristique nulla, at lobortis enim nibh eu orci. Curabitur eu purus porttitor, rhoncus libero sed, mattis tellus. Praesent ullamcorper tincidunt ex. Vivamus lectus urna, dignissim sit amet efficitur a, malesuada at nisi. \n Curabitur auctor ut libero ac pharetra. Nunc rutrum facilisis felis, ac rhoncus lorem pulvinar quis. In felis neque, mollis nec sagittis feugiat, finibus maximus mauris. Nullam varius, risus id scelerisque tempor, justo purus malesuada nulla, eu sagittis purus arcu eget justo. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Fusce vel pretium augue. Pellentesque eu semper odio. Suspendisse congue varius est, et euismod justo accumsan sed. Etiam nec scelerisque risus, sed tempus ante. Proin fringilla leo urna, eget pulvinar leo placerat et. \n Etiam mollis lacus ut sapien elementum, sed volutpat dui faucibus. Fusce ligula risus, tempor at justo ac, tincidunt finibus magna. Duis eget sapien et nibh tincidunt faucibus. Duis tempus tincidunt leo. Aenean sit amet cursus ex. Etiam eget finibus nulla, a rutrum turpis. Proin imperdiet, augue consectetur varius varius, lectus elit egestas velit, ullamcorper pulvinar dolor felis at leo. Cras nec est ut est efficitur pulvinar nec vel nisi. Nullam sed elit eu ante finibus volutpat. Nam id diam a urna rutrum dictum. \n Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Integer accumsan et mi eu sagittis. Ut id nulla at quam efficitur molestie. Donec viverra ex vitae mauris ullamcorper elementum. Proin sed felis enim. Suspendisse potenti. Integer malesuada interdum mi, ornare semper lorem tempus condimentum. Cras sodales risus quis nibh fermentum volutpat. Sed vel tincidunt lectus.",
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
                        "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/allocations",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/allocations"
                            }
                        },
                        "categorisations": {
                            "data": [
                                {
                                    "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                                    "type": "categorisations"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/categorisations",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/categorisations"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/participants",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
                },
                {
                    "attributes": {
                        "aliases": None,
                        "concept": "https://www.example.com/category-scheme-2/category-term-1",
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The contents of this term, and resources it relates to, will not change. \n This term (0) is the root term with a single child term (1)."
                        ],
                        "examples": None,
                        "notation": None,
                        "notes": None,
                        "scheme": "https://www.example.com/category-scheme-2",
                        "scope-notes": None,
                        "title": "Example Category Term: 0"
                    },
                    "id": "01DC6HYAKXY0JT6583RCXTJY3Q",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKXY0JT6583RCXTJY3Q"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXY0JT6583RCXTJY3Q/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKXY0JT6583RCXTJY3Q/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXMK47A45KCHZBH0CQ",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXY0JT6583RCXTJY3Q/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKXY0JT6583RCXTJY3Q/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": None,
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXY0JT6583RCXTJY3Q/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKXY0JT6583RCXTJY3Q/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                },
                {
                    "attributes": {
                        "aliases": None,
                        "concept": "https://www.example.com/category-scheme-2/category-term-2",
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The contents of this term, and resources it relates to, will not change. \n This term (1A) is a first level term with the root term as a parent (0) and no child terms."
                        ],
                        "examples": None,
                        "notation": None,
                        "notes": None,
                        "scheme": "https://www.example.com/category-scheme-2",
                        "scope-notes": None,
                        "title": "Example Category Term: Level 1"
                    },
                    "id": "01DC6HYAKXK6PMXX2TTTFTK5B4",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKXK6PMXX2TTTFTK5B4"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [
                                {
                                    "id": "01DC6HYAKY9ZEK8NQ1JGDMKCK7",
                                    "type": "categorisations"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXK6PMXX2TTTFTK5B4/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKXK6PMXX2TTTFTK5B4/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXMK47A45KCHZBH0CQ",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXK6PMXX2TTTFTK5B4/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKXK6PMXX2TTTFTK5B4/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": {
                                "id": "01DC6HYAKXY0JT6583RCXTJY3Q",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXK6PMXX2TTTFTK5B4/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKXK6PMXX2TTTFTK5B4/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                },
                {
                    "id": "01DC6HYAKY9ZEK8NQ1JGDMKCK7",
                    "links": {
                        "self": "http://localhost:9000/categorisations/01DC6HYAKY9ZEK8NQ1JGDMKCK7"
                    },
                    "relationships": {
                        "category": {
                            "data": {
                                "id": "01DC6HYAKXK6PMXX2TTTFTK5B4",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categorisations/01DC6HYAKY9ZEK8NQ1JGDMKCK7/categories",
                                "self": "http://localhost:9000/categorisations/01DC6HYAKY9ZEK8NQ1JGDMKCK7/relationships/categories"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP2MB2Z9K1BSK5BND0V",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/categorisations/01DC6HYAKY9ZEK8NQ1JGDMKCK7/projects",
                                "self": "http://localhost:9000/categorisations/01DC6HYAKY9ZEK8NQ1JGDMKCK7/relationships/projects"
                            }
                        }
                    },
                    "type": "categorisations"
                },
                {
                    "attributes": {
                        "abstract": "This project is used as an example, for demonstration or testing purposes. The contents of this project, and resources it relates to, will not change. This example project (3) has a single PI and multiple CoIs belonging to different organisations. It is also associated with a single grant and funder. The resources related to this project will also relate to other projects. This project has an acronym and country properties, it does not have a website or publications. The project duration is in the future. \n The remainder of this abstract is padding text to give a realistic abstract length. \n Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eget lorem eleifend turpis vestibulum sollicitudin. Curabitur libero nulla, maximus ut facilisis et, maximus quis dolor. Nunc ut malesuada felis. Sed volutpat et lectus vitae convallis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Fusce ullamcorper nec ante ut vulputate. Praesent ultricies mattis dolor quis ultrices. Ut sagittis scelerisque leo fringilla malesuada. Donec euismod tincidunt purus vel commodo. \n Aenean volutpat libero quis imperdiet tincidunt. Proin iaculis eros at turpis laoreet molestie. Quisque pellentesque, lorem id ornare fermentum, nunc urna ultrices libero, eget tempor ipsum lectus sollicitudin nibh. Sed sit amet vestibulum nulla. Vivamus dictum, dui id consectetur mattis, sapien erat tristique nulla, at lobortis enim nibh eu orci. Curabitur eu purus porttitor, rhoncus libero sed, mattis tellus. Praesent ullamcorper tincidunt ex. Vivamus lectus urna, dignissim sit amet efficitur a, malesuada at nisi. \n Curabitur auctor ut libero ac pharetra. Nunc rutrum facilisis felis, ac rhoncus lorem pulvinar quis. In felis neque, mollis nec sagittis feugiat, finibus maximus mauris. Nullam varius, risus id scelerisque tempor, justo purus malesuada nulla, eu sagittis purus arcu eget justo. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Fusce vel pretium augue. Pellentesque eu semper odio. Suspendisse congue varius est, et euismod justo accumsan sed. Etiam nec scelerisque risus, sed tempus ante. Proin fringilla leo urna, eget pulvinar leo placerat et. \n Etiam mollis lacus ut sapien elementum, sed volutpat dui faucibus. Fusce ligula risus, tempor at justo ac, tincidunt finibus magna. Duis eget sapien et nibh tincidunt faucibus. Duis tempus tincidunt leo. Aenean sit amet cursus ex. Etiam eget finibus nulla, a rutrum turpis. Proin imperdiet, augue consectetur varius varius, lectus elit egestas velit, ullamcorper pulvinar dolor felis at leo. Cras nec est ut est efficitur pulvinar nec vel nisi. Nullam sed elit eu ante finibus volutpat. Nam id diam a urna rutrum dictum. \n Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Integer accumsan et mi eu sagittis. Ut id nulla at quam efficitur molestie. Donec viverra ex vitae mauris ullamcorper elementum. Proin sed felis enim. Suspendisse potenti. Integer malesuada interdum mi, ornare semper lorem tempus condimentum. Cras sodales risus quis nibh fermentum volutpat. Sed vel tincidunt lectus.",
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
                        "self": "http://localhost:9000/projects/01DB2ECBP2MB2Z9K1BSK5BND0V"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP2MB2Z9K1BSK5BND0V/allocations",
                                "self": "http://localhost:9000/projects/01DB2ECBP2MB2Z9K1BSK5BND0V/relationships/allocations"
                            }
                        },
                        "categorisations": {
                            "data": [
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
                            "links": {
                                "related": "http://localhost:9000/projects/01DB2ECBP2MB2Z9K1BSK5BND0V/categorisations",
                                "self": "http://localhost:9000/projects/01DB2ECBP2MB2Z9K1BSK5BND0V/relationships/categorisations"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP2MB2Z9K1BSK5BND0V/participants",
                                "self": "http://localhost:9000/projects/01DB2ECBP2MB2Z9K1BSK5BND0V/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
                }
            ],
            "links": {
                "first": "http://localhost:9000/category-schemes?page=1",
                "last": "http://localhost:9000/category-schemes?page=2",
                "next": "http://localhost:9000/category-schemes?page=2",
                "prev": None,
                "self": "http://localhost:9000/category-schemes?page=1"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/category-schemes',
            base_url='http://localhost:9000',
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

    def test_category_scheme_detail(self):
        expected_payload = {
            "data": {
                "attributes": {
                    "acronym": "EXCATSCH1",
                    "description": "This category scheme is used as an example, for demonstration or testing purposes. "
                                   "The terms in this scheme, and resources they relates to, will not change.",
                    "name": "Example Category Scheme 1",
                    "revision": "2019-05-28",
                    "version": "1.0"
                },
                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                "links": {
                    "self": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84"
                },
                "relationships": {
                    "categories": {
                        "data": [
                            {
                                "id": "01DC6HYAKX993ZK6YHCVWAE169",
                                "type": "categories"
                            },
                            {
                                "id": "01DC6HYAKX5NT8WBYWASQ9ENC8",
                                "type": "categories"
                            },
                            {
                                "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                                "type": "categories"
                            },
                            {
                                "id": "01DC6HYAKX53S13HCN2SBN4333",
                                "type": "categories"
                            }
                        ],
                        "links": {
                            "related": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84/categories",
                            "self": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84/relationships/categories"
                        }
                    }
                },
                "type": "category-schemes"
            },
            "included": [
                {
                    "attributes": {
                        "aliases": [
                            "ROOT"
                        ],
                        "concept": "https://www.example.com/category-scheme-1/category-term-1",
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The "
                            "contents of this term, and resources it relates to, will not change. \n This term (0) is "
                            "the root term with a single child term (1)."
                        ],
                        "examples": [
                            "Example root category term - example"
                        ],
                        "notation": "0",
                        "notes": [
                            "Example root category term - note"
                        ],
                        "scheme": "https://www.example.com/category-scheme-1",
                        "scope-notes": [
                            "Example root category term - scope note"
                        ],
                        "title": "Example Category Term: 0"
                    },
                    "id": "01DC6HYAKX993ZK6YHCVWAE169",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": None,
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                },
                {
                    "attributes": {
                        "aliases": [
                            "First Term"
                        ],
                        "concept": "https://www.example.com/category-scheme-1/category-term-2",
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The "
                            "contents of this term, and resources it relates to, will not change. \n This term (1) is "
                            "a first level term with the root term (0) as a parent and a single child term (2)."
                        ],
                        "examples": [
                            "Example category term 1 - example"
                        ],
                        "notation": "1",
                        "notes": [
                            "Example category term 1 - note"
                        ],
                        "scheme": "https://www.example.com/category-scheme-1",
                        "scope-notes": [
                            "Example category term 1 - scope note"
                        ],
                        "title": "Example Category Term: Level 1"
                    },
                    "id": "01DC6HYAKX5NT8WBYWASQ9ENC8",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": {
                                "id": "01DC6HYAKX993ZK6YHCVWAE169",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                },
                {
                    "attributes": {
                        "aliases": [
                            "Second Term"
                        ],
                        "concept": "https://www.example.com/category-scheme-1/category-term-3",
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The "
                            "contents of this term, and resources it relates to, will not change. \n This term (2) is "
                            "a second level term with a first level term as a parent (1) and a single child term (3)."
                        ],
                        "examples": [
                            "Example category term 2 - example"
                        ],
                        "notation": "1.2",
                        "notes": [
                            "Example category term 2 - note"
                        ],
                        "scheme": "https://www.example.com/category-scheme-1",
                        "scope-notes": [
                            "Example category term 2 - scope note"
                        ],
                        "title": "Example Category Term: Level 2"
                    },
                    "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": {
                                "id": "01DC6HYAKX5NT8WBYWASQ9ENC8",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                },
                {
                    "attributes": {
                        "aliases": [
                            "Third Term"
                        ],
                        "concept": "https://www.example.com/category-scheme-1/category-term-4",
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The "
                            "contents of this term, and resources it relates to, will not change. \n This term (3) is "
                            "a third level term with a second level term as a parent (2) and no child terms."
                        ],
                        "examples": [
                            "Example category term 3 - example"
                        ],
                        "notation": "1.2.3",
                        "notes": [
                            "Example category term 3 - note"
                        ],
                        "scheme": "https://www.example.com/category-scheme-1",
                        "scope-notes": [
                            "Example category term 3 - scope note"
                        ],
                        "title": "Example Category Term: Level 3"
                    },
                    "id": "01DC6HYAKX53S13HCN2SBN4333",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [
                                {
                                    "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                                    "type": "categorisations"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": {
                                "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                },
                {
                    "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                    "links": {
                        "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG"
                    },
                    "relationships": {
                        "category": {
                            "data": {
                                "id": "01DC6HYAKX53S13HCN2SBN4333",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/categories",
                                "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/relationships/categories"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/projects",
                                "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/relationships/projects"
                            }
                        }
                    },
                    "type": "categorisations"
                },
                {
                    "attributes": {
                        "abstract": "This project is used as an example, for demonstration or testing purposes. The contents of this project, and resources it relates to, will not change. \n This example project (1) is a project with a single PI and single CoI belonging to the same organisation. It is also associated with a single grant and funder. The people, grants and organisations related to this project will not be related to another project. This project has an acronym, abstract, website and country property. The project duration is in the past. \n The remainder of this abstract is padding text to give a realistic abstract length. \n Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eget lorem eleifend turpis vestibulum sollicitudin. Curabitur libero nulla, maximus ut facilisis et, maximus quis dolor. Nunc ut malesuada felis. Sed volutpat et lectus vitae convallis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Fusce ullamcorper nec ante ut vulputate. Praesent ultricies mattis dolor quis ultrices. Ut sagittis scelerisque leo fringilla malesuada. Donec euismod tincidunt purus vel commodo. \n Aenean volutpat libero quis imperdiet tincidunt. Proin iaculis eros at turpis laoreet molestie. Quisque pellentesque, lorem id ornare fermentum, nunc urna ultrices libero, eget tempor ipsum lectus sollicitudin nibh. Sed sit amet vestibulum nulla. Vivamus dictum, dui id consectetur mattis, sapien erat tristique nulla, at lobortis enim nibh eu orci. Curabitur eu purus porttitor, rhoncus libero sed, mattis tellus. Praesent ullamcorper tincidunt ex. Vivamus lectus urna, dignissim sit amet efficitur a, malesuada at nisi. \n Curabitur auctor ut libero ac pharetra. Nunc rutrum facilisis felis, ac rhoncus lorem pulvinar quis. In felis neque, mollis nec sagittis feugiat, finibus maximus mauris. Nullam varius, risus id scelerisque tempor, justo purus malesuada nulla, eu sagittis purus arcu eget justo. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Fusce vel pretium augue. Pellentesque eu semper odio. Suspendisse congue varius est, et euismod justo accumsan sed. Etiam nec scelerisque risus, sed tempus ante. Proin fringilla leo urna, eget pulvinar leo placerat et. \n Etiam mollis lacus ut sapien elementum, sed volutpat dui faucibus. Fusce ligula risus, tempor at justo ac, tincidunt finibus magna. Duis eget sapien et nibh tincidunt faucibus. Duis tempus tincidunt leo. Aenean sit amet cursus ex. Etiam eget finibus nulla, a rutrum turpis. Proin imperdiet, augue consectetur varius varius, lectus elit egestas velit, ullamcorper pulvinar dolor felis at leo. Cras nec est ut est efficitur pulvinar nec vel nisi. Nullam sed elit eu ante finibus volutpat. Nam id diam a urna rutrum dictum. \n Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Integer accumsan et mi eu sagittis. Ut id nulla at quam efficitur molestie. Donec viverra ex vitae mauris ullamcorper elementum. Proin sed felis enim. Suspendisse potenti. Integer malesuada interdum mi, ornare semper lorem tempus condimentum. Cras sodales risus quis nibh fermentum volutpat. Sed vel tincidunt lectus.",
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
                        "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/allocations",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/allocations"
                            }
                        },
                        "categorisations": {
                            "data": [
                                {
                                    "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                                    "type": "categorisations"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/categorisations",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/categorisations"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/participants",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
                }
            ],
            "links": {
                "self": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/category-schemes/01DC6HYAKXG8FCN63D7DH06W84',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response['data'], expected_payload['data'])
        self.assertCountEqual(json_response['included'], expected_payload['included'])
        self.assertDictEqual(json_response['links'], expected_payload['links'])

    def test_category_scheme_single_missing_unknown_id(self):
        error = ApiNotFoundError()
        expected_payload = self.util_prepare_expected_error_payload(error)

        for allocation_id in ['', 'unknown']:
            with self.subTest(allocation_id=allocation_id):
                token = self.util_create_auth_token()
                response = self.client.get(
                    f"/category-scheme/{allocation_id}",
                    headers={'authorization': f"bearer {token}"},
                    base_url='http://localhost:9000'
                )
                json_response = response.get_json()
                json_response = self.util_prepare_error_response(json_response)
                self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
                self.assertDictEqual(json_response, expected_payload)

    def test_category_scheme_relationship_category_terms(self):
        expected_payload = {
            "data": [
                {
                    "id": "01DC6HYAKX993ZK6YHCVWAE169",
                    "type": "categories"
                },
                {
                    "id": "01DC6HYAKX5NT8WBYWASQ9ENC8",
                    "type": "categories"
                },
                {
                    "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                    "type": "categories"
                },
                {
                    "id": "01DC6HYAKX53S13HCN2SBN4333",
                    "type": "categories"
                }
            ],
            "links": {
                "related": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84/categories",
                "self": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84/relationships/categories"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/category-schemes/01DC6HYAKXG8FCN63D7DH06W84/relationships/categories',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_category_scheme_category_terms(self):
        expected_payload = {
            "data": [
                {
                    "attributes": {
                        "aliases": [
                            "ROOT"
                        ],
                        "concept": "https://www.example.com/category-scheme-1/category-term-1",
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The "
                            "contents of this term, and resources it relates to, will not change. \n This term (0) is "
                            "the root term with a single child term (1)."
                        ],
                        "examples": [
                            "Example root category term - example"
                        ],
                        "notation": "0",
                        "notes": [
                            "Example root category term - note"
                        ],
                        "scheme": "https://www.example.com/category-scheme-1",
                        "scope-notes": [
                            "Example root category term - scope note"
                        ],
                        "title": "Example Category Term: 0"
                    },
                    "id": "01DC6HYAKX993ZK6YHCVWAE169",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": None,
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                },
                {
                    "attributes": {
                        "aliases": [
                            "First Term"
                        ],
                        "concept": "https://www.example.com/category-scheme-1/category-term-2",
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The "
                            "contents of this term, and resources it relates to, will not change. \n This term (1) is "
                            "a first level term with the root term (0) as a parent and a single child term (2)."
                        ],
                        "examples": [
                            "Example category term 1 - example"
                        ],
                        "notation": "1",
                        "notes": [
                            "Example category term 1 - note"
                        ],
                        "scheme": "https://www.example.com/category-scheme-1",
                        "scope-notes": [
                            "Example category term 1 - scope note"
                        ],
                        "title": "Example Category Term: Level 1"
                    },
                    "id": "01DC6HYAKX5NT8WBYWASQ9ENC8",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": {
                                "id": "01DC6HYAKX993ZK6YHCVWAE169",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                },
                {
                    "attributes": {
                        "aliases": [
                            "Second Term"
                        ],
                        "concept": "https://www.example.com/category-scheme-1/category-term-3",
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The "
                            "contents of this term, and resources it relates to, will not change. \n This term (2) is "
                            "a second level term with a first level term as a parent (1) and a single child term (3)."
                        ],
                        "examples": [
                            "Example category term 2 - example"
                        ],
                        "notation": "1.2",
                        "notes": [
                            "Example category term 2 - note"
                        ],
                        "scheme": "https://www.example.com/category-scheme-1",
                        "scope-notes": [
                            "Example category term 2 - scope note"
                        ],
                        "title": "Example Category Term: Level 2"
                    },
                    "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": {
                                "id": "01DC6HYAKX5NT8WBYWASQ9ENC8",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                },
                {
                    "attributes": {
                        "aliases": [
                            "Third Term"
                        ],
                        "concept": "https://www.example.com/category-scheme-1/category-term-4",
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The "
                            "contents of this term, and resources it relates to, will not change. \n This term (3) is "
                            "a third level term with a second level term as a parent (2) and no child terms."
                        ],
                        "examples": [
                            "Example category term 3 - example"
                        ],
                        "notation": "1.2.3",
                        "notes": [
                            "Example category term 3 - note"
                        ],
                        "scheme": "https://www.example.com/category-scheme-1",
                        "scope-notes": [
                            "Example category term 3 - scope note"
                        ],
                        "title": "Example Category Term: Level 3"
                    },
                    "id": "01DC6HYAKX53S13HCN2SBN4333",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [
                                {
                                    "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                                    "type": "categorisations"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": {
                                "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                }
            ],
            "links": {
                "self": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84/categories"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/category-schemes/01DC6HYAKXG8FCN63D7DH06W84/categories',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_category_term_list(self):
        expected_payload = {
            "data": [
                {
                    "attributes": {
                        "aliases": [
                            "ROOT"
                        ],
                        "concept": "https://www.example.com/category-scheme-1/category-term-1",
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The "
                            "contents of this term, and resources it relates to, will not change. \n This term (0) is "
                            "the root term with a single child term (1)."
                        ],
                        "examples": [
                            "Example root category term - example"
                        ],
                        "notation": "0",
                        "notes": [
                            "Example root category term - note"
                        ],
                        "scheme": "https://www.example.com/category-scheme-1",
                        "scope-notes": [
                            "Example root category term - scope note"
                        ],
                        "title": "Example Category Term: 0"
                    },
                    "id": "01DC6HYAKX993ZK6YHCVWAE169",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": None,
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                },
                {
                    "attributes": {
                        "aliases": [
                            "First Term"
                        ],
                        "concept": "https://www.example.com/category-scheme-1/category-term-2",
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The "
                            "contents of this term, and resources it relates to, will not change. \n This term (1) is "
                            "a first level term with the root term (0) as a parent and a single child term (2)."
                        ],
                        "examples": [
                            "Example category term 1 - example"
                        ],
                        "notation": "1",
                        "notes": [
                            "Example category term 1 - note"
                        ],
                        "scheme": "https://www.example.com/category-scheme-1",
                        "scope-notes": [
                            "Example category term 1 - scope note"
                        ],
                        "title": "Example Category Term: Level 1"
                    },
                    "id": "01DC6HYAKX5NT8WBYWASQ9ENC8",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": {
                                "id": "01DC6HYAKX993ZK6YHCVWAE169",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKX5NT8WBYWASQ9ENC8/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                }
            ],
            "included": [
                {
                    "attributes": {
                        "acronym": "EXCATSCH1",
                        "description": "This category scheme is used as an example, for demonstration or testing "
                                       "purposes. The terms in this scheme, and resources they relates to, will not "
                                       "change.",
                        "name": "Example Category Scheme 1",
                        "revision": "2019-05-28",
                        "version": "1.0"
                    },
                    "id": "01DC6HYAKXG8FCN63D7DH06W84",
                    "links": {
                        "self": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84"
                    },
                    "relationships": {
                        "categories": {
                            "data": [
                                {
                                    "id": "01DC6HYAKX993ZK6YHCVWAE169",
                                    "type": "categories"
                                },
                                {
                                    "id": "01DC6HYAKX5NT8WBYWASQ9ENC8",
                                    "type": "categories"
                                },
                                {
                                    "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                                    "type": "categories"
                                },
                                {
                                    "id": "01DC6HYAKX53S13HCN2SBN4333",
                                    "type": "categories"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84/categories",
                                "self": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84/relationships/categories"
                            }
                        }
                    },
                    "type": "category-schemes"
                },
                {
                    "attributes": {
                        "aliases": [
                            "ROOT"
                        ],
                        'concept': 'https://www.example.com/category-scheme-1/category-term-1',
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The "
                            "contents of this term, and resources it relates to, will not change. \n This term (0) is "
                            "the root term with a single child term (1)."
                        ],
                        "examples": [
                            "Example root category term - example"
                        ],
                        "notation": "0",
                        "notes": [
                            "Example root category term - note"
                        ],
                        'scheme': 'https://www.example.com/category-scheme-1',
                        "scope-notes": [
                            "Example root category term - scope note"
                        ],
                        "title": "Example Category Term: 0"
                    },
                    "id": "01DC6HYAKX993ZK6YHCVWAE169",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": None,
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKX993ZK6YHCVWAE169/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                }
            ],
            "links": {
                "first": "http://localhost:9000/categories?page=1",
                "last": "http://localhost:9000/categories?page=11",
                "next": "http://localhost:9000/categories?page=2",
                "prev": None,
                "self": "http://localhost:9000/categories?page=1"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/categories',
            base_url='http://localhost:9000',
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

    def test_category_term_detail(self):
        expected_payload = {
            "data": {
                "attributes": {
                    "aliases": [
                        "Third Term"
                    ],
                    "concept": "https://www.example.com/category-scheme-1/category-term-4",
                    "definitions": [
                        "This category term is used as an example, for demonstration or testing purposes. The contents "
                        "of this term, and resources it relates to, will not change. \n This term (3) is a third level "
                        "term with a second level term as a parent (2) and no child terms."
                    ],
                    "examples": [
                        "Example category term 3 - example"
                    ],
                    "notation": "1.2.3",
                    "notes": [
                        "Example category term 3 - note"
                    ],
                    "scheme": "https://www.example.com/category-scheme-1",
                    "scope-notes": [
                        "Example category term 3 - scope note"
                    ],
                    "title": "Example Category Term: Level 3"
                },
                "id": "01DC6HYAKX53S13HCN2SBN4333",
                "links": {
                    "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333"
                },
                "relationships": {
                    "categorisations": {
                        "data": [
                            {
                                "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                                "type": "categorisations"
                            }
                        ],
                        "links": {
                            "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/categorisations",
                            "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/categorisations"
                        }
                    },
                    "category-scheme": {
                        "data": {
                            "id": "01DC6HYAKXG8FCN63D7DH06W84",
                            "type": "category-schemes"
                        },
                        "links": {
                            "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/category-schemes",
                            "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/category-schemes"
                        }
                    },
                    "parent-category": {
                        "data": {
                            "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                            "type": "categories"
                        },
                        "links": {
                            "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/parent-categories",
                            "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/parent-categories"
                        }
                    }
                },
                "type": "categories"
            },
            "included": [
                {
                    "attributes": {
                        "acronym": "EXCATSCH1",
                        "description": "This category scheme is used as an example, for demonstration or testing "
                                       "purposes. The terms in this scheme, and resources they relates to, will not "
                                       "change.",
                        "name": "Example Category Scheme 1",
                        "revision": "2019-05-28",
                        "version": "1.0"
                    },
                    "id": "01DC6HYAKXG8FCN63D7DH06W84",
                    "links": {
                        "self": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84"
                    },
                    "relationships": {
                        "categories": {
                            "data": [
                                {
                                    "id": "01DC6HYAKX993ZK6YHCVWAE169",
                                    "type": "categories"
                                },
                                {
                                    "id": "01DC6HYAKX5NT8WBYWASQ9ENC8",
                                    "type": "categories"
                                },
                                {
                                    "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                                    "type": "categories"
                                },
                                {
                                    "id": "01DC6HYAKX53S13HCN2SBN4333",
                                    "type": "categories"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84/categories",
                                "self": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84/relationships/categories"
                            }
                        }
                    },
                    "type": "category-schemes"
                },
                {
                    "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                    "links": {
                        "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG"
                    },
                    "relationships": {
                        "category": {
                            "data": {
                                "id": "01DC6HYAKX53S13HCN2SBN4333",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/categories",
                                "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/relationships/categories"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/projects",
                                "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/relationships/projects"
                            }
                        }
                    },
                    "type": "categorisations"
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
                                    "is padding text to give a realistic abstract length. \n Lorem ipsum dolor sit "
                                    "amet, consectetur adipiscing elit. Maecenas eget lorem eleifend turpis vestibulum "
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
                        "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/allocations",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/allocations"
                            }
                        },
                        "categorisations": {
                            "data": [
                                {
                                    "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                                    "type": "categorisations"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/categorisations",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/categorisations"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/participants",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
                },
                {
                    "attributes": {
                        "aliases": [
                            "Second Term"
                        ],
                        'concept': 'https://www.example.com/category-scheme-1/category-term-3',
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The "
                            "contents of this term, and resources it relates to, will not change. \n This term (2) is "
                            "a second level term with a first level term as a parent (1) and a single child term (3)."
                        ],
                        "examples": [
                            "Example category term 2 - example"
                        ],
                        "notation": "1.2",
                        "notes": [
                            "Example category term 2 - note"
                        ],
                        'scheme': 'https://www.example.com/category-scheme-1',
                        "scope-notes": [
                            "Example category term 2 - scope note"
                        ],
                        "title": "Example Category Term: Level 2"
                    },
                    "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": {
                                "id": "01DC6HYAKX5NT8WBYWASQ9ENC8",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                }
            ],
            "links": {
                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/categories/01DC6HYAKX53S13HCN2SBN4333',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response['data'], expected_payload['data'])
        self.assertCountEqual(json_response['included'], expected_payload['included'])
        self.assertDictEqual(json_response['links'], expected_payload['links'])

    def test_category_term_single_missing_unknown_id(self):
        error = ApiNotFoundError()
        expected_payload = self.util_prepare_expected_error_payload(error)

        for allocation_id in ['', 'unknown']:
            with self.subTest(allocation_id=allocation_id):
                token = self.util_create_auth_token()
                response = self.client.get(
                    f"/categories/{allocation_id}",
                    headers={'authorization': f"bearer {token}"},
                    base_url='http://localhost:9000'
                )
                json_response = response.get_json()
                json_response = self.util_prepare_error_response(json_response)
                self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
                self.assertDictEqual(json_response, expected_payload)

    def test_category_term_relationship_parent_category_terms(self):
        expected_payload = {
            "data": {
                "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                "type": "categories"
            },
            "links": {
                "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/parent-categories",
                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/parent-categories"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/parent-categories',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_category_term_relationship_category_schemes(self):
        expected_payload = {
            "data": {
                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                "type": "category-schemes"
            },
            "links": {
                "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/category-schemes",
                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/category-schemes"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/category-schemes',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_category_term_relationship_categorisations(self):
        expected_payload = {
            "data": [
                {
                    "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                    "type": "categorisations"
                }
            ],
            "links": {
                "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/categorisations",
                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/categorisations"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/categorisations',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_category_term_parent_category_terms(self):
        expected_payload = {
            "data": {
                "attributes": {
                    "aliases": [
                        "Second Term"
                    ],
                    'concept': 'https://www.example.com/category-scheme-1/category-term-3',
                    "definitions": [
                        "This category term is used as an example, for demonstration or testing purposes. The "
                        "contents of this term, and resources it relates to, will not change. \n This term (2) is "
                        "a second level term with a first level term as a parent (1) and a single child term (3)."
                    ],
                    "examples": [
                        "Example category term 2 - example"
                    ],
                    "notation": "1.2",
                    "notes": [
                        "Example category term 2 - note"
                    ],
                    'scheme': 'https://www.example.com/category-scheme-1',
                    "scope-notes": [
                        "Example category term 2 - scope note"
                    ],
                    "title": "Example Category Term: Level 2"
                },
                "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                "links": {
                    "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE"
                },
                "relationships": {
                    "categorisations": {
                        "data": [],
                        "links": {
                            "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/categorisations",
                            "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/categorisations"
                        }
                    },
                    "category-scheme": {
                        "data": {
                            "id": "01DC6HYAKXG8FCN63D7DH06W84",
                            "type": "category-schemes"
                        },
                        "links": {
                            "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/category-schemes",
                            "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/category-schemes"
                        }
                    },
                    "parent-category": {
                        "data": {
                            "id": "01DC6HYAKX5NT8WBYWASQ9ENC8",
                            "type": "categories"
                        },
                        "links": {
                            "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/parent-categories",
                            "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/parent-categories"
                        }
                    }
                },
                "type": "categories"
            },
            "links": {
                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/parent-categories"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/categories/01DC6HYAKX53S13HCN2SBN4333/parent-categories',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_category_term_category_schemes(self):
        expected_payload = {
            "data": {
                "attributes": {
                    "acronym": "EXCATSCH1",
                    "description": "This category scheme is used as an example, for demonstration or testing "
                                   "purposes. The terms in this scheme, and resources they relates to, will not "
                                   "change.",
                    "name": "Example Category Scheme 1",
                    "revision": "2019-05-28",
                    "version": "1.0"
                },
                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                "links": {
                    "self": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84"
                },
                "relationships": {
                    "categories": {
                        "data": [
                            {
                                "id": "01DC6HYAKX993ZK6YHCVWAE169",
                                "type": "categories"
                            },
                            {
                                "id": "01DC6HYAKX5NT8WBYWASQ9ENC8",
                                "type": "categories"
                            },
                            {
                                "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                                "type": "categories"
                            },
                            {
                                "id": "01DC6HYAKX53S13HCN2SBN4333",
                                "type": "categories"
                            }
                        ],
                        "links": {
                            "related": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84/categories",
                            "self": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84/relationships/categories"
                        }
                    }
                },
                "type": "category-schemes"
            },
            "links": {
                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/category-schemes"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/categories/01DC6HYAKX53S13HCN2SBN4333/category-schemes',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_category_term_categorisations(self):
        expected_payload = {
            "data": [
                {
                    "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                    "links": {
                        "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG"
                    },
                    "relationships": {
                        "category": {
                            "data": {
                                "id": "01DC6HYAKX53S13HCN2SBN4333",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/categories",
                                "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/relationships/categories"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/projects",
                                "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/relationships/projects"
                            }
                        }
                    },
                    "type": "categorisations"
                }
            ],
            "links": {
                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/categorisations"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/categories/01DC6HYAKX53S13HCN2SBN4333/categorisations',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_categorisations_list(self):
        expected_payload = {
            "data": [
                {
                    "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                    "links": {
                        "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG"
                    },
                    "relationships": {
                        "category": {
                            "data": {
                                "id": "01DC6HYAKX53S13HCN2SBN4333",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/categories",
                                "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/relationships/categories"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/projects",
                                "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/relationships/projects"
                            }
                        }
                    },
                    "type": "categorisations"
                },
                {
                    "id": "01DC6HYAKY9ZEK8NQ1JGDMKCK7",
                    "links": {
                        "self": "http://localhost:9000/categorisations/01DC6HYAKY9ZEK8NQ1JGDMKCK7"
                    },
                    "relationships": {
                        "category": {
                            "data": {
                                "id": "01DC6HYAKXK6PMXX2TTTFTK5B4",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categorisations/01DC6HYAKY9ZEK8NQ1JGDMKCK7/categories",
                                "self": "http://localhost:9000/categorisations/01DC6HYAKY9ZEK8NQ1JGDMKCK7/relationships/categories"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01DB2ECBP2MB2Z9K1BSK5BND0V",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/categorisations/01DC6HYAKY9ZEK8NQ1JGDMKCK7/projects",
                                "self": "http://localhost:9000/categorisations/01DC6HYAKY9ZEK8NQ1JGDMKCK7/relationships/projects"
                            }
                        }
                    },
                    "type": "categorisations"
                }
            ],
            "included": [
                {
                    "attributes": {
                        "abstract": "This project is used as an example, for demonstration or testing purposes. The contents of this project, and resources it relates to, will not change. \n This example project (1) is a project with a single PI and single CoI belonging to the same organisation. It is also associated with a single grant and funder. The people, grants and organisations related to this project will not be related to another project. This project has an acronym, abstract, website and country property. The project duration is in the past. \n The remainder of this abstract is padding text to give a realistic abstract length. \n Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eget lorem eleifend turpis vestibulum sollicitudin. Curabitur libero nulla, maximus ut facilisis et, maximus quis dolor. Nunc ut malesuada felis. Sed volutpat et lectus vitae convallis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Fusce ullamcorper nec ante ut vulputate. Praesent ultricies mattis dolor quis ultrices. Ut sagittis scelerisque leo fringilla malesuada. Donec euismod tincidunt purus vel commodo. \n Aenean volutpat libero quis imperdiet tincidunt. Proin iaculis eros at turpis laoreet molestie. Quisque pellentesque, lorem id ornare fermentum, nunc urna ultrices libero, eget tempor ipsum lectus sollicitudin nibh. Sed sit amet vestibulum nulla. Vivamus dictum, dui id consectetur mattis, sapien erat tristique nulla, at lobortis enim nibh eu orci. Curabitur eu purus porttitor, rhoncus libero sed, mattis tellus. Praesent ullamcorper tincidunt ex. Vivamus lectus urna, dignissim sit amet efficitur a, malesuada at nisi. \n Curabitur auctor ut libero ac pharetra. Nunc rutrum facilisis felis, ac rhoncus lorem pulvinar quis. In felis neque, mollis nec sagittis feugiat, finibus maximus mauris. Nullam varius, risus id scelerisque tempor, justo purus malesuada nulla, eu sagittis purus arcu eget justo. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Fusce vel pretium augue. Pellentesque eu semper odio. Suspendisse congue varius est, et euismod justo accumsan sed. Etiam nec scelerisque risus, sed tempus ante. Proin fringilla leo urna, eget pulvinar leo placerat et. \n Etiam mollis lacus ut sapien elementum, sed volutpat dui faucibus. Fusce ligula risus, tempor at justo ac, tincidunt finibus magna. Duis eget sapien et nibh tincidunt faucibus. Duis tempus tincidunt leo. Aenean sit amet cursus ex. Etiam eget finibus nulla, a rutrum turpis. Proin imperdiet, augue consectetur varius varius, lectus elit egestas velit, ullamcorper pulvinar dolor felis at leo. Cras nec est ut est efficitur pulvinar nec vel nisi. Nullam sed elit eu ante finibus volutpat. Nam id diam a urna rutrum dictum. \n Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Integer accumsan et mi eu sagittis. Ut id nulla at quam efficitur molestie. Donec viverra ex vitae mauris ullamcorper elementum. Proin sed felis enim. Suspendisse potenti. Integer malesuada interdum mi, ornare semper lorem tempus condimentum. Cras sodales risus quis nibh fermentum volutpat. Sed vel tincidunt lectus.",
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
                        "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/allocations",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/allocations"
                            }
                        },
                        "categorisations": {
                            "data": [
                                {
                                    "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                                    "type": "categorisations"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/categorisations",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/categorisations"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/participants",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
                },
                {
                    "attributes": {
                        "aliases": [
                            "Third Term"
                        ],
                        "concept": "https://www.example.com/category-scheme-1/category-term-4",
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The contents of this term, and resources it relates to, will not change. \n This term (3) is a third level term with a second level term as a parent (2) and no child terms."
                        ],
                        "examples": [
                            "Example category term 3 - example"
                        ],
                        "notation": "1.2.3",
                        "notes": [
                            "Example category term 3 - note"
                        ],
                        "scheme": "https://www.example.com/category-scheme-1",
                        "scope-notes": [
                            "Example category term 3 - scope note"
                        ],
                        "title": "Example Category Term: Level 3"
                    },
                    "id": "01DC6HYAKX53S13HCN2SBN4333",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [
                                {
                                    "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                                    "type": "categorisations"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": {
                                "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                },
                {
                    "attributes": {
                        "acronym": "EXCATSCH1",
                        "description": "This category scheme is used as an example, for demonstration or testing purposes. The terms in this scheme, and resources they relates to, will not change.",
                        "name": "Example Category Scheme 1",
                        "revision": "2019-05-28",
                        "version": "1.0"
                    },
                    "id": "01DC6HYAKXG8FCN63D7DH06W84",
                    "links": {
                        "self": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84"
                    },
                    "relationships": {
                        "categories": {
                            "data": [
                                {
                                    "id": "01DC6HYAKX993ZK6YHCVWAE169",
                                    "type": "categories"
                                },
                                {
                                    "id": "01DC6HYAKX5NT8WBYWASQ9ENC8",
                                    "type": "categories"
                                },
                                {
                                    "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                                    "type": "categories"
                                },
                                {
                                    "id": "01DC6HYAKX53S13HCN2SBN4333",
                                    "type": "categories"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84/categories",
                                "self": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84/relationships/categories"
                            }
                        }
                    },
                    "type": "category-schemes"
                },
                {
                    "attributes": {
                        "aliases": [
                            "Second Term"
                        ],
                        "concept": "https://www.example.com/category-scheme-1/category-term-3",
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The contents of this term, and resources it relates to, will not change. \n This term (2) is a second level term with a first level term as a parent (1) and a single child term (3)."
                        ],
                        "examples": [
                            "Example category term 2 - example"
                        ],
                        "notation": "1.2",
                        "notes": [
                            "Example category term 2 - note"
                        ],
                        "scheme": "https://www.example.com/category-scheme-1",
                        "scope-notes": [
                            "Example category term 2 - scope note"
                        ],
                        "title": "Example Category Term: Level 2"
                    },
                    "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": {
                                "id": "01DC6HYAKX5NT8WBYWASQ9ENC8",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                },
                {
                    "attributes": {
                        "abstract": "This project is used as an example, for demonstration or testing purposes. The contents of this project, and resources it relates to, will not change. This example project (3) has a single PI and multiple CoIs belonging to different organisations. It is also associated with a single grant and funder. The resources related to this project will also relate to other projects. This project has an acronym and country properties, it does not have a website or publications. The project duration is in the future. \n The remainder of this abstract is padding text to give a realistic abstract length. \n Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eget lorem eleifend turpis vestibulum sollicitudin. Curabitur libero nulla, maximus ut facilisis et, maximus quis dolor. Nunc ut malesuada felis. Sed volutpat et lectus vitae convallis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Fusce ullamcorper nec ante ut vulputate. Praesent ultricies mattis dolor quis ultrices. Ut sagittis scelerisque leo fringilla malesuada. Donec euismod tincidunt purus vel commodo. \n Aenean volutpat libero quis imperdiet tincidunt. Proin iaculis eros at turpis laoreet molestie. Quisque pellentesque, lorem id ornare fermentum, nunc urna ultrices libero, eget tempor ipsum lectus sollicitudin nibh. Sed sit amet vestibulum nulla. Vivamus dictum, dui id consectetur mattis, sapien erat tristique nulla, at lobortis enim nibh eu orci. Curabitur eu purus porttitor, rhoncus libero sed, mattis tellus. Praesent ullamcorper tincidunt ex. Vivamus lectus urna, dignissim sit amet efficitur a, malesuada at nisi. \n Curabitur auctor ut libero ac pharetra. Nunc rutrum facilisis felis, ac rhoncus lorem pulvinar quis. In felis neque, mollis nec sagittis feugiat, finibus maximus mauris. Nullam varius, risus id scelerisque tempor, justo purus malesuada nulla, eu sagittis purus arcu eget justo. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Fusce vel pretium augue. Pellentesque eu semper odio. Suspendisse congue varius est, et euismod justo accumsan sed. Etiam nec scelerisque risus, sed tempus ante. Proin fringilla leo urna, eget pulvinar leo placerat et. \n Etiam mollis lacus ut sapien elementum, sed volutpat dui faucibus. Fusce ligula risus, tempor at justo ac, tincidunt finibus magna. Duis eget sapien et nibh tincidunt faucibus. Duis tempus tincidunt leo. Aenean sit amet cursus ex. Etiam eget finibus nulla, a rutrum turpis. Proin imperdiet, augue consectetur varius varius, lectus elit egestas velit, ullamcorper pulvinar dolor felis at leo. Cras nec est ut est efficitur pulvinar nec vel nisi. Nullam sed elit eu ante finibus volutpat. Nam id diam a urna rutrum dictum. \n Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Integer accumsan et mi eu sagittis. Ut id nulla at quam efficitur molestie. Donec viverra ex vitae mauris ullamcorper elementum. Proin sed felis enim. Suspendisse potenti. Integer malesuada interdum mi, ornare semper lorem tempus condimentum. Cras sodales risus quis nibh fermentum volutpat. Sed vel tincidunt lectus.",
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
                        "self": "http://localhost:9000/projects/01DB2ECBP2MB2Z9K1BSK5BND0V"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP2MB2Z9K1BSK5BND0V/allocations",
                                "self": "http://localhost:9000/projects/01DB2ECBP2MB2Z9K1BSK5BND0V/relationships/allocations"
                            }
                        },
                        "categorisations": {
                            "data": [
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
                            "links": {
                                "related": "http://localhost:9000/projects/01DB2ECBP2MB2Z9K1BSK5BND0V/categorisations",
                                "self": "http://localhost:9000/projects/01DB2ECBP2MB2Z9K1BSK5BND0V/relationships/categorisations"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP2MB2Z9K1BSK5BND0V/participants",
                                "self": "http://localhost:9000/projects/01DB2ECBP2MB2Z9K1BSK5BND0V/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
                },
                {
                    "attributes": {
                        "aliases": None,
                        "concept": "https://www.example.com/category-scheme-2/category-term-2",
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The contents of this term, and resources it relates to, will not change. \n This term (1A) is a first level term with the root term as a parent (0) and no child terms."
                        ],
                        "examples": None,
                        "notation": None,
                        "notes": None,
                        "scheme": "https://www.example.com/category-scheme-2",
                        "scope-notes": None,
                        "title": "Example Category Term: Level 1"
                    },
                    "id": "01DC6HYAKXK6PMXX2TTTFTK5B4",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKXK6PMXX2TTTFTK5B4"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [
                                {
                                    "id": "01DC6HYAKY9ZEK8NQ1JGDMKCK7",
                                    "type": "categorisations"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXK6PMXX2TTTFTK5B4/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKXK6PMXX2TTTFTK5B4/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXMK47A45KCHZBH0CQ",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXK6PMXX2TTTFTK5B4/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKXK6PMXX2TTTFTK5B4/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": {
                                "id": "01DC6HYAKXY0JT6583RCXTJY3Q",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXK6PMXX2TTTFTK5B4/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKXK6PMXX2TTTFTK5B4/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                },
                {
                    "attributes": {
                        "acronym": None,
                        "description": None,
                        "name": "Example Category Scheme 2",
                        "revision": None,
                        "version": None
                    },
                    "id": "01DC6HYAKXMK47A45KCHZBH0CQ",
                    "links": {
                        "self": "http://localhost:9000/category-schemes/01DC6HYAKXMK47A45KCHZBH0CQ"
                    },
                    "relationships": {
                        "categories": {
                            "data": [
                                {
                                    "id": "01DC6HYAKXY0JT6583RCXTJY3Q",
                                    "type": "categories"
                                },
                                {
                                    "id": "01DC6HYAKXK6PMXX2TTTFTK5B4",
                                    "type": "categories"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/category-schemes/01DC6HYAKXMK47A45KCHZBH0CQ/categories",
                                "self": "http://localhost:9000/category-schemes/01DC6HYAKXMK47A45KCHZBH0CQ/relationships/categories"
                            }
                        }
                    },
                    "type": "category-schemes"
                },
                {
                    "attributes": {
                        "aliases": None,
                        "concept": "https://www.example.com/category-scheme-2/category-term-1",
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The contents of this term, and resources it relates to, will not change. \n This term (0) is the root term with a single child term (1)."
                        ],
                        "examples": None,
                        "notation": None,
                        "notes": None,
                        "scheme": "https://www.example.com/category-scheme-2",
                        "scope-notes": None,
                        "title": "Example Category Term: 0"
                    },
                    "id": "01DC6HYAKXY0JT6583RCXTJY3Q",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKXY0JT6583RCXTJY3Q"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXY0JT6583RCXTJY3Q/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKXY0JT6583RCXTJY3Q/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXMK47A45KCHZBH0CQ",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXY0JT6583RCXTJY3Q/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKXY0JT6583RCXTJY3Q/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": None,
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXY0JT6583RCXTJY3Q/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKXY0JT6583RCXTJY3Q/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                }
            ],
            "links": {
                "first": "http://localhost:9000/categorisations?page=1",
                "last": "http://localhost:9000/categorisations?page=2",
                "next": "http://localhost:9000/categorisations?page=2",
                "prev": None,
                "self": "http://localhost:9000/categorisations?page=1"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/categorisations',
            base_url='http://localhost:9000',
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

    def test_categorisations_detail(self):
        expected_payload = {
            "data": {
                "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                "links": {
                    "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG"
                },
                "relationships": {
                    "category": {
                        "data": {
                            "id": "01DC6HYAKX53S13HCN2SBN4333",
                            "type": "categories"
                        },
                        "links": {
                            "related": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/categories",
                            "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/relationships/categories"
                        }
                    },
                    "project": {
                        "data": {
                            "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                            "type": "projects"
                        },
                        "links": {
                            "related": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/projects",
                            "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/relationships/projects"
                        }
                    }
                },
                "type": "categorisations"
            },
            "included": [
                {
                    "attributes": {
                        "acronym": "EXCATSCH1",
                        "description": "This category scheme is used as an example, for demonstration or testing "
                                       "purposes. The terms in this scheme, and resources they relates to, will not "
                                       "change.",
                        "name": "Example Category Scheme 1",
                        "revision": "2019-05-28",
                        "version": "1.0"
                    },
                    "id": "01DC6HYAKXG8FCN63D7DH06W84",
                    "links": {
                        "self": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84"
                    },
                    "relationships": {
                        "categories": {
                            "data": [
                                {
                                    "id": "01DC6HYAKX993ZK6YHCVWAE169",
                                    "type": "categories"
                                },
                                {
                                    "id": "01DC6HYAKX5NT8WBYWASQ9ENC8",
                                    "type": "categories"
                                },
                                {
                                    "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                                    "type": "categories"
                                },
                                {
                                    "id": "01DC6HYAKX53S13HCN2SBN4333",
                                    "type": "categories"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84/categories",
                                "self": "http://localhost:9000/category-schemes/01DC6HYAKXG8FCN63D7DH06W84/relationships/categories"
                            }
                        }
                    },
                    "type": "category-schemes"
                },
                {
                    "attributes": {
                        "aliases": [
                            "Third Term"
                        ],
                        "concept": "https://www.example.com/category-scheme-1/category-term-4",
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The "
                            "contents of this term, and resources it relates to, will not change. \n This term (3) is "
                            "a third level term with a second level term as a parent (2) and no child terms."
                        ],
                        "examples": [
                            "Example category term 3 - example"
                        ],
                        "notation": "1.2.3",
                        "notes": [
                            "Example category term 3 - note"
                        ],
                        "scheme": "https://www.example.com/category-scheme-1",
                        "scope-notes": [
                            "Example category term 3 - scope note"
                        ],
                        "title": "Example Category Term: Level 3"
                    },
                    "id": "01DC6HYAKX53S13HCN2SBN4333",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [
                                {
                                    "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                                    "type": "categorisations"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": {
                                "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
                },
                {
                    "attributes": {
                        "aliases": [
                            "Second Term"
                        ],
                        'concept': 'https://www.example.com/category-scheme-1/category-term-3',
                        "definitions": [
                            "This category term is used as an example, for demonstration or testing purposes. The "
                            "contents of this term, and resources it relates to, will not change. \n This term (2) is "
                            "a second level term with a first level term as a parent (1) and a single child term (3)."
                        ],
                        "examples": [
                            "Example category term 2 - example"
                        ],
                        "notation": "1.2",
                        "notes": [
                            "Example category term 2 - note"
                        ],
                        'scheme': 'https://www.example.com/category-scheme-1',
                        "scope-notes": [
                            "Example category term 2 - scope note"
                        ],
                        "title": "Example Category Term: Level 2"
                    },
                    "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                    "links": {
                        "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE"
                    },
                    "relationships": {
                        "categorisations": {
                            "data": [],
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/categorisations",
                                "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/categorisations"
                            }
                        },
                        "category-scheme": {
                            "data": {
                                "id": "01DC6HYAKXG8FCN63D7DH06W84",
                                "type": "category-schemes"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/category-schemes",
                                "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/category-schemes"
                            }
                        },
                        "parent-category": {
                            "data": {
                                "id": "01DC6HYAKX5NT8WBYWASQ9ENC8",
                                "type": "categories"
                            },
                            "links": {
                                "related": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/parent-categories",
                                "self": "http://localhost:9000/categories/01DC6HYAKXSM2ZRMVQ2P1PHKZE/relationships/parent-categories"
                            }
                        }
                    },
                    "type": "categories"
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
                                    "is padding text to give a realistic abstract length. \n Lorem ipsum dolor sit "
                                    "amet, consectetur adipiscing elit. Maecenas eget lorem eleifend turpis vestibulum "
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
                        "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/allocations",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/allocations"
                            }
                        },
                        "categorisations": {
                            "data": [
                                {
                                    "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                                    "type": "categorisations"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/categorisations",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/categorisations"
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
                                "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/participants",
                                "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
                }
            ],
            "links": {
                "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response['data'], expected_payload['data'])
        self.assertCountEqual(json_response['included'], expected_payload['included'])
        self.assertDictEqual(json_response['links'], expected_payload['links'])

    def test_categorisations_single_missing_unknown_id(self):
        error = ApiNotFoundError()
        expected_payload = self.util_prepare_expected_error_payload(error)

        for allocation_id in ['', 'unknown']:
            with self.subTest(allocation_id=allocation_id):
                token = self.util_create_auth_token()
                response = self.client.get(
                    f"/categorisations/{allocation_id}",
                    headers={'authorization': f"bearer {token}"},
                    base_url='http://localhost:9000'
                )
                json_response = response.get_json()
                json_response = self.util_prepare_error_response(json_response)
                self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
                self.assertDictEqual(json_response, expected_payload)

    def test_categorisations_relationship_projects(self):
        expected_payload = {
            "data": {
                "id": "01DB2ECBP24NHYV5KZQG2N3FS2",
                "type": "projects"
            },
            "links": {
                "related": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/projects",
                "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/relationships/projects"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/relationships/projects',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_categorisations_relationship_categories(self):
        expected_payload = {
            "data": {
                "id": "01DC6HYAKX53S13HCN2SBN4333",
                "type": "categories"
            },
            "links": {
                "related": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/categories",
                "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/relationships/categories"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/relationships/categories',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_categorisations_projects(self):
        expected_payload = {
            "data": {
                "attributes": {
                    "abstract": "This project is used as an example, for demonstration or testing purposes. The contents of "
                                "this project, and resources it relates to, will not change. \n This example project (1) is a "
                                "project with a single PI and single CoI belonging to the same organisation. It is also "
                                "associated with a single grant and funder. The people, grants and organisations related to "
                                "this project will not be related to another project. This project has an acronym, abstract, "
                                "website and country property. The project duration is in the past. \n The remainder of this "
                                "abstract is padding text to give a realistic abstract length. \n Lorem ipsum dolor sit amet, "
                                "consectetur adipiscing elit. Maecenas eget lorem eleifend turpis vestibulum sollicitudin. "
                                "Curabitur libero nulla, maximus ut facilisis et, maximus quis dolor. Nunc ut malesuada "
                                "felis. Sed volutpat et lectus vitae convallis. Class aptent taciti sociosqu ad litora "
                                "torquent per conubia nostra, per inceptos himenaeos. Fusce ullamcorper nec ante ut "
                                "vulputate. Praesent ultricies mattis dolor quis ultrices. Ut sagittis scelerisque leo "
                                "fringilla malesuada. Donec euismod tincidunt purus vel commodo. \n Aenean volutpat libero "
                                "quis imperdiet tincidunt. Proin iaculis eros at turpis laoreet molestie. Quisque "
                                "pellentesque, lorem id ornare fermentum, nunc urna ultrices libero, eget tempor ipsum "
                                "lectus sollicitudin nibh. Sed sit amet vestibulum nulla. Vivamus dictum, dui id consectetur "
                                "mattis, sapien erat tristique nulla, at lobortis enim nibh eu orci. Curabitur eu purus "
                                "porttitor, rhoncus libero sed, mattis tellus. Praesent ullamcorper tincidunt ex. Vivamus "
                                "lectus urna, dignissim sit amet efficitur a, malesuada at nisi. \n Curabitur auctor ut "
                                "libero ac pharetra. Nunc rutrum facilisis felis, ac rhoncus lorem pulvinar quis. In felis "
                                "neque, mollis nec sagittis feugiat, finibus maximus mauris. Nullam varius, risus id "
                                "scelerisque tempor, justo purus malesuada nulla, eu sagittis purus arcu eget justo. Orci "
                                "varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Fusce vel "
                                "pretium augue. Pellentesque eu semper odio. Suspendisse congue varius est, et euismod justo "
                                "accumsan sed. Etiam nec scelerisque risus, sed tempus ante. Proin fringilla leo urna, eget "
                                "pulvinar leo placerat et. \n Etiam mollis lacus ut sapien elementum, sed volutpat dui "
                                "faucibus. Fusce ligula risus, tempor at justo ac, tincidunt finibus magna. Duis eget sapien "
                                "et nibh tincidunt faucibus. Duis tempus tincidunt leo. Aenean sit amet cursus ex. Etiam "
                                "eget finibus nulla, a rutrum turpis. Proin imperdiet, augue consectetur varius varius, "
                                "lectus elit egestas velit, ullamcorper pulvinar dolor felis at leo. Cras nec est ut est "
                                "efficitur pulvinar nec vel nisi. Nullam sed elit eu ante finibus volutpat. Nam id diam a "
                                "urna rutrum dictum. \n Pellentesque habitant morbi tristique senectus et netus et malesuada "
                                "fames ac turpis egestas. Integer accumsan et mi eu sagittis. Ut id nulla at quam efficitur "
                                "molestie. Donec viverra ex vitae mauris ullamcorper elementum. Proin sed felis enim. "
                                "Suspendisse potenti. Integer malesuada interdum mi, ornare semper lorem tempus condimentum. "
                                "Cras sodales risus quis nibh fermentum volutpat. Sed vel tincidunt lectus.",
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
                    "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2"
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
                            "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/allocations",
                            "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/allocations"
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
                            'related': 'http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/categorisations',
                            'self': 'http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/categorisations'
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
                            "related": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/participants",
                            "self": "http://localhost:9000/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/participants"
                        }
                    }
                },
                "type": "projects"
            },
            "links": {
                "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/projects"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/projects',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_categorisations_categories(self):
        expected_payload = {
            "data": {
                "attributes": {
                    "aliases": [
                        "Third Term"
                    ],
                    "concept": "https://www.example.com/category-scheme-1/category-term-4",
                    "definitions": [
                        "This category term is used as an example, for demonstration or testing purposes. The "
                        "contents of this term, and resources it relates to, will not change. \n This term (3) is "
                        "a third level term with a second level term as a parent (2) and no child terms."
                    ],
                    "examples": [
                        "Example category term 3 - example"
                    ],
                    "notation": "1.2.3",
                    "notes": [
                        "Example category term 3 - note"
                    ],
                    "scheme": "https://www.example.com/category-scheme-1",
                    "scope-notes": [
                        "Example category term 3 - scope note"
                    ],
                    "title": "Example Category Term: Level 3"
                },
                "id": "01DC6HYAKX53S13HCN2SBN4333",
                "links": {
                    "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333"
                },
                "relationships": {
                    "categorisations": {
                        "data": [
                            {
                                "id": "01DC6HYAKYAXE7MZMD08QV5JWG",
                                "type": "categorisations"
                            }
                        ],
                        "links": {
                            "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/categorisations",
                            "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/categorisations"
                        }
                    },
                    "category-scheme": {
                        "data": {
                            "id": "01DC6HYAKXG8FCN63D7DH06W84",
                            "type": "category-schemes"
                        },
                        "links": {
                            "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/category-schemes",
                            "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/category-schemes"
                        }
                    },
                    "parent-category": {
                        "data": {
                            "id": "01DC6HYAKXSM2ZRMVQ2P1PHKZE",
                            "type": "categories"
                        },
                        "links": {
                            "related": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/parent-categories",
                            "self": "http://localhost:9000/categories/01DC6HYAKX53S13HCN2SBN4333/relationships/parent-categories"
                        }
                    }
                },
                "type": "categories"
            },
            "links": {
                "self": "http://localhost:9000/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/categories"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/categories',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)
