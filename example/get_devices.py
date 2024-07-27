from duco import discover_duco_devices, DucoDevice

# Discover Duco devices on the network
devices = discover_duco_devices(timeout=5)

# Print the discovered devices
for device in devices:
    print(f"Name: {device['name']}, Address: {device['address']}, Port: {device['port']}")
    duco_device = DucoDevice(address=device['address'], port=device['port'])
    boardinfo = duco_device.get_cap_board_info()
    print(f"Communication and Print Board Serial Number: {boardinfo['serial']}, Uptime: {boardinfo['uptime']}, Software Version: {boardinfo['swversion']}")
    nodelist = duco_device.get_node_list()
    print(f"Node List: {nodelist}")
    for node in nodelist:
        nodeinfo = duco_device.get_node_info(node)
        print(f"Node {nodeinfo['node']} is a {nodeinfo['devtype']} with a serial number of {nodeinfo['serialnb']} and a firmware version of {nodeinfo['swversion']}")
        
        # Get valid node keys
        valid_node_keys = duco_device.get_valid_node_sensors(node)
        print(f"Valid Node Keys: {valid_node_keys}")
        
        for valid_node_key in valid_node_keys:
            node_value = duco_device.get_node_key_value(node, valid_node_key)
            print(f"---> {valid_node_key} value of {node_value}")

    # Get wired nodes
    wired_nodes = duco_device.get_wired_nodes()
    print(f"Wired Nodes: {wired_nodes}")
    
    # Get wireless nodes
    wireless_nodes = duco_device.get_wireless_nodes()
    print(f"Wireless Nodes: {wireless_nodes}")

    # Get virtual nodes
    virtual_nodes = duco_device.get_virtual_nodes()
    print(f"Virtual Nodes: {virtual_nodes}")
