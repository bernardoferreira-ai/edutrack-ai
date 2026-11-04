// Add subjects record
query subjects verb=POST {
  api_group = "Subjects"
  auth = "user"

  input {
    dblink {
      table = "subjects"
    }
  }

  stack {
    db.add subjects {
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
  guid = "lEyU8McN_ayv7Opvt2E3yW_XdiU"
}