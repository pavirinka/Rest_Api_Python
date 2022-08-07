import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserDelete(BaseCase):
    #REGISTER
    def setup(self):
        register_data = self.prepare_registration_data()
        response = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

        self.email = register_data['email']
        self.first_name = register_data['firstName']
        self.password = register_data['password']
        self.user_id = self.get_json_value(response, "id")

        self.login_data = {
            'email': self.email,
            'password': self.password
        }

        # попыткa удалить пользователя по ID 2
    def test_delete_user_with_id_2(self):
        #AUTH
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        response2 = requests.get(
            "https://playground.learnqa.ru/api/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        unexpected_fields = ["email","firstName","lastName","username"]
        Assertions.assert_json_has_keys(response2,unexpected_fields)
        # DELETE
        response3 = requests.delete(f"https://playground.learnqa.ru/api/user/{id}")

        Assertions.assert_status_code(response3, 404)
        assert response3.content.decode("utf-8") == "This is 404 error!\n<a href='/'>Home</a>" , \
            f"Unexpected response content {response3.content}"
    #создание пользователя, удаление и получение его по id
    def test_delete_just_created_user(self):
        response4 = requests.post("https://playground.learnqa.ru/api/user/login", data=self.login_data)

        auth_sid = self.get_cookie(response4, "auth_sid")
        token = self.get_header(response4, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response4, "user_id")
        # DELETE
        response5 = requests.delete(
            f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}",
            headers = {"x-csrf-token": token},
            cookies = {"auth_sid": auth_sid}
        )

        Assertions.assert_status_code(response5, 200)
        # GETgUSER
        response6 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        assert response6.content.decode("utf-8") == "User not found", \
            f"Unexpected response content {response6.content}"

    #удаление пользователя, будучи авторизованными другим пользователем
    def test_delete_user_with_auth_another_user(self):
        #AUTH
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response7 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        Assertions.assert_status_code(response7, 200)
        auth_sid = self.get_cookie(response7, "auth_sid")
        token = self.get_header(response7, "x-csrf-token")

        # DELETE
        response8 = requests.delete(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",
            headers = {"x-csrf-token": token},
            cookies = {"auth_sid": auth_sid}
        )

        Assertions.assert_status_code(response8, 400)
        assert response8.content.decode("utf-8") == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
              f"Unexpected response content {response8.content}"

