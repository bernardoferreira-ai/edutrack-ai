// List academic tasks for the authenticated user
query "academic_tasks" verb=GET {
  api_group = "Academic Tasks"
  auth = "user"
  description = "List all academic tasks belonging to the authenticated user with optional filtering"

  input {
    int? subject_id {
      description = "Optional filter by subject ID"
    }
    text? status filters=trim {
      description = "Optional filter by task status"
    }
  }

  stack {
    db.query academic_tasks {
      where = $db.academic_tasks.user_id == $auth.id && ($input.subject_id == null || $db.academic_tasks.subject_id == $input.subject_id) && ($input.status == null || $db.academic_tasks.status == $input.status)
      return = {type: "list"}
    } as $user_tasks
  }

  response = $user_tasks
  guid = "CXCJmdhHPK-h81f9Es11tyc3YmY"
}

