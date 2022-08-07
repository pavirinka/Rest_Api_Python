import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):
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
        self.new_name = "Changet Name"

    # изменение данных пользователя, будучи неавторизованными
    def test_edit_just_created_user_without_auth(self):
    #EDIT
        response3 = requests.put(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",
            data = {"firstName": self.new_name}
        )

        Assertions.assert_status_code(response3, 400)
        assert response3.content.decode("utf-8") == "Auth token not supplied", \
            f"Unexpected response content {response3.content}"

    def test_edit_just_created_user_with_another_user_auth(self):
    #изменение данных пользователя, будучи авторизованными другим пользователем
    #LOGIN

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=self.login_data)
        Assertions.assert_status_code(response2, 200)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")



        response4 = requests.put(
            "https://playground.learnqa.ru/api/user/40439",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"username": self.new_name}
        )


        #Assertions.assert_status_code(response4, 200)
        response5 = requests.get(
            "https://playground.learnqa.ru/api/user/40439",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
            )
        assert response5.content.decode("utf-8") == '{"username":"learnqa"}', \
            f"Unexpected response content {response2.content}"

    def test_edit_email_just_created_user_with_user_auth(self):
    # изменение email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @
    # REGISTRATE
        #register_data = self.prepare_registration_data()
        #response6 = requests.post("https://playground.learnqa.ru/api/user/", data= register_data)

        #Assertions.assert_status_code(response6, 200)
        #Assertions.assert_json_has_key(response6, "id")
    #LOGIN
        response7 = requests.post("https://playground.learnqa.ru/api/user/login", data=self.login_data)

        Assertions.assert_status_code(response7, 200)
        self.auth_sid = self.get_cookie(response7, "auth_sid")
        self.token = self.get_header(response7, "x-csrf-token")
    #EDIT
        response8 = requests.put(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",

            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"email": 'vinkotovexample.com'}
        )

        Assertions.assert_status_code(response8, 400)
        assert response8.content.decode("utf-8") == "Invalid email format", \
              f"Unexpected response content {response8.content}"

   #изменнение firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
    def test_edit_short_firstName_just_created_user_with_user_auth(self):
    #LOGIN
        response9 = requests.post("https://playground.learnqa.ru/api/user/login", data=self.login_data)

        Assertions.assert_status_code(response9, 200)
        self.auth_sid = self.get_cookie(response9, "auth_sid")
        self.token = self.get_header(response9, "x-csrf-token")

    #EDIT
        response10 = requests.put(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",

            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"firstName": "."}
        )

        Assertions.assert_status_code(response10, 400)
        assert response10.content.decode("utf-8") == '{"error":"Too short value for field firstName"}', \
              f"Unexpected response content {response10.content}"

