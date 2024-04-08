from http import HTTPStatus

from arctic_office_projects_api.errors import ApiNotFoundError

from tests.base_test import BaseResourceTestCase


class PeopleResourceTestCase(BaseResourceTestCase):
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
                        "lead-project": None,
                        "publications": [
                            "https://doi.org/10.5555/15822411",
                            "https://doi.org/10.5555/45284431",
                            "https://doi.org/10.5555/59959290"
                        ],
                        "reference": "EX-GRANT-0001",
                        "status": "closed",
                        "title": "Example grant 1",
                        "total-funds": {
                            "currency": {"iso-4217-code": "GBP", "major-symbol": "£"},
                            "value": "120000.00",
                        },
                        "website": "https://www.example.com",
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
                        "lead-project": None,
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
                        "lead-project": None,
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
                        "lead-project": None,
                        "project-duration": {
                            "end-instant": "2015-10-01",
                            "interval": "2012-03-01/2015-10-01",
                            "start-instant": "2012-03-01"
                        },
                        "lead-project": None,
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
                        "lead-project": None,
                        "publications": [
                            "https://doi.org/10.5555/15822411",
                            "https://doi.org/10.5555/45284431",
                            "https://doi.org/10.5555/59959290"
                        ],
                        "reference": "EX-GRANT-0001",
                        "status": "closed",
                        "title": "Example grant 1",
                        "total-funds": {
                            "currency": {"iso-4217-code": "GBP", "major-symbol": "£"},
                            "value": "120000.00",
                        },
                        "website": "https://www.example.com",
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

        self.maxDiff = None

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
                    "lead-project": None,
                    "publications": [
                        "https://doi.org/10.5555/15822411",
                        "https://doi.org/10.5555/45284431",
                        "https://doi.org/10.5555/59959290"
                    ],
                    "reference": "EX-GRANT-0001",
                    "status": "closed",
                    "title": "Example grant 1",
                        "total-funds": {
                            "currency": {"iso-4217-code": "GBP", "major-symbol": "£"},
                            "value": "120000.00",
                        },
                        "website": "https://www.example.com",
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
                    "lead-project": None,
                    "project-duration": {
                        "end-instant": "2015-10-01",
                        "interval": "2012-03-01/2015-10-01",
                        "start-instant": "2012-03-01"
                    },
                    "lead-project": None,
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
