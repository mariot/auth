from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str


class UserCreateResponse(BaseModel):
    token: str


class User(BaseModel):
    id: int
    username: str
    token: str
    is_active: bool

    class Config:
        from_attributes = True
