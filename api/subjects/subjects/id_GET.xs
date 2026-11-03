// Get a single subject by ID ensuring user ownership
// Retrieve a single subject if owned by the authenticated user
query "subjects/{id}" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
    // ID of the subject
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
  }

  response = $subject
  guid = "Q_AHJj7Nw6DNU4sP2Bjn10xamLU"
}