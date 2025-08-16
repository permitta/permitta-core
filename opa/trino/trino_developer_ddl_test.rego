package permitta.trino

import rego.v1
import data.input.input_filter_cols

# ---------------------------- CREATE SCHEMA -----------------------------
test_admin_create_schema if {
  allow with input as {
    "action": {
      "operation": "CreateSchema",
      "resource": {
        "schema": {
          "catalogName": "iceberg",
          "properties": {},
          "schemaName": "test_schema"
        }
      }
    },
    "context": {
      "identity": {
        "user": "admin"
      }
    }
  }
}

test_bob_create_schema if {
  not allow with input as {
    "action": {
      "operation": "CreateSchema",
      "resource": {
        "schema": {
          "catalogName": "iceberg",
          "properties": {},
          "schemaName": "test_schema"
        }
      }
    },
    "context": {
      "identity": {
        "user": "bob"
      }
    }
  }
}

# ---------------------------- DROP SCHEMA -----------------------------
test_admin_drop_schema if {
  allow with input as {
    "action": {
      "operation": "DropSchema",
      "resource": {
        "schema": {
          "catalogName": "iceberg",
          "properties": {},
          "schemaName": "test_schema"
        }
      }
    },
    "context": {
      "identity": {
        "user": "admin"
      }
    }
  }
}

test_bob_drop_schema if {
  not allow with input as {
    "action": {
      "operation": "DropSchema",
      "resource": {
        "schema": {
          "catalogName": "iceberg",
          "properties": {},
          "schemaName": "test_schema"
        }
      }
    },
    "context": {
      "identity": {
        "user": "bob"
      }
    }
  }
}

# ---------------------------- ACCESS CATALOG -----------------------------
test_alice_access_catalog_iceberg if {
  allow with input as {
    "action": {
        "operation": "AccessCatalog",
        "resource": {
          "catalog": {
            "name": "iceberg"
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

# ---------------------------- FILTER SCHEMAS -----------------------------
test_alice_filter_schema_workspace if {
  allow with input as {
    "action": {
      "operation": "FilterSchemas",
      "resource": {
        "schema": {
          "catalogName": "iceberg",
          "schemaName": "workspace"
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

# ---------------------------- CREATE TABLE -----------------------------
test_admin_create_table if {
  allow with input as {
    "action": {
      "operation": "CreateTable",
      "resource": {
        "table": {
          "catalogName": "iceberg",
          "properties": {},
          "schemaName": "workspace",
          "tableName": "table_a"
        }
      }
    },
    "context": {
      "identity": {
        "user": "admin"
      }
    }
  }
}

# alice can create tables in iceberg.workspace with prefix v_
test_alice_create_table_iceberg_workspace_with_prefix_v if {
  allow with input as {
    "action": {
      "operation": "CreateTable",
      "resource": {
        "table": {
          "catalogName": "iceberg",
          "properties": {},
          "schemaName": "workspace",
          "tableName": "v_table_a"
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

# alice cannot create tables in iceberg.workspace without prefix v_
test_alice_create_table_iceberg_workspace_with_prefix_u if {
  allow with input as {
    "action": {
      "operation": "CreateTable",
      "resource": {
        "table": {
          "catalogName": "iceberg",
          "properties": {},
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

# alice cannot create tables in iceberg.workspace without prefix v_
test_alice_create_table_iceberg_workspace_without_prefix if {
  not allow with input as {
    "action": {
      "operation": "CreateTable",
      "resource": {
        "table": {
          "catalogName": "iceberg",
          "properties": {},
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

# alice cannot create tables in iceberg.hr
test_alice_create_table_iceberg_hr if {
  not allow with input as {
    "action": {
      "operation": "CreateTable",
      "resource": {
        "table": {
          "catalogName": "iceberg",
          "properties": {},
          "schemaName": "hr",
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
# ---------------------------- SHOW CREATE TABLE -----------------------------

test_alice_show_create_table_iceberg_workspace_with_prefix if {
  allow with input as {
    "action": {
      "operation": "ShowCreateTable",
      "resource": {
        "table": {
          "catalogName": "iceberg",
          "properties": {},
          "schemaName": "workspace",
          "tableName": "v_table_a"
        }
      }
    },
    "context": {
      "identity": {
        "user": "admin"
      }
    }
  }
}

# ---------------------------- DROP TABLE  -----------------------------

test_admin_drop_table if {
  allow with input as {
    "action": {
      "operation": "DropTable",
      "resource": {
        "table": {
          "catalogName": "iceberg",
          "properties": {},
          "schemaName": "workspace",
          "tableName": "table_a"
        }
      }
    },
    "context": {
      "identity": {
        "user": "admin"
      }
    }
  }
}

test_alice_drop_table_iceberg_workspace_with_prefix if {
  allow with input as {
    "action": {
      "operation": "DropTable",
      "resource": {
        "table": {
          "catalogName": "iceberg",
          "properties": {},
          "schemaName": "workspace",
          "tableName": "v_table_a"
        }
      }
    },
    "context": {
      "identity": {
        "user": "admin"
      }
    }
  }
}

# alice cannot create tables in iceberg.workspace without prefix v_
test_alice_drop_table_iceberg_workspace_without_prefix if {
  not allow with input as {
    "action": {
      "operation": "DropTable",
      "resource": {
        "table": {
          "catalogName": "iceberg",
          "properties": {},
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


# ---------------------------- UPDATE  -----------------------------


# ---------------------------- DELETE  -----------------------------


# ---------------------------- CREATE VIEW  -----------------------------


# ---------------------------- SHOW CREATE VIEW  -----------------------------

# ---------------------------- DROP VIEW  -----------------------------


# ---------------------------- CREATE MV  -----------------------------

# ---------------------------- DROP MV  -----------------------------
