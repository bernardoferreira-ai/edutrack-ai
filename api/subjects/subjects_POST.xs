// Create a new academic subject
// Create a new subject record owned by the authenticated user
query subjects verb=POST {
  api_group = "Subjects"
  auth = "user"

  input {
    // Mandatory name of the academic subject
    text name filters=trim
  
    // Optional instructor or teacher name
    text? teacher filters=trim
  
    // Optional workload hours
    int? hours filters=min:0
  }

  stack {
    precondition ($input.name != null && ($input.name|length) > 0) {
      error_type = "badrequest"
      error = "Subject name is required."
    }
  
    db.add subjects {
      data = {
        created_at: "now"
        user_id   : $auth.id
        name      : $input.name
        teacher   : $input.teacher
        hours     : $input.hours
      }
    } as $new_subject
  }

  response = $new_subject
  guid = "gOywh_lWjZPxpJYX4vZYpBzdDec"
}