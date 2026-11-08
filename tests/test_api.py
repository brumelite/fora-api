from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    assert client.get("/health").json() == {"status":"ok"}

def test_openapi_paths():
    schema = client.get("/openapi.json").json()
    expected = {"/health","/v1/fortunes/random","/v1/fortunes/daily","/v1/fortunes/answer","/v1/fortunes/{id}","/v1/categories","/v1/languages"}
    assert expected <= set(schema["paths"])

def test_error_shape():
    from fastapi import HTTPException
    from app.main import err
    try:
        err("FORTUNE_NOT_FOUND","No entry")
    except HTTPException as exc:
        assert exc.detail["code"] == "FORTUNE_NOT_FOUND"
