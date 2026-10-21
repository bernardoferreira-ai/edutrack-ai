// Create a new academic subject
query "subjects" verb=POST {
  api_group = "Subjects"
  auth = "user"
  description = "Create a new subject record owned by the authenticated user"

  input {
    text name filters=trim {
      description = "Mandatory name of the academic subject"
    }
    text? teacher filters=trim {
      description = "Optional instructor or teacher name"
    }
    int? hours filters=min:0 {
      description = "Optional workload hours"
    }
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

