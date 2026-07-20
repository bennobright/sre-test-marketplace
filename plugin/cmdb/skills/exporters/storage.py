def export_storage(storage_client, wb):
    ws = wb.create_sheet("StorageAccounts")
    ws.append(["Resource Group", "Name", "Location", "SKU", "Kind", "AccessTier"])
    for sa in storage_client.storage_accounts.list():
        ws.append([
            sa.id.split("/")[4],
            sa.name,
            sa.location,
            sa.sku.name if sa.sku else "",
            sa.kind,
            getattr(sa, "access_tier", "")
        ])
