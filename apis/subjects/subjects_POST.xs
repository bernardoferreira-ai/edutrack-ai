// Create a new academic subject
query "subjects" verb=POST {
  api_group = "Subjects"
  description = "Create a new subject record with mandatory name and optional course details"

  input {
    text name filters=trim {
      description = "Mandatory name of the academic subject"
    }
    text? code filters=trim {
      description = "Optional course code identifier (e.g. MAT101, CS50)"
    }
    text? professor filters=trim {
      description = "Optional instructor or professor name"
    }
    text? semester filters=trim {
      description = "Optional academic term or semester (e.g. 2026.1)"
    }
    text? color filters=trim {
      description = "Optional visual tag or hex color code"
    }
    text? status?="active" {
      description = "Academic status of the subject (default: active)"
    }
  }

  stack {
    // Validate that name is non-empty after trimming
    precondition ($input.name != null && ($input.name|length) > 0) {
      error_type = "badrequest"
      error = "Subject name is required."
    }

    // Add record to subject table
    db.add subject {
      data = {
        created_at: "now"
        name      : $input.name
        code      : $input.code
        professor : $input.professor
        semester  : $input.semester
        color     : $input.color
        status    : $input.status || "active"
      }
    } as $new_subject
  }

  response = $new_subject
}

