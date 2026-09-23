// Get a single subject by ID
query "subjects/{subject_id}" verb=GET {
  api_group = "Subjects"
  description = "Retrieve details of a single academic subject by its ID"

  input {
    int subject_id {
      description = "Unique identifier of the subject"
    }
  }

  stack {
    // Query subject record matching the provided ID
    db.query subject {
      where = $db.subject.id == $input.subject_id
      return = {type: "single"}
    } as $subject

    // Verify record exists
    precondition ($subject != null) {
      error_type = "notfound"
      error = "Subject not found."
    }
  }

  response = $subject
}

