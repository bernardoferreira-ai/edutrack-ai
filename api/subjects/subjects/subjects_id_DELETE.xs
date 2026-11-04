// Delete subjects record
query "subjects/{subjects_id}" verb=DELETE {
  api_group = "Subjects"
  auth = "user"

  input {
    int subjects_id? filters=min:1
  }

  stack {
    db.del subjects {
      field_name = "id"
      field_value = $input.subjects_id
    }
  }

  response = null
  guid = "zwxuqjFs8RWF6hyBU3Qh3MybD-E"
}