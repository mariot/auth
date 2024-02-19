from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserCreate(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: int
    username: str
    is_active: bool | None = None


class UserInDB(User):
    hashed_password: str

    class Config:
        from_attributes = True
