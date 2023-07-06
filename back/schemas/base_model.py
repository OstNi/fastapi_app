from pydantic import BaseModel


class PydanticBaseModel(BaseModel):
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
