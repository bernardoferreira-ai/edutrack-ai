// Create a new academic task for the authenticated user
// Create a new academic task verifying subject ownership and assigning user_id
query academic_tasks verb=POST {
  api_group = "Academic Tasks"
  auth = "user"

  input {
    // ID of the academic subject
    int subject_id
  
    // Title of the task
    text title filters=trim
  
    // Optional detailed description
    text? description filters=trim
  
    // Optional due date deadline
    date? due_date
  
    // Initial task status
    text? status?=pending filters=trim
  }

  stack {
    precondition ($input.title != null && $input.title != "") {
      error_type = "badrequest"
      error = "Task title is required."
    }
  
    // Verify that the referenced subject belongs to the authenticated user
    db.get subjects {
      field_name = "id"
      field_value = $input.subject_id
    } as $subject
  
    precondition ($subject != null && $subject.user_id == $auth.id) {
      error_type = "badrequest"
      error = "Invalid subject_id: subject not found or not owned by user."
    }
  
    db.add academic_tasks {
      data = {
        created_at : "now"
        user_id    : $auth.id
        subject_id : $input.subject_id
        title      : $input.title
        description: $input.description
        due_date   : $input.due_date
        status     : $input.status || "pending"
      }
    } as $new_task
  }

  response = $new_task
  guid = "iUI6XoF7h1_JLBHXZaZh-n-m6Rs"
}