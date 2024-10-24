from enum import Enum


class MessageOrder(str, Enum):
    ID = "message_id"
    CREATED_AT = "created_at"
