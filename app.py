from fastapi import FastAPI, HTTPException, Depends, Request, status, Form
from fastapi.templating import Jinja2Templates
from db_utils import expire_session_for_user, get_user, add_user, get_user_by_session_id, log, add_session, valid_session
import models as model
from fastapi.staticfiles import StaticFiles
import random
from datetime import datetime
templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


def authenticate_user(username: str = Form(...), password: str = Form(...)):
    user_data = model.UserLogin(**{"username": username, "password": password})
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
    log("Session Created", (user.id, user.username))
    session_id = random.randint(0, 1000000)
    session_id = add_session(model.Session(session_id=session_id, user_id=user.id, username=user.username,
                             created_at=datetime.now().timestamp(), valid_before=datetime.now().timestamp()+3600))
    return session_id


@app.get('/')
def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("login.html", context=context)


@app.get("/me")
def read_current_user(user: model.User = Depends(verify_through_session_id)):
    return user


@app.post("/login", response_model=dict)
def login(request: Request, user: model.User = Depends(authenticate_user)):
    session_id = create_session(user)
    context = {"request": request, "session_id": session_id}
    return templates.TemplateResponse("dashboard.html", context=context)


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


@app.get("/logout")
def logout(request: Request, verified=Depends(verify_through_session_id)):

    if verified and expire_session_for_user(verified):
        context = {"request": request}
        return templates.TemplateResponse('login.html', context=context)
    else:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)


@app.get("/users")
def users(request: Request, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)
    context = {"request": request, "session_id": int(
        request.cookies.get("session_id"))}
    return templates.TemplateResponse('users.html', context=context)


@app.get("/dashboard")
def dashboard(request: Request, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)

    context = {"request": request, "session_id": int(
        request.cookies.get("session_id"))}
    return templates.TemplateResponse('dashboard.html', context=context)
