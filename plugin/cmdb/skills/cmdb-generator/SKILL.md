---
name: cmdb_export
description: 
---

skills:
  - name: AzureCMDBExport
    description: "Export Azure subscription resources into CMDB Excel and commit to repo"
    triggers:
      - intent: "generate cmdb"
        action: createCMDB.py:run
    parameters:
      subscription_id: "da25b37b-00a6-48d6-99cb-0596ca5ac032"
      storage_account: "srereportsstore"
      container_name: "cmdb"