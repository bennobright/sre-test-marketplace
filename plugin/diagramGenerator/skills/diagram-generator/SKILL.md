name: diagram_generator
description: "Generate Azure VNet/Subnet/NIC dependency JSON and produce diagrams. Triggered when the user asks to visualize network dependencies."
---

# Azure Diagram Generator Skill

This skill generates a dependency map of Virtual Networks, Subnets, NICs, and attached VMs in a subscription. The `vnetDependencies.py` script collects the data and saves it as `diagram/vnet_subnet_nic.json`. The JSON can then be passed to the MCP diagram tool to render PNG diagrams.

## Execution Steps

1. **Install dependencies**:  
   Run:
   ```bash
   pip install --break-system-packages -q -r requirements.txt
2. **Determine subscription:**:
   * Check the agent's azure_resource_access settings for accessible subscriptions.
   * If only one subscription is available, use it automatically.
   * If multiple subscriptions are available, list them and ask the user to select one before proceeding.
3. **Run the export script using vnetDependencies.py**:
   * IMPORTANT: Do NOT use DefaultAzureCredential. Use the agent's user-assigned managed identity.
   * Look up the user-assigned identity client ID from the agent's agent_identity settings.
   * Execute the script using the resolved subscription ID and client ID:
      Bash
      python vnetDependencies.py --subscription-id <subscription_id> --client-id <user_assigned_client_id>
4. **Save and share**:
   * Confirm that diagram/vnet_subnet_nic.json was generated successfully.
   * Pass the JSON file to the MCP diagram tool to render the visualization, and provide the final diagram output to the user.