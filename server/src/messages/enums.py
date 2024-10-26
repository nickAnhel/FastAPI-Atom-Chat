from enum import Enum


class MessagesOrder(str, Enum):
    ID = "message_id"
    CREATED_AT = "created_at"
