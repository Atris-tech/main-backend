import os
os.environ["TESTING_ATRIS"] = "True"
from db_models.models.user_model import UserModel
import unittest
import json
from fastapi.testclient import TestClient
from main import app
from mongoengine.connection import get_connection


class TestAuthMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        payload = {
            "email": "Atristestcase@admin.com",
            "first_name": "Atris",
            "last_name": "Testcase",
            "password": "1234",
            "user_name": "AtrisTestcase"
        }
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.signup_response = self.client.post("/api/register/", headers=self.headers, json=payload)
        print(self.signup_response)
        print(self.signup_response.text)
        try:
            self.user_obj = UserModel.objects.get(email_id="atristestcase@admin.com")
            # explicitly lowered case of email
            self.user_obj.verified = True
            self.user_obj.save()
        except UserModel.DoesNotExist:
            print("user does not exists")
        payload = {
            "email": "Atristestcase@admin.com",
            "password": "1234",
        }
        self.login_response = self.client.post("/api/login/", headers=self.headers, json=payload)
        token_data = json.loads(self.login_response.text)
        self.ref_token = str(token_data["ref_token"])
        self.access_token = str(token_data["access_token"])
        self.headers["Authorization"] = "Bearer " + self.access_token
        payload = {
            "workspace_name": "Atris Test Case",
            "emoji": "👨"
        }

        self.workspace_response = self.client.post("/api/create_workspace/", headers=self.headers, json=payload)
        print(self.workspace_response.text)

    def test_auth(self):
        self.assertEqual(json.loads(self.signup_response.text), True)
        self.assertEqual(self.signup_response.status_code, 200)

        self.assertNotEqual(self.login_response.text, False)
        self.assertEqual(self.login_response.status_code, 200)

    def test_workspace(self):
        self.assertEqual(self.workspace_response.status_code, 200)
        self.workspace_id = str(json.loads(self.workspace_response.text))

    @classmethod
    def teardown_class(cls):
        pass
        c1 = get_connection(alias='core')
        c1.drop_database('atris_test')
        os.environ["TESTING_ATRIS"] = "False"
