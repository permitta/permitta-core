package permitta.trino

import rego.v1
import data.trino

# bob's builder policy
# principal must have principal tags, object must have object tags
#builder_policy_allows_principal_access_by_mapping(data_object) if {
#  required_principal_attributes := [
#    {
#      "key": "Sales",
#      "value": "Commercial"
#    }
#  ]
#
#  permitted_object_attributes := [
#    {
#      "key": "Sales",
#      "value": "Commercial"
#    },
#    {
#      "key": "Marketing",
#      "value": "Commercial"
#    }
#  ]
#
#  # assert that the principal has all required_principal_attributes
#  principal_has_all_required_attributes(required_principal_attributes)
#
  # assert that the object has permitted_object_attributes and no others
#  some permitted_object_attribute in permitted_object_attributes
#  permitted_object_attribute == data_object.attributes[_]
#  count(permitted_object_attributes) == count(data_object.attributes)
#}
