import unittest
from unittest.mock import patch, Mock
from duco import DucoDevice  # Adjust the import according to your module name

class TestDucoDevice(unittest.TestCase):
    def setUp(self):
        # Set up a DucoDevice instance with test parameters
        self.device = DucoDevice(address="192.168.1.100", port=80)

    @patch('requests.get')
    def test_fetch_json_success(self, mock_get):
        # Mock response object
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{"action_state": "SUCCESS"}'
        mock_response.headers = {'content-type': 'application/json'}
        mock_response.json.return_value = {"action_state": "SUCCESS"}
        mock_get.return_value = mock_response
        
        # Call fetch_json and check the result
        result = self.device.fetch_json("some_query")
        self.assertEqual(result, {"action_state": "SUCCESS"})

    @patch('requests.get')
    def test_fetch_json_failed_response(self, mock_get):
        # Mock response object
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = 'FAILED'
        mock_response.headers = {'content-type': 'text/plain'}
        mock_get.return_value = mock_response
        
        # Call fetch_json and check the result
        result = self.device.fetch_json("some_query")
        self.assertEqual(result, {"action_state": "FAILED"})
    
    @patch('requests.get')
    def test_fetch_json_non_json(self, mock_get):
        # Mock a non-JSON response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = 'Non-JSON response'
        mock_response.headers = {'content-type': 'text/html'}
        mock_get.return_value = mock_response
        
        # Call fetch_json and check for None (unexpected content type)
        result = self.device.fetch_json("some_query")
        self.assertIsNone(result)

    @patch('requests.get')
    def test_get_cap_board_info(self, mock_get):
        # Mock response for board info
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "serial": "ASDF22403066",
            "uptime": 5433179,
            "swversion": "16036.13.4.0",
            "mac": "01:02:0f:34:a6:0f",
            "ip": "192.168.11.6"
        }
        mock_get.return_value = mock_response
        
        # Call get_cap_board_info and check the result
        result = self.device.get_cap_board_info()
        self.assertEqual(result, {
            "serial": "ASDF22403066",
            "uptime": 5433179,
            "swversion": "16036.13.4.0",
            "mac": "01:02:0f:34:a6:0f",
            "ip": "192.168.11.6"
        })
    
    @patch('requests.get')
    def test_get_node_list(self, mock_get):
        # Mock response for node list
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"nodelist": [1, 2, 3]}
        mock_get.return_value = mock_response
        
        # Call get_node_list and check the result
        result = self.device.get_node_list()
        self.assertEqual(result, [1, 2, 3])
    
    @patch('requests.get')
    def test_get_node_info(self, mock_get):
        # Mock response for node info
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "node": 1,
            "devtype": "BOX",
            "subtype": 0,
            "netw": "VIRT",
            "addr": 1,
            "sub": 1,
            "location": "Washing Machine",
            "state": "AUTO"
        }
        mock_get.return_value = mock_response
        
        # Call get_node_info and check the result
        result = self.device.get_node_info(1)
        self.assertEqual(result, {
            "node": 1,
            "devtype": "BOX",
            "subtype": 0,
            "netw": "VIRT",
            "addr": 1,
            "sub": 1,
            "location": "Washing Machine",
            "state": "AUTO"
        })
    
    @patch('requests.get')
    def test_set_node_operational_state(self, mock_get):
        # Mock response for setting operational state
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"action_state": "SUCCESS"}
        mock_get.return_value = mock_response
        
        # Call set_node_operational_state and check the result
        result = self.device.set_node_operational_state(1, "OFF")
        self.assertEqual(result, {"action_state": "SUCCESS"})

if __name__ == '__main__':
    unittest.main()