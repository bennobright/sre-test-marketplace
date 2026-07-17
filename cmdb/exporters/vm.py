def export_vms(compute_client, wb):
    ws = wb.create_sheet("VirtualMachines")
    ws.append([
        "Resource Group", "Name", "Location",
        "VM Size", "OS Type", "PowerState",
        "ProvisioningState", "ComputerName",
        "NICs", "Disks"
    ])

    for vm in compute_client.virtual_machines.list_all():
        rg = vm.id.split("/")[4]

        # Get instance view for runtime status
        instance_view = compute_client.virtual_machines.instance_view(rg, vm.name)

        # Extract PowerState
        power_state = ""
        if instance_view and instance_view.statuses:
            for status in instance_view.statuses:
                if status.code.startswith("PowerState/"):
                    power_state = status.display_status

        # Collect NICs
        nic_list = [nic.id.split("/")[-1] for nic in vm.network_profile.network_interfaces] if vm.network_profile else []

        # Collect Disks
        disk_list = []
        if vm.storage_profile and vm.storage_profile.data_disks:
            disk_list = [disk.name for disk in vm.storage_profile.data_disks]

        ws.append([
            rg,
            vm.name,
            vm.location,
            vm.hardware_profile.vm_size,
            vm.storage_profile.os_disk.os_type if vm.storage_profile and vm.storage_profile.os_disk else "",
            power_state,
            vm.provisioning_state,
            vm.os_profile.computer_name if vm.os_profile else "",
            ", ".join(nic_list),
            ", ".join(disk_list)
        ])
