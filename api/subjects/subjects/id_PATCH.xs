// Update an existing subject ensuring user ownership
// Update subject attributes for an owned record
query "subjects/{id}" verb=PATCH {
  api_group = "Subjects"
  auth = "user"

  input {
    // ID of the subject to update
    int id
  
    // Updated subject name
    text? name filters=trim
  
    // Updated teacher name
    text? teacher filters=trim
  
    // Updated workload hours
    int? hours filters=min:0
  }

  stack {
    db.get subjects {
      field_name = "id"
      field_value = $input.id
    } as $subject
  
    precondition ($subject != null && $subject.user_id == $auth.id) {
      error_type = "notfound"
      error = "Subject not found."
    }
  
    db.edit subjects {
      field_name = "id"
      field_value = $input.id
      data = {
        name   : $input.name || $subject.name
        teacher: $input.teacher || $subject.teacher
        hours  : $input.hours || $subject.hours
      }
    } as $updated_subject
  }

  response = $updated_subject
  guid = "bTEjlVXc2UxtOUhCsvtlHwACsaA"
}