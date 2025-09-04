package permitta.trino

import rego.v1
import data.trino

allow if {
  input_principal_name == "admin"
}

principal_has_access_to_column(attributes) if {
  input_principal_name == "admin"
}
