from fastapi import FastAPI, HTTPException, Depends, Request, status, Form, Query, Body, File, UploadFile
from fastapi.templating import Jinja2Templates
from db_utils import *
import models as model
from fastapi.staticfiles import StaticFiles
import random
import json
from datetime import datetime
import pandas as pd
from configs import months
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
    return templates.TemplateResponse('form_user.html', context=context)


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

@app.get('/subject_details')
def subject_details(request: Request, subject_id: int, verified=Depends(verify_through_session_id)):
    subject = get_one_subject(subject_id)
    
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)
    
    context = {"request": request, "session_id": int(
        request.cookies.get("session_id")), "user": verified, "subject_id": subject.subject_id, "subject_name": subject.subject_name}
    
    return templates.TemplateResponse('subject_details.html', context=context)


@app.get('/monthly_subject_result')
def monthly_subject_result(request: Request, subject_id: int, verified=Depends(verify_through_session_id)):
    print("Aaleloa", '\n')
    subject = get_one_subject(subject_id)
    
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)
    
    context = {"request": request, "session_id": int(
        request.cookies.get("session_id")), "user": verified, "subject_id": subject.subject_id, "subject_name": subject.subject_name}
    
    return templates.TemplateResponse('monthly_subject_result.html', context=context)



@app.get('/subjects')
def subjects(request: Request, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)

    subjects = get_all_subjects()

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


@app.get('/edit_subject')
def edit_subject(request: Request, subject_id: int, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)
    subject_to_edit = get_one_subject(subject_id)
    context = {"request": request, "session_id": int(
        request.cookies.get("session_id")), "user": verified, 'subject_to_edit': subject_to_edit}
    return templates.TemplateResponse('edit_subject.html', context=context)


@app.post('/update_subject')
def update_subject(request: Request, subject: Subject, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)
    return update_and_save_subject(subject)

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


@app.get('/form_marks')
def form_marks(request: Request, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)

    students = get_all_students()
    subjects = get_all_subjects()
    context = {"request": request, "session_id": int(
        request.cookies.get("session_id")), "user": verified, "students": students, "subjects": subjects, "months": months, "year": datetime.today().year}
    return templates.TemplateResponse('form_marks.html', context=context)


@app.post('/add_marks')
def add_marks(request: Request, marks: MarksCreate, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)

    return add_new_marks(marks)


@app.post('/add_marks_via_sheet')
def add_students_via_sheet(request: Request, xlsxfile: UploadFile = File(...), verified=Depends(verify_through_session_id)):
    df = pd.read_excel(xlsxfile.file)

    for _, row in df.iterrows():
        subject_id = get_subject_id_by_name(row.iloc[0])
        student_id = get_student_id_by_name(row.iloc[1])
        new_student = MarksCreate(
            subject_id=subject_id,
            student_id=student_id,
            month=str(row.iloc[2]),
            marks_total=row.iloc[3],
            marks_obtained=row.iloc[4]
        )
        add_new_marks(new_student)

    return {"success": True, "message": "File Uploaded Successfully"}

# Student Related Routes


@app.get('/students')
def students(request: Request, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)
    all_students = get_all_students()
    context = {"request": request, "session_id": int(
        request.cookies.get("session_id")), "user": verified, "students": all_students}
    return templates.TemplateResponse('students.html', context=context)


@app.get('/form_student')
def form_student(request: Request, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)
    all_campuses = get_all_campuses()
    context = {"request": request, "session_id": int(
        request.cookies.get("session_id")), "user": verified, "campuses": all_campuses}
    return templates.TemplateResponse('form_student.html', context=context)


@app.post('/add_student')
def add_student(request: Request, student: StudentCreate, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)

    return add_new_student(student)


@app.post('/add_students_via_sheet')
def add_students_via_sheet(request: Request, xlsxfile: UploadFile = File(...), verified=Depends(verify_through_session_id)):
    df = pd.read_excel(xlsxfile.file)
    for _, row in df.iterrows():
        campus_id = get_campus_id_by_name(row.iloc[1])
        new_student = StudentCreate(student_name=row.iloc[0],
                                    campus_id=campus_id,
                                    roll_no=row.iloc[5],
                                    batch=row.iloc[6],
                                    date_joined=row.iloc[7],
                                    parent_name=row.iloc[2],
                                    parent_contact=row.iloc[3],
                                    group=row.iloc[4],
                                    last_class_percentage=row.iloc[9],
                                    reference=row.iloc[8])
        add_new_student(new_student)

    return {"success": True, "message": "File Uploaded Successfully"}

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


# Admission Related Routes

@app.get("/admissions")
def admissions(request: Request, verified=Depends(verify_through_session_id)):
    if not verified:
        context = {"request": request,
                   "message": "Unauthorized Access Denied!"}
        return templates.TemplateResponse('login.html', context=context)

    context = {"request": request, "session_id": int(
        request.cookies.get("session_id")), "user": verified}
    return templates.TemplateResponse('admissions.html', context=context)
