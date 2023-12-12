from fastapi import FastAPI, HTTPException, Depends, Request, status, Form, Query, Body
from fastapi.templating import Jinja2Templates
from db_utils import *
import models as model
from fastapi.staticfiles import StaticFiles
import random
import json
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
        context = {"request": request, "session_id": session_id, "user": user}
        return templates.TemplateResponse("dashboard.html", context=context)
    else:
        context = {"request": request, "message": "Wrong Credentials!"}
        return templates.TemplateResponse("login.html", context=context)


@app.post("/signup", response_model=dict)
async def signup(request: Request, user: model.UserCreate, verified=Depends(verify_through_session_id)):

    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)
    return add_new_user(user)


@app.get("/verify")
def check(request: Request, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)
    return {"sucess": True, "message": "Authorized!"}


@app.get("/logout")
def logout(request: Request, verified=Depends(verify_through_session_id)):

    if verified and expire_session_for_user(verified):
        context = {"request": request, "message": "Logged out successfully!"}
        return templates.TemplateResponse('login.html', context=context)
    else:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)

# User Related Routes


@app.get("/users")
def users(request: Request, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)
    users = get_all_users()
    context = {"request": request, "session_id": int(
        request.cookies.get("session_id")), "user": verified, "users": users}
    return templates.TemplateResponse('users.html', context=context)


@app.get("/dashboard")
def dashboard(request: Request, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)

    context = {"request": request, "session_id": int(
        request.cookies.get("session_id")), "user": verified}
    return templates.TemplateResponse('dashboard.html', context=context)


@app.get("/add_user")
def add_user(request: Request, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)

    context = {"request": request, "session_id": int(
        request.cookies.get("session_id")), "user": verified}
    return templates.TemplateResponse('add_user.html', context=context)


@app.get("/edit_user")
def edit_user(request: Request, id: int, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)
    user_to_edit = get_one_user(id)

    context = {"request": request, "session_id": int(
        request.cookies.get("session_id")), "user": verified, 'user_to_edit': user_to_edit}
    return templates.TemplateResponse('edit_user.html', context=context)


@app.post("/update_user")
def update_user(request: Request, user: UserUpdate, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)
    return update_and_save_user(user)


@app.post('/delete_user')
def delete_user(request: Request, user: UserDelete, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)
    return delete_one_user(user)

# Subject Related Routes


@app.get('/subjects')
def subjects(request: Request, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)

    subjects = get_all_subjects()
    print(subjects)

    context = {"request": request, "session_id": int(
        request.cookies.get("session_id")), "user": verified, "subjects": subjects}
    return templates.TemplateResponse('subjects.html', context=context)


@app.get('/form_subject')
def form_subject(request: Request, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)

    context = {"request": request, "session_id": int(
        request.cookies.get("session_id")), "user": verified}
    return templates.TemplateResponse('form_subject.html', context=context)


@app.post('/add_subject')
def add_subject(request: Request, subject: SubjectCreate, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)
    return add_new_subject(subject)

# Results Related Routes


@app.get('/results')
def results(request: Request, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)
    context = {"request": request, "session_id": int(
        request.cookies.get("session_id")), "user": verified}
    return templates.TemplateResponse('results.html', context=context)

# Examination Board Related Routes


@app.get('/examination_board')
def examination_board(request: Request, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)
    context = {"request": request, "session_id": int(
        request.cookies.get("session_id")), "user": verified}
    return templates.TemplateResponse('examination_board.html', context=context)


@app.get('/add_marks')
def add_mark(request: Request, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)
    context = {"request": request, "session_id": int(
        request.cookies.get("session_id")), "user": verified}
    return templates.TemplateResponse('add_marks.html', context=context)


# Student Related Routes

@app.get('/students')
def students(request: Request, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)
    context = {"request": request, "session_id": int(
        request.cookies.get("session_id")), "user": verified}
    return templates.TemplateResponse('students.html', context=context)


# Campuses Related Routes

@app.get('/campuses')
def campuses(request: Request, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)

    campuses = get_all_campuses()
    context = {"request": request, "session_id": int(
        request.cookies.get("session_id")), "user": verified, "campuses": campuses}
    return templates.TemplateResponse('campuses.html', context=context)


@app.get("/form_campus")
def form_campus(request: Request, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)

    context = {"request": request, "session_id": int(
        request.cookies.get("session_id")), "user": verified}
    return templates.TemplateResponse('form_campus.html', context=context)


@app.post("/add_campus", response_model=dict)
def add_campus(request: Request, campus: CampusCreate, verified=Depends(verify_through_session_id)):

    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)
    print(campus)
    return add_new_campus(campus)


@app.get("/edit_campus")
def edit_campus(request: Request, campus_id: int, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)
    campus_to_edit = get_one_campus(campus_id)

    context = {"request": request, "session_id": int(
        request.cookies.get("session_id")), "user": verified, 'campus_to_edit': campus_to_edit}
    return templates.TemplateResponse('edit_campus.html', context=context)


@app.post("/update_campus")
def update_campus(request: Request, campus: Campus, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)
    return update_and_save_campus(campus)


@app.post("/delete_campus")
def delete_campus(request: Request, campus: CampusDelete, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)
    return delete_one_campus(campus)
