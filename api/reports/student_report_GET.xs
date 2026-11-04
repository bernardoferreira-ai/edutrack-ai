// Generates and downloads student academic performance report
// Get academic performance report data for the authenticated student
query student_report verb=GET {
  api_group = "Reports"
  auth = "user"

  input {
  }

  stack {
    // Query all academic subjects belonging to the authenticated student
    db.query subjects {
      where = $db.subjects.user_id == $auth.id
      return = {type: "list"}
    } as $user_subjects

    // Query all academic tasks belonging to the authenticated student
    db.query academic_tasks {
      where = $db.academic_tasks.user_id == $auth.id
      return = {type: "list"}
    } as $user_tasks
  }

  response = {
    user_id: $auth.id,
    generated_at: "now",
    subjects: $user_subjects,
    tasks: $user_tasks
  }
  guid = "Qry_Student_Report_Get_01"
}

