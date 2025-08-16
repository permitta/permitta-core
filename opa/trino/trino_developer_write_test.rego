package permitta.trino

import rego.v1


# ---------------------------- SELECT  -----------------------------
test_alice_select_from_table_iceberg_workspace_with_prefix if {
  allow with input as {
    "action": {
      "operation": "SelectFromColumns",
      "resource": {
        "table": {
          "catalogName": "iceberg",
          "columns": [
            "a"
          ],
          "schemaName": "workspace",
          "tableName": "u_table_a"
        }
      }
    },
    "context": {
      "identity": {
        "user": "alice"
      }
    }
  }
}

test_alice_select_from_table_iceberg_workspace_without_prefix if {
  not allow with input as {
    "action": {
      "operation": "SelectFromColumns",
      "resource": {
        "table": {
          "catalogName": "iceberg",
          "columns": [
            "a"
          ],
          "schemaName": "workspace",
          "tableName": "table_a"
        }
      }
    },
    "context": {
      "identity": {
        "user": "alice"
      }
    }
  }
}

# ---------------------------- INSERT  -----------------------------

test_alice_insert_into_table_iceberg_workspace_with_prefix if {
  allow with input as {
    "action": {
      "operation": "InsertIntoTable",
      "resource": {
        "table": {
          "catalogName": "iceberg",
          "schemaName": "workspace",
          "tableName": "u_table_a"
        }
      }
    },
    "context": {
      "identity": {
        "user": "alice"
      }
    }
  }
}

test_alice_insert_into_table_iceberg_workspace_without_prefix if {
  not allow with input as {
    "action": {
      "operation": "InsertIntoTable",
      "resource": {
        "table": {
          "catalogName": "iceberg",
          "schemaName": "workspace",
          "tableName": "table_a"
        }
      }
    },
    "context": {
      "identity": {
        "user": "alice"
      }
    }
  }
}

# ---------------------------- UPDATE  -----------------------------

test_alice_update_table_iceberg_workspace_with_prefix if {
  allow with input as {
    "action": {
      "operation": "UpdateTableColumns",
      "resource": {
        "table": {
          "catalogName": "iceberg",
          "columns": [
            "a"
          ],
          "schemaName": "workspace",
          "tableName": "u_table_a"
        }
      }
    },
    "context": {
      "identity": {
        "user": "alice"
      }
    }
  }
}

test_alice_update_table_iceberg_workspace_without_prefix if {
  not allow with input as {
    "action": {
      "operation": "UpdateTableColumns",
      "resource": {
        "table": {
          "catalogName": "iceberg",
          "columns": [
            "a"
          ],
          "schemaName": "workspace",
          "tableName": "table_a"
        }
      }
    },
    "context": {
      "identity": {
        "user": "alice"
      }
    }
  }
}

# ---------------------------- DELETE  -----------------------------

test_alice_delete_from_table_iceberg_workspace_with_prefix if {
  allow with input as {
    "action": {
      "operation": "DeleteFromTable",
      "resource": {
        "table": {
          "catalogName": "iceberg",
          "schemaName": "workspace",
          "tableName": "u_table_a"
        }
      }
    },
    "context": {
      "identity": {
        "user": "alice"
      }
    }
  }
}

test_alice_delete_from_table_iceberg_workspace_without_prefix if {
  not allow with input as {
    "action": {
      "operation": "DeleteFromTable",
      "resource": {
        "table": {
          "catalogName": "iceberg",
          "schemaName": "workspace",
          "tableName": "table_a"
        }
      }
    },
    "context": {
      "identity": {
        "user": "alice"
      }
    }
  }
}