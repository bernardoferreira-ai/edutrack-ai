// Edit academic_tasks record
query "academic_tasks/{academic_tasks_id}" verb=PATCH {
  api_group = "Academic Tasks"
  auth = "user"

  input {
    int academic_tasks_id filters=min:1
    dblink {
      table = "academic_tasks"
      override = {
        title      : {hidden: false}
        user_id    : {hidden: false}
        due_date   : {hidden: false}
        created_at : {hidden: false}
        subject_id : {hidden: false}
        description: {hidden: false}
      }
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch academic_tasks {
      field_name = "id"
      field_value = $input.academic_tasks_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $model
  }

  response = $model
  guid = "9oxGbnUbrRazUNghBxLcUn1fWQM"
}