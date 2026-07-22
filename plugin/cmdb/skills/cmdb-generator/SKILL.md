---
name: cmdb_export
description: "Export Azure subscription resources into a CMDB Excel workbook. Triggered when the user asks to generate a CMDB."
---

# Azure CMDB Export Skill

This skill generates a CMDB (Configuration Management Database) Excel workbook containing an inventory of Azure resources in a subscription. The `createCMDB.py` script handles all resource type exports automatically.

## Execution Steps

1. **Install dependencies**: Run `pip install --break-system-packages -q -r requirements.txt` from the skill directory.

2. **Determine subscription**:
   - Check the agent's `azure_resource_access` settings for accessible subscriptions.
   - If only **one subscription** is available, use it automatically.
   - If **multiple subscriptions** are available, list them and ask the user to select one before proceeding.

3. **Run the export script** using `createCMDB.py`.
   - **IMPORTANT**: Do NOT use `DefaultAzureCredential`. Use the agent's **user-assigned managed identity** with `ManagedIdentityCredential`. Look up the user-assigned identity client ID from the agent's `agent_identity` settings and pass it to `ManagedIdentityCredential(client_id=<user_assigned_client_id>)`.
   - Pass the resolved subscription ID to the `run()` function or replicate its logic using `ManagedIdentityCredential` instead of `DefaultAzureCredential`.

4. **Save and share**: Save the generated `.xlsx` file and provide a download link to the user.
