// Update subjects record
query "subjects/{subjects_id}" verb=PUT {
  api_group = "Subjects"
  auth = "user"

  input {
    int subjects_id? filters=min:1
    dblink {
      table = "subjects"
    }
  }

  stack {
    db.edit subjects {
      field_name = "id"
      field_value = $input.subjects_id
      enforce_hidden_fields = false
      data = {
        created_at: $input.created_at
        user_id   : $input.user_id
        name      : $input.name
        teacher   : $input.teacher
        hours     : $input.hours
      }
    } as $model
  }

  response = $model
  guid = "RsXiDdFJINoHdWmIzYHBQnqM1io"
}