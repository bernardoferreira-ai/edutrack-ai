// Create a new academic task for the authenticated user
query "academic_tasks" verb=POST {
  api_group = "Academic Tasks"
  auth = "user"
  description = "Create a new academic task verifying subject ownership and assigning user_id"

  input {
    int subject_id {
      description = "ID of the academic subject"
    }
    text title filters=trim {
      description = "Title of the task"
    }
    text? description filters=trim {
      description = "Optional detailed description"
    }
    date? due_date {
      description = "Optional due date deadline"
    }
    text? status?="pending" filters=trim {
      description = "Initial task status"
    }
  }

  stack {
    precondition ($input.title != null && ($input.title|length) > 0) {
      error_type = "badrequest"
      error = "Task title is required."
    }

    // Verify that the referenced subject belongs to the authenticated user
    db.get subjects {
      field_name = "id"
      field_value = $input.subject_id
    } as $subject

    precondition ($subject != null && $subject.user_id == $auth.id) {
      error_type = "badrequest"
      error = "Invalid subject_id: subject not found or not owned by user."
    }

    db.add academic_tasks {
      data = {
        created_at : "now"
        user_id    : $auth.id
        subject_id : $input.subject_id
        title      : $input.title
        description: $input.description
        due_date   : $input.due_date
        status     : $input.status || "pending"
      }
    } as $new_task
  }

  response = $new_task
  guid = "iUI6XoF7h1_JLBHXZaZh-n-m6Rs"
}

