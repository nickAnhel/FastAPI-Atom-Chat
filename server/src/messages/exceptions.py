class CantUpdateMessage(Exception):
    """Raised when trying to update a message that belongs to another user or message does not exist"""
