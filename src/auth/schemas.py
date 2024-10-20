from pydantic import BaseModel, ConfigDict


class TokenBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Token(TokenBase):
    access_token: str
    token_type: str = "Bearer"
