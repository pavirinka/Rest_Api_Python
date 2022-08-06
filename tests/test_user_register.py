import requests
import pytest
import json
from lib.base_case import BaseCase
from lib.assertions import Assertions
import random
import string

class TestUserRegister(BaseCase):
    def test_create_user_with_incorrect_email(self):
        email = 'learnqaexample.com'
        data ={
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response1 =requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response1, 400)
        assert  response1.content.decode("utf-8") == "Invalid email format",\
            f"Unexpected response content {response1.content}"


    def test_create_user_with_short_firstName(self):
        firstName = random.choice(string.ascii_letters)
        data ={
            'password': '123',
            'username': 'learnqa',
            'firstName': firstName,
            'lastName': 'learnqa',
            'email': 'learnqa@example.com'
        }

        response2 =requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response2, 400)
        assert  response2.content.decode("utf-8") == "The value of 'firstName' field is too short",\
            f"Unexpected response content {response2.content}"


    def test_create_user_with_long_firstName(self):
        firstName = ''.join(random.choice(string.ascii_letters) for x in range(251))
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': firstName,
            'lastName': 'learnqa',
            'email': 'learnqa@example.com'
        }

        response3 =requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response3, 400)
        assert  response3.content.decode("utf-8") == "The value of 'firstName' field is too long",\
            f"Unexpected response content {response3.content}"

    datas = [({

            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'learnqa@example.com'
        },
            'password'),
        ({
            'password': '123',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'learnqa@example.com'
        },
            'username'),
        ({
            'password': '123',
            'username': 'learnqa',
            'lastName': 'learnqa',
            'email': 'learnqa@example.com'
        },
            'firstName'),
        ({
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'email': 'learnqa@example.com'
        },
            'lastName'),
        ({
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa'
        },
            'email')
    ]


    @pytest.mark.parametrize("datas, skipped_param", datas)
    def test_create_user_with_no_parametr(self, datas, skipped_param):
        data = datas
        response4 = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response4, 400)
        assert response4.content.decode("utf-8") == f"The following required params are missed: {skipped_param}",\
            f"Unexpected response content {response4.content}"
