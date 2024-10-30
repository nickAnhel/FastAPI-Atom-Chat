from pydantic import BaseModel


class Success(BaseModel):
    detail: str = "Successfully processed request"
