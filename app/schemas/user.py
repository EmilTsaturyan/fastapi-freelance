from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    username: str
    password: str


class UserUpdate(UserCreate):
    pass


class UserUpdatePartial(UserCreate):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserLogin(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    username: str

    class Config:
        from_attributes = True