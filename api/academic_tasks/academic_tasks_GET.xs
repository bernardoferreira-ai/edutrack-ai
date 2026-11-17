// Query all academic_tasks records
query academic_tasks verb=GET {
  api_group = "Academic Tasks"
  auth = "user"

  input {
  }

  stack {
    db.query academic_tasks {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "uogfgLR7-sQ6g-mBohP9MFAEeMg"
}