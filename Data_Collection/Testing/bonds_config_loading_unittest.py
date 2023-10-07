import unittest
from Data_Collection import bonds_api_query


class ConfigLoadTestCase(unittest.TestCase):
    json_config = bonds_api_query.load_config()

    def test_url(self):
        expected_url = "https://financialmodelingprep.com/api/v4/treasury?from={START_DATE}&to={END_DATE}&apikey={API_KEY}"
        retrieved_url = self.json_config[0]['api']  # Get the API field from the loaded JSON
        self.assertEqual(expected_url, retrieved_url, "Retrieved API URL does not match what was expected.")

    def test_api_key(self):
        expected_key = "CENSORED"
        retrieved_key = self.json_config[0]['api_key']  # Get the API field from the loaded JSON
        self.assertEqual(expected_key, retrieved_key, "Retrieved API key does not match what was expected.")


if __name__ == '__main__':
    unittest.main()
