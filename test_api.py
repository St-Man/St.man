import unittest
import DemoApi as demoapi
import json
from tornado.testing import AsyncHTTPTestCase


class TestApi(AsyncHTTPTestCase):

    def get_app(self):
        """Initializing the app from the API."""
        return demoapi.make_app()

    def test_HomeHandler(self):
        """Test the HomeHandler."""
        response = self.fetch('/')
        self.assertEqual(response.body.decode('utf-8'), 'RestAPI Home')

    def test_NumberOfVictimsHandler(self):
        """Test the NumberOfVictimsHandler."""
        response = self.fetch('/numberofvictims')
        number_of_victims = json.loads(response.body)
        self.assertEqual(number_of_victims['number of connected victims'], 2)

    def test_ConnectedVictimsHandler(self):
        """Test the ConnectedVIctimsHandler."""
        response = self.fetch('/connectedvictims')
        victims_json = json.loads(response.body)

        self.assertEqual(victims_json, {"victims": [{"IP": "192.168.1.1",
                                        "MAC": "78:44:76:bf:8d:6f",
                                        "Manufacturer":
                                        "Zioncom Electronics (Shenzhen)"},
                                        {"IP": "192.168.1.2",
                                        "MAC": "94:0e:6b:3f:5a:6d",
                                        "Manufacturer":
                                        "Huawei Technologies"}]})

    def test_VictimInfoHandler(self):
        """Test the VictimInfoHandler."""
        response = self.fetch('/victiminfo?macaddress=78:44:76:bf:8d:6f')
        victims_json = json.loads(response.body)

        self.assertEqual(victims_json, {"IP": "192.168.1.1", "MAC":
                                         "78:44:76:bf:8d:6f", "Manufacturer":
                                         "Zioncom Electronics (Shenzhen)"})


if __name__ == '__main__':
    unittest.main()
