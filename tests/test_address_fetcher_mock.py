import unittest
from unittest.mock import patch, MagicMock
from app.utils.address_fetcher import address_fetcher

class TestAddressFetcher(unittest.TestCase):

    @patch('app.utils.address_fetcher.requests.get')
    def test_fetch_real_address_success(self, mock_get):
        # Mock Response Data (Real sample from OSM)
        mock_response = {
            "place_id": 12345,
            "display_name": "Hotel Empire, 44, West 63rd Street, Lincoln Square, Manhattan, New York County, New York, 10023, United States",
            "address": {
                "hotel": "Hotel Empire",
                "house_number": "44",
                "road": "West 63rd Street",
                "suburb": "Lincoln Square",
                "borough": "Manhattan",
                "county": "New York County",
                "city": "New York",
                "state": "New York",
                "postcode": "10023",
                "country": "United States",
                "country_code": "us"
            }
        }
        
        mock_resp_obj = MagicMock()
        mock_resp_obj.status_code = 200
        mock_resp_obj.json.return_value = [mock_response] 
        mock_get.return_value = mock_resp_obj

        result = address_fetcher.fetch_real_address("US", city="New York")

        self.assertIsNotNone(result)
        self.assertEqual(result['city'], "New York")
        self.assertEqual(result['zipcode'], "10023")
        self.assertEqual(result['country'], "United States")
        self.assertIn("West 63rd Street", result['address'])
        print("\n✅ Test Success: Parsed Mock OSM Response correctly.")

    @patch('app.utils.address_fetcher.requests.get')
    def test_fallback_logic(self, mock_get):
        # Scenario: Level 1 fails (empty list), Level 2 succeeds
        empty_resp = MagicMock()
        empty_resp.status_code = 200
        empty_resp.json.return_value = []

        valid_resp_data = {
            "address": {
                "road": "Random St",
                "city": "Chicago",
                "country": "United States",
                "postcode": "60601"
            },
            "display_name": "Random St, Chicago, US"
        }
        valid_resp = MagicMock()
        valid_resp.status_code = 200
        valid_resp.json.return_value = [valid_resp_data]

        mock_get.side_effect = [empty_resp, valid_resp, valid_resp, valid_resp] 

        result = address_fetcher.fetch_real_address("US", city="NonExistentCity")
        
        self.assertIsNotNone(result)
        self.assertEqual(result['city'], "Chicago")
        print("✅ Test Success: Fallback logic worked.")

    @patch('app.utils.address_fetcher.requests.get')
    def test_zipcode_search(self, mock_get):
        # Scenario: Search with Zipcode
        mock_response = {
            "address": {
                "road": "Beverly Dr",
                "city": "Beverly Hills",
                "postcode": "90210",
                "country": "United States"
            },
            "display_name": "Beverly Dr, Beverly Hills, US"
        }
        mock_resp_obj = MagicMock()
        mock_resp_obj.status_code = 200
        mock_resp_obj.json.return_value = [mock_response]
        mock_get.return_value = mock_resp_obj

        result = address_fetcher.fetch_real_address("US", zipcode="90210")

        self.assertIsNotNone(result)
        self.assertEqual(result['zipcode'], "90210")
        
        # Verify that zipcode was actually in the query params of the call
        args, kwargs = mock_get.call_args
        params = kwargs['params']
        self.assertIn("90210", params['q'])
        print("✅ Test Success: Zipcode included in search query.")

if __name__ == '__main__':
    unittest.main()
