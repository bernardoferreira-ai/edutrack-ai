// Add academic_tasks record
query academic_tasks verb=POST {
  api_group = "Academic Tasks"
  auth = "user"

  input {
    dblink {
      table = "academic_tasks"
    }
  }

  stack {
    db.add academic_tasks {
      enforce_hidden_fields = false
      data = {
        created_at : $input.created_at
        user_id    : $input.user_id
        subject_id : $input.subject_id
        title      : $input.title
        description: $input.description
        due_date   : $input.due_date
        status     : $input.status
      }
    } as $model
  }

  response = $model
  guid = "9kQ-OAxHIT9mKTznCf-mh6gZpo4"
}