// List all academic subjects with optional status filter
query "subjects" verb=GET {
  api_group = "Subjects"
  description = "Retrieve all subjects, optionally filtered by status (e.g., active, completed, archived)"

  input {
    text? status {
      description = "Filter subjects by status (e.g., active, completed, archived)"
    }
  }

  stack {
    // Query subject table with optional status filtering
    db.query subject {
      where = $db.subject.status ==? $input.status
      return = {type: "list"}
    } as $subjects
  }

  response = $subjects
}

