import pytest
from lib.my_requests import MyRequests
import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("Тесты на авторизацию")
@allure.link("Cсылка на какой-то внешний ресурс")
class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]
    def setup(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234',
        }
        response1 = MyRequests.post("/user/login",data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token= self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    @allure.issue("ID дефекта в баг-треккинговой системе")
    @allure.testcase("ID теста в системе управления тестированием")
    @allure.description("This test successfuly authorise user by email and password")
    def test_auth_user(self):
        response2 = MyRequests.get("/user/auth",
        headers={"x-csrf-token": self.token},
        cookies={"auth_sid":self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            self.user_id_from_auth_method,
            "User id from auth method is not equal to user id from check method"
        )

    @allure.description("This test checks uatorization status w/o sending auth cookie or token")
    @pytest.mark.parametrize('condition',exclude_params)
    def test_auth_check_negative(self,condition):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234',
        }

        if condition == "no_cookie":
            #resp2 = requests.get("https://playground.learnqa.ru/api/user/auth",
            resp2=MyRequests.get("/user/auth",
            headers={"x-csrf-token": self.token},
            )
        else:
            #resp2 = requests.get("https://playground.learnqa.ru/api/user/auth",
             resp2=MyRequests.get("/user/auth",
             cookies={"auth_sid": self.auth_sid}
            )

        Assertions.assert_json_value_by_name(
            resp2,
            "user_id",
            0,
            f"User autorised wiht method {condition}"
        )