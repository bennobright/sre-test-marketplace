import argparse
import json
import os
from azure.identity import ManagedIdentityCredential, DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient

def create_diagram(subscription_id: str, client_id: str = None):
    # Use Managed Identity for the SRE Agent, fallback to Default for local testing
    if client_id:
        credential = ManagedIdentityCredential(client_id=client_id)
    else:
        credential = DefaultAzureCredential()

    client = NetworkManagementClient(credential, subscription_id)
    vnets = client.virtual_networks.list_all()
    data = []

    for vnet in vnets:
        rg_name = vnet.id.split("/")[4]   # extract resource group
        subnets = client.subnets.list(rg_name, vnet.name)

        # Pre-fetch NICs for this resource group to avoid redundant API calls per subnet
        all_nics = list(client.network_interfaces.list(rg_name))

        subnet_data = []
        for s in subnets:
            # Collect NICs attached to this subnet
            nic_list = []
            for nic in all_nics:
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

    print(f"Saved {json_path}")
    return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Azure VNet/Subnet/NIC dependency JSON.")
    parser.add_argument("--subscription-id", required=True, help="Azure Subscription ID to scan")
    parser.add_argument("--client-id", required=False, help="User-assigned Managed Identity Client ID")
    
    args = parser.parse_args()

    result = create_diagram(args.subscription_id, args.client_id)
    