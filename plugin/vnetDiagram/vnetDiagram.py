from diagrams import Diagram, Cluster
from diagrams.azure.network import VirtualNetworks, Subnets, NetworkInterfaces
from diagrams.azure.compute import VirtualMachine
import json, os

# Ensure diagram folder exists
os.makedirs("diagram", exist_ok=True)

json_path = os.path.join("diagram", "vnet_subnet_nic.json")
with open(json_path) as f:
    data = json.load(f)

for vnet in data:
    # Build filename inside diagram folder
    filename = os.path.join("diagram", f"{vnet['vnetName']}_Diagram")

    with Diagram(
        f"{vnet['vnetName']}_Diagram",
        show=False,
        direction="TB",   # top-to-bottom layout
        filename=filename   # <-- saves PNG into diagram folder
    ):
        with Cluster(f"{vnet['vnetName']} ({vnet['location']})"):
            vnet_node = VirtualNetworks(f"{vnet['vnetName']}")

            for subnet in vnet["subnets"]:
                with Cluster(f"{subnet['name']} ({subnet['addressPrefix']})"):
                    subnet_node = Subnets(subnet["name"])
                    vnet_node >> subnet_node

                    for nic in subnet.get("nics", []):
                        nic_node = NetworkInterfaces(f"{nic['nicName']} \n ({nic['privateIP']})")
                        subnet_node >> nic_node

                        if "vmId" in nic and nic["vmId"]:
                            vm_name = nic["vmId"].split("/")[-1]
                            vm_node = VirtualMachine(vm_name)
                            nic_node >> vm_node
