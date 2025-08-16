package permitta.authz
import rego.v1

# phase 1 tests:
# admin can move any policy to any state
# maintainer can move policies between allowed workflow states
# admin is required to approve
# maintainer or owner can publish an approved policy

# phase 2 tests
# domain owner can approve policies which match their attributes
  # multiple domain owners may be required to approve

# all reads are allowed - no tag matching required
test_allow_read if {
  allow with input as {
    "action": "READ",
    "subject": {
      "username": "alice",
      "attributes": [
        {"key": "HR", "value": "Commercial"},
        {"key": "HR", "value": "Privacy"},
      ],
    },
    "object": {
      "type": "POLICY",
      "attributes": [{"key": "IT", "value": "Commercial"}],
    },
  }
}

# test policy writes
test_allow_policy_edit_draft_maintainer if {
  allow with input as {
    "action": "EDIT_POLICY",
    "subject": {
      "username": "alice",
      "attributes": [
        {"key": "permitta_role", "value": "maintainer"}
      ],
    },
    "object": {
      "type": "POLICY",
      "state": "draft",
      "attributes": [],
    },
  }
}

test_allow_policy_request_publish_draft_maintainer if {
  allow with input as {
    "action": "REQUEST_PUBLISH_POLICY",
    "subject": {
      "username": "alice",
      "attributes": [
        {"key": "permitta_role", "value": "maintainer"}
      ],
    },
    "object": {
      "type": "POLICY",
      "state": "draft",
      "attributes": [],
    },
  }
}

test_allow_policy_request_publish_published_maintainer if {
  not allow with input as {
    "action": "REQUEST_PUBLISH_POLICY",
    "subject": {
      "username": "alice",
      "attributes": [
        {"key": "permitta_role", "value": "maintainer"}
      ],
    },
    "object": {
      "type": "POLICY",
      "state": "published",
      "attributes": [],
    },
  }
}

test_allow_policy_delete_draft_maintainer if {
  allow with input as {
    "action": "DELETE_POLICY",
    "subject": {
      "username": "alice",
      "attributes": [
        {"key": "permitta_role", "value": "maintainer"}
      ],
    },
    "object": {
      "type": "POLICY",
      "state": "draft",
      "attributes": [],
    },
  }
}

test_allow_policy_edit_published_maintainer if {
  not allow with input as {
    "action": "EDIT_POLICY",
    "subject": {
      "username": "alice",
      "attributes": [
        {"key": "permitta_role", "value": "maintainer"}
      ],
    },
    "object": {
      "type": "POLICY",
      "state": "published",
      "attributes": [],
    },
  }
}

test_allow_policy_edit_draft_user if {
  not allow with input as {
    "action": "EDIT_POLICY",
    "subject": {
      "username": "alice",
      "attributes": [
      ],
    },
    "object": {
      "type": "POLICY",
      "state": "draft",
      "attributes": [],
    },
  }
}

test_allow_policy_publish_draft_admin if {
  allow with input as {
    "action": "PUBLISH_POLICY",
    "subject": {
      "username": "alice",
      "attributes": [
        {"key": "permitta_role", "value": "admin"}
      ],
    },
    "object": {
      "type": "POLICY",
      "state": "draft",
      "attributes": [],
    },
  }
}