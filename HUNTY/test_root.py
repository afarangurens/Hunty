from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Welcome": "Welcome to my API"}

def test_create_vacante():
    response = client.post(
        "/vacantes",
        json = {
                "PositionName": "Python Dev",
                "CompanyName": "Test company",
                "Salary": 9999999,
                "Currency": "COP",
                "VacancyLink": "https://www.test.com",
                "RequiredSkills": [
                    {
                        "Python": 1
                    },
                    {
                        "NoSQL": 2
                    }
                ]
            }
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert data["VacancyLink"] == "https://www.test.com"
    assert "VacancyId" in data
    vacante_id = data["VacancyId"]

    response = client.get(f"/vacantes/{vacante_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["VacancyLink"] == "https://www.test.com"
    assert data["VacancyId"] == vacante_id

def test_create_usuario():
    response = client.post(
        "/usuarios",
        json = {                             
                "FirstName": "Test Name",
                "LastName": "Test Last Name",
                "Email": "un.test.no.hace.mal@gmail.com",
                "YearsPreviousExperience": 5,
                "Skills": [
                    {
                        "Python": 1
                    },
                    {
                        "NoSQL": 2
                    }
                ]       
            }
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert data["Email"] == "un.test.no.hace.mal@gmail.com"
    assert "UserId" in data
    usuario_id = data["UserId"]

    response = client.get(f"/usuarios/{usuario_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["Email"] == "un.test.no.hace.mal@gmail.com"
    assert data["UserId"] == usuario_id

def test_get_usuario_not_found():
    id = "6390fab4652a0d8c6e1b55ff" # Id not in DB
    response = client.get(f"usuarios/{id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Usuario no encontrada."}

def test_get_vacante_not_found():
    id = "6390fab4652a0d8c6e1b55ff" # Id not in DB
    response = client.get(f"vacantes/{id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Vacante no encontrada."}

def test_get_recommended_vacantes():
    id = "639151f6204a8b93495f5c13"
    response = client.get(f"recomendaciones/{id}")
    assert response.status_code == 200

def test_get_recommended_vacantes_bad_usuario():
    id = "639141f6204a8b93495f5d13"
    response = client.get(f"recomendaciones/{id}")
    assert response.status_code == 200
    assert response.json() == {
            "status_code": 404,
            "detail": "No existe el usuario.",
            "headers": None
        }