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

        expected_fields = ["email","firstName","lastName","username"]
        Assertions.assert_json_has_keys(response2,expected_fields)
        # DELETE
        response3 = requests.delete(
            f"https://playground.learnqa.ru/api/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid})


        Assertions.assert_status_code(response3, 400)
        assert response3.content.decode("utf-8") == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response content {response3.content}"
         #GET_USER
        response4 = requests.get(
            f"https://playground.learnqa.ru/api/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["email", "firstName", "lastName", "username"]
        Assertions.assert_json_has_keys(response4, expected_fields)

    #создание пользователя, удаление и получение его по id
    def test_delete_just_created_user(self):
        response5 = requests.post("https://playground.learnqa.ru/api/user/login", data=self.login_data)

        auth_sid = self.get_cookie(response5, "auth_sid")
        token = self.get_header(response5, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response5, "user_id")
        # DELETE
        response6 = requests.delete(
            f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}",
            headers = {"x-csrf-token": token},
            cookies = {"auth_sid": auth_sid}
        )

        Assertions.assert_status_code(response6, 200)
        # GET_USER
        response7 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        assert response7.content.decode("utf-8") == "User not found", \
            f"Unexpected response content {response7.content}"

    #удаление пользователя, будучи авторизованными другим пользователем
    def test_delete_user_with_auth_another_user(self):
        #AUTH
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response8 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)


        Assertions.assert_status_code(response8, 200)
        auth_sid = self.get_cookie(response8, "auth_sid")
        token = self.get_header(response8, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response8, "user_id")

        # DELETE
        response9 = requests.delete(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",
            headers = {"x-csrf-token": token},
            cookies = {"auth_sid": auth_sid}

        )

        Assertions.assert_status_code(response9, 400)
        assert response9.content.decode("utf-8") == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
              f"Unexpected response content {response9.content}"

        #GET_USER
        response10 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["email", "firstName", "lastName", "username"]
        Assertions.assert_json_has_keys(response10, expected_fields)