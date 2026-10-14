// Stores student academic obligations (assignments, exams, projects) linked to subjects.
table academic_tasks {
  auth = false

  schema {
    int id
    timestamp created_at?=now

    // Reference to the user who owns this task.
    int user_id? {
      table = "user"
    }

    // Reference to the academic subject.
    int subject_id? {
      table = "subjects"
    }

    // Title of the academic task.
    text title filters=trim

    // Detailed description of the task.
    text? description filters=trim

    // Due date for the task.
    date? due_date

    // Current status of the task (e.g., pending, completed).
    text? status?="pending" filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
    {type: "btree", field: [{name: "subject_id", op: "asc"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
  guid = "5h3FtTIYHai0-mc7oH-sRecxUwU"
}

