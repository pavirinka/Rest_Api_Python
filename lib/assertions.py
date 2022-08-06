from requests import Response
import json

class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not json format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response json doesn't have key '{name}'"
        assert response_as_dict[name] == expected_value , f"Response json doesn't have key '{error_message}'"

    @staticmethod
    def assert_status_code(response: Response, expected_status_code):
        assert response.status_code == expected_status_code,\
            f"Unexpected status code! Expected : {expected_status_code}. Actual: {response.status_code}"

