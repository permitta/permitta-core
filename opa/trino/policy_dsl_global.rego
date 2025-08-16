package permitta.trino

import rego.v1
import data.trino

# global policy - if all object tags are on the principal, then allow
all_object_attrs_exist_on_principal if {
  # ensure all attrs on object exist on principal
	every data_object_attribute in data_object_attributes {
    some principal_attribute in principal_attributes
    data_object_attribute == principal_attribute
  }
}