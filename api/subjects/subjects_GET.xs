// List all subjects belonging to the authenticated user
query "subjects" verb=GET {
  api_group = "Subjects"
  auth = "user"
  description = "List all academic subjects for the authenticated user"

  input {
  }

  stack {
    db.query subjects {
      where = $db.subjects.user_id == $auth.id
      return = {type: "list"}
    } as $user_subjects
  }

  response = $user_subjects
  guid = "l0bGxFxTGGqCubzbgLE01za3S28"
}

