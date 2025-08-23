# Overview
## Permitta makes using OPA with Trino simple and fun

OPA and Trino are an awesome combination, but maintaining the policy documents and required data object
can be painful. Permitta-core makes this easy with managed curation of principals and tables,
as well as a predefined set of ABAC policies suitable for most uses

Permitta-core provides an API to serve bundles to OPA, including:

* Data objects and attributes ingested from various sources (SQL DBs,data catalogs etc)
* Principals and attributes/groups ingested from identity providers (SQL DB, LDAP, etc)
* Pre-built `rego` policy documents to support common use cases (e.g. RBAC) 

## Architecture

Drawing TBA


## Motivation
In late 2023 [Open Policy Agent (OPA)](https://www.openpolicyagent.org/) was introduced into Trino as an [authentication method](https://trino.io/docs/current/security/opa-access-control.html).
OPA is a very powerful policy enforcement engine which helps to solve many authorisation issues with the previously available 
authorisation options in Trino. 

OPA provides the capability to implement very fine-grained R/ABAC policies to control access to data in Trino. OPA
policies can control access at the catalog, schema, table or column level and provide column masking. 

OPA policies are defined in a language called Rego. While it is an expressive and powerful language, it has a steep
learning curve and limits policy definition to users with software development skills. It is expected that users within 
many organisations who are tasked with data policy definition do not possess these types of skills.

OPA also requires context on the principals and objects, such as attributes or group mappings. This must be provided to OPA
as a (possibly) large JSON object, and updated whenever these values change.  

While extremely powerful, OPA is hard to use for non-developers, and has a significant integration cost. 

**Permitta simplifies the use of OPA with Trino by:**

* Aggregating metadata from sources such as `Active Directory`
* Delivering bundles of policy and context metadata to instances of OPA

## How Trino and OPA work together

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

### Policy Implementation
To implement ABAC/RBAC policies with OPA, we require a `data` object containing the `principals` 
and `data-objects` (schemas, tables, columns etc) as well at attributes or groups for each. 
OPA uses the information in the `data` object, along with `input` object to enforce the rules
defined in the rego policy document.

#### Example Rego Policy Document
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

#### Example Data object
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