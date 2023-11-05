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
    return user


def verify_through_session_id(request: Request):
    try:
        session_id = int(request.cookies.get("session_id"))
        if not valid_session(session_id):
            return None
        print(f"Getting user for {session_id}")
        return get_user_by_session_id(session_id)

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
    context = {"request": request, "message": "login"}
    return templates.TemplateResponse("login.html", context=context)


@app.get("/me")
def read_current_user(request: Request, verified=Depends(verify_through_session_id)):
    if verified:
        return verified


@app.post("/login", response_model=dict)
def login(request: Request, user: model.User = Depends(authenticate_user)):
    if user:
        session_id = create_session(user)
        context = {"request": request, "session_id": session_id,"user":user}
        return templates.TemplateResponse("dashboard.html", context=context)
    else:
        context = {"request": request, "message":"Wrong Credentials!"}
        return templates.TemplateResponse("login.html",context=context)


@app.post("/signup", response_model=dict)
def signup(request: Request, user: model.UserCreate, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)
    return add_user(user)


@app.get("/verify")
def check(request: Request, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)
    return {"message": "Authorized!"}


@app.get("/logout")
def logout(request: Request, verified=Depends(verify_through_session_id)):

    if verified and expire_session_for_user(verified):
        context = {"request": request, "message": "Logged out successfully!"}
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
        request.cookies.get("session_id")),"user":verified}
    return templates.TemplateResponse('users.html', context=context)


@app.get("/dashboard")
def dashboard(request: Request, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)

    context = {"request": request, "session_id": int(
        request.cookies.get("session_id")),"user":verified}
    return templates.TemplateResponse('dashboard.html', context=context)
