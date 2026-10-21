// Update an existing subject ensuring user ownership
query "subjects/{id}" verb=PATCH {
  api_group = "Subjects"
  auth = "user"
  description = "Update subject attributes for an owned record"

  input {
    int id {
      description = "ID of the subject to update"
    }
    text? name filters=trim {
      description = "Updated subject name"
    }
    text? teacher filters=trim {
      description = "Updated teacher name"
    }
    int? hours filters=min:0 {
      description = "Updated workload hours"
    }
  }

  stack {
    db.get subjects {
      field_name = "id"
      field_value = $input.id
    } as $subject

    precondition ($subject != null && $subject.user_id == $auth.id) {
      error_type = "notfound"
      error = "Subject not found."
    }

    db.edit subjects {
      field_name = "id"
      field_value = $input.id
      data = {
        name   : $input.name || $subject.name
        teacher: $input.teacher || $subject.teacher
        hours  : $input.hours || $subject.hours
      }
    } as $updated_subject
  }

  response = $updated_subject
  guid = "bTEjlVXc2UxtOUhCsvtlHwACsaA"
}

