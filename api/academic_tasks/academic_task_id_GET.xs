// Get a single academic task by ID ensuring user ownership
query "academic_tasks/{id}" verb=GET {
  api_group = "Academic Tasks"
  auth = "user"
  description = "Retrieve a single academic task if owned by the authenticated user"

  input {
    int id {
      description = "ID of the academic task"
    }
  }

  stack {
    db.get academic_tasks {
      field_name = "id"
      field_value = $input.id
    } as $task

    precondition ($task != null && $task.user_id == $auth.id) {
      error_type = "notfound"
      error = "Task not found."
    }
  }

  response = $task
  guid = "GhtgKlHljBRMznT8VqgUM6v_ptA"
}

