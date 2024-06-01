"""
Unit tests for the module heat_pump_backend
"""

from unittest import TestCase
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.heat_pump_backend import app


class TestHeatPumpBackend(TestCase):
    """
    TestCase class, which contains all the unit test for the FastAPI
    endpoints.

    The calls to our .c functions are mocked, to ensure reproducibility
    and atomicity
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Runs only once, before all the tests. Set up shared variables
        across all the tests
        """
        cls.client = TestClient(app)

    @patch("backend.heat_pump_backend.HP_TOOLS.read_water_temperature")
    def test_get_water_temperature(self, mock_read_water_temperature):
        """
        Tests the endpoint ``get_water_temperature``
        """
        # prepare the mock
        mock_read_water_temperature.return_value = 275

        # test
        response = self.client.get("/get_water_temperature/")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"current_water_temperature": 27.5})
        mock_read_water_temperature.assert_called_once()

    @patch("backend.heat_pump_backend.HP_TOOLS.read_water_temperature")
    def test_get_water_temperature_communication_error(
        self, mock_read_water_temperature
    ):
        """
        Tests the endpoint ``get_water_temperature``, when the program is unable
        to communicate with the heat pump
        """
        # prepare the mock
        mock_read_water_temperature.return_value = -1

        # test
        response = self.client.get("/get_water_temperature/")
        self.assertEqual(response.status_code, 500)
        self.assertDictEqual(
            response.json(), {"detail": "Unable to communicate with the heat pump"}
        )
        mock_read_water_temperature.assert_called_once()

    @patch("backend.heat_pump_backend.HP_TOOLS.read_target_water_temperature")
    def test_get_target_water_temperature(self, mock_read_target_water_temperature):
        """
        Tests the endpoint ``get_target_water_temperature``
        """
        # prepare the mock
        mock_read_target_water_temperature.return_value = 280

        # test
        response = self.client.get("/get_target_water_temperature/")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"target_water_temperature": 28.0})
        mock_read_target_water_temperature.assert_called_once()

    @patch("backend.heat_pump_backend.HP_TOOLS.read_target_water_temperature")
    def test_get_target_water_temperature_communication_error(
        self, mock_read_target_water_temperature
    ):
        """
        Tests the endpoint ``get_target_water_temperature``, when the program
        is unable to communicate with the heat pump
        """
        # prepare the mock
        mock_read_target_water_temperature.return_value = -1

        # test
        response = self.client.get("/get_target_water_temperature/")
        self.assertEqual(response.status_code, 500)
        self.assertDictEqual(
            response.json(), {"detail": "Unable to communicate with the heat pump"}
        )
        mock_read_target_water_temperature.assert_called_once()

    @patch("backend.heat_pump_backend.HP_TOOLS.set_target_water_temperature")
    def test_set_target_water_temperature(self, mock_set_target_water_temperature):
        """
        Tests the endpoint ``set_target_water_temperature``
        """
        # prepare the mock
        mock_set_target_water_temperature.return_value = 30

        # test
        response = self.client.post(
            "/set_target_water_temperature/", json={"target_water_temperature": 30}
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"target_water_temperature": 30})
        mock_set_target_water_temperature.assert_called_once_with(300)

    def test_set_target_water_temperature_value_out_of_range(self):
        """
        Tests the endpoint ``set_target_water_temperature``, when the user input is out of the expected range
        """
        # when the target is too small
        response = self.client.post(
            "/set_target_water_temperature/", json={"target_water_temperature": 10}
        )
        self.assertEqual(response.status_code, 422)

        # or too big
        response = self.client.post(
            "/set_target_water_temperature/", json={"target_water_temperature": 50}
        )
        self.assertEqual(response.status_code, 422)

    def test_set_target_water_temperature_value_not_multiple_of_half(self):
        """
        Tests the endpoint ``set_target_water_temperature``, when the user input is not a multiple of 0.5
        """
        response = self.client.post(
            "/set_target_water_temperature/", json={"target_water_temperature": 28.7}
        )
        self.assertEqual(response.status_code, 422)

    @patch("backend.heat_pump_backend.HP_TOOLS.set_target_water_temperature")
    def test_set_target_water_temperature_communication_error(
        self, mock_set_target_water_temperature
    ):
        """
        Tests the endpoint ``set_target_water_temperature``, when the program
        is unable to communicate with the heat pump
        """
        # prepare the mock
        mock_set_target_water_temperature.return_value = -1

        # test
        response = self.client.post(
            "/set_target_water_temperature/", json={"target_water_temperature": 30.5}
        )
        self.assertEqual(response.status_code, 500)
        self.assertDictEqual(
            response.json(), {"detail": "Unable to communicate with the heat pump"}
        )
        mock_set_target_water_temperature.assert_called_once_with(305)
