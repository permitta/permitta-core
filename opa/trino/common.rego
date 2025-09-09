package moat.trino

import rego.v1
import data.trino

data_objects := data.trino.data_objects
principals := data.trino.principals

input_principal_name := input.context.identity.user
action := input.action.operation

input_table := {
	"database": input.action.resource.table.catalogName,
	"schema": input.action.resource.table.schemaName,
	"table": input.action.resource.table.tableName
}

input_columns := input.action.resource.table.columns

data_object_attributes contains attribute if {
  some data_object in data_objects
	data_object.object == input_table
	some attribute in data_object.attributes
}

principal_attributes contains attribute if {
  some principal in principals
  principal.name == input_principal_name
  some attribute in principal.attributes
}

principal_exists(principal_name) if {
  principal_name
  some principal in principals
  principal.name == principal_name
}

data_object_is_tagged(data_object) if {
  data_object
  count(data_object.attributes) > 0
}

principal_has_all_required_attributes(required_principal_attributes) if {
  # assert that the principal has all required_principal_attributes
  every required_principal_attribute in required_principal_attributes {
    required_principal_attribute == principal_attributes[_]
  }
}

# if columns are specified on the data object, they they have their
# own classification, we need to test them here
# if a column is selected then we need to check it on the object
classified_columns contains classified_column if {
  # get the table from the data
  some data_object in data_objects
	data_object.object == input_table

  # get the set of columns in the input which match the data
  some input_column in input_columns
  input_column == data_object.columns[i].name

  # get the full column object from the data
  some classified_column in data_object.columns
  classified_column.name == input_column
}

all_classified_column_attrs_exist_on_principal if {
  # for all columns which are in both the input and data
  every classified_column in classified_columns {
    # for every attribute on each of the columns
    every column_attribute in classified_column.attributes {
      # all attrs on the column must be on the principal
      column_attribute == principal_attributes[_]
    }
  }
}
