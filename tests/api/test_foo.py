import unittest

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


class TestAPI(unittest.TestCase):
    def test_foo(self):
        response = client.get("/")

        assert response.status_code == 200
        assert response.json() == {"Hello": "World"}


if __name__ == "__main__":
    unittest.main()
