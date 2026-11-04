// Edit subjects record
query "subjects/{subjects_id}" verb=PATCH {
  api_group = "Subjects"
  auth = "user"

  input {
    int subjects_id? filters=min:1
    dblink {
      table = "subjects"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch subjects {
      field_name = "id"
      field_value = $input.subjects_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $model
  }

  response = $model
  guid = "FJk_lB9q0atzkGqpvRZupaBz7WY"
}