// Delete academic_tasks record
query "academic_tasks/{academic_tasks_id}" verb=DELETE {
  api_group = "Academic Tasks"
  auth = "user"

  input {
    int academic_tasks_id? filters=min:1
  }

  stack {
    db.del academic_tasks {
      field_name = "id"
      field_value = $input.academic_tasks_id
    }
  }

  response = null
  guid = "Io3mMlPnlsNNfLlS_OvMatWE8EI"
}