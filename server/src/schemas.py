from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Success(BaseModel):
    detail: str = "Successfully processed request"
