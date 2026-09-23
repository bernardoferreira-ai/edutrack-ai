// Update an existing academic subject
query "subjects/{subject_id}" verb=PATCH {
  api_group = "Subjects"
  description = "Update details or status of an existing academic subject by ID"

  input {
    int subject_id {
      description = "Unique identifier of the subject to update"
    }
    text? name filters=trim {
      description = "Updated name of the academic subject"
    }
    text? code filters=trim {
      description = "Updated course code identifier"
    }
    text? professor filters=trim {
      description = "Updated instructor or professor name"
    }
    text? semester filters=trim {
      description = "Updated academic term or semester"
    }
    text? color filters=trim {
      description = "Updated visual tag or hex color code"
    }
    text? status {
      description = "Updated academic status (active, completed, archived)"
    }
  }

  stack {
    // Retrieve existing subject to ensure it exists
    db.get subject {
      field_name = "id"
      field_value = $input.subject_id
    } as $subject

    // Verify record exists
    precondition ($subject != null) {
      error_type = "notfound"
      error = "Subject not found."
    }

    // Build update payload dynamically for partial update
    var $payload {
      value = {}
    }

    conditional {
      if ($input.name != null) {
        var.update $payload.name {
          value = $input.name
        }
      }
    }

    conditional {
      if ($input.code != null) {
        var.update $payload.code {
          value = $input.code
        }
      }
    }

    conditional {
      if ($input.professor != null) {
        var.update $payload.professor {
          value = $input.professor
        }
      }
    }

    conditional {
      if ($input.semester != null) {
        var.update $payload.semester {
          value = $input.semester
        }
      }
    }

    conditional {
      if ($input.color != null) {
        var.update $payload.color {
          value = $input.color
        }
      }
    }

    conditional {
      if ($input.status != null) {
        var.update $payload.status {
          value = $input.status
        }
      }
    }

    // Apply partial updates to the subject record
    db.patch subject {
      field_name = "id"
      field_value = $input.subject_id
      data = $payload
    } as $updated_subject
  }

  response = $updated_subject
}

