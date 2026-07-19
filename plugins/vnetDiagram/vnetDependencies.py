from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
import json, os

sub_id = os.getenv("AZURE_SUBSCRIPTION_ID", "da25b37b-00a6-48d6-99cb-0596ca5ac032")
client = NetworkManagementClient(DefaultAzureCredential(), sub_id)

vnets = client.virtual_networks.list_all()
data = []

for vnet in vnets:
    rg_name = vnet.id.split("/")[4]   # extract resource group
    subnets = client.subnets.list(rg_name, vnet.name)

    subnet_data = []
    for s in subnets:
        # Collect NICs attached to this subnet
        nic_list = []
        for nic in client.network_interfaces.list(rg_name):
            for ipconf in nic.ip_configurations:
                if ipconf.subnet and ipconf.subnet.id.endswith(s.name):
                    nic_list.append({
                        "nicName": nic.name,
                        "privateIP": ipconf.private_ip_address,
                        "vmId": nic.virtual_machine.id if nic.virtual_machine else None
                    })

        subnet_data.append({
            "name": s.name,
            "addressPrefix": s.address_prefix,
            "nics": nic_list
        })

    data.append({
        "vnetName": vnet.name,
        "location": vnet.location,
        "subnets": subnet_data
    })

# Ensure diagram folder exists
os.makedirs("diagram", exist_ok=True)

# Save JSON
json_path = os.path.join("diagram", "vnet_subnet_nic.json")
with open(json_path, "w") as f:
    json.dump(data, f, indent=2)

print("Saved vnet_subnet_nic.json")
