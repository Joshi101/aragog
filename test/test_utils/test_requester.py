import requests

from utils.requester import Requester


class TestRequester:

    @classmethod
    def setup_class(cls):

        print(f"creating setup for class {cls.__name__}")
        cls.url = "http://www.example.com"
        cls.test_response = requests.get("http://www.example.com")

    def test_make_request(self):

        response = Requester(url=self.url).make_request()
        assert response == self.test_response.text

    @classmethod
    def teardown_class(cls):
        print(f"tearing setup for class {cls.__name__}")

