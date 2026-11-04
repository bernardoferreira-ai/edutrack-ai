// Get subjects record
query "subjects/{subjects_id}" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
    int subjects_id? filters=min:1
  }

  stack {
    db.get subjects {
      field_name = "id"
      field_value = $input.subjects_id
    } as $model
  
    precondition ($model != null) {
      error_type = "notfound"
      error = "Not Found"
    }
  }

  response = $model
  guid = "Ndp6P8I0Pi81dzVK80d030_rwOU"
}