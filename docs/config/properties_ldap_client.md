# LDAP Client Properties

These properties configure the LDAP client which is used to ingest principals.

## `ldap_client.host`
* Type: `url`
* Default: `<none>`
* Example: `ldap.domain.com`

## `ldap_client.port`
* Type: `string`
* Default: `<none>`
* Example: `3890`

## `ldap_client.user_dn`
* Type: `string`
* Default: `<none>`
* Example: `uid=admin,ou=people,dc=example,dc=com`

## `ldap_client.password`
* Type: `string`
* Default: `<none>`
* Example: `$LDAP_PASSWORD`

## `ldap_client.base_dn`
* Type: `string`
* Default: `<none>`
* Example: `dc=example,dc=com`

## `ldap_client.user_base_dn`
* Type: `string`
* Default: `<none>`
* Example: `ou=people,dc=example,dc=com`
