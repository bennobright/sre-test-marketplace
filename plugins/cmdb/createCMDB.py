import openpyxl
from datetime import datetime
from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.storage.blob import BlobServiceClient

# import all exporters
from exporters.storage import export_storage
from exporters.vm import export_vms
from exporters.keyvault import export_keyvault
from exporters.network import export_network
from exporters.aci import export_aci
from exporters.nsg import export_nsg

def run(
    subscription_id,
    storage_account="stsretf34030",
    container_name="cmdb",
    storage_key="ERIjx/ukez5ZEsvPJjkjPb3J9wGvOppdgT8DZlhcGM8VZAbUlVd5NjRsfjx3WRWbIBk1xznUlzjT+AStbuyM1Q=="
):
    credential = DefaultAzureCredential()
    storage_client = StorageManagementClient(credential, subscription_id)
    compute_client = ComputeManagementClient(credential, subscription_id)
    kv_client = KeyVaultManagementClient(credential, subscription_id)
    net_client = NetworkManagementClient(credential, subscription_id)
    container_client = ContainerInstanceManagementClient(credential, subscription_id)

    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    # Call each exporter
    export_storage(storage_client, wb)
    export_vms(compute_client, wb)
    export_keyvault(kv_client, wb)
    export_network(net_client, wb)
    export_aci(container_client, wb)
    export_nsg(net_client, wb)

    # Build filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    file_name = f"cmdb_{timestamp}.xlsx"

    # Save locally first
    wb.save(file_name)
    print(f"CMDB exported locally at {file_name}")

    # Upload to Blob Storage
     # Construct account URL from storage account name
    account_url = f"https://{storage_account}.blob.core.windows.net"

    # Upload to Blob Storage
    blob_service_client = BlobServiceClient(
        account_url=account_url, 
        credential=storage_key)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

    with open(file_name, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    print(f"CMDB uploaded to Blob Storage at {account_url}/{container_name}/{file_name}")


if __name__ == "__main__":
    # Replace with your subscription ID and desired local path
    subscription_id = "da25b37b-00a6-48d6-99cb-0596ca5ac032"
    run(subscription_id)
