package permitta.authz
import rego.v1

# allowed policy actions with admin tag
test_allowed_policy_actions_admin if {
  actual := allowed_policy_actions with input as {
    "action": "READ",
    "subject": {
      "username": "alice",
      "attributes": [
        {"key": "permitta_role", "value": "admin"}
      ],
    },
    "object": {
      "type": "POLICY",
      "attributes": [{"key": "IT", "value": "Commercial"}],
    },
  }
  expected := {
    "EDIT_POLICY",
    "CLONE_POLICY",
    "UP_VERSION_POLICY",
    "REQUEST_PUBLISH_POLICY",
    "REQUEST_DISABLE_POLICY",
    "CANCEL_PUBLISH_POLICY",
    "CANCEL_DISABLE_POLICY",
    "PUBLISH_POLICY",
    "DISABLE_POLICY",
    "DELETE_POLICY"
  }
  actual == expected
}

# should not be allowed to do anything
test_allowed_policy_actions_non_admin if {
  actual := allowed_policy_actions with input as {
    "action": "READ",
    "subject": {
      "username": "alice",
      "attributes": [
        {"key": "HR", "value": "Commercial"},
      ],
    },
    "object": {
      "type": "POLICY",
      "attributes": [{"key": "HR", "value": "Commercial"}],
    },
  }
  expected := set()
  actual == expected
}

# maintainer should be allowed to do some actions on a policy
test_allowed_policy_actions_maintainer if {
  actual := allowed_policy_actions with input as {
    "action": "READ",
    "subject": {
      "username": "alice",
      "attributes": [
        {"key": "permitta_role", "value": "maintainer"},
      ],
    },
    "object": {
      "type": "POLICY",
      "state": "draft",
      "attributes": [],
    },
  }
  count(actual) > 0
}



# policy actions by state
test_allowed_policy_actions_state_draft if {
  actual := allowed_policy_actions with input as {
    "action": "READ",
    "subject": {
      "username": "alice",
      "attributes": [
        {"key": "HR", "value": "Commercial"},
        {"key": "permitta_role", "value": "maintainer"}
      ],
    },
    "object": {
      "type": "POLICY",
      "state": "draft",
      "attributes": [{"key": "HR", "value": "Commercial"}],
    },
  }
  expected := {
    "EDIT_POLICY",
    "CLONE_POLICY",
    "REQUEST_PUBLISH_POLICY",
    "DELETE_POLICY"
  }
  actual == expected
}

test_allowed_policy_actions_state_published if {
  actual := allowed_policy_actions with input as {
    "action": "READ",
    "subject": {
      "username": "alice",
      "attributes": [
        {"key": "HR", "value": "Commercial"},
        {"key": "permitta_role", "value": "maintainer"}
      ],
    },
    "object": {
      "type": "POLICY",
      "state": "published",
      "attributes": [{"key": "HR", "value": "Commercial"}],
    },
  }
  expected := {
    "CLONE_POLICY",
    "UP_VERSION_POLICY",
    "REQUEST_DISABLE_POLICY",
  }
  actual == expected
}

test_allowed_policy_actions_state_pending_publish if {
  actual := allowed_policy_actions with input as {
    "action": "READ",
    "subject": {
      "username": "alice",
      "attributes": [
        {"key": "HR", "value": "Commercial"},
        {"key": "permitta_role", "value": "maintainer"}
      ],
    },
    "object": {
      "type": "POLICY",
      "state": "pending_publish",
      "attributes": [{"key": "HR", "value": "Commercial"}],
    },
  }
  expected := {
    "CANCEL_PUBLISH_POLICY",
    "CLONE_POLICY",
    "EDIT_POLICY",
  }
  actual == expected
}

test_allowed_policy_actions_state_pending_disable if {
  actual := allowed_policy_actions with input as {
    "action": "READ",
    "subject": {
      "username": "alice",
      "attributes": [
        {"key": "HR", "value": "Commercial"},
        {"key": "permitta_role", "value": "maintainer"}
      ],
    },
    "object": {
      "type": "POLICY",
      "state": "pending_disable",
      "attributes": [{"key": "HR", "value": "Commercial"}],
    },
  }
  expected := {
    "CANCEL_DISABLE_POLICY",
    "CLONE_POLICY",
  }
  actual == expected
}

test_allowed_policy_actions_state_disabled if {
  actual := allowed_policy_actions with input as {
    "action": "READ",
    "subject": {
      "username": "alice",
      "attributes": [
        {"key": "HR", "value": "Commercial"},
        {"key": "permitta_role", "value": "maintainer"}
      ],
    },
    "object": {
      "type": "POLICY",
      "state": "disabled",
      "attributes": [{"key": "HR", "value": "Commercial"}],
    },
  }
  expected := {
    "REQUEST_PUBLISH_POLICY",
    "DELETE_POLICY",
    "CLONE_POLICY",
    "EDIT_POLICY"
  }
  actual == expected
}