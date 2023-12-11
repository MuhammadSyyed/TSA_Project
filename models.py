from pydantic import BaseModel
from enum import Enum
from datetime import date


class SessionCreate(BaseModel):
    user_id: int
    username: str
    created_at: float
    valid_before: float


class Session(SessionCreate):
    session_id: int


class UserRole(str, Enum):
    admin = "admin"
    coo = "COO"
    ci = "CI"
    master = "master"


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


class UserEdit(BaseModel):
    id: int
    username: str
    password: str
    role: UserRole


class UserLogin(BaseModel):
    username: str
    password: str

# Campus Related Models


class CampusCreate(BaseModel):
    campus_name: str
    address: str
    incharge: str
    admin: str
    coo: str
    head_eb: str
    contact_number: str


class Campus(CampusCreate):
    campus_id: int

class CampusDelete(BaseModel):
    campus_id:int


# Student Related Models


class StudentBase(BaseModel):
    campus_id: int
    name: str
    roll_no: str
    batch: str
    date_joined: date
    image: bytes


class Student(StudentBase):
    student_id: int


class UpdateStudent(StudentBase):
    STUDENT_ID: int
