// Delete a subject ensuring user ownership
// Delete a subject owned by the authenticated user
query "subjects/{id}" verb=DELETE {
  api_group = "Subjects"
  auth = "user"

  input {
    // ID of the subject to delete
    int id
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

  response = {
    success: true
    message: "Subject deleted successfully."
  }

  guid = "8EaxkMmzHM7yVS8zNpWZ2uqC89E"
}