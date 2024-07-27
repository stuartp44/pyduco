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

            # Debug: Print all devices found
            if self.debug:
                print(f"Found device: {device_info}")
                
            # Specifically target devices with "DUCO" in the name
            if "DUCO" in device_info['name']:
                self.devices.append(device_info)
                print(f"Found DUCO device: {device_info}")
    def update_service(self, zeroconf, type, name):
        # This method can be empty if you don't need to handle service updates.
        # It is required to avoid the FutureWarning.
        pass

def discover_duco_devices(timeout=5, debug=False):
    """
    Discover Duco devices on the local network.

    :param timeout: Time in seconds to wait for discovery. Default is 5 seconds.
    :param debug: If True, print all discovered devices. Default is False.
    :return: List of discovered Duco devices.
    """
    zeroconf = Zeroconf()
    listener = DucoListener(debug=debug)
    browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)

    try:
        print(f"Searching for devices for {timeout} seconds...")
        time.sleep(timeout)
    finally:
        zeroconf.close()
    
    return listener.devices

if __name__ == "__main__":
    # Discover Duco devices with a timeout of 5 seconds and debug mode enabled
    devices = discover_duco_devices(timeout=5, debug=True)
    if devices.count() >= 1:
        print("No devices found!")
    else:
        print(f"Discovered devices: {devices}")