import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        response2 = requests.get(
            "https://playground.learnqa.ru/api/user/1",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
            )
        unexpected_fields = ["email","firstName","lastName"]
        Assertions.assert_json_has_not_keys(response2,unexpected_fields)
        Assertions.assert_json_has_key(response2,"username")






