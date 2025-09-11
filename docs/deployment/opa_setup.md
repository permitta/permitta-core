# OPA Setup
OPA should be configured to load its bundle from the bundle API exposed by moat. 

```yaml
services:
  moat:
    url: https://moat.example.com/api/v1/opa/     # replace with the hostname of your installation
    credentials:
      bearer:
        token_path: /config/token.txt             # pre-shared bearer token should be applied to the moat config and mounted here

decision_logs:                                    # if decision logs are required, enable this block
  service: moat
  resource: /decision
  reporting:
    min_delay_seconds: 1
    max_delay_seconds: 10

bundles:                                          # ensure that the bundle persistence is enabled for better durability
  trino:
    service: moat
    resource: /bundle/trino
    persist: true
    polling:
      min_delay_seconds: 10
      max_delay_seconds: 20

status:
  service: moat

persistence_directory: /persistence
```