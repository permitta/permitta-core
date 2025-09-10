import json

with open("moat/seed_data/principals.json") as f:
    principals = json.load(f)

with open("moat/seed_data/principal_groups.json") as tags_file:
    all_group_props = [
        g.get("membership_property") for g in json.load(tags_file).get("groups")
    ]

with open("docker/lldap/bootstrap/group-configs/groups.json", "w") as f:
    f.write(json.dumps({"name": "moat_users_gl"}) + "\n")

    for group_prop in all_group_props:
        f.write(json.dumps({"name": group_prop.get("value")}) + "\n")

with open("docker/lldap/bootstrap/user-configs/users.json", "w") as f:
    group_prop_index: int = 0

    for principal in principals:
        group_prop: dict = all_group_props[group_prop_index]
        group_prop_index += 1
        if group_prop_index == len(all_group_props):
            group_prop_index = 0

        ldap_user: dict = {
            "id": principal.get("email").split("@")[0],
            "email": principal.get("email"),
            "password": "changeme",
            "displayName": principal.get("first_name").title()
            + " "
            + principal.get("last_name").title(),
            "firstName": principal.get("first_name").title(),
            "lastName": principal.get("last_name").title(),
            "gravatar_avatar": "true",
            "groups": [group_prop["value"], "moat_users_gl"],
        }
        f.write(json.dumps(ldap_user) + "\n")
