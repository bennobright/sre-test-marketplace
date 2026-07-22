---
name: cmdb_export
description: "Export Azure subscription resources (Storage, VMs, KeyVaults, Networks, ACI, NSGs) into a CMDB Excel workbook. Triggered when the user asks to generate a CMDB."
---

# Azure CMDB Export Skill

This skill generates a CMDB (Configuration Management Database) Excel workbook containing an inventory of Azure resources in the subscription.

## What it exports

| Sheet              | Resource Type                        |
|--------------------|--------------------------------------|
| StorageAccounts    | Azure Storage Accounts               |
| VirtualMachines    | Azure Virtual Machines (with status)  |
| KeyVaults          | Azure Key Vaults                     |
| Networks           | VNets and Subnets                    |
| ContainerInstances | Azure Container Instances            |
| NSGs               | Network Security Groups and Rules    |

## Execution Steps

1. **Install dependencies**: Run `pip install --break-system-packages -q -r requirements.txt` from the skill directory.

2. **Run the export script** using `createCMDB.py`. 
   - **IMPORTANT**: Do NOT use `DefaultAzureCredential`. Use the **user-assigned managed identity** with `ManagedIdentityCredential(client_id="5ce90174-9004-421f-9c82-752c5db35847")` — the system-assigned identity lacks Reader role on the subscription.
   - Subscription ID: `da25b37b-00a6-48d6-99cb-0596ca5ac032`
   - Call the `run()` function or replicate its logic using `ManagedIdentityCredential` instead of `DefaultAzureCredential`.

3. **Save and share**: Save the generated `.xlsx` file and provide a download link to the user.

## Parameters

- `subscription_id`: `da25b37b-00a6-48d6-99cb-0596ca5ac032`
- `storage_account`: `srereportsstore` (for optional blob upload)
- `container_name`: `cmdb` (for optional blob upload)
