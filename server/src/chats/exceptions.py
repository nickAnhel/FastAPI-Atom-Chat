class ChatNotFound(Exception):
    """Raised when chat is not found"""


class PermissionDenied(Exception):
    """Raised when user does not have permission to perform action"""


class AlreadyInChat(Exception):
    """Raised when user is already in chat"""


class CantAddMembers(Exception):
    """Raised when cannot add members to chat"""
