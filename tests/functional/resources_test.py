import json
import pytest
from unittest.mock import patch
from sqlalchemy.orm.exc import NoResultFound
from arctic_office_projects_api.models import (
    Project,
    Person,
    Grant,
    Organisation,
    CategoryScheme,
    CategoryTerm,
    Participant,
    Allocation,
    Categorisation,
)


@pytest.mark.usefixtures("db_create")
def test_projects(client, app):
    response = client.get("/projects", headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 200
    assert response.get_json() is not None

    response = client.get("/projects/123", headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 404

    response = client.get("/projects/01DB2ECBP24NHYV5KZQG2N3FS2", headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 200

    with open("tests/responses/project.json", "r") as f:
        expected_data = json.load(f)

    response_data = response.json
    assert response_data == expected_data


@pytest.mark.usefixtures("db_create")
@patch("arctic_office_projects_api.models.Project.query.filter_by")
def test_projects_relationships_success(mock_filter_by, client):
    # Mock a project object and its schema output
    mock_project = Project(
        neutral_id="01DB2ECBP24NHYV5KZQG2N3FS2"
    )  # Example, adjust as needed
    mock_filter_by.return_value.one.return_value = mock_project

    with patch("arctic_office_projects_api.schemas.ProjectSchema.dump") as mock_dump:
        mock_dump.return_value = {"data": "expected_payload"}

        response = client.get(
            "/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/participants",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        response = client.get(
            "/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/allocations",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        response = client.get(
            "/projects/01DB2ECBP24NHYV5KZQG2N3FS2/participants",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        response = client.get(
            "/projects/01DB2ECBP24NHYV5KZQG2N3FS2/allocations",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        response = client.get(
            "/projects/01DB2ECBP24NHYV5KZQG2N3FS2/relationships/categorisations",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        response = client.get(
            "/projects/01DB2ECBP24NHYV5KZQG2N3FS2/categorisations",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}


@patch("arctic_office_projects_api.models.Project.query.filter_by")
def test_projects_not_found(mock_filter_by, client):
    # Mock NoResultFound being raised
    mock_filter_by.return_value.one.side_effect = NoResultFound

    response = client.get(
        "/projects/unknown-id/relationships/participants",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/projects/unknown-id/relationships/allocations",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/projects/unknown-id/participants",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/projects/unknown-id/allocations",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/projects/unknown-id/relationships/categorisations",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/projects/unknown-id/categorisations",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound


@pytest.mark.usefixtures("db_create")
def test_grants(client):
    response = client.get("/grants", headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 200
    assert response.get_json() is not None

    response = client.get("/grants/123", headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 404

    response = client.get("/grants/01DB2ECBP3XQ4B8Z5DW7W963YD", headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 200

    with open("tests/responses/grant.json", "r") as f:
        expected_data = json.load(f)

    response_data = response.json
    assert response_data == expected_data


@pytest.mark.usefixtures("db_create")
@patch("arctic_office_projects_api.models.Grant.query.filter_by")
def test_grants_relationships_success(mock_filter_by, client):
    # Mock a project object and its schema output
    mock_project = Grant(
        neutral_id="01DB2ECBP3XQ4B8Z5DW7W963YD"
    )  # Example, adjust as needed
    mock_filter_by.return_value.one.return_value = mock_project

    with patch("arctic_office_projects_api.schemas.GrantSchema.dump") as mock_dump:
        mock_dump.return_value = {"data": "expected_payload"}

        response = client.get(
            "/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/relationships/allocations",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        response = client.get(
            "/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/relationships/organisations",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        response = client.get(
            "/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/allocations",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        response = client.get(
            "/grants/01DB2ECBP3XQ4B8Z5DW7W963YD/organisations",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}


@patch("arctic_office_projects_api.models.Grant.query.filter_by")
def test_grants_not_found(mock_filter_by, client):
    # Mock NoResultFound being raised
    mock_filter_by.return_value.one.side_effect = NoResultFound

    response = client.get(
        "/grants/unknown-id/relationships/allocations",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/grants/unknown-id/relationships/organisations",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/grants/unknown-id/allocations",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/grants/unknown-id/organisations",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound


@pytest.mark.usefixtures("db_create")
def test_people(client):
    response = client.get("/people", headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 200
    assert response.get_json() is not None

    response = client.get("/people/123", headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 404

    response = client.get(
        "/people/01DB2ECBP2MFB0DH3EF3PH74R0",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 200

    with open("tests/responses/person.json", "r") as f:
        expected_data = json.load(f)

    response_data = response.json
    assert response_data == expected_data


@pytest.mark.usefixtures("db_create")
@patch("arctic_office_projects_api.models.Project.query.filter_by")
def test_people_relationships_success(mock_filter_by, client):
    # Mock a project object and its schema output
    mock_project = Person(
        neutral_id="01DB2ECBP2MFB0DH3EF3PH74R0"
    )  # Example, adjust as needed
    mock_filter_by.return_value.one.return_value = mock_project

    with patch("arctic_office_projects_api.schemas.PersonSchema.dump") as mock_dump:
        mock_dump.return_value = {"data": "expected_payload"}

        response = client.get(
            "/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/participants",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        response = client.get(
            "/people/01DB2ECBP2MFB0DH3EF3PH74R0/relationships/organisations",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        response = client.get(
            "/people/01DB2ECBP2MFB0DH3EF3PH74R0/participants",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        response = client.get(
            "/people/01DB2ECBP2MFB0DH3EF3PH74R0/organisations",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}


@patch("arctic_office_projects_api.models.Person.query.filter_by")
def test_people_relationships_participants_not_found(mock_filter_by, client):
    # Mock NoResultFound being raised
    mock_filter_by.return_value.one.side_effect = NoResultFound

    response = client.get(
        "/people/unknown-id/relationships/participants",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/people/unknown-id/relationships/organisations",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/people/unknown-id/participants",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/people/unknown-id/organisations",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound


@pytest.mark.usefixtures("db_create")
def test_participants(client):
    response = client.get("/participants", headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 200
    assert response.get_json() is not None

    response = client.get("/participants/123", headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 404

    response = client.get(
        "/participants/01DB2ECBP3622SPB5PS3J8W4XF",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 200

    with open("tests/responses/participant.json", "r") as f:
        expected_data = json.load(f)

    response_data = response.json
    assert response_data == expected_data


@pytest.mark.usefixtures("db_create")
@patch("arctic_office_projects_api.models.Participant.query.filter_by")
def test_participants_relationships_projects(mock_filter_by, client):
    # Mock a project object and its schema output
    mock_project = Participant(
        neutral_id="01DB2ECBP3622SPB5PS3J8W4XF"
    )  # Example, adjust as needed
    mock_filter_by.return_value.one.return_value = mock_project

    with patch(
        "arctic_office_projects_api.schemas.ParticipantSchema.dump"
    ) as mock_dump:
        mock_dump.return_value = {"data": "expected_payload"}

        response = client.get(
            "/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/projects",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        response = client.get(
            "/participants/01DB2ECBP3622SPB5PS3J8W4XF/relationships/people",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        response = client.get(
            "/participants/01DB2ECBP3622SPB5PS3J8W4XF/projects",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        response = client.get(
            "/participants/01DB2ECBP3622SPB5PS3J8W4XF/people",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}


@patch("arctic_office_projects_api.models.Project.query.filter_by")
def test_participants_not_found(mock_filter_by, client):
    # Mock NoResultFound being raised
    mock_filter_by.return_value.one.side_effect = NoResultFound

    response = client.get(
        "/participants/unknown-id/relationships/projects",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/participants/unknown-id/relationships/people",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/participants/unknown-id/projects",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/participants/unknown-id/people",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound


@pytest.mark.usefixtures("db_create")
def test_organisations(client):
    response = client.get("/organisations", headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 200
    assert response.get_json() is not None

    response = client.get(
        "/organisations/123",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404

    response = client.get(
        "/organisations/01DB2ECBP3WZDP4PES64XKXJ1A",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 200

    with open("tests/responses/organisation.json", "r") as f:
        expected_data = json.load(f)

    response_data = response.json
    assert response_data == expected_data


@pytest.mark.usefixtures("db_create")
@patch("arctic_office_projects_api.models.Organisation.query.filter_by")
def test_organisations_relationships_success(mock_filter_by, client):
    # Mock a project object and its schema output
    mock_project = Organisation(
        neutral_id="01DB2ECBP3WZDP4PES64XKXJ1A"
    )  # Example, adjust as needed
    mock_filter_by.return_value.one.return_value = mock_project

    with patch(
        "arctic_office_projects_api.schemas.OrganisationSchema.dump"
    ) as mock_dump:
        mock_dump.return_value = {"data": "expected_payload"}

        response = client.get(
            "/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/people",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        response = client.get(
            "/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/relationships/grants",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        response = client.get(
            "/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/people",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        response = client.get(
            "/organisations/01DB2ECBP3WZDP4PES64XKXJ1A/grants",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}


@patch("arctic_office_projects_api.models.Organisation.query.filter_by")
def test_organisations_not_found(mock_filter_by, client):
    # Mock NoResultFound being raised
    mock_filter_by.return_value.one.side_effect = NoResultFound

    response = client.get(
        "/organisations/unknown-id/relationships/people",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/organisations/unknown-id/relationships/grants",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/organisations/unknown-id/people",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/organisations/unknown-id/grants",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound


@pytest.mark.usefixtures("db_create")
def test_allocations(client):
    response = client.get("/allocations", headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 200
    assert response.get_json() is not None

    response = client.get("/allocations/123", headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 404

    response = client.get(
        "/allocations/01DB2ECBP35AT5WBG092J5GDQ9",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 200

    with open("tests/responses/allocation.json", "r") as f:
        expected_data = json.load(f)

    response_data = response.json
    assert response_data == expected_data


@pytest.mark.usefixtures("db_create")
@patch("arctic_office_projects_api.models.Allocation.query.filter_by")
def test_allocations_relationships_success(mock_filter_by, client):
    # Mock a project object and its schema output
    mock_project = Allocation(
        neutral_id="01DB2ECBP35AT5WBG092J5GDQ9"
    )  # Example, adjust as needed
    mock_filter_by.return_value.one.return_value = mock_project

    with patch("arctic_office_projects_api.schemas.AllocationSchema.dump") as mock_dump:
        mock_dump.return_value = {"data": "expected_payload"}

        response = client.get(
            "/allocations/01DB2ECBP35AT5WBG092J5GDQ9/relationships/projects",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        response = client.get(
            "/allocations/01DB2ECBP35AT5WBG092J5GDQ9/relationships/grants",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        response = client.get(
            "/allocations/01DB2ECBP35AT5WBG092J5GDQ9/projects",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        response = client.get(
            "/allocations/01DB2ECBP35AT5WBG092J5GDQ9/grants",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}


@patch("arctic_office_projects_api.models.Allocation.query.filter_by")
def test_allocations_not_found(mock_filter_by, client):
    # Mock NoResultFound being raised
    mock_filter_by.return_value.one.side_effect = NoResultFound

    response = client.get(
        "/allocations/unknown-id/relationships/projects",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/allocations/unknown-id/relationships/grants",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/allocations/unknown-id/projects",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/allocations/unknown-id/grants",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound


@pytest.mark.usefixtures("db_create")
def test_categorisations(client):
    response = client.get(
        "/categorisations",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 200
    assert response.get_json() is not None

    response = client.get(
        "/categorisations/123",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404

    response = client.get(
        "/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 200

    with open("tests/responses/categorisation.json", "r") as f:
        expected_data = json.load(f)

    response_data = response.json
    assert response_data == expected_data


@pytest.mark.usefixtures("db_create")
@patch("arctic_office_projects_api.models.Categorisation.query.filter_by")
def test_categorisations_relationships_success(mock_filter_by, client):
    # Mock a project object and its schema output
    mock_project = Categorisation(
        neutral_id="01DC6HYAKYAXE7MZMD08QV5JWG"
    )  # Example, adjust as needed
    mock_filter_by.return_value.one.return_value = mock_project

    with patch(
        "arctic_office_projects_api.schemas.CategorisationSchema.dump"
    ) as mock_dump:
        mock_dump.return_value = {"data": "expected_payload"}

        response = client.get(
            "/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/relationships/projects",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        response = client.get(
            "/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/relationships/categories",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        response = client.get(
            "/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/projects",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        response = client.get(
            "/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG/categories",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}


@patch("arctic_office_projects_api.models.Categorisation.query.filter_by")
def test_categorisations_not_found(mock_filter_by, client):
    # Mock NoResultFound being raised
    mock_filter_by.return_value.one.side_effect = NoResultFound

    response = client.get(
        "/categorisations/unknown-id/relationships/projects",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/categorisations/unknown-id/relationships/categories",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/categorisations/unknown-id/projects",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/categorisations/unknown-id/categories",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound


@pytest.mark.usefixtures("db_create")
def test_category_schemes(client):
    response = client.get(
        "/category-schemes",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 200
    assert response.get_json() is not None

    response = client.get(
        "/category-schemes/123",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404

    response = client.get(
        "/category-schemes/01DC6HYAKXG8FCN63D7DH06W84",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 200

    with open("tests/responses/category_scheme.json", "r") as f:
        expected_data = json.load(f)

    response_data = response.json
    assert response_data == expected_data


@pytest.mark.usefixtures("db_create")
@patch("arctic_office_projects_api.models.CategoryScheme.query.filter_by")
def test_categoryschemes_relationships_categories(mock_filter_by, client):
    # Mock a project object and its schema output
    mock_project = CategoryScheme(
        neutral_id="01DC6HYAKXG8FCN63D7DH06W84"
    )  # Example, adjust as needed
    mock_filter_by.return_value.one.return_value = mock_project

    with patch(
        "arctic_office_projects_api.schemas.CategorySchemeSchema.dump"
    ) as mock_dump:
        mock_dump.return_value = {"data": "expected_payload"}

        response = client.get(
            "/category-schemes/01DC6HYAKXG8FCN63D7DH06W84/relationships/categories",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        response = client.get(
            "/category-schemes/01DC6HYAKXG8FCN63D7DH06W84/categories",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}


@patch("arctic_office_projects_api.models.Project.query.filter_by")
def test_categoryschemes_not_found(mock_filter_by, client):
    # Mock NoResultFound being raised
    mock_filter_by.return_value.one.side_effect = NoResultFound

    response = client.get(
        "/category-schemes/unknown-id/relationships/categories",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/category-schemes/unknown-id/categories",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound


@pytest.mark.usefixtures("db_create")
def test_category_terms(client):
    response = client.get("/categories", headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 200
    assert response.get_json() is not None

    response = client.get("/categories/123", headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 404

    response = client.get(
        "/categories/01DC6HYAKX993ZK6YHCVWAE169",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 200

    with open("tests/responses/category_term.json", "r") as f:
        expected_data = json.load(f)

    response_data = response.json
    assert response_data == expected_data


@pytest.mark.usefixtures("db_create")
@patch("arctic_office_projects_api.models.CategoryTerm.query.filter_by")
def test_categoryterms_relationships_parent_categories(mock_filter_by, client):
    # Mock a project object and its schema output
    mock_project = CategoryTerm(
        neutral_id="01DC6HYAKX993ZK6YHCVWAE169"
    )  # Example, adjust as needed
    mock_filter_by.return_value.one.return_value = mock_project

    with patch(
        "arctic_office_projects_api.schemas.CategoryTermSchema.dump"
    ) as mock_dump:
        mock_dump.return_value = {"data": "expected_payload"}
        response = client.get(
            "/categories/01DC6HYAKX993ZK6YHCVWAE169/relationships/parent-categories",
            headers={"Authorization": "Bearer fake_token"}
        )

        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        mock_dump.return_value = {"data": "expected_payload"}
        response = client.get(
            "/categories/01DC6HYAKX993ZK6YHCVWAE169/relationships/category-schemes",
            headers={"Authorization": "Bearer fake_token"}
        )

        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        mock_dump.return_value = {"data": "expected_payload"}
        response = client.get(
            "/categories/01DC6HYAKX993ZK6YHCVWAE169/relationships/categorisations",
            headers={"Authorization": "Bearer fake_token"}
        )

        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        mock_dump.return_value = {"data": "expected_payload"}
        response = client.get(
            "/categories/01DC6HYAKX993ZK6YHCVWAE169/parent-categories",
            headers={"Authorization": "Bearer fake_token"}
        )

        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        mock_dump.return_value = {"data": "expected_payload"}
        response = client.get(
            "/categories/01DC6HYAKX993ZK6YHCVWAE169/category-schemes",
            headers={"Authorization": "Bearer fake_token"}
        )

        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}

        mock_dump.return_value = {"data": "expected_payload"}
        response = client.get(
            "/categories/01DC6HYAKX993ZK6YHCVWAE169/categorisations",
            headers={"Authorization": "Bearer fake_token"}
        )

        assert response.status_code == 200
        assert response.json == {"data": "expected_payload"}


@patch("arctic_office_projects_api.models.CategoryTerm.query.filter_by")
def test_categories_not_found(mock_filter_by, client):
    # Mock NoResultFound being raised
    mock_filter_by.return_value.one.side_effect = NoResultFound

    response = client.get(
        "/categories/unknown-id/relationships/parent-categories",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/categories/unknown-id/relationships/category-schemes",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/categories/unknown-id/relationships/categorisations",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/categories/unknown-id/parent-categories",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/categories/unknown-id/category-schemes",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound

    response = client.get(
        "/categories/unknown-id/categorisations",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code == 404  # NotFound
