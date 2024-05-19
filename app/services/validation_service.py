from app.models.expense import Expense
from app.models.revenue import Revenue
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
    if not validation_functions.is_valid_string(new_user.password):
        raise ValueError("Invalid user password")
    if not validation_functions.is_valid_email(new_user.email):
        raise ValueError("Invalid email")
    if not validation_functions.is_valid_israeli_id(new_user.id):
        raise ValueError("Invalid israeli id")
    if not validation_functions.is_valid_phone(new_user.phone):
        raise ValueError("Invalid phone")
    if not validation_functions.is_valid_birth_date(new_user.birth_date):
        raise ValueError("Invalid birthdate")
    return True


def is_valid_revenue(new_revenue: Revenue):
    """
    Validate if the revenue object is valid.
    Args:
        new_revenue (Revenue): The revenue object to validate.
    Returns:
        bool: True if the revenue object is valid, False otherwise.
    """
    if not validation_functions.is_valid_string(new_revenue.benefactor):
        raise ValueError("Invalid benefactor")
    if not validation_functions.is_valid_string(new_revenue.documentation):
        raise ValueError("Invalid documentation")
    if not validation_functions.is_valid_positive_number(new_revenue.amount):
        raise ValueError("Invalid amount")
    return True


def is_valid_expense(new_expense: Expense):
    """
    Validate if the expense object is valid.
    Args:
        new_expense (Expense): The expense object to validate.
    Returns:
        bool: True if the expense object is valid, False otherwise.
    """
    if not validation_functions.is_valid_string(new_expense.beneficiary):
        raise ValueError("Invalid beneficiary")
    if not validation_functions.is_valid_string(new_expense.documentation):
        raise ValueError("Invalid documentation")
    if not validation_functions.is_valid_positive_number(new_expense.amount):
        raise ValueError("Invalid amount")
    return True
