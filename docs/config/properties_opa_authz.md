# OPA Authorisation Properties

On startup, Permitta pushes a `rego` policy document to OPA. This
document contains the rules for authorisation within Permitta.

These properties define the name and location of the `rego` document
which is provided to OPA. This document can be replaced by the developer,
allowing a high level of flexibility of authorisation.

## `opa_authz_provider.policy_name`
* Type: `string`
* Default: `permitta/authz`
* Example: `permitta/authz`

## `opa_authz_provider.policy_file_path`
* Type: `string`
* Default: `<none>`
* Example: `opa/permitta/authz.rego`

## OPA Connectivity Properties
These properties control the connectivity to the OPA instance
used for authorisation of actions within the Permitta UI and APIs.
This can be the same instance used by `trino`, however it is 
recommended that Permitta has a dedicated instance.

## `opa_client.scheme`
* Type: `enum`
* Values: `https`, `http`
* Default: `<none>`
* Example: `https`

For production deployments, HTTPS should be used everywhere.

## `opa_client.hostname`
* Type: `string`
* Default: `localhost`
* Example: `opa.permitta.svc.cluster.local`

The hostname of the OPA instance that Permitta should connect to

## `opa_client.port`
* Type: `string`
* Default: `8181`
* Example: `8181`

## `opa_client.path`
* Type: `path`
* Default: `/v1/data/permitta/authz/allow`
* Example: `/v1/data/permitta/authz/allow`

## `opa_client.timeout_seconds`
* Type: `string`
* Default: `1`
* Example: `10`
