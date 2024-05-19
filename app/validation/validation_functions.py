from datetime import datetime
import re


def is_valid_string(string: str):
    """
    Validate if the string is a valid alphanumeric string with special characters.
    Args:
        string (str): The string to validate.
    Returns:
        bool: True if the string is valid, False otherwise.
    """
    if not string or not string.strip():
        return False
    return bool(re.match(r'^[a-zA-Z0-9\s+\-\/\']+$', string))


def is_valid_email(email: str):
    """
    Validate if the string is a valid email address.
    Args:
        email (str): The email address to validate.
    Returns:
        bool: True if the email address is valid, False otherwise.
    """
    if not email or not email.strip():
        return False
    # Regular expression pattern for validating email addresses
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))


def is_valid_israeli_id(id_user: int) -> bool:
    """
    Validate if the number is a valid Israeli ID (Teudat Zehut).
    Args:
        id_user (int): The Israeli ID to validate.
    Returns:
        bool: True if the Israeli ID is valid, False otherwise.
    """
    id_str = str(id_user)
    if len(id_str) != 9:
        return False
    id_digits = [int(digit) for digit in id_str]

    def double_and_sum(digit: int) -> int:
        doubled = digit * 2
        return doubled if doubled < 10 else doubled - 9

    total = sum(id_digits[i] if i % 2 == 0 else double_and_sum(id_digits[i]) for i in range(8))
    check_digit = id_digits[-1]

    return (total + check_digit) % 10 == 0


def is_valid_phone(phone_number: str):
    """
    Validate if the string is a valid Israeli phone number (landline or mobile).
    Args:
        phone_number (str): The Israeli phone number to validate.
    Returns:
        bool: True if the phone number is valid, False otherwise.
    """
    if not phone_number or not phone_number.strip():
        return False
    if re.match(r'^0\d{0,2}-?\d{7}$', phone_number):  # Check for Israeli landline phone number
        return True
    if re.match(r'^05\d(-|\s)?\d{7}$', phone_number):  # Check for Israeli mobile phone number
        return True
    return False


def is_valid_birth_date(birth_date: datetime):
    """
    Validate if the birthdate is valid.
    Args:
        birth_date (datetime): The birthdate to validate.
    Returns:
        bool: True if the birthdate is valid, False otherwise.
    """
    return birth_date is not None and birth_date <= datetime.today()


def is_valid_positive_number(value):
    """
    Check if a value is a valid positive number.
    Args:
        value: The value to check.
    Returns:
        bool: True if the value is a valid positive number, False otherwise.
    """
    try:
        number = float(value)
        return number > 0
    except ValueError:
        return False
