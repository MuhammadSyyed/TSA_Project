from pydantic import BaseModel
from enum import Enum
from datetime import date


class UserRole(str, Enum):
    admin = "admin"
    coo = "coo"
    ci = "CI"


class UserBase(BaseModel):
    username: str
    role: UserRole


class UserCreate(UserBase):
    password: str


class UserUpdate(UserCreate):
    id: int


class User(UserBase):
    id: int


class UserDelete(BaseModel):
    id: int


class UserLogin(BaseModel):
    username: str
    password: str


class StudentBase(BaseModel):
    CAMPUS_ID: int
    NAME: str
    ROLL_NO: str
    BATCH: str
    DATE_JOINED: date  # Assuming you want to use datetime.date for date values
    IMAGE: bytes


class Student(StudentBase):
    STUDENT_ID: int
