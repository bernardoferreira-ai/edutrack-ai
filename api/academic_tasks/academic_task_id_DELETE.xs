// Delete an academic task ensuring user ownership
query "academic_tasks/{id}" verb=DELETE {
  api_group = "Academic Tasks"
  auth = "user"
  description = "Delete an academic task owned by the authenticated user"

  input {
    int id {
      description = "ID of the task to delete"
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

    db.del academic_tasks {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {success: true, message: "Task deleted successfully."}
  guid = "cgvxo8dX9uOsr_DkpRm3U0WzYCI"
}

