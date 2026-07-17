def export_aci(container_client, wb):
    ws = wb.create_sheet("ContainerInstances")
    ws.append([
        "Resource Group", "Name", "Location",
        "Image", "CPU Cores", "Memory (GB)",
        "OS Type", "Restart Policy", "IP Address", "FQDN"
    ])

    for ci in container_client.container_groups.list():
        rg = ci.id.split("/")[4]
        ip = ci.ip_address.ip if ci.ip_address else ""
        fqdn = ci.ip_address.fqdn if ci.ip_address else ""

        ws.append([
            rg,
            ci.name,
            ci.location,
            ci.containers[0].image if ci.containers else "",
            ci.containers[0].resources.requests.cpu if ci.containers else "",
            ci.containers[0].resources.requests.memory_in_gb if ci.containers else "",
            ci.os_type,
            ci.restart_policy,
            ip,
            fqdn
        ])
