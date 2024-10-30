class CantUpdateMessage(Exception):
    """Raised when trying to update a message that belongs to another user or message does not exist"""


class CantDeleteMessage(Exception):
    """Raised can not delete message"""
