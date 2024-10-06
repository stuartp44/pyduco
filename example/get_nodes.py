import asyncio
from duco import DucoDevice

async def main():
    # Discover Duco devices on the network
    devices = [
        {
            'name': 'DUCO-123456',
            'address': '192.168.13.248',
            'port': 80,
            'api_version': 2.2
        }
    ]

    # Print the discovered devices
    for device in devices:
        print(f"Name: {device['name']}, Address: {device['address']}, Port: {device['port']}, API Version: {device['api_version']}")
        duco_device = DucoDevice(address=device['address'], port=device['port'], api_version=device['api_version'])
        if device['api_version'] == '1.0':
            boardinfo = await duco_device.get_cap_board_info()
            print(f"Communication and Print Board Serial Number: {boardinfo['serial']}, Uptime: {boardinfo['uptime']}, Software Version: {boardinfo['swversion']}")
        nodelist = await duco_device.get_node_list()
        print(f"Node List: {nodelist}")
        for node in nodelist:
            nodeinfo = await duco_device.get_node_info(node)
            print(f"Node {nodeinfo['node']} is a {nodeinfo['devtype']}")
            
            # Get valid node keys
            valid_node_keys = await duco_device.get_valid_node_sensors(node)
            print(f"Valid Node Keys: {valid_node_keys}")
            
            for valid_node_key in valid_node_keys:
                node_value = await duco_device.get_node_key_value(node, valid_node_key)
                print(f"---> {valid_node_key} value of {node_value}")

        # Get wired nodes
        wired_nodes = await duco_device.get_wired_nodes()
        print(f"Wired Nodes: {wired_nodes}")
        
        # Get wireless nodes
        wireless_nodes = await duco_device.get_wireless_nodes()
        print(f"Wireless Nodes: {wireless_nodes}")

        # Get virtual nodes
        virtual_nodes = await duco_device.get_virtual_nodes()
        print(f"Virtual Nodes: {virtual_nodes}")

# Run the main function
asyncio.run(main())
