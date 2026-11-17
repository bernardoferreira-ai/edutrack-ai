// Update academic_tasks record
query "academic_tasks/{academic_tasks_id}" verb=PUT {
  api_group = "Academic Tasks"
  auth = "user"

  input {
    int academic_tasks_id? filters=min:1
    dblink {
      table = "academic_tasks"
    }
  }

  stack {
    db.edit academic_tasks {
      field_name = "id"
      field_value = $input.academic_tasks_id
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
  guid = "a9JpZFdrewsNaIbTDAdEz5zDmk4"
}