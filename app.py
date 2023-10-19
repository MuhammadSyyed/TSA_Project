from fastapi import FastAPI, HTTPException, Depends, Request, status
from db_utils import get_user, add_user, log
import models as model
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import configs as config
import random

app = FastAPI()


def authenticate_user(user_data: model.UserLogin):
    user = get_user(user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user


def get_user_from_session_id(request: Request):
    return config.sessions.get(int(request.cookies.get("session_id")))


def verify_through_session_id(request: Request):
    try:
        session_id = int(request.cookies.get("session_id"))
        print(session_id)
        if session_id not in config.sessions:
            raise HTTPException(
                status_code=401,
                detail="Invalid session ID",
            )
        user = get_user_from_session_id(request)
        return user
    except Exception as e:
        return None


def create_session(user_id: int):
    session_id = len(config.sessions) + random.randint(0, 1000000)
    config.sessions[session_id] = user_id
    return session_id


def get_session_id(request: Request):
    session_id = int(request.cookies.get("session_id"))
    if session_id is None or session_id not in config.sessions:
        raise HTTPException(status_code=401, detail="Invalid session ID")
    return session_id


@app.get('/')
def index():
    return {"message": "Server is running"}


@app.get("/me")
def read_current_user(user: model.User = Depends(get_user_from_session_id)):
    return user


@app.post("/login", response_model=dict)
def login(user: model.User = Depends(authenticate_user)):
    session_id = create_session(user.id)
    return {"message": "Logged in successfully", "session_id": session_id}


@app.post("/signup", response_model=dict)
def signup(user: model.UserCreate, verified=Depends(verify_through_session_id)):
    if not verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated")
    return add_user(user)


@app.post("/verify")
def check(verified=Depends(verify_through_session_id)):
    if not verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated")
    return {"message": "Authorized!"}


@app.post("/logout")
def logout(session_id: int = Depends(get_session_id)):
    if session_id not in config.sessions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    config.sessions.pop(session_id)
    return {"message": "Logged out successfully"}
