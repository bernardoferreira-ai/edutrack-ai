// Stores academic subjects and courses managed by users.
table subject {
  auth = false

  schema {
    int id
    timestamp created_at?=now

    // Reference to the user who owns this subject.
    int user_id? {
      table = "user"
    }

    // Name of the academic subject or course.
    text name filters=trim

    // Optional course code identifier (e.g., MAT101, CS50).
    text? code filters=trim

    // Optional name of the instructor or professor.
    text? professor filters=trim

    // Optional academic term or semester (e.g., 2026.1).
    text? semester filters=trim

    // Optional visual tag or hex color code.
    text? color filters=trim

    // Academic status of the subject.
    enum status? {
      values = ["active", "completed", "archived"]
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
}

