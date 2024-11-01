from enum import Enum


class EventType(str, Enum):
    CREATE = "created"
    JOIN = "joined"
    LEAVE = "leaved"
    ADD = "added"
    REMOVE = "removed"
