package permitta.trino

import rego.v1
import data.trino

# developer permissions
# user can create and drop tables, views and MVs
# user can select, insert, update and delete
# policy has:
  # selector tags for the user
  # actions list
  # list of regexes for the object
  # devs can have access at any object level
allow if {
  permitted_actions := [
    "SelectFromColumns",
    "InsertIntoTable",
    "CreateTable",
    "ShowCreateTable",
    "DropTable",
    "UpdateTableColumns",
    "DeleteFromTable"
    ]

  required_principal_attributes := [
    {
      "key": "Sales",
      "value": "Commercial"
    }
  ]

  # everything in sales schema with prefix of v_ or u_
  permitted_object_regexes := [
    {
      "database": "iceberg",
      "schema": "workspace",
      "table": "v_.*"
    },
    {
      "database": "iceberg",
      "schema": "workspace",
      "table": "u_.*"
    }
  ]

  input.action.operation in permitted_actions
  principal_has_all_required_attributes(required_principal_attributes)

  # TODO check the props the user is using

  # check the input object matches a regex
  some permitted_object_regex in permitted_object_regexes
  regex.match(permitted_object_regex.database, input_table.database)
  regex.match(permitted_object_regex.schema, input_table.schema)
  regex.match(permitted_object_regex.table, input_table.table)

}

allow if {
  permitted_actions := ["FilterSchemas"]

  required_principal_attributes := [
    {
      "key": "Sales",
      "value": "Commercial"
    }
  ]

  # everything in sales schema with prefix of v_ or u_
  permitted_object_regexes := [
    {
      "database": "iceberg",
      "schema": "workspace",
      "table": "v_.*"
    },
    {
      "database": "iceberg",
      "schema": "workspace",
      "table": "u_.*"
    }
  ]

  input.action.operation in permitted_actions
  principal_has_all_required_attributes(required_principal_attributes)

  some permitted_object_regex in permitted_object_regexes
  regex.match(permitted_object_regex.database, input.action.resource.schema.catalogName)
  regex.match(permitted_object_regex.schema, input.action.resource.schema.schemaName)
}


allow if {
  permitted_actions := ["FilterCatalogs", "AccessCatalog"]

  required_principal_attributes := [
    {
      "key": "Sales",
      "value": "Commercial"
    }
  ]

  # everything in sales schema with prefix of v_ or u_
  permitted_object_regexes := [
    {
      "database": "iceberg",
      "schema": "workspace",
      "table": "v_.*"
    },
    {
      "database": "iceberg",
      "schema": "workspace",
      "table": "u_.*"
    }
  ]

  input.action.operation in permitted_actions
  principal_has_all_required_attributes(required_principal_attributes)

  some permitted_object_regex in permitted_object_regexes
  regex.match(permitted_object_regex.database, input.action.resource.catalog.name)
}

