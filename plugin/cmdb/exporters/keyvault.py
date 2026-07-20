def export_keyvault(kv_client, wb):
    ws = wb.create_sheet("KeyVaults")
    ws.append([
        "Resource Group", "Name", "Location",
        "SKU", "TenantId", "SoftDeleteEnabled",
        "PublicNetworkAccess", "EnabledForDeployment",
        "EnabledForDiskEncryption", "EnabledForTemplateDeployment"
    ])

    for vault in kv_client.vaults.list():
        rg = vault.id.split("/")[4]

        # Fetch full vault details
        full_vault = kv_client.vaults.get(rg, vault.name)
        props = full_vault.properties

        ws.append([
            rg,
            vault.name,
            vault.location,
            props.sku.name if props.sku else "",
            props.tenant_id,
            getattr(props, "enable_soft_delete", ""),
            getattr(props, "public_network_access", ""),
            getattr(props, "enabled_for_deployment", ""),
            getattr(props, "enabled_for_disk_encryption", ""),
            getattr(props, "enabled_for_template_deployment", "")
        ])
