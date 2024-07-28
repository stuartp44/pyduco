import requests

class DucoDevice:
    def __init__(self, address, port=80, protocol="http"):
        self.address = address
        self.port = port
        self.protocol = protocol

    def fetch_json(self, query_string):
        """
        Fetch JSON data from a URL.

        :param url: The URL to fetch data from.
        :return: Parsed JSON data, or None if the request fails.
        """
        try:
            base_url = f"{self.protocol}://{self.address}:{self.port}/"
            url = base_url + query_string
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # Raise an error for bad status codes
            
            # if the response is json, return that else check if it is a simple response like "SUCCESS" or "FAILED" in the body. In all cases the content header is wrong
            if "SUCCESS" in response.text or "FAILED" in response.text:
                returned_data = response.text.strip()
                return { "action_state": returned_data }
            # if the body contains json, return that ignoring the headers
            elif response.headers['content-type'] == "application/json":
                return response.json()
            else:
                print(f"Unexpected content type: {response.headers['content-type']}")
                return None
            
        except requests.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            return None

    def get_cap_board_info(self):
        """
        Fetch the board information from the Duco device.

        :return: A dictionary containing the board information, or None if the request fails.
        """
        query_string = "board_info"
        data = self.fetch_json(query_string)
        return data
    
    def get_node_list(self):
        """
        Fetch the node list from the Duco device.

        :return: A list of node IDs, or None if the request fails.
        """
        query_string = "nodelist"
        data = self.fetch_json(query_string)
        return data.get('nodelist', []) if data else []
    
    def get_node_info(self, node_id):
        """
        Fetch the node information from the Duco device.
        
        :return: A dictionary containing the node information, or None if the request fails.
        """
        query_string = f"nodeinfoget?node={node_id}"
        data = self.fetch_json(query_string)
        return data if data else None
    
    def get_node_attribute_value(self, node, attribute):
        """
        Fetch the attribute values from the Duco device.
        
        :return: A dictionary containing the attribute values, or None if the request fails.
        """
        node_info = self.get_node_info(node)
        return node_info.get(attribute, None) if node_info else None
    
    def get_node_types(self, node_type):
        """
        Fetch the wireless node list from the Duco device.
        
        :return: A list of wireless node IDs, or None if the request fails.	
        """
        get_node_list = self.get_node_list()
        node_type_match = []
        for node in get_node_list:
            if self.get_node_attribute_value(node, 'netw') == node_type:
                node_type_match.append(node)
        if node_type_match:
            return node_type_match
        else:
            print(f"No {node_type} nodes found")
            return None
    
    def get_wireless_nodes(self):
        """
        Fetch the wireless node list from the Duco device.
        
        :return: A list of wireless node IDs, or None if the request fails.
        """
        return self.get_node_types("RF")
    
    def get_wired_nodes(self):
        """
        Fetch the wired node list from the Duco device.
        
        :return: A list of wired node IDs, or None if the request fails.
        """
        return self.get_node_types("WI")
    
    def get_virtual_nodes(self):
        """
        Fetch the virtual node list from the Duco device.
        
        :return: A list of virtual node IDs, or None if the request fails.
        """
        return self.get_node_types("VIRT")
    
    def get_valid_node_sensors(self, node):
        """
        Fetch the valid node sensors from the Duco device.
        
        :return: A list of valid sensor IDs, or None if the request fails.
        """
        node_info = self.get_node_info(node)
        valid_sensors = []
        # get json and check if it is not "-" or "0" and add key name to valid_sensors
        for key, value in node_info.items():
            if key not in ("node", "devtype", "subtype", "netw", "addr", "sub", "prnt", "asso", "location", "error", "show", "link", "serialnb", "swversion", "show", "link", "cntdwn", "endtime") and value not in ("-", 0):
                valid_sensors.append(key)
        if valid_sensors:
            return valid_sensors
        else:
            print("No valid sensors found")
            return None

    def get_node_key_value(self, node, key):
        """
        Fetch the key value from the Duco device.
        
        :return: A dictionary containing the key value, or None if the request fails.
        """
        value = self.get_node_attribute_value(node, key)
        if value:
            return value
        else:
            print(f"No value found for {key}")
            return None
        
    def set_node_parameters(self, node, key, value):
        """
        Set the key value from the Duco device.
        
        :return: A dictionary containing the key value, or None if the request fails.
        """
        query_string = f"nodeinfoset?node={node}&para={key}&value={value}"
        data = self.fetch_json(query_string)
        return data

    def set_node_operational_state(self, node, state):
        """
        Set the operational state of the node.
        
        :return: A dictionary containing the operational state, or None if the request fails.
        """
        query_string = f"nodesetoperstate?node={node}&value={state}"
        set_status = self.fetch_json(query_string)
        if set_status.get('action_state') == "SUCCESS":
            return set_status
        else:
            return set_status

    def set_node_location(self, node, location):
        """
        Set the location of the node.
        
        :return: A dictionary containing the location, or None if the request fails.
        """
        return self.set_node_parameters(node, "location", location)
