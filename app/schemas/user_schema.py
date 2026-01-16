from enum import unique
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime


class RoleResponse(BaseModel):
    id: int
    role_name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


# Base schema with common attributes
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    first_name: str = Field(..., min_length=2, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    phone_number: str = Field(..., min_length=11, max_length=20)
    phone_number2: Optional[str] = Field(None, min_length=11, max_length=20)
    role_id: int = Field(default=1)


# Schema for creating a user
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)


# Schema for updating a user
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    first_name: Optional[str] = Field(None, min_length=2, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone_number: Optional[str] = Field(None, min_length=11, max_length=20)
    phone_number2: Optional[str] = Field(None, min_length=11, max_length=20)
    password: Optional[str] = Field(None, min_length=8, max_length=100)
    role_id: Optional[int] = None
    is_active: Optional[bool] = None


# Schema for user response
class UserResponse(UserBase):
    id: int
    uuid: str
    is_active: bool
    created_on: datetime
    updated_on: datetime
    role: RoleResponse

    model_config = ConfigDict(from_attributes=True)


# Schema for user in database (internal use)
class UserInDB(UserResponse):
    hashed_password: str


class UserDetailResponse(UserResponse):
    deleted_on: Optional[datetime] = None
    deleted_by: Optional[int] = None
