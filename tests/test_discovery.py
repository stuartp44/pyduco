import unittest
from unittest.mock import patch, Mock
from zeroconf import Zeroconf, ServiceInfo
from duco import discover_duco_devices  # Adjust import paths as necessary

class TestDucoDiscovery(unittest.TestCase):

    @patch('zeroconf.Zeroconf')
    @patch('zeroconf.ServiceBrowser')
    def test_discover_duco_devices(self, mock_service_browser, mock_zeroconf):
        # Mock Zeroconf instance
        mock_zeroconf_instance = Mock()
        mock_zeroconf.return_value = mock_zeroconf_instance

        # Create a mock ServiceInfo object
        mock_service_info = Mock(spec=ServiceInfo)
        mock_service_info.name = "DUCO [01025334A506]._http._tcp.local."
        mock_service_info.server = "duco001.local."
        mock_service_info.addresses = [[192, 168, 1, 16]]
        mock_service_info.port = 80

        # Mock ServiceBrowser and its behavior
        def add_listener(listener):
            # Directly call the listener's method to simulate service discovery
            listener.add_service(mock_zeroconf_instance, "_http._tcp.local.", mock_service_info.name)
        
        mock_service_browser.side_effect = lambda *args, **kwargs: add_service(args[2])

        # Test discover_duco_devices function
        devices = discover_duco_devices(timeout=5, debug=True)
        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0]['name'], mock_service_info.name)
        self.assertEqual(devices[0]['address'], '192.168.11.16')
        self.assertEqual(devices[0]['port'], mock_service_info.port)
        self.assertEqual(devices[0]['server'], mock_service_info.server)

    @patch('zeroconf.ServiceBrowser')
    @patch('zeroconf.Zeroconf')
    def test_no_duco_devices_found(self, mock_zeroconf, mock_service_browser):
        # Simulate no services being discovered
        mock_service_browser.return_value = None

        # Test discover_duco_devices function
        devices = discover_duco_devices(timeout=1, debug=True)
        self.assertEqual(len(devices), 0)

if __name__ == '__main__':
    unittest.main()