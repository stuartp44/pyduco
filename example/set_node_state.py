from duco import DucoDevice

duco = DucoDevice(address='192.168.10.216')

# Set the state of a node
node_id = 1
state = 'MAN2'
response = duco.set_node_operational_state(node_id, state)
if response.get('action_state') == "SUCCESS":
    print(f"Successfully set the operational state to {state} on node {node_id}")
else:
    print(f"Failed to set the operational state to {state} on node {node_id}")
