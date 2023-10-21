from fastapi import FastAPI, HTTPException, Depends, Request, status
from db_utils import expire_session_for_user, get_user, add_user, get_user_by_session_id, log, add_session, valid_session
import models as model
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import configs as config
import random
from datetime import datetime, timedelta

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


def verify_through_session_id(request: Request):
    try:
        session_id = int(request.cookies.get("session_id"))
        if not valid_session(session_id):
            raise HTTPException(
                status_code=401,
                detail="Invalid session ID",
            )
        print(f"Getting user for {session_id}")
        user = get_user_by_session_id(session_id)
        return user
    except Exception as e:
        return None


def create_session(user: model.User):
    log("out", (user.id, user.username))
    session_id = random.randint(0, 1000000)
    session_id = add_session(model.Session(session_id=session_id, user_id=user.id, username=user.username,
                             created_at=datetime.now().timestamp(), valid_before=datetime.now().timestamp()+3600))
    return session_id


@app.get('/')
def index():
    return {"message": "Server is running"}


@app.get("/me")
def read_current_user(user: model.User = Depends(verify_through_session_id)):
    return user


@app.post("/login", response_model=dict)
def login(user: model.User = Depends(authenticate_user)):
    session_id = create_session(user)
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
def logout(verified=Depends(verify_through_session_id)):
    if not verified:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return expire_session_for_user(verified)
