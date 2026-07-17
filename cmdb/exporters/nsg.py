def export_nsg(net_client, wb):
    ws = wb.create_sheet("NSGs")
    ws.append([
        "Resource Group", "NSG Name", "Location",
        "Rule Name", "Priority", "Direction",
        "Access", "Protocol", "Source", "Destination", "Port"
    ])

    for nsg in net_client.network_security_groups.list_all():
        rg = nsg.id.split("/")[4]
        for rule in nsg.security_rules:
            ws.append([
                rg,
                nsg.name,
                nsg.location,
                rule.name,
                rule.priority,
                rule.direction,
                rule.access,
                rule.protocol,
                rule.source_address_prefix,
                rule.destination_address_prefix,
                rule.destination_port_range
            ])
