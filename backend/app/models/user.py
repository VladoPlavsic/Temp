import string
from datetime import datetime
from typing import Optional, Any
from pydantic import EmailStr, constr, validator
from app.models.core import BaseModel
from app.models.token import AccessToken

# simple check for valid username
def validate_username(username: str) -> str:
    allowed = string.ascii_letters + string.digits + "-" + "_"
    assert all(char in allowed for char in username), "Invalid characters in username."
    assert len(username) >= 3, "Username must be 3 characters or more."
    return username

class UserBase(BaseModel):
    """
    Leaving off password and salt from base model
    """
    email: Optional[EmailStr]
    username: Optional[str]
    email_verified: bool = False
    is_active: bool = False
    is_superuser: bool = False

class UserCreate(BaseModel):
    """
    Email, username, and password are required for registering a new user
    """
    email: EmailStr
    password: constr(min_length=7, max_length=100)
    username: str
    full_name: str
    @validator("username", pre=True)
    def username_is_valid(cls, username: str) -> str:
        return validate_username(username)

class UserUpdate(BaseModel):
    """
    Users are allowed to update their email and/or username
    """
    email: Optional[EmailStr]
    username: Optional[str]
    @validator("username", pre=True)
    def username_is_valid(cls, username: str) -> str:
        return validate_username(username)    

class UserPasswordUpdate(BaseModel):
    """
    Users can change their password
    """
    password: constr(min_length=7, max_length=100)
    salt: str

class UserInDB(UserBase):
    """
    Add in id, created_at, updated_at, and user's password and salt
    """
    id: int
    password: constr(min_length=7, max_length=100)
    salt: str
    confirmation_code: Optional[str]
    jwt: Optional[str]

class PublicUserInDB(UserBase):
    id: int
    access_token: Optional[AccessToken]


# availble subjects/grades
class UserAvailableGrades(BaseModel):
    grade_id: int
    crated_at: Any
    updated_at: Any

class UserAvailableSubjects(BaseModel):
    subject_id: int
    created_at: datetime
    updated_at: datetime