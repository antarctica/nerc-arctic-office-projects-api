from http import HTTPStatus

from flask_migrate import Config, upgrade, downgrade, Migrate

from arctic_office_projects_api.meta.errors import ApiNotFoundError
from arctic_office_projects_api import db
from arctic_office_projects_api.models import Project, Person, Participant
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
            project = Project()
            project.seed(quantity=5)
            Person.seed(quantity=5)
            Participant.seed(quantity=1)
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
            'xxx',
            json_response['meta']['summary']
        )

    def test_projects_list(self):
        expected_payload_data_item = {
            "attributes": {
                "abstract": "The Arctic climate is changing twice as fast as the global average and these dramatic "
                            "changes are evident in the decreases in sea ice extent over the last few decades. The "
                            "lowest sea ice cover to date was recorded in 2007 and recent data suggests sea ice cover "
                            "this year may be even lower. Clouds play a major role in the Arctic climate and therefore "
                            "influence the extent of sea ice, but our understanding of these clouds is very poor. Low "
                            "level, visually thick, clouds in much of the world tend to have a cooling effect, because "
                            "they reflect sunlight back into space that would otherwise be absorbed at the surface. "
                            "However, in the Arctic this albedo effect is not as important because the surface, often "
                            "being covered in snow and ice, is already highly reflective and Arctic clouds therefore "
                            "tend to warm instead of cooling. Warming in the Arctic can, in turn, lead to sea ice "
                            "break-up which exposes dark underlying sea water. The sea water absorbs more of the sun's "
                            "energy, thus amplifying the original warming. Hence, small changes in cloud properties or "
                            "coverage can lead to dramatic changes in the Arctic climate; this is where the proposed "
                            "research project comes in. \n A large portion of clouds, including those found in the "
                            "Arctic region, are categorized as mixed phase clouds. This means they contain both "
                            "supercooled water droplets and ice crystals (for a demonstration of supercooled water "
                            "see: http://www.youtube.com/watch?v=0JtBZGXd5zo). Liquid cloud droplets can exist in a "
                            "supercooled state well below zero degrees centigrade without freezing. Freezing will, "
                            "however, be observed if the droplets contain a particle known as an ice nucleus that can "
                            "catalyze ice formation and growth. Ice formation dramatically alters a cloud's properties "
                            "and therefore its influence on climate. At lower latitudes, ice nuclei are typically made "
                            "up of desert dusts, soot or even bacteria. But the composition and source of ice nuclei "
                            "in the Arctic environment remains a mystery. \n A likely source of ice nuclei in the "
                            "Arctic is the ocean. Particles emitted at the sea surface, through the action of waves "
                            "breaking and bubble bursting, may serve as ice nuclei when they are lofted into the "
                            "atmosphere and are incorporated in cloud droplets. This source of ice nuclei has not yet "
                            "been quantified. We will be the first to make measurements of ice nuclei in the central "
                            "Arctic region. We will make measurements of ice nuclei in the surface layers of the sea "
                            "from a research ship as well as measuring airborne ice nuclei from the BAe-146 research "
                            "aircraft. \n The sea's surface contains a wide range of bacteria, viruses, plankton and "
                            "other materials which are ejected into the atmosphere and may cause ice to form. We will "
                            "use state-of-the-art equipment developed at Leeds to measure how well sea-derived "
                            "particles and particles sampled in the atmosphere nucleate ice. We will piggy back on a "
                            "NERC funded project called ACACCIA, which not only represents excellent value for money "
                            "(since the ship and aircraft are already paid for under ACCACIA), but is a unique "
                            "opportunity to access this remote region. \n Results from the proposed study will build "
                            "upon previous work performed in the Murray laboratory and generate quantitative results "
                            "that can be directly used to improve computer-based cloud, aerosol and climate models. "
                            "Our results will further our understanding of these mysterious and important mixed phase "
                            "clouds and, in turn, the global climate.",
                "access-duration": {
                    "end_instant": "2018-10-01",
                    "interval": "2013-03-01/2018-10-01",
                    "start_instant": "2013-03-01"
                },
                "acronym": "ACCACIA",
                "impact-statements": [
                    "We discovered that there is a source of atmospheric ice nucleating particles in the oceans "
                    "associated with organic material produced by plankton. This was published in a high impact study "
                    "in Nature in 2015 (https://doi.org/10.1038/nature14986). We have now also used this data in a "
                    "modelling study of the global distribution of ice nucleating particles which was published in "
                    "March 2017 (https://doi.org/10.5194/acp-17-3637-2017)."
                ],
                "notes": [
                    "You can follow the ACCACIA project via their blog as well as on Twitter under @_ACCACIA_."
                ],
                "project-duration": {
                    "end_instant": "2016-10-01",
                    "interval": "2013-03-01/2016-10-01",
                    "start_instant": "2013-03-01"
                },
                "publications": [
                    "https://doi.org/10.5194/acp-2018-283",
                    "https://doi.org/10.5194/acp-15-3719-2015",
                    "https://doi.org/10.5194/acp-15-5599-2015",
                    "https://doi.org/10.5194/acp-16-4063-2016"
                ],
                "title": "Aerosol-Cloud Coupling And Climate Interactions in the Arctic",
                "website": "http://arp.arctic.ac.uk/projects/aerosol-cloud-coupling-and-climate-interactions-ar/"
            },
            "id": "01D5M0CFQV4M7JASW7F87SRDYB",
            "links": {
                "self": "http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB"
            },
            "relationships": {
                "participants": {
                    "data": [
                        {
                            "id": "01D5T4N25RV2062NVVQKZ9NBYX",
                            "type": "participants"
                        }
                    ],
                    "links": {
                        "related": "http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB/participants",
                        "self": "http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB/relationships/participants"
                    }
                }
            },
            "type": "projects"
        }
        expected_payload_links = {
            'first': 'http://localhost:9000/projects?page=1',
            'prev': None,
            'self': 'http://localhost:9000/projects?page=1',
            'next': 'http://localhost:9000/projects?page=2',
            'last': 'http://localhost:9000/projects?page=3'
        }

        expected_payload_included_items = list()
        expected_payload_included_items.append(
            {
                "attributes": {
                    "role": {
                        "class": "http://purl.org/spar/scoro/InvestigationRole",
                        "description": "The principle investigator of the research project.",
                        "member": "http://purl.org/spar/scoro/principle-investigator",
                        "title": "principle investigator"
                    }
                },
                "id": "01D5T4N25RV2062NVVQKZ9NBYX",
                "links": {
                    "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX"
                },
                "relationships": {
                    "person": {
                        "data": {
                            "id": "01D5MHQN3ZPH47YVSVQEVB0DAE",
                            "type": "people"
                        },
                        "links": {
                            "related": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/people",
                            "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/relationships/people"
                        }
                    },
                    "project": {
                        "data": {
                            "id": "01D5M0CFQV4M7JASW7F87SRDYB",
                            "type": "projects"
                        },
                        "links": {
                            "related": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/projects",
                            "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/relationships/projects"
                        }
                    }
                },
                "type": "participants"
            }
        )
        expected_payload_included_items.append(
            {
                "attributes": {
                    "avatar-url": "https://cdn.web.bas.ac.uk/bas-registers-service/v1/sample-avatars/conwat/conwat-256.jpg",
                    "first-name": "Constance",
                    "last-name": "Watson",
                    "orcid-id": "https://sandbox.orcid.org/0000-0001-8373-6934"
                },
                "id": "01D5MHQN3ZPH47YVSVQEVB0DAE",
                "links": {
                    "self": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE"
                },
                "relationships": {
                    "participation": {
                        "data": [
                            {
                                "id": "01D5T4N25RV2062NVVQKZ9NBYX",
                                "type": "participants"
                            }
                        ],
                        "links": {
                            "related": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE/participants",
                            "self": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE/relationships/participants"
                        }
                    }
                },
                "type": "people"
            }
        )

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
        self.assertIn('data', json_response.keys())
        self.assertEqual(2, len(json_response['data']))
        self.assertDictEqual(json_response['data'][0], expected_payload_data_item)
        self.assertIn('links', json_response.keys())
        self.assertDictEqual(json_response['links'], expected_payload_links)
        self.assertIn('included', json_response.keys())
        # noinspection PyTypeChecker
        self.assertListEqual(json_response['included'], expected_payload_included_items)

    def test_projects_detail(self):
        expected_payload = {
            "data": {
                "attributes": {
                    "abstract": "The Arctic climate is changing twice as fast as the global average and these dramatic "
                                "changes are evident in the decreases in sea ice extent over the last few decades. The "
                                "lowest sea ice cover to date was recorded in 2007 and recent data suggests sea ice cover "
                                "this year may be even lower. Clouds play a major role in the Arctic climate and therefore "
                                "influence the extent of sea ice, but our understanding of these clouds is very poor. Low "
                                "level, visually thick, clouds in much of the world tend to have a cooling effect, because "
                                "they reflect sunlight back into space that would otherwise be absorbed at the surface. "
                                "However, in the Arctic this albedo effect is not as important because the surface, often "
                                "being covered in snow and ice, is already highly reflective and Arctic clouds therefore "
                                "tend to warm instead of cooling. Warming in the Arctic can, in turn, lead to sea ice "
                                "break-up which exposes dark underlying sea water. The sea water absorbs more of the sun's "
                                "energy, thus amplifying the original warming. Hence, small changes in cloud properties or "
                                "coverage can lead to dramatic changes in the Arctic climate; this is where the proposed "
                                "research project comes in. \n A large portion of clouds, including those found in the "
                                "Arctic region, are categorized as mixed phase clouds. This means they contain both "
                                "supercooled water droplets and ice crystals (for a demonstration of supercooled water "
                                "see: http://www.youtube.com/watch?v=0JtBZGXd5zo). Liquid cloud droplets can exist in a "
                                "supercooled state well below zero degrees centigrade without freezing. Freezing will, "
                                "however, be observed if the droplets contain a particle known as an ice nucleus that can "
                                "catalyze ice formation and growth. Ice formation dramatically alters a cloud's properties "
                                "and therefore its influence on climate. At lower latitudes, ice nuclei are typically made "
                                "up of desert dusts, soot or even bacteria. But the composition and source of ice nuclei "
                                "in the Arctic environment remains a mystery. \n A likely source of ice nuclei in the "
                                "Arctic is the ocean. Particles emitted at the sea surface, through the action of waves "
                                "breaking and bubble bursting, may serve as ice nuclei when they are lofted into the "
                                "atmosphere and are incorporated in cloud droplets. This source of ice nuclei has not yet "
                                "been quantified. We will be the first to make measurements of ice nuclei in the central "
                                "Arctic region. We will make measurements of ice nuclei in the surface layers of the sea "
                                "from a research ship as well as measuring airborne ice nuclei from the BAe-146 research "
                                "aircraft. \n The sea's surface contains a wide range of bacteria, viruses, plankton and "
                                "other materials which are ejected into the atmosphere and may cause ice to form. We will "
                                "use state-of-the-art equipment developed at Leeds to measure how well sea-derived "
                                "particles and particles sampled in the atmosphere nucleate ice. We will piggy back on a "
                                "NERC funded project called ACACCIA, which not only represents excellent value for money "
                                "(since the ship and aircraft are already paid for under ACCACIA), but is a unique "
                                "opportunity to access this remote region. \n Results from the proposed study will build "
                                "upon previous work performed in the Murray laboratory and generate quantitative results "
                                "that can be directly used to improve computer-based cloud, aerosol and climate models. "
                                "Our results will further our understanding of these mysterious and important mixed phase "
                                "clouds and, in turn, the global climate.",
                    "access-duration": {
                        "end_instant": "2018-10-01",
                        "interval": "2013-03-01/2018-10-01",
                        "start_instant": "2013-03-01"
                    },
                    "acronym": "ACCACIA",
                    "impact-statements": [
                        "We discovered that there is a source of atmospheric ice nucleating particles in the oceans "
                        "associated with organic material produced by plankton. This was published in a high impact study "
                        "in Nature in 2015 (https://doi.org/10.1038/nature14986). We have now also used this data in a "
                        "modelling study of the global distribution of ice nucleating particles which was published in "
                        "March 2017 (https://doi.org/10.5194/acp-17-3637-2017)."
                    ],
                    "notes": [
                        "You can follow the ACCACIA project via their blog as well as on Twitter under @_ACCACIA_."
                    ],
                    "project-duration": {
                        "end_instant": "2016-10-01",
                        "interval": "2013-03-01/2016-10-01",
                        "start_instant": "2013-03-01"
                    },
                    "publications": [
                        "https://doi.org/10.5194/acp-2018-283",
                        "https://doi.org/10.5194/acp-15-3719-2015",
                        "https://doi.org/10.5194/acp-15-5599-2015",
                        "https://doi.org/10.5194/acp-16-4063-2016"
                    ],
                    "title": "Aerosol-Cloud Coupling And Climate Interactions in the Arctic",
                    "website": "http://arp.arctic.ac.uk/projects/aerosol-cloud-coupling-and-climate-interactions-ar/"
                },
                "id": "01D5M0CFQV4M7JASW7F87SRDYB",
                "links": {
                    "self": "http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB"
                },
                "relationships": {
                    "participants": {
                        "data": [
                            {
                                "id": "01D5T4N25RV2062NVVQKZ9NBYX",
                                "type": "participants"
                            }
                        ],
                        "links": {
                            "related": "http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB/participants",
                            "self": "http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB/relationships/participants"
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
                    "id": "01D5T4N25RV2062NVVQKZ9NBYX",
                    "links": {
                        "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01D5MHQN3ZPH47YVSVQEVB0DAE",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/people",
                                "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01D5M0CFQV4M7JASW7F87SRDYB",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/projects",
                                "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/relationships/projects"
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
                    "id": "01D5MHQN3ZPH47YVSVQEVB0DAE",
                    "links": {
                        "self": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE"
                    },
                    "relationships": {
                        "participation": {
                            "data": [
                                {
                                    "id": "01D5T4N25RV2062NVVQKZ9NBYX",
                                    "type": "participants"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE/participants",
                                "self": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE/relationships/participants"
                            }
                        }
                    },
                    "type": "people"
                }
            ],
            "links": {
                "self": "http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/projects/01D5M0CFQV4M7JASW7F87SRDYB',
            headers={'authorization': f"bearer { token }"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_projects_single_missing_unknown_id(self):
        error = ApiNotFoundError()
        expected_payload = self.util_prepare_expected_error_payload(error)

        for project_id in ['', 'unknown']:
            with self.subTest(project_id=project_id):
                token = self.util_create_auth_token()
                response = self.client.get(
                    f"/projects/{ project_id }",
                    headers={'authorization': f"bearer { token }"},
                    base_url='http://localhost:9000'
                )
                json_response = response.get_json()
                json_response = self.util_prepare_error_response(json_response)
                self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
                self.assertDictEqual(json_response, expected_payload)

    def test_projects_relationship_participants(self):
        expected_payload = {
            "data": [
                {
                    "id": "01D5T4N25RV2062NVVQKZ9NBYX",
                    "type": "participants"
                }
            ],
            "links": {
                "related": "http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB/participants",
                "self": "http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB/relationships/participants"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/projects/01D5M0CFQV4M7JASW7F87SRDYB/relationships/participants',
            headers={'authorization': f"bearer { token }"},
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
                    "id": "01D5T4N25RV2062NVVQKZ9NBYX",
                    "links": {
                        "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01D5MHQN3ZPH47YVSVQEVB0DAE",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/people",
                                "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01D5M0CFQV4M7JASW7F87SRDYB",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/projects",
                                "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/relationships/projects"
                            }
                        }
                    },
                    "type": "participants"
                }
            ],
            "links": {
                "self": "http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB/relationships/participants"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/projects/01D5M0CFQV4M7JASW7F87SRDYB/participants',
            headers={'authorization': f"bearer { token }"},
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
                    "id": "01D5T4N25RV2062NVVQKZ9NBYX",
                    "links": {
                        "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01D5MHQN3ZPH47YVSVQEVB0DAE",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/people",
                                "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01D5M0CFQV4M7JASW7F87SRDYB",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/projects",
                                "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/relationships/projects"
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
                    "id": "01D5MHQN3ZPH47YVSVQEVB0DAE",
                    "links": {
                        "self": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE"
                    },
                    "relationships": {
                        "participation": {
                            "data": [
                                {
                                    "id": "01D5T4N25RV2062NVVQKZ9NBYX",
                                    "type": "participants"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE/participants",
                                "self": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE/relationships/participants"
                            }
                        }
                    },
                    "type": "people"
                },
                {
                    "attributes": {
                        "abstract": "The Arctic climate is changing twice as fast as the global average and these dramatic "
                                    "changes are evident in the decreases in sea ice extent over the last few decades. The "
                                    "lowest sea ice cover to date was recorded in 2007 and recent data suggests sea ice cover "
                                    "this year may be even lower. Clouds play a major role in the Arctic climate and therefore "
                                    "influence the extent of sea ice, but our understanding of these clouds is very poor. Low "
                                    "level, visually thick, clouds in much of the world tend to have a cooling effect, because "
                                    "they reflect sunlight back into space that would otherwise be absorbed at the surface. "
                                    "However, in the Arctic this albedo effect is not as important because the surface, often "
                                    "being covered in snow and ice, is already highly reflective and Arctic clouds therefore "
                                    "tend to warm instead of cooling. Warming in the Arctic can, in turn, lead to sea ice "
                                    "break-up which exposes dark underlying sea water. The sea water absorbs more of the sun's "
                                    "energy, thus amplifying the original warming. Hence, small changes in cloud properties or "
                                    "coverage can lead to dramatic changes in the Arctic climate; this is where the proposed "
                                    "research project comes in. \n A large portion of clouds, including those found in the "
                                    "Arctic region, are categorized as mixed phase clouds. This means they contain both "
                                    "supercooled water droplets and ice crystals (for a demonstration of supercooled water "
                                    "see: http://www.youtube.com/watch?v=0JtBZGXd5zo). Liquid cloud droplets can exist in a "
                                    "supercooled state well below zero degrees centigrade without freezing. Freezing will, "
                                    "however, be observed if the droplets contain a particle known as an ice nucleus that can "
                                    "catalyze ice formation and growth. Ice formation dramatically alters a cloud's properties "
                                    "and therefore its influence on climate. At lower latitudes, ice nuclei are typically made "
                                    "up of desert dusts, soot or even bacteria. But the composition and source of ice nuclei "
                                    "in the Arctic environment remains a mystery. \n A likely source of ice nuclei in the "
                                    "Arctic is the ocean. Particles emitted at the sea surface, through the action of waves "
                                    "breaking and bubble bursting, may serve as ice nuclei when they are lofted into the "
                                    "atmosphere and are incorporated in cloud droplets. This source of ice nuclei has not yet "
                                    "been quantified. We will be the first to make measurements of ice nuclei in the central "
                                    "Arctic region. We will make measurements of ice nuclei in the surface layers of the sea "
                                    "from a research ship as well as measuring airborne ice nuclei from the BAe-146 research "
                                    "aircraft. \n The sea's surface contains a wide range of bacteria, viruses, plankton and "
                                    "other materials which are ejected into the atmosphere and may cause ice to form. We will "
                                    "use state-of-the-art equipment developed at Leeds to measure how well sea-derived "
                                    "particles and particles sampled in the atmosphere nucleate ice. We will piggy back on a "
                                    "NERC funded project called ACACCIA, which not only represents excellent value for money "
                                    "(since the ship and aircraft are already paid for under ACCACIA), but is a unique "
                                    "opportunity to access this remote region. \n Results from the proposed study will build "
                                    "upon previous work performed in the Murray laboratory and generate quantitative results "
                                    "that can be directly used to improve computer-based cloud, aerosol and climate models. "
                                    "Our results will further our understanding of these mysterious and important mixed phase "
                                    "clouds and, in turn, the global climate.",
                        "access-duration": {
                            "end_instant": "2018-10-01",
                            "interval": "2013-03-01/2018-10-01",
                            "start_instant": "2013-03-01"
                        },
                        "acronym": "ACCACIA",
                        "impact-statements": [
                            "We discovered that there is a source of atmospheric ice nucleating particles in the oceans "
                            "associated with organic material produced by plankton. This was published in a high impact study "
                            "in Nature in 2015 (https://doi.org/10.1038/nature14986). We have now also used this data in a "
                            "modelling study of the global distribution of ice nucleating particles which was published in "
                            "March 2017 (https://doi.org/10.5194/acp-17-3637-2017)."
                        ],
                        "notes": [
                            "You can follow the ACCACIA project via their blog as well as on Twitter under @_ACCACIA_."
                        ],
                        "project-duration": {
                            "end_instant": "2016-10-01",
                            "interval": "2013-03-01/2016-10-01",
                            "start_instant": "2013-03-01"
                        },
                        "publications": [
                            "https://doi.org/10.5194/acp-2018-283",
                            "https://doi.org/10.5194/acp-15-3719-2015",
                            "https://doi.org/10.5194/acp-15-5599-2015",
                            "https://doi.org/10.5194/acp-16-4063-2016"
                        ],
                        "title": "Aerosol-Cloud Coupling And Climate Interactions in the Arctic",
                        "website": "http://arp.arctic.ac.uk/projects/aerosol-cloud-coupling-and-climate-interactions-ar/"
                    },
                    "id": "01D5M0CFQV4M7JASW7F87SRDYB",
                    "links": {
                        "self": "http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB"
                    },
                    "relationships": {
                        "participants": {
                            "data": [
                                {
                                    "id": "01D5T4N25RV2062NVVQKZ9NBYX",
                                    "type": "participants"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB/participants",
                                "self": "http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
                }
            ],
            "links": {
                "first": "http://localhost:9000/participants?page=1",
                "last": "http://localhost:9000/participants?page=1",
                "next": None,
                "prev": None,
                "self": "http://localhost:9000/participants?page=1"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/participants',
            headers={'authorization': f"bearer { token }"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

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
                "id": "01D5T4N25RV2062NVVQKZ9NBYX",
                "links": {
                    "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX"
                },
                "relationships": {
                    "person": {
                        "data": {
                            "id": "01D5MHQN3ZPH47YVSVQEVB0DAE",
                            "type": "people"
                        },
                        "links": {
                            "related": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/people",
                            "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/relationships/people"
                        }
                    },
                    "project": {
                        "data": {
                            "id": "01D5M0CFQV4M7JASW7F87SRDYB",
                            "type": "projects"
                        },
                        "links": {
                            "related": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/projects",
                            "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/relationships/projects"
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
                    "id": "01D5MHQN3ZPH47YVSVQEVB0DAE",
                    "links": {
                        "self": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE"
                    },
                    "relationships": {
                        "participation": {
                            "data": [
                                {
                                    "id": "01D5T4N25RV2062NVVQKZ9NBYX",
                                    "type": "participants"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE/participants",
                                "self": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE/relationships/participants"
                            }
                        }
                    },
                    "type": "people"
                },
                {
                    "attributes": {
                        "abstract": "The Arctic climate is changing twice as fast as the global average and these dramatic "
                                    "changes are evident in the decreases in sea ice extent over the last few decades. The "
                                    "lowest sea ice cover to date was recorded in 2007 and recent data suggests sea ice cover "
                                    "this year may be even lower. Clouds play a major role in the Arctic climate and therefore "
                                    "influence the extent of sea ice, but our understanding of these clouds is very poor. Low "
                                    "level, visually thick, clouds in much of the world tend to have a cooling effect, because "
                                    "they reflect sunlight back into space that would otherwise be absorbed at the surface. "
                                    "However, in the Arctic this albedo effect is not as important because the surface, often "
                                    "being covered in snow and ice, is already highly reflective and Arctic clouds therefore "
                                    "tend to warm instead of cooling. Warming in the Arctic can, in turn, lead to sea ice "
                                    "break-up which exposes dark underlying sea water. The sea water absorbs more of the sun's "
                                    "energy, thus amplifying the original warming. Hence, small changes in cloud properties or "
                                    "coverage can lead to dramatic changes in the Arctic climate; this is where the proposed "
                                    "research project comes in. \n A large portion of clouds, including those found in the "
                                    "Arctic region, are categorized as mixed phase clouds. This means they contain both "
                                    "supercooled water droplets and ice crystals (for a demonstration of supercooled water "
                                    "see: http://www.youtube.com/watch?v=0JtBZGXd5zo). Liquid cloud droplets can exist in a "
                                    "supercooled state well below zero degrees centigrade without freezing. Freezing will, "
                                    "however, be observed if the droplets contain a particle known as an ice nucleus that can "
                                    "catalyze ice formation and growth. Ice formation dramatically alters a cloud's properties "
                                    "and therefore its influence on climate. At lower latitudes, ice nuclei are typically made "
                                    "up of desert dusts, soot or even bacteria. But the composition and source of ice nuclei "
                                    "in the Arctic environment remains a mystery. \n A likely source of ice nuclei in the "
                                    "Arctic is the ocean. Particles emitted at the sea surface, through the action of waves "
                                    "breaking and bubble bursting, may serve as ice nuclei when they are lofted into the "
                                    "atmosphere and are incorporated in cloud droplets. This source of ice nuclei has not yet "
                                    "been quantified. We will be the first to make measurements of ice nuclei in the central "
                                    "Arctic region. We will make measurements of ice nuclei in the surface layers of the sea "
                                    "from a research ship as well as measuring airborne ice nuclei from the BAe-146 research "
                                    "aircraft. \n The sea's surface contains a wide range of bacteria, viruses, plankton and "
                                    "other materials which are ejected into the atmosphere and may cause ice to form. We will "
                                    "use state-of-the-art equipment developed at Leeds to measure how well sea-derived "
                                    "particles and particles sampled in the atmosphere nucleate ice. We will piggy back on a "
                                    "NERC funded project called ACACCIA, which not only represents excellent value for money "
                                    "(since the ship and aircraft are already paid for under ACCACIA), but is a unique "
                                    "opportunity to access this remote region. \n Results from the proposed study will build "
                                    "upon previous work performed in the Murray laboratory and generate quantitative results "
                                    "that can be directly used to improve computer-based cloud, aerosol and climate models. "
                                    "Our results will further our understanding of these mysterious and important mixed phase "
                                    "clouds and, in turn, the global climate.",
                        "access-duration": {
                            "end_instant": "2018-10-01",
                            "interval": "2013-03-01/2018-10-01",
                            "start_instant": "2013-03-01"
                        },
                        "acronym": "ACCACIA",
                        "impact-statements": [
                            "We discovered that there is a source of atmospheric ice nucleating particles in the oceans "
                            "associated with organic material produced by plankton. This was published in a high impact study "
                            "in Nature in 2015 (https://doi.org/10.1038/nature14986). We have now also used this data in a "
                            "modelling study of the global distribution of ice nucleating particles which was published in "
                            "March 2017 (https://doi.org/10.5194/acp-17-3637-2017)."
                        ],
                        "notes": [
                            "You can follow the ACCACIA project via their blog as well as on Twitter under @_ACCACIA_."
                        ],
                        "project-duration": {
                            "end_instant": "2016-10-01",
                            "interval": "2013-03-01/2016-10-01",
                            "start_instant": "2013-03-01"
                        },
                        "publications": [
                            "https://doi.org/10.5194/acp-2018-283",
                            "https://doi.org/10.5194/acp-15-3719-2015",
                            "https://doi.org/10.5194/acp-15-5599-2015",
                            "https://doi.org/10.5194/acp-16-4063-2016"
                        ],
                        "title": "Aerosol-Cloud Coupling And Climate Interactions in the Arctic",
                        "website": "http://arp.arctic.ac.uk/projects/aerosol-cloud-coupling-and-climate-interactions-ar/"
                    },
                    "id": "01D5M0CFQV4M7JASW7F87SRDYB",
                    "links": {
                        "self": "http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB"
                    },
                    "relationships": {
                        "participants": {
                            "data": [
                                {
                                    "id": "01D5T4N25RV2062NVVQKZ9NBYX",
                                    "type": "participants"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB/participants",
                                "self": "http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
                }
            ],
            "links": {
                "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/participants/01D5T4N25RV2062NVVQKZ9NBYX',
            headers={'authorization': f"bearer { token }"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_participants_single_missing_unknown_id(self):
        error = ApiNotFoundError()
        expected_payload = self.util_prepare_expected_error_payload(error)

        for participant_id in ['', 'unknown']:
            with self.subTest(participant_id=participant_id):
                token = self.util_create_auth_token()
                response = self.client.get(
                    f"/participants/{ participant_id }",
                    headers={'authorization': f"bearer { token }"},
                    base_url='http://localhost:9000'
                )
                json_response = response.get_json()
                json_response = self.util_prepare_error_response(json_response)
                self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
                self.assertDictEqual(json_response, expected_payload)

    def test_participants_relationship_projects(self):
        expected_payload = {
            "data": {
                "id": "01D5M0CFQV4M7JASW7F87SRDYB",
                "type": "projects"
            },
            "links": {
                "related": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/projects",
                "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/relationships/projects"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/participants/01D5T4N25RV2062NVVQKZ9NBYX/relationships/projects',
            headers={'authorization': f"bearer { token }"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_participants_relationship_people(self):
        expected_payload = {
            "data": {
                "id": "01D5MHQN3ZPH47YVSVQEVB0DAE",
                "type": "people"
            },
            "links": {
                "related": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/people",
                "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/relationships/people"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/participants/01D5T4N25RV2062NVVQKZ9NBYX/relationships/people',
            headers={'authorization': f"bearer { token }"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_participants_projects(self):
        expected_payload = {
            "data": {
                "attributes": {
                    "abstract": "The Arctic climate is changing twice as fast as the global average and these dramatic "
                                "changes are evident in the decreases in sea ice extent over the last few decades. The "
                                "lowest sea ice cover to date was recorded in 2007 and recent data suggests sea ice cover "
                                "this year may be even lower. Clouds play a major role in the Arctic climate and therefore "
                                "influence the extent of sea ice, but our understanding of these clouds is very poor. Low "
                                "level, visually thick, clouds in much of the world tend to have a cooling effect, because "
                                "they reflect sunlight back into space that would otherwise be absorbed at the surface. "
                                "However, in the Arctic this albedo effect is not as important because the surface, often "
                                "being covered in snow and ice, is already highly reflective and Arctic clouds therefore "
                                "tend to warm instead of cooling. Warming in the Arctic can, in turn, lead to sea ice "
                                "break-up which exposes dark underlying sea water. The sea water absorbs more of the sun's "
                                "energy, thus amplifying the original warming. Hence, small changes in cloud properties or "
                                "coverage can lead to dramatic changes in the Arctic climate; this is where the proposed "
                                "research project comes in. \n A large portion of clouds, including those found in the "
                                "Arctic region, are categorized as mixed phase clouds. This means they contain both "
                                "supercooled water droplets and ice crystals (for a demonstration of supercooled water "
                                "see: http://www.youtube.com/watch?v=0JtBZGXd5zo). Liquid cloud droplets can exist in a "
                                "supercooled state well below zero degrees centigrade without freezing. Freezing will, "
                                "however, be observed if the droplets contain a particle known as an ice nucleus that can "
                                "catalyze ice formation and growth. Ice formation dramatically alters a cloud's properties "
                                "and therefore its influence on climate. At lower latitudes, ice nuclei are typically made "
                                "up of desert dusts, soot or even bacteria. But the composition and source of ice nuclei "
                                "in the Arctic environment remains a mystery. \n A likely source of ice nuclei in the "
                                "Arctic is the ocean. Particles emitted at the sea surface, through the action of waves "
                                "breaking and bubble bursting, may serve as ice nuclei when they are lofted into the "
                                "atmosphere and are incorporated in cloud droplets. This source of ice nuclei has not yet "
                                "been quantified. We will be the first to make measurements of ice nuclei in the central "
                                "Arctic region. We will make measurements of ice nuclei in the surface layers of the sea "
                                "from a research ship as well as measuring airborne ice nuclei from the BAe-146 research "
                                "aircraft. \n The sea's surface contains a wide range of bacteria, viruses, plankton and "
                                "other materials which are ejected into the atmosphere and may cause ice to form. We will "
                                "use state-of-the-art equipment developed at Leeds to measure how well sea-derived "
                                "particles and particles sampled in the atmosphere nucleate ice. We will piggy back on a "
                                "NERC funded project called ACACCIA, which not only represents excellent value for money "
                                "(since the ship and aircraft are already paid for under ACCACIA), but is a unique "
                                "opportunity to access this remote region. \n Results from the proposed study will build "
                                "upon previous work performed in the Murray laboratory and generate quantitative results "
                                "that can be directly used to improve computer-based cloud, aerosol and climate models. "
                                "Our results will further our understanding of these mysterious and important mixed phase "
                                "clouds and, in turn, the global climate.",
                    "access-duration": {
                        "end_instant": "2018-10-01",
                        "interval": "2013-03-01/2018-10-01",
                        "start_instant": "2013-03-01"
                    },
                    "acronym": "ACCACIA",
                    "impact-statements": [
                        "We discovered that there is a source of atmospheric ice nucleating particles in the oceans "
                        "associated with organic material produced by plankton. This was published in a high impact study "
                        "in Nature in 2015 (https://doi.org/10.1038/nature14986). We have now also used this data in a "
                        "modelling study of the global distribution of ice nucleating particles which was published in "
                        "March 2017 (https://doi.org/10.5194/acp-17-3637-2017)."
                    ],
                    "notes": [
                        "You can follow the ACCACIA project via their blog as well as on Twitter under @_ACCACIA_."
                    ],
                    "project-duration": {
                        "end_instant": "2016-10-01",
                        "interval": "2013-03-01/2016-10-01",
                        "start_instant": "2013-03-01"
                    },
                    "publications": [
                        "https://doi.org/10.5194/acp-2018-283",
                        "https://doi.org/10.5194/acp-15-3719-2015",
                        "https://doi.org/10.5194/acp-15-5599-2015",
                        "https://doi.org/10.5194/acp-16-4063-2016"
                    ],
                    "title": "Aerosol-Cloud Coupling And Climate Interactions in the Arctic",
                    "website": "http://arp.arctic.ac.uk/projects/aerosol-cloud-coupling-and-climate-interactions-ar/"
                },
                "id": "01D5M0CFQV4M7JASW7F87SRDYB",
                "links": {
                    "self": "http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB"
                },
                "relationships": {
                    "participants": {
                        "data": [
                            {
                                "id": "01D5T4N25RV2062NVVQKZ9NBYX",
                                "type": "participants"
                            }
                        ],
                        "links": {
                            "related": "http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB/participants",
                            "self": "http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB/relationships/participants"
                        }
                    }
                },
                "type": "projects"
            },
            "links": {
                "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/relationships/projects"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/participants/01D5T4N25RV2062NVVQKZ9NBYX/projects',
            headers={'authorization': f"bearer { token }"},
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
                "id": "01D5MHQN3ZPH47YVSVQEVB0DAE",
                "links": {
                    "self": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE"
                },
                "relationships": {
                    "participation": {
                        "data": [
                            {
                                "id": "01D5T4N25RV2062NVVQKZ9NBYX",
                                "type": "participants"
                            }
                        ],
                        "links": {
                            "related": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE/participants",
                            "self": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE/relationships/participants"
                        }
                    }
                },
                "type": "people"
            },
            "links": {
                "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/relationships/people"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/participants/01D5T4N25RV2062NVVQKZ9NBYX/people',
            headers={'authorization': f"bearer { token }"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_people_list(self):
        expected_payload_data_item = {
            "attributes": {
                "avatar-url": "https://cdn.web.bas.ac.uk/bas-registers-service/v1/sample-avatars/conwat/conwat-256.jpg",
                "first-name": "Constance",
                "last-name": "Watson",
                "orcid-id": "https://sandbox.orcid.org/0000-0001-8373-6934"
            },
            "id": "01D5MHQN3ZPH47YVSVQEVB0DAE",
            "links": {
                "self": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE"
            },
            "relationships": {
                "participation": {
                    "data": [
                        {
                            "id": "01D5T4N25RV2062NVVQKZ9NBYX",
                            "type": "participants"
                        }
                    ],
                    "links": {
                        "related": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE/participants",
                        "self": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE/relationships/participants"
                    }
                }
            },
            "type": "people"
        }
        expected_payload_links = {
            'first': 'http://localhost:9000/people?page=1',
            'prev': None,
            'self': 'http://localhost:9000/people?page=1',
            'next': 'http://localhost:9000/people?page=2',
            'last': 'http://localhost:9000/people?page=3'
        }

        expected_payload_included_items = list()
        expected_payload_included_items.append(
            {
                "attributes": {
                    "role": {
                        "class": "http://purl.org/spar/scoro/InvestigationRole",
                        "description": "The principle investigator of the research project.",
                        "member": "http://purl.org/spar/scoro/principle-investigator",
                        "title": "principle investigator"
                    }
                },
                "id": "01D5T4N25RV2062NVVQKZ9NBYX",
                "links": {
                    "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX"
                },
                "relationships": {
                    "person": {
                        "data": {
                            "id": "01D5MHQN3ZPH47YVSVQEVB0DAE",
                            "type": "people"
                        },
                        "links": {
                            "related": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/people",
                            "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/relationships/people"
                        }
                    },
                    "project": {
                        "data": {
                            "id": "01D5M0CFQV4M7JASW7F87SRDYB",
                            "type": "projects"
                        },
                        "links": {
                            "related": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/projects",
                            "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/relationships/projects"
                        }
                    }
                },
                "type": "participants"
            }
        )
        expected_payload_included_items.append(
            {
                "attributes": {
                    "abstract": "The Arctic climate is changing twice as fast as the global average and these dramatic "
                                "changes are evident in the decreases in sea ice extent over the last few decades. The "
                                "lowest sea ice cover to date was recorded in 2007 and recent data suggests sea ice cover "
                                "this year may be even lower. Clouds play a major role in the Arctic climate and therefore "
                                "influence the extent of sea ice, but our understanding of these clouds is very poor. Low "
                                "level, visually thick, clouds in much of the world tend to have a cooling effect, because "
                                "they reflect sunlight back into space that would otherwise be absorbed at the surface. "
                                "However, in the Arctic this albedo effect is not as important because the surface, often "
                                "being covered in snow and ice, is already highly reflective and Arctic clouds therefore "
                                "tend to warm instead of cooling. Warming in the Arctic can, in turn, lead to sea ice "
                                "break-up which exposes dark underlying sea water. The sea water absorbs more of the sun's "
                                "energy, thus amplifying the original warming. Hence, small changes in cloud properties or "
                                "coverage can lead to dramatic changes in the Arctic climate; this is where the proposed "
                                "research project comes in. \n A large portion of clouds, including those found in the "
                                "Arctic region, are categorized as mixed phase clouds. This means they contain both "
                                "supercooled water droplets and ice crystals (for a demonstration of supercooled water "
                                "see: http://www.youtube.com/watch?v=0JtBZGXd5zo). Liquid cloud droplets can exist in a "
                                "supercooled state well below zero degrees centigrade without freezing. Freezing will, "
                                "however, be observed if the droplets contain a particle known as an ice nucleus that can "
                                "catalyze ice formation and growth. Ice formation dramatically alters a cloud's properties "
                                "and therefore its influence on climate. At lower latitudes, ice nuclei are typically made "
                                "up of desert dusts, soot or even bacteria. But the composition and source of ice nuclei "
                                "in the Arctic environment remains a mystery. \n A likely source of ice nuclei in the "
                                "Arctic is the ocean. Particles emitted at the sea surface, through the action of waves "
                                "breaking and bubble bursting, may serve as ice nuclei when they are lofted into the "
                                "atmosphere and are incorporated in cloud droplets. This source of ice nuclei has not yet "
                                "been quantified. We will be the first to make measurements of ice nuclei in the central "
                                "Arctic region. We will make measurements of ice nuclei in the surface layers of the sea "
                                "from a research ship as well as measuring airborne ice nuclei from the BAe-146 research "
                                "aircraft. \n The sea's surface contains a wide range of bacteria, viruses, plankton and "
                                "other materials which are ejected into the atmosphere and may cause ice to form. We will "
                                "use state-of-the-art equipment developed at Leeds to measure how well sea-derived "
                                "particles and particles sampled in the atmosphere nucleate ice. We will piggy back on a "
                                "NERC funded project called ACACCIA, which not only represents excellent value for money "
                                "(since the ship and aircraft are already paid for under ACCACIA), but is a unique "
                                "opportunity to access this remote region. \n Results from the proposed study will build "
                                "upon previous work performed in the Murray laboratory and generate quantitative results "
                                "that can be directly used to improve computer-based cloud, aerosol and climate models. "
                                "Our results will further our understanding of these mysterious and important mixed phase "
                                "clouds and, in turn, the global climate.",
                    "access-duration": {
                        "end_instant": "2018-10-01",
                        "interval": "2013-03-01/2018-10-01",
                        "start_instant": "2013-03-01"
                    },
                    "acronym": "ACCACIA",
                    "impact-statements": [
                        "We discovered that there is a source of atmospheric ice nucleating particles in the oceans "
                        "associated with organic material produced by plankton. This was published in a high impact study "
                        "in Nature in 2015 (https://doi.org/10.1038/nature14986). We have now also used this data in a "
                        "modelling study of the global distribution of ice nucleating particles which was published in "
                        "March 2017 (https://doi.org/10.5194/acp-17-3637-2017)."
                    ],
                    "notes": [
                        "You can follow the ACCACIA project via their blog as well as on Twitter under @_ACCACIA_."
                    ],
                    "project-duration": {
                        "end_instant": "2016-10-01",
                        "interval": "2013-03-01/2016-10-01",
                        "start_instant": "2013-03-01"
                    },
                    "publications": [
                        "https://doi.org/10.5194/acp-2018-283",
                        "https://doi.org/10.5194/acp-15-3719-2015",
                        "https://doi.org/10.5194/acp-15-5599-2015",
                        "https://doi.org/10.5194/acp-16-4063-2016"
                    ],
                    "title": "Aerosol-Cloud Coupling And Climate Interactions in the Arctic",
                    "website": "http://arp.arctic.ac.uk/projects/aerosol-cloud-coupling-and-climate-interactions-ar/"
                },
                "id": "01D5M0CFQV4M7JASW7F87SRDYB",
                "links": {
                    "self": "http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB"
                },
                "relationships": {
                    "participants": {
                        "data": [
                            {
                                "id": "01D5T4N25RV2062NVVQKZ9NBYX",
                                "type": "participants"
                            }
                        ],
                        "links": {
                            "related": "http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB/participants",
                            "self": "http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB/relationships/participants"
                        }
                    }
                },
                "type": "projects"
            }
        )

        token = self.util_create_auth_token()
        response = self.client.get(
            '/people',
            base_url='http://localhost:9000',
            headers={'authorization': f"bearer { token }"},
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIn('data', json_response.keys())
        self.assertEqual(2, len(json_response['data']))
        self.assertDictEqual(json_response['data'][0], expected_payload_data_item)
        self.assertIn('links', json_response.keys())
        self.assertDictEqual(json_response['links'], expected_payload_links)
        self.assertIn('included', json_response.keys())
        # noinspection PyTypeChecker
        self.assertListEqual(json_response['included'], expected_payload_included_items)

    def test_people_detail(self):
        expected_payload = {
            "data": {
                "attributes": {
                    "avatar-url": "https://cdn.web.bas.ac.uk/bas-registers-service/v1/sample-avatars/conwat/conwat-256.jpg",
                    "first-name": "Constance",
                    "last-name": "Watson",
                    "orcid-id": "https://sandbox.orcid.org/0000-0001-8373-6934"
                },
                "id": "01D5MHQN3ZPH47YVSVQEVB0DAE",
                "links": {
                    "self": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE"
                },
                "relationships": {
                    "participation": {
                        "data": [
                            {
                                "id": "01D5T4N25RV2062NVVQKZ9NBYX",
                                "type": "participants"
                            }
                        ],
                        "links": {
                            "related": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE/participants",
                            "self": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE/relationships/participants"
                        }
                    }
                },
                "type": "people"
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
                    "id": "01D5T4N25RV2062NVVQKZ9NBYX",
                    "links": {
                        "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01D5MHQN3ZPH47YVSVQEVB0DAE",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/people",
                                "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01D5M0CFQV4M7JASW7F87SRDYB",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/projects",
                                "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/relationships/projects"
                            }
                        }
                    },
                    "type": "participants"
                },
                {
                    "attributes": {
                        "abstract": "The Arctic climate is changing twice as fast as the global average and these dramatic "
                                    "changes are evident in the decreases in sea ice extent over the last few decades. The "
                                    "lowest sea ice cover to date was recorded in 2007 and recent data suggests sea ice cover "
                                    "this year may be even lower. Clouds play a major role in the Arctic climate and therefore "
                                    "influence the extent of sea ice, but our understanding of these clouds is very poor. Low "
                                    "level, visually thick, clouds in much of the world tend to have a cooling effect, because "
                                    "they reflect sunlight back into space that would otherwise be absorbed at the surface. "
                                    "However, in the Arctic this albedo effect is not as important because the surface, often "
                                    "being covered in snow and ice, is already highly reflective and Arctic clouds therefore "
                                    "tend to warm instead of cooling. Warming in the Arctic can, in turn, lead to sea ice "
                                    "break-up which exposes dark underlying sea water. The sea water absorbs more of the sun's "
                                    "energy, thus amplifying the original warming. Hence, small changes in cloud properties or "
                                    "coverage can lead to dramatic changes in the Arctic climate; this is where the proposed "
                                    "research project comes in. \n A large portion of clouds, including those found in the "
                                    "Arctic region, are categorized as mixed phase clouds. This means they contain both "
                                    "supercooled water droplets and ice crystals (for a demonstration of supercooled water "
                                    "see: http://www.youtube.com/watch?v=0JtBZGXd5zo). Liquid cloud droplets can exist in a "
                                    "supercooled state well below zero degrees centigrade without freezing. Freezing will, "
                                    "however, be observed if the droplets contain a particle known as an ice nucleus that can "
                                    "catalyze ice formation and growth. Ice formation dramatically alters a cloud's properties "
                                    "and therefore its influence on climate. At lower latitudes, ice nuclei are typically made "
                                    "up of desert dusts, soot or even bacteria. But the composition and source of ice nuclei "
                                    "in the Arctic environment remains a mystery. \n A likely source of ice nuclei in the "
                                    "Arctic is the ocean. Particles emitted at the sea surface, through the action of waves "
                                    "breaking and bubble bursting, may serve as ice nuclei when they are lofted into the "
                                    "atmosphere and are incorporated in cloud droplets. This source of ice nuclei has not yet "
                                    "been quantified. We will be the first to make measurements of ice nuclei in the central "
                                    "Arctic region. We will make measurements of ice nuclei in the surface layers of the sea "
                                    "from a research ship as well as measuring airborne ice nuclei from the BAe-146 research "
                                    "aircraft. \n The sea's surface contains a wide range of bacteria, viruses, plankton and "
                                    "other materials which are ejected into the atmosphere and may cause ice to form. We will "
                                    "use state-of-the-art equipment developed at Leeds to measure how well sea-derived "
                                    "particles and particles sampled in the atmosphere nucleate ice. We will piggy back on a "
                                    "NERC funded project called ACACCIA, which not only represents excellent value for money "
                                    "(since the ship and aircraft are already paid for under ACCACIA), but is a unique "
                                    "opportunity to access this remote region. \n Results from the proposed study will build "
                                    "upon previous work performed in the Murray laboratory and generate quantitative results "
                                    "that can be directly used to improve computer-based cloud, aerosol and climate models. "
                                    "Our results will further our understanding of these mysterious and important mixed phase "
                                    "clouds and, in turn, the global climate.",
                        "access-duration": {
                            "end_instant": "2018-10-01",
                            "interval": "2013-03-01/2018-10-01",
                            "start_instant": "2013-03-01"
                        },
                        "acronym": "ACCACIA",
                        "impact-statements": [
                            "We discovered that there is a source of atmospheric ice nucleating particles in the oceans "
                            "associated with organic material produced by plankton. This was published in a high impact study "
                            "in Nature in 2015 (https://doi.org/10.1038/nature14986). We have now also used this data in a "
                            "modelling study of the global distribution of ice nucleating particles which was published in "
                            "March 2017 (https://doi.org/10.5194/acp-17-3637-2017)."
                        ],
                        "notes": [
                            "You can follow the ACCACIA project via their blog as well as on Twitter under @_ACCACIA_."
                        ],
                        "project-duration": {
                            "end_instant": "2016-10-01",
                            "interval": "2013-03-01/2016-10-01",
                            "start_instant": "2013-03-01"
                        },
                        "publications": [
                            "https://doi.org/10.5194/acp-2018-283",
                            "https://doi.org/10.5194/acp-15-3719-2015",
                            "https://doi.org/10.5194/acp-15-5599-2015",
                            "https://doi.org/10.5194/acp-16-4063-2016"
                        ],
                        "title": "Aerosol-Cloud Coupling And Climate Interactions in the Arctic",
                        "website": "http://arp.arctic.ac.uk/projects/aerosol-cloud-coupling-and-climate-interactions-ar/"
                    },
                    "id": "01D5M0CFQV4M7JASW7F87SRDYB",
                    "links": {
                        "self": "http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB"
                    },
                    "relationships": {
                        "participants": {
                            "data": [
                                {
                                    "id": "01D5T4N25RV2062NVVQKZ9NBYX",
                                    "type": "participants"
                                }
                            ],
                            "links": {
                                "related": "http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB/participants",
                                "self": "http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB/relationships/participants"
                            }
                        }
                    },
                    "type": "projects"
                }
            ],
            "links": {
                "self": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/people/01D5MHQN3ZPH47YVSVQEVB0DAE',
            headers={'authorization': f"bearer { token }"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_people_single_missing_unknown_id(self):
        error = ApiNotFoundError()
        expected_payload = self.util_prepare_expected_error_payload(error)

        for person_id in ['', 'unknown']:
            with self.subTest(person_id=person_id):
                token = self.util_create_auth_token()
                response = self.client.get(
                    f"/people/{ person_id }",
                    base_url='http://localhost:9000',
                    headers={'authorization': f"bearer { token }"},
                )
                json_response = response.get_json()
                json_response = self.util_prepare_error_response(json_response)
                self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
                self.assertDictEqual(json_response, expected_payload)

    def test_people_relationship_participants(self):
        expected_payload = {
            "data": [
                {
                    "id": "01D5T4N25RV2062NVVQKZ9NBYX",
                    "type": "participants"
                }
            ],
            "links": {
                "related": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE/participants",
                "self": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE/relationships/participants"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/people/01D5MHQN3ZPH47YVSVQEVB0DAE/relationships/participants',
            headers={'authorization': f"bearer { token }"},
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
                    "id": "01D5T4N25RV2062NVVQKZ9NBYX",
                    "links": {
                        "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX"
                    },
                    "relationships": {
                        "person": {
                            "data": {
                                "id": "01D5MHQN3ZPH47YVSVQEVB0DAE",
                                "type": "people"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/people",
                                "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/relationships/people"
                            }
                        },
                        "project": {
                            "data": {
                                "id": "01D5M0CFQV4M7JASW7F87SRDYB",
                                "type": "projects"
                            },
                            "links": {
                                "related": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/projects",
                                "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/relationships/projects"
                            }
                        }
                    },
                    "type": "participants"
                }
            ],
            "links": {
                "self": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE/relationships/participants"
            }
        }

        token = self.util_create_auth_token()
        response = self.client.get(
            '/people/01D5MHQN3ZPH47YVSVQEVB0DAE/participants',
            headers={'authorization': f"bearer {token}"},
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)
