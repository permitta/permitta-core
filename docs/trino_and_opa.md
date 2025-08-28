# How Trino and OPA work together

When an SQL statement is supplied to Trino for execution, it executes a (potentially) large number of authorisation 
checks. Each of these authorisation checks includes an action, a subject and an object. The subject is the user executing
the query, and the object is the catalog, schema, table or column. 

Upon receiving an authorisation request OPA executes tests defined in the policy document using an input variable 
provided by Trino, against the data in the context data object.

For example, a user executes a simple query:

`SELECT a, b, c from datalake.hr.employees`

This results in many requests to OPA, one of which checks if this user (alice) 
is allowed to select these columns:

```json
{
  "context": {
    "identity": {
      "user": "alice"
    }
  },
  "action": {
    "operation": "SelectFromColumns",
    "resource": {
      "table": {
        "catalogName": "datalake",
        "schemaName": "hr",
        "tableName": "employees",
        "columns": ["a", "b", "c"]
      }
    }
  }
}
```

## Policy Implementation
To implement ABAC/RBAC policies with OPA, we require a `data` object containing the `principals` 
and `data-objects` (schemas, tables, columns etc) as well at attributes or groups for each. 
OPA uses the information in the `data` object, along with `input` object to enforce the rules
defined in the rego policy document.

### Example Rego Policy Document
This policy ensures that any user who exists in our data object is allowed to `SELECT` from
any table in the `datalake` catalog, as long as the schema is in our data object. 
All other operations on any other object will be denied

```rego
package permitta.trino

import rego.v1
import data.trino

allow if {
  # action is SELECT
  input.action.operation == "SelectFromColumns"
  
  # user exists in our data object
  some principal in data.trino.principals
  principal.name == input.context.identity.user
  
  # catalog is datalake
  input.action.resource.table.catalogName == "datalake"
  
  # schema is in our data object
  some schema in data.trino.schemas
  schema.name == input.action.resource.table.schemaName
}
```

### Example Data object
```json
{ 
  "principals": [
    {
      "name": "alice"
    },
    {
      "name": "bob"
    }
  ],
  "schemas": [
    {
      "name": "hr"
    }
  ]
}

```