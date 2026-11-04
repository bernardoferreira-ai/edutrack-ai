// Query all subjects records
query subjects verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
  }

  stack {
    db.query subjects {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "m6MN6BuPjkxc7SSrK1AY5_7Q3J0"
}