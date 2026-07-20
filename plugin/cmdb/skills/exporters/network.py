def export_network(net_client, wb):
    ws = wb.create_sheet("Networks")
    ws.append([
        "Resource Group", "VNet Name", "Location",
        "AddressSpace", "Subnet Name", "Subnet CIDR",
        "AvailableIPs", "NSG Name", "UDR Name"
    ])

    for vnet in net_client.virtual_networks.list_all():
        rg = vnet.id.split("/")[4]
        addr_space = ", ".join(vnet.address_space.address_prefixes)

        # Iterate subnets
        for subnet in vnet.subnets:
            # CIDR
            cidr = subnet.address_prefix
            # Available IPs (rough estimate: total - reserved)
            available_ips = ""
            if cidr:
                import ipaddress
                net = ipaddress.ip_network(cidr)
                available_ips = net.num_addresses - 5  # Azure reserves 5

            # NSG
            nsg_name = subnet.network_security_group.id.split("/")[-1] if subnet.network_security_group else ""

            # UDR
            udr_name = subnet.route_table.id.split("/")[-1] if subnet.route_table else ""

            ws.append([
                rg,
                vnet.name,
                vnet.location,
                addr_space,
                subnet.name,
                cidr,
                available_ips,
                nsg_name,
                udr_name
            ])
