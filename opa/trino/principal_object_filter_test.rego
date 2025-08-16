package permitta.trino

import rego.v1

test_principals_with_all_attributes_sales_comm_priv if {
  actual := principals_with_all_attributes with input as {
    "required_principal_attributes": [
      {
        "key": "Sales", "value": "Commercial"
      },
      {
        "key": "Sales", "value": "Privacy"
      }
    ]
  }

  expected := {
    "bob"
  }
  actual == expected
}

test_principals_with_all_attributes_sales_comm if {
  actual := principals_with_all_attributes with input as {
    "required_principal_attributes": [
      {
        "key": "Sales", "value": "Commercial"
      }
    ]
  }

  expected := {
    "bob", "alice", "frank"
  }
  actual == expected
}

test_principals_with_all_attributes_none if {
  actual := principals_with_all_attributes with input as {
    "required_principal_attributes": [
    ]
  }

  expected := {
    "bob", "alice", "frank", "anne", "janis"
  }
  actual == expected
}

# -------------------- data objects ----------------------

test_data_objects_with_all_attributes_sales_comm if {
  actual := data_objects_with_all_attributes with input as {
    "permitted_object_attributes": [
      {
        "key": "Sales", "value": "Commercial"
      }
    ]
  }

  expected := {
      {
        "database": "datalake",
        "schema": "logistics",
        "table": "shippers"
      },
      {
        "database": "datalake",
        "schema": "logistics",
        "table": "territories"
      },
      {
        "database": "datalake",
        "schema": "sales",
        "table": "products"
      }
  }
  actual == expected
}

test_data_objects_with_all_attributes_none if {
  actual := data_objects_with_all_attributes with input as {
    "permitted_object_attributes": [
    ]
  }
  count(actual) == 0
}

