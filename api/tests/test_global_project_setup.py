import unittest
from db_models.models import UserModel


class TestStringMethods(unittest.TestCase):


    def test_auth(self):
        response = self.client.get('',follow= TR)
        self.signup = UserModel.sign_up(user_name="Atris", email="atris@admin.com", first_name="Atris",
                                        last_name="Test", picture=False, password=False, user_check=True)
        user_model_obj = UserModel()
        self.token = user_model_obj.
        self.verfiy = user_model_obj.verified = True
        self.assertTrue(