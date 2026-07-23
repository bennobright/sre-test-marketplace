---
name: diagram_generator
description: "Generate Azure VNet/Subnet/NIC dependency JSON and produce diagrams. Triggered when the user asks to visualize network dependencies."
---

# Azure Diagram Generator Skill

This skill generates a dependency map of Virtual Networks, Subnets, NICs, and attached VMs in a subscription. The `vnetDependencies.py` script collects the data and saves it as `diagram/vnet_subnet_nic.json`. The `vnetDiagram.py` script then renders PNG diagrams from that JSON using the `diagrams` library.

## Execution Steps

1. **Install dependencies**:  
   Run:
   ```bash
   pip install --break-system-packages -q -r requirements.txt
   ```

2. **Determine subscription**:
   * Check the agent's azure_resource_access settings for accessible subscriptions.
   * If only one subscription is available, use it automatically.
   * If multiple subscriptions are available, list them and ask the user to select one before proceeding.

3. **Run the export script using vnetDependencies.py**:
   * IMPORTANT: Do NOT use DefaultAzureCredential. Use the agent's user-assigned managed identity.
   * Look up the user-assigned identity client ID from the agent's agent_identity settings.
   * Execute the script using the resolved subscription ID and client ID:
     ```bash
     python3 vnetDependencies.py --subscription-id <subscription_id> --client-id <user_assigned_client_id>
     ```

4. **Render the diagrams using vnetDiagram.py**:
   * Confirm that `diagram/vnet_subnet_nic.json` was generated successfully in the previous step.
   * Run the rendering script from the same working directory:
     ```bash
     python3 vnetDiagram.py
     ```
   * This produces one PNG file per VNet inside the `diagram/` folder (e.g. `diagram/<vnetName>_Diagram.png`).

5. **Save and share**:
   * Persist all generated files using SaveFileToBlob.
   * Present the output as **download links only** (do NOT embed images inline). This keeps the response compact and avoids excessive scrolling.
   * Format the output as a list with the JSON file first, followed by each diagram PNG with its VNet name:
 
     ```
     **Generated Files:**
 
     1. [Download VNet Dependency JSON](link-to-json)
 
     **Diagrams:**
     2. [vnet-name-1 Diagram](link-to-png)
     3. [vnet-name-2 Diagram](link-to-png)
     4. [vnet-name-3 Diagram](link-to-png)
     ...
     ```
 
   * Do NOT use `![image](...)` markdown syntax. Use `[text](link)` download links only.