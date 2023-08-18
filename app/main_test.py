from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_generate_gherkin_code():
    """testing generate_gherkin_code method"""
    request_body = {
        "domain": "test_domain",
        "requestId": 123,
        "requirementText": "Test requirement text",
    }
    response = client.post("/v1/generate-gherkin", json=request_body)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SUCCESS"
    assert data["statusCode"] == 200
    assert data["requestId"] == request_body["requestId"]
    assert "generatedGherkin" in data


def test_generate_gherkin_code_invalid_request_id():
    request_body = {
        "domain": "test_domain",
        "requestId": -123,
        "requirementText": "Test requirement text",
    }
    response = client.post("/v1/generate-gherkin", json=request_body)
    assert response.status_code == 422
    data = response.json()
    assert data["status"] == "FAIL"
    assert data["statusCode"] == 422
    assert "message" in data


def test_check_health():
    health_response = client.get("/v1/health")
    data = health_response.json()
    assert data == {"isAlive": True}


def test_get_model_metadata():
    response = client.get("/v1/model")
    assert response.status_code == 200
    data = response.json()
    assert data["modelName"] == "Curiosity Model"
    assert data["version"] == "1.0.0"
    assert (
        data["description"]
        == "This is the Curiosity Model\
        used for Gherkin code generation."
    )
    assert data["author"] == "Curiosity"
    assert data["lastUpdated"] == "2023-07-26T12:34:56Z"


def test_not_found():
    response = client.get("/invalid-endpoint")
    assert response.status_code == 404
    data = response.json()
    assert data["status"] == "FAIL"
    assert data["statusCode"] == 404
    assert data["message"] == "Requested Endpoint Not Found"
