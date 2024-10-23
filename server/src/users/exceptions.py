class UsernameAlreadyExists(Exception):
    """Raised when trying to create a user with an existing username"""


class UserNotFound(Exception):
    """Raised when trying to get, update or delete a user that does not exist"""
