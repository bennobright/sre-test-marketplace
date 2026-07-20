---
name: cmdb-generator
description: >
  Generate a CMDB (Configuration Management Database) report as an Excel workbook
  by inventorying Azure resources across a subscription. Exports Storage Accounts,
  Virtual Machines, Key Vaults, Virtual Networks, Container Instances, and NSGs.
  Optionally uploads the report to Azure Blob Storage.
---

# CMDB Generator Skill

Generate a comprehensive CMDB inventory of Azure resources in a subscription and
export it as an Excel (.xlsx) workbook.

## When to use

Load this skill when the user asks to:
- Generate a CMDB report or inventory of Azure resources
- Export Azure resource details (VMs, storage accounts, key vaults, networks, NSGs, container instances) to Excel
- Create an infrastructure inventory spreadsheet
- Upload a CMDB report to Azure Blob Storage

## What it covers

The CMDB generator inventories the following Azure resource types:

| Sheet               | Resource Type              | Key Fields                                                        |
|---------------------|----------------------------|-------------------------------------------------------------------|
| StorageAccounts     | Storage Accounts           | Name, Location, SKU, Kind, Access Tier                            |
| VirtualMachines     | Virtual Machines           | Name, VM Size, OS Type, Power State, NICs, Disks                  |
| KeyVaults           | Key Vaults                 | Name, SKU, Soft Delete, Public Network Access, Deployment Flags   |
| Networks            | Virtual Networks & Subnets | VNet Name, Address Space, Subnet CIDR, Available IPs, NSG, UDR   |
| ContainerInstances  | Container Instances        | Name, Image, CPU, Memory, OS Type, IP, FQDN                      |
| NSGs                | Network Security Groups    | NSG Name, Rule Name, Priority, Direction, Access, Protocol, Ports |

## Parameters

- **subscription_id** (required): The Azure subscription ID to inventory.
- **storage_account** (optional): Name of the Azure Storage account for uploading the report.
- **container_name** (optional): Blob container name (default: `cmdb`).
- **storage_key** (optional): Storage account access key for upload. If omitted, the report is saved locally only.

## Output

- An Excel file named `cmdb_YYYYMMDDHHMM.xlsx` saved locally.
- Optionally uploaded to the specified Azure Blob Storage container.

## Prerequisites

- The agent's managed identity must have **Reader** role on the target subscription.
- For blob upload: the storage account key or a managed identity with **Storage Blob Data Contributor** role.
