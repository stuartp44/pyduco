import aiohttp

class DucoDevice:
    def __init__(self, address, port=80, protocol="http", api_version=1.0):
        self.address = address
        self.port = port
        self.protocol = protocol
        self.api_version = api_version

    async def fetch_json(self, query_string):
        """
        Fetch JSON data from a URL.

        :param query_string: The query string to append to the base URL.
        :return: Parsed JSON data, or None if the request fails.
        """
        base_url = f"{self.protocol}://{self.address}:{self.port}/"
        url = base_url + query_string
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=5) as response:
                    response.raise_for_status()
                    text = await response.text()

                    if "SUCCESS" in text or "FAILED" in text:
                        returned_data = text.strip()
                        return {"action_state": returned_data}
                    elif response.headers.get('content-type') == "application/json; charset=UTF-8":
                        return await response.json()
                    else:
                        print(f"Unexpected content type: {response.headers.get('content-type')}")
                        return None

            except aiohttp.ClientError as e:
                print(f"Error fetching data from {url}: {e}")
                return None

    async def get_cap_board_info(self):
        """
        Fetch the board information from the Duco device.

        :return: A dictionary containing the board information, or None if the request fails.
        """
        query_string = "board_info"
        data = await self.fetch_json(query_string)
        return data
    
    async def get_node_list(self):
        """
        Fetch the node list from the Duco device.

        :return: A list of node IDs, or None if the request fails.
        """
        if self.api_version == 1.0:
            query_string = "nodelist"
        else:
            query_string = "nodes"
        data = await self.fetch_json(query_string)
        if isinstance(data, list):
            if all(isinstance(item, dict) and 'Node' in item for item in data):
                data = [item['Node'] for item in data]
            return data
        elif isinstance(data, dict):
            return data.get('nodelist', [])
        else:
            print("Unexpected data format")
            return []

    async def get_node_info(self, node_id):
        """
        Fetch the node information from the Duco device.

        :return: A dictionary containing the node information, or None if the request fails.
        """
        if self.api_version == 1.0:
            query_string = f"nodeinfoget?node={node_id}"
        else:
            query_string = f"info/nodes/{node_id}"
        data = await self.fetch_json(query_string)
        if self.api_version == 1.0:
            return data
        elif self.api_version == 2.2:
            if isinstance(data, dict):
                node_info = {
                    "node": data.get("Node"),
                    "devtype": data.get("General", {}).get("Type", {}).get("Val"),
                    "subtype": data.get("General", {}).get("SubType", {}).get("Val"),
                    "netw": data.get("General", {}).get("NetworkType", {}).get("Val"),
                    "prnt": data.get("General", {}).get("Parent", {}).get("Val"),
                    "asso": data.get("General", {}).get("Asso", {}).get("Val"),
                    "location": data.get("General", {}).get("Name", {}).get("Val"),
                    "identify": data.get("General", {}).get("Identify", {}).get("Val"),
                    "ventilation_state": data.get("Ventilation", {}).get("State", {}).get("Val"),
                    "ventilation_time_state_remain": data.get("Ventilation", {}).get("TimeStateRemain", {}).get("Val"),
                    "ventilation_time_state_end": data.get("Ventilation", {}).get("TimeStateEnd", {}).get("Val"),
                    "ventilation_mode": data.get("Ventilation", {}).get("Mode", {}).get("Val"),
                    "ventilation_flow_lvl_tgt": data.get("Ventilation", {}).get("FlowLvlTgt", {}).get("Val"),
                }
                # Check if sensor information is available
                sensor_data = data.get("Sensor", {})
                for sensor_key, sensor_value in sensor_data.items():
                    if isinstance(sensor_value, dict) and "Val" in sensor_value:
                        node_info[sensor_key.lower()] = sensor_value["Val"]
                return node_info
            else:
                print("Unexpected data format")
            return None
        else:
            print(f"Unsupported API version: {self.api_version}")
            return None
    
    async def get_node_attribute_value(self, node, attribute):
        """
        Fetch the attribute values from the Duco device.

        :return: The attribute value, or None if the request fails.
        """
        node_info = await self.get_node_info(node)
        return node_info.get(attribute, None) if node_info else None
    
    async def get_node_types(self, node_type):
        """
        Fetch the nodes of a specific type from the Duco device.

        :return: A list of node IDs, or None if the request fails.
        """
        node_list = await self.get_node_list()
        node_type_match = []
        for node in node_list:
            if await self.get_node_attribute_value(node, 'netw') == node_type:
                node_type_match.append(node)
        if node_type_match:
            return node_type_match
        else:
            print(f"No {node_type} nodes found")
            return None
    
    async def get_wireless_nodes(self):
        """
        Fetch the wireless node list from the Duco device.

        :return: A list of wireless node IDs, or None if the request fails.
        """
        return await self.get_node_types("RF")
    
    async def get_wired_nodes(self):
        """
        Fetch the wired node list from the Duco device.

        :return: A list of wired node IDs, or None if the request fails.
        """
        return await self.get_node_types("WI")
    
    async def get_virtual_nodes(self):
        """
        Fetch the virtual node list from the Duco device.

        :return: A list of virtual node IDs, or None if the request fails.
        """
        return await self.get_node_types("VIRT")
    
    async def get_valid_node_sensors(self, node):
        """
        Fetch the valid node sensors from the Duco device.

        :return: A list of valid sensor IDs, or None if the request fails.
        """
        node_info = await self.get_node_info(node)
        valid_sensors = []
        if node_info:
            for key, value in node_info.items():
                if key not in ("node", "devtype", "subtype", "netw", "addr", "sub", "prnt", "asso", "location", "error", "show", "link", "serialnb", "swversion", "cntdwn", "endtime") and value not in ("-", 0):
                    valid_sensors.append(key)
        if valid_sensors:
            return valid_sensors
        else:
            print("No valid sensors found")
            return None

    async def get_node_key_value(self, node, key):
        """
        Fetch the key value from the Duco device.

        :return: The key value, or None if the request fails.
        """
        value = await self.get_node_attribute_value(node, key)
        if value:
            return value
        else:
            print(f"No value found for {key}")
            return None
        
    async def set_node_parameters(self, node, key, value):
        """
        Set the key value for a node on the Duco device.

        :return: The response from the device, or None if the request fails.
        """
        query_string = f"nodeinfoset?node={node}&para={key}&value={value}"
        data = await self.fetch_json(query_string)
        return data

    async def set_node_operational_state(self, node, state):
        """
        Set the operational state of the node.

        :return: The response from the device, or None if the request fails.
        """
        query_string = f"nodesetoperstate?node={node}&value={state}"
        set_status = await self.fetch_json(query_string)
        if set_status.get('action_state') == "SUCCESS":
            return set_status
        else:
            return set_status

    async def set_node_location(self, node, location):
        """
        Set the location of the node.

        :return: The response from the device, or None if the request fails.
        """
        return await self.set_node_parameters(node, "location", location)