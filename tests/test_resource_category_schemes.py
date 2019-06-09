from http import HTTPStatus

from arctic_office_projects_api.errors import ApiNotFoundError

from tests.base_test import BaseResourceTestCase


class CategorySchemesResourceTestCase(BaseResourceTestCase):
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
