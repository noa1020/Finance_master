from app.models.user import User
from app.validation import validation_functions


def is_valid_user(new_user: User):
    """
    Validate if the user object is valid.
    Args:
        new_user (User): The user object to validate.
    Returns:
        bool: True if the user object is valid, False otherwise.
    """
    if not validation_functions.is_valid_string(new_user.user_name):
        raise ValueError("Invalid user name")
    if not validation_functions.is_valid_email(new_user.email):
        raise ValueError("Invalid email")
    if not validation_functions.is_valid_israeli_id(new_user.id):
        raise ValueError("Invalid israeli id")
    if not validation_functions.is_valid_phone(new_user.phone):
        raise ValueError("Invalid phone")
    if not validation_functions.is_valid_birth_date(new_user.birth_date):
        raise ValueError("Invalid birthdate")
    return True
