from zeroconf import ServiceBrowser, Zeroconf
import time
import requests

class DucoListener:
    def __init__(self, debug=False):
        self.devices = []
        self.debug = debug
        self.version = None

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        
        if info:
            api_version = get_api_version(info.address, self.debug)
            
            device_info = {
                'name': info.name,
                'address': '.'.join(map(str, info.addresses[0])),
                'port': info.port,
                'server': info.server,
                'api_version': api_version
            }

            if self.debug:
                print(f"Found device: {device_info}")

            if "DUCO" in device_info['name']:
                self.devices.append(device_info)
                print(f"Found DUCO device: {device_info}")

    def update_service(self, zeroconf, type, name):
        pass

def get_api_version(ip, debug=False):
    try:
        response = requests.get(f"http://{ip}/info")
        if response.status_code == 200:
            data = response.json()
            version = data.get('General', {}).get('Board', {}).get('PublicApiVersion', {}).get('Val', 'unknown')
            if debug:
                print(response)
                print(data)
                print(version)
        elif response.status_code == 404:
            response = requests.get(f"http://{ip}/boxinfoget")
            # Todo do more here to get information that its a v1
            if debug:
                print(response)
            if response.status_code == 200:
                version = '1.0'
        else:
            version = 'unknown'
    except requests.RequestException as e:
        if debug:
            print(f"Error fetching version info: {e}")
        version = 'unknown'
    
    return version

def discover_duco_devices(timeout=5, debug=False, zeroconf_instance=None):
    """
    Discover Duco devices on the local network.

    :param timeout: Time in seconds to wait for discovery. Default is 5 seconds.
    :param debug: If True, print all discovered devices. Default is False.
    :param zeroconf_instance: Optional Zeroconf instance. If not provided, a new one will be created.
    :return: List of discovered Duco devices.
    """
    zeroconf = zeroconf_instance or Zeroconf()
    listener = DucoListener(debug=debug)
    browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)

    try:
        print(f"Searching for devices for {timeout} seconds...")
        time.sleep(timeout)
    finally:
        if zeroconf_instance is None:
            zeroconf.close()
    
    return listener.devices