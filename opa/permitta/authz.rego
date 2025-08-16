package permitta.authz
import rego.v1

action_read := "READ"
action_create := "CREATE"
action_update := "UPDATE"
action_delete := "DELETE"

object_type_policy := "POLICY"
object_type_principal := "PRINCIPAL"
object_type_table := "TABLE"

admin_role_attribute := {"key": "ad_group", "value": "ADMINISTRATORS"}
maintainer_role_attribute := {"key": "ad_group", "value": "DEVELOPERS"}

has_role(role_attribute) if {
  subject_has_all_object_attributes(input.subject.attributes, [role_attribute])
}

# Read policies - if the action = READ, then allow
allow if {
  input.action == "READ"
}

# admin policy: if the user has permitta:admin then they can do anything
allow if {
  has_role(admin_role_attribute)
}

# Write actions - user must have all attributes that the subject does
# for all object types except policies
allow if {
  input.action in [action_create, action_update, action_delete]
  input.object.type != object_type_policy
  subject_has_all_object_attributes(input.subject.attributes, input.object.attributes)
}

# policy writes
allow if {
  input.action in allowed_policy_actions  # checks the role
}

# allowed policy actions
# based on the user attributes (admin?) and state, some policy actions can be performed

policy_action_create := "CREATE_POLICY"
policy_action_edit := "EDIT_POLICY"
policy_action_clone := "CLONE_POLICY"
policy_action_up_version := "UP_VERSION_POLICY"
policy_action_request_publish := "REQUEST_PUBLISH_POLICY"
policy_action_request_disable := "REQUEST_DISABLE_POLICY"
policy_action_cancel_publish := "CANCEL_PUBLISH_POLICY"
policy_action_cancel_disable := "CANCEL_DISABLE_POLICY"
policy_action_publish := "PUBLISH_POLICY"
policy_action_disable := "DISABLE_POLICY"
policy_action_delete := "DELETE_POLICY"

policy_actions := [
  policy_action_create,
  policy_action_edit,
  policy_action_clone,
  policy_action_request_publish,
  policy_action_request_disable,
  policy_action_cancel_publish,
  policy_action_cancel_disable,
  policy_action_publish,
  policy_action_disable,
  policy_action_delete,
  policy_action_up_version
]

policy_state_new := "New"
policy_state_draft := "Draft"
policy_state_published := "Published"
policy_state_pending_publish := "Pending Publish"
policy_state_pending_disable := "Pending Delete"
policy_state_disabled := "Disabled"

policy_actions_by_state := {
  policy_state_new: [policy_action_create],
  policy_state_draft: [policy_action_create, policy_action_request_publish, policy_action_delete, policy_action_clone, policy_action_edit],
  policy_state_published: [policy_action_request_disable, policy_action_clone, policy_action_up_version],
  policy_state_pending_publish: [policy_action_publish, policy_action_clone, policy_action_edit, policy_action_cancel_publish],
  policy_state_pending_disable: [policy_action_disable, policy_action_cancel_disable, policy_action_clone],
  policy_state_disabled: [policy_action_request_publish, policy_action_delete, policy_action_clone, policy_action_edit]
}

# if the user has permitta:admin then they can do anything in any state
allowed_policy_actions contains action if {
  input.object.type == object_type_policy
  has_role(admin_role_attribute)
  some action in policy_actions
}

allowed_policy_actions contains action if {
  input.object.type == object_type_policy
  
  # only a maintainer can do anything here:
  has_role(maintainer_role_attribute)

  # filter the available options by the current state
  some action in policy_actions_by_state[input.object.state]

  # phase 1: noone but admin can publish or deactivate
  action != policy_action_publish
  action != policy_action_disable
}

subject_has_all_object_attributes(subject_attributes, object_attributes) if {
  # assert that the subject has all required_attributes
  every object_attribute in object_attributes {
    object_attribute == subject_attributes[_]
  }
}
