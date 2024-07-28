from zeroconf import ServiceBrowser, Zeroconf
import time

class DucoListener:
    def __init__(self, debug=False):
        self.devices = []
        self.debug = debug

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info:
            device_info = {
                'name': info.name,
                'address': '.'.join(map(str, info.addresses[0])),
                'port': info.port,
                'server': info.server
            }

            if self.debug:
                print(f"Found device: {device_info}")

            if "DUCO" in device_info['name']:
                self.devices.append(device_info)
                print(f"Found DUCO device: {device_info}")

    def update_service(self, zeroconf, type, name):
        pass

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