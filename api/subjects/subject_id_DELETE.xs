// Delete a subject ensuring user ownership
query "subjects/{id}" verb=DELETE {
  api_group = "Subjects"
  auth = "user"
  description = "Delete a subject owned by the authenticated user"

  input {
    int id {
      description = "ID of the subject to delete"
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

    db.del subjects {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {success: true, message: "Subject deleted successfully."}
  guid = "8EaxkMmzHM7yVS8zNpWZ2uqC89E"
}

