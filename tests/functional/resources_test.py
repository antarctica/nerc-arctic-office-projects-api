import json
import pytest

from arctic_office_projects_api.extensions import db
from arctic_office_projects_api.models import Project

@pytest.mark.usefixtures("db_create")
def test_projects(client, app):
    response = client.get('/projects')
    assert response.status_code == 200
    assert response.get_json() is not None

    response = client.get('/projects/123')
    assert response.status_code == 404

    response = client.get('/projects/01DB2ECBP24NHYV5KZQG2N3FS2')
    assert response.status_code == 200

    with open('tests/responses/project.json', 'r') as f:
        expected_data = json.load(f)
    
    response_data = response.json
    assert response_data == expected_data

    duplicate_project = Project(
        neutral_id="01DB2ECBP24NHYV5KZQG2N3FS3",
        grant_reference="EX-GRANT-0001",
        title="Example project 1",
        access_duration="[2012-03-01,)",
        project_duration="[2012-03-01,2015-10-01)"
        )
    db.session.add(duplicate_project)
    db.session.commit()

    response = client.get("/projects/01DB2ECBP24NHYV5KZQG2N3FS3")

    # Ensure the response status code is 422 (Unprocessable Entity)
    assert response.status_code == 422
    assert response.json.get("error") == "Unprocessable Entity"

    db.session.(duplicate_project)
    db.session.commit()



@pytest.mark.usefixtures("db_create")
def test_grants(client):
    response = client.get('/grants')
    assert response.status_code == 200
    assert response.get_json() is not None

    response = client.get('/grants/123')
    assert response.status_code == 404

    response = client.get('/grants/01DB2ECBP3XQ4B8Z5DW7W963YD')
    assert response.status_code == 200

    with open('tests/responses/grant.json', 'r') as f:
        expected_data = json.load(f)
    
    response_data = response.json
    assert response_data == expected_data

@pytest.mark.usefixtures("db_create")
def test_people(client):
    response = client.get('/people')
    assert response.status_code == 200
    assert response.get_json() is not None

    response = client.get('/people/123')
    assert response.status_code == 404

    response = client.get('/people/01DB2ECBP2MFB0DH3EF3PH74R0')
    assert response.status_code == 200

    with open('tests/responses/person.json', 'r') as f:
        expected_data = json.load(f)
    
    response_data = response.json
    assert response_data == expected_data

@pytest.mark.usefixtures("db_create")
def test_participants(client):
    response = client.get('/participants')
    assert response.status_code == 200
    assert response.get_json() is not None

    response = client.get('/participants/123')
    assert response.status_code == 404

    response = client.get('/participants/01DB2ECBP3622SPB5PS3J8W4XF')
    assert response.status_code == 200

    with open('tests/responses/participant.json', 'r') as f:
        expected_data = json.load(f)
    
    response_data = response.json
    assert response_data == expected_data

@pytest.mark.usefixtures("db_create")
def test_organisations(client):
    response = client.get('/organisations')
    assert response.status_code == 200
    assert response.get_json() is not None

    response = client.get('/organisations/123')
    assert response.status_code == 404

    response = client.get('/organisations/01DB2ECBP3WZDP4PES64XKXJ1A')
    assert response.status_code == 200

    with open('tests/responses/organisation.json', 'r') as f:
        expected_data = json.load(f)
    
    response_data = response.json
    assert response_data == expected_data

@pytest.mark.usefixtures("db_create")
def test_allocations(client):
    response = client.get('/allocations')
    assert response.status_code == 200
    assert response.get_json() is not None

    response = client.get('/allocations/123')
    assert response.status_code == 404

    response = client.get('/allocations/01DB2ECBP35AT5WBG092J5GDQ9')
    assert response.status_code == 200

    with open('tests/responses/allocation.json', 'r') as f:
        expected_data = json.load(f)
    
    response_data = response.json
    assert response_data == expected_data

@pytest.mark.usefixtures("db_create")
def test_categorisations(client):
    response = client.get('/categorisations')
    assert response.status_code == 200
    assert response.get_json() is not None

    response = client.get('/categorisations/123')
    assert response.status_code == 404

    response = client.get('/categorisations/01DC6HYAKYAXE7MZMD08QV5JWG')
    assert response.status_code == 200

    with open('tests/responses/categorisation.json', 'r') as f:
        expected_data = json.load(f)
    
    response_data = response.json
    assert response_data == expected_data

@pytest.mark.usefixtures("db_create")
def test_category_schemes(client):
    response = client.get('/category-schemes')
    assert response.status_code == 200
    assert response.get_json() is not None

    response = client.get('/category-schemes/123')
    assert response.status_code == 404

    response = client.get('/category-schemes/01DC6HYAKXG8FCN63D7DH06W84')
    assert response.status_code == 200

    with open('tests/responses/category_scheme.json', 'r') as f:
        expected_data = json.load(f)
    
    response_data = response.json
    assert response_data == expected_data

@pytest.mark.usefixtures("db_create")
def test_category_terms(client):
    response = client.get('/categories')
    assert response.status_code == 200
    assert response.get_json() is not None

    response = client.get('/categories/123')
    assert response.status_code == 404

    response = client.get('/categories/01DC6HYAKX993ZK6YHCVWAE169')
    assert response.status_code == 200

    with open('tests/responses/category_term.json', 'r') as f:
        expected_data = json.load(f)
    
    response_data = response.json
    assert response_data == expected_data