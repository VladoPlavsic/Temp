def register_new_user_query(full_name, username, email, salt, password) -> str:
    return \
        f"SELECT (users.create_user_function('{full_name}', '{username}', '{email}', '{salt}', '{password}')).*"

def set_jwt_token_query(user_id, token) -> str:
    return \
        f"SELECT users.set_jwt_token({user_id}, '{token}')"

def verify_email_query(user_id) -> str:
    return \
        f"SELECT users.verify_email({user_id})"


def add_grade_to_user_query(user_id, grade_id, days) -> str:
    return \
        f"SELECT users.add_grade_to_user_function({user_id}, {grade_id}, {days})"

def add_subject_to_user_query(user_id, subject_id, days) -> str:
    return \
        f"SELECT users.add_subject_to_user_function({user_id}, {subject_id}, {days})"