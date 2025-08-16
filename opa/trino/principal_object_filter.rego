package permitta.trino

import rego.v1
import data.trino

principals_with_all_attributes contains principal.name if {
  # loop over the principals
  some principal in principals

  # assert that the principal has all required_principal_attributes
  every required_principal_attribute in input.required_principal_attributes {
    required_principal_attribute == principal.attributes[_]
  }
}

data_objects_with_all_attributes contains data_object.object if {
  # loop over the objects
  some data_object in data_objects

  # assert that the object has all permitted_object_attributes
  permitted_object_attributes = input.permitted_object_attributes

  every permitted_object_attribute in permitted_object_attributes {
    permitted_object_attribute == data_object.attributes[_]
  }
  count(permitted_object_attributes) == count(data_object.attributes)
}