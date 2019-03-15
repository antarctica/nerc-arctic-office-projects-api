import unittest

from http import HTTPStatus

from flask_migrate import Config, upgrade, downgrade, Migrate
from arctic_office_projects_api.errors import ApiException

from arctic_office_projects_api.meta.errors import ApiNotFoundError
from arctic_office_projects_api import create_app, db
from arctic_office_projects_api.models import Project, Person, Participant


class MainBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        with self.app.app_context():
            # Migrate and seed database
            config = Config("migrations/alembic.ini")
            config.set_main_option("script_location", "migrations")
            Migrate(self.app, db)
            upgrade()
            Project.seed(quantity=5)
            Person.seed(quantity=5)
            Participant.seed(quantity=1)
            db.session.commit()

        self.maxDiff = None

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

        with self.app.app_context():
            # Rollback all DB migrations
            downgrade(revision='base')

    @staticmethod
    def _prepare_expected_error_payload(error: ApiException):
        error = error.dict()
        # Overwrite dynamic error ID with static value to allow comparision
        error['id'] = 'a611b89f-f1bb-43c5-8efa-913c83c9109e'

        return {'errors': [error]}

    @staticmethod
    def _prepare_error_response(json_response: dict) -> dict:
        # Overwrite dynamic error ID with static value to allow comparision
        if 'id' in json_response['errors'][0].keys():
            json_response['errors'][0]['id'] = 'a611b89f-f1bb-43c5-8efa-913c83c9109e'

        return json_response

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
                "title": "xxx"
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
                    "investigative-role": "InvestigativeRole.principal_investigator"
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
                    "first-name": "Constance",
                    "last-name": "Watson"
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

        response = self.client.get(
            '/projects',
            base_url='http://localhost:9000',
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
                    "title": "xxx"
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
                        "investigative-role": "InvestigativeRole.principal_investigator"
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
                        "first-name": "Constance",
                        "last-name": "Watson"
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

        response = self.client.get(
            '/projects/01D5M0CFQV4M7JASW7F87SRDYB',
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_projects_single_missing_unknown_id(self):
        error = ApiNotFoundError()
        expected_payload = self._prepare_expected_error_payload(error)

        for project_id in ['', 'unknown']:
            with self.subTest(project_id=project_id):
                response = self.client.get(
                    f"/projects/{ project_id }",
                    base_url='http://localhost:9000'
                )
                json_response = response.get_json()
                json_response = self._prepare_error_response(json_response)
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

        response = self.client.get(
            '/projects/01D5M0CFQV4M7JASW7F87SRDYB/relationships/participants',
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
                        "investigative-role": "InvestigativeRole.principal_investigator"
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

        response = self.client.get(
            '/projects/01D5M0CFQV4M7JASW7F87SRDYB/participants',
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
                        "investigative-role": "InvestigativeRole.principal_investigator"
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
                        "first-name": "Constance",
                        "last-name": "Watson"
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
                        "title": "xxx"
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

        response = self.client.get(
            '/participants',
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_participants_detail(self):
        expected_payload = {
            "data": {
                "attributes": {
                    "investigative-role": "InvestigativeRole.principal_investigator"
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
                        "first-name": "Constance",
                        "last-name": "Watson"
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
                        "title": "xxx"
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

        response = self.client.get(
            '/participants/01D5T4N25RV2062NVVQKZ9NBYX',
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_participants_single_missing_unknown_id(self):
        error = ApiNotFoundError()
        expected_payload = self._prepare_expected_error_payload(error)

        for participant_id in ['', 'unknown']:
            with self.subTest(participant_id=participant_id):
                response = self.client.get(
                    f"/participants/{ participant_id }",
                    base_url='http://localhost:9000'
                )
                json_response = response.get_json()
                json_response = self._prepare_error_response(json_response)
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

        response = self.client.get(
            '/participants/01D5T4N25RV2062NVVQKZ9NBYX/relationships/projects',
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

        response = self.client.get(
            '/participants/01D5T4N25RV2062NVVQKZ9NBYX/relationships/people',
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_participants_projects(self):
        expected_payload = {
            "data": {
                "attributes": {
                    "title": "xxx"
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

        response = self.client.get(
            '/participants/01D5T4N25RV2062NVVQKZ9NBYX/projects',
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_participants_people(self):
        expected_payload = {
            "data": {
                "attributes": {
                    "first-name": "Constance",
                    "last-name": "Watson"
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

        response = self.client.get(
            '/participants/01D5T4N25RV2062NVVQKZ9NBYX/people',
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_people_list(self):
        expected_payload_data_item = {
            "attributes": {
                "first-name": "Constance",
                "last-name": "Watson"
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
                    "investigative-role": "InvestigativeRole.principal_investigator"
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
                    "title": "xxx"
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

        response = self.client.get(
            '/people',
            base_url='http://localhost:9000'
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
                    "first-name": "Constance",
                    "last-name": "Watson"
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
                        "investigative-role": "InvestigativeRole.principal_investigator"
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
                        "title": "xxx"
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

        response = self.client.get(
            '/people/01D5MHQN3ZPH47YVSVQEVB0DAE',
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)

    def test_people_single_missing_unknown_id(self):
        error = ApiNotFoundError()
        expected_payload = self._prepare_expected_error_payload(error)

        for person_id in ['', 'unknown']:
            with self.subTest(person_id=person_id):
                response = self.client.get(
                    f"/people/{ person_id }",
                    base_url='http://localhost:9000'
                )
                json_response = response.get_json()
                json_response = self._prepare_error_response(json_response)
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

        response = self.client.get(
            '/people/01D5MHQN3ZPH47YVSVQEVB0DAE/relationships/participants',
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
                        "investigative-role": "InvestigativeRole.principal_investigator"
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

        response = self.client.get(
            '/people/01D5MHQN3ZPH47YVSVQEVB0DAE/participants',
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(json_response, expected_payload)
