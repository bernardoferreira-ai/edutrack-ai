// Stores academic subjects with instructor and workload details.
table subjects {
  auth = false

  schema {
    int id
    timestamp created_at?=now

    // Reference to the user who owns this subject.
    int user_id? {
      table = "user"
    }

    // Mandatory course/subject name.
    text name filters=trim

    // Instructor or professor name.
    text? teacher filters=trim

    // Workload hours.
    int? hours filters=min:0
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
}

