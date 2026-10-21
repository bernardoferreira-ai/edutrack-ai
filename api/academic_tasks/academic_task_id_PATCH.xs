// Update an existing academic task ensuring user ownership
query "academic_tasks/{id}" verb=PATCH {
  api_group = "Academic Tasks"
  auth = "user"
  description = "Update academic task fields for an owned record"

  input {
    int id {
      description = "ID of the task to update"
    }
    int? subject_id {
      description = "Updated subject ID"
    }
    text? title filters=trim {
      description = "Updated title"
    }
    text? description filters=trim {
      description = "Updated description"
    }
    date? due_date {
      description = "Updated due date"
    }
    text? status filters=trim {
      description = "Updated status"
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

    // Verify subject ownership (checks updated subject_id or keeps existing)
    db.get subjects {
      field_name = "id"
      field_value = $input.subject_id || $task.subject_id
    } as $subject

    precondition ($subject != null && $subject.user_id == $auth.id) {
      error_type = "badrequest"
      error = "Invalid subject_id: subject not found or not owned by user."
    }

    db.edit academic_tasks {
      field_name = "id"
      field_value = $input.id
      data = {
        subject_id : $input.subject_id || $task.subject_id
        title      : $input.title || $task.title
        description: $input.description || $task.description
        due_date   : $input.due_date || $task.due_date
        status     : $input.status || $task.status
      }
    } as $updated_task
  }

  response = $updated_task
  guid = "VTKWWfIue67-6lSskhDhmSEJ82Y"
}
