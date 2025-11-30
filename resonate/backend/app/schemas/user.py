from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    id: int
    email: EmailStr
    display_name: str | None = None
    subscription_status: str

    class Config:
        orm_mode = True
