# Configuration File
All configuration items are defined in a yaml file provided to the application.
The location of this file is defined by an environment variable called 
`CONFIG_FILE_PATH`. The value of this variable should be an absolute path.

The yaml file is a flat structure, with all keys at the top level. E.g:

```yaml
ldap_client.host: localhost
ldap_client.port: "3890"
ldap_client.base_dn: dc=example,dc=com
ldap_client.user_dn: uid=admin,ou=people,dc=example,dc=com
```

## Environment Variables
If environment variables are preferred for some configuration items (e.g secrets)
these can be referenced in the configuration file using a bash-style syntax. These
values will be retrieved from the environment and included in the configuration
object at runtime.

```yaml
ldap_client.password: $LDAP_PASSWORD 
ldap_client.user_dn: uid=$LDAP_UID,ou=people,dc=example,dc=com
```