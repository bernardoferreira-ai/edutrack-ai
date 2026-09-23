// Delete an academic subject by ID
query "subjects/{subject_id}" verb=DELETE {
  api_group = "Subjects"
  description = "Delete an existing academic subject by ID"

  input {
    int subject_id {
      description = "Unique identifier of the subject to delete"
    }
  }

  stack {
    // Retrieve existing subject to ensure it exists and preserve it for response
    db.get subject {
      field_name = "id"
      field_value = $input.subject_id
    } as $subject

    // Verify record exists
    precondition ($subject != null) {
      error_type = "notfound"
      error = "Subject not found."
    }

    // Delete record from subject table
    db.del subject {
      field_name = "id"
      field_value = $input.subject_id
    }
  }

  response = $subject
}

