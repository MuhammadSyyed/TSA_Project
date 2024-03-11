import sqlite3
from models import *
import configs
import schemas
from datetime import datetime


# Sessions

def add_session(session: Session):
    try:
        conn = sqlite3.connect(configs.db_file)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) AS TOTAL  FROM SESSIONS')
        rows = cursor.fetchone()
        cursor.execute(
            "INSERT INTO SESSIONS (SESSION_ID, USER_ID, USERNAME, CREATED_AT, VALID_BEFORE) "
            "VALUES (?, ?, ?, ?, ?)",
            (session.session_id+int(rows["total"]),
             session.user_id,
             session.username,
             session.created_at,
             session.valid_before
             ))
        conn.commit()
        conn.close()
        return session.session_id+int(rows["total"])
    except sqlite3.IntegrityError:
        conn.commit()
        conn.close()
        return {"success": False, "Error": "Session Already Exists!"}


def valid_session(session_id: int):
    conn = sqlite3.connect(configs.db_file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM SESSIONS WHERE SESSION_ID = ? AND VALID_BEFORE  > ?', (session_id, datetime.now().timestamp()))
    valid_session = cursor.fetchone()
    conn.close()
    if valid_session:
        print(f"Session ID: {session_id} verified!")
        return True
    return False


def get_user_by_session_id(session_id: int):
    conn = sqlite3.connect(configs.db_file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        ''' SELECT
                USERS.*
            FROM
                USERS
            inner JOIN SESSIONS ON
                SESSIONS.USER_ID = USERS.ID
            WHERE
                SESSION_ID = ?''', (session_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        print(f"User Verfied {user}")
        user_data = {
            "id": user['id'],
            "username": user['username'],
            "role": UserRole(user['role'])
        }
        return User(**user_data)


def expire_session_for_user(user: User):
    try:
        conn = sqlite3.connect(configs.db_file)
        cursor = conn.cursor()
        cursor.execute('UPDATE SESSIONS SET VALID_BEFORE = ? WHERE USER_ID = ?',
                       (datetime.now().timestamp(), user.id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


# Utilities


def log(head, msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f'[{timestamp}] {head}\n{msg}\n'
    print(log_entry, end='')
    with open('logs.txt', 'a') as log_file:
        log_file.write(log_entry)


def create_table(conn, table_schema):
    cursor = conn.cursor()
    cursor.execute(table_schema)
    conn.commit()
    cursor.close()

# Users Related Functions


def add_new_user(user: UserCreate):
    try:
        conn = sqlite3.connect(configs.db_file)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO USERS (USERNAME, PASSWORD, ROLE) VALUES (?, ?, ?)',
                       (user.username, user.password, user.role))
        conn.commit()
        conn.close()
        return {"success": True, "message": "User added successfully"}
    except sqlite3.IntegrityError:
        conn.commit()
        conn.close()
        return {"success": False, "message": "Username already exists"}


def get_user(user: UserLogin):
    conn = sqlite3.connect(configs.db_file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM USERS WHERE USERNAME = ? AND PASSWORD = ?', (user.username, user.password))
    user = cursor.fetchone()
    conn.close()

    if user:
        user_data = {
            "id": user['id'],
            "username": user['username'],
            "role": UserRole(user['role'])
        }
        return User(**user_data)


def get_one_user(user_id: int):
    conn = sqlite3.connect(configs.db_file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM USERS WHERE ID = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        user_data = {
            "id": user['id'],
            "username": user['username'],
            "password": user['password'],
            "role": UserRole(user['role'])
        }
        return UserEdit(**user_data)


def get_all_users():
    conn = sqlite3.connect(configs.db_file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM USERS')
    all_users = cursor.fetchall()
    conn.close()

    if all_users:
        all_users = [User(**{
            "id": user['id'],
            "username": user['username'],
            "role": UserRole(user['role'])
        }) for user in all_users]
    return all_users


def update_and_save_user(user: UserUpdate):
    try:
        conn = sqlite3.connect(configs.db_file)
        cursor = conn.cursor()
        cursor.execute('UPDATE USERS SET USERNAME = ?, PASSWORD = ?, ROLE = ? WHERE ID = ?',
                       (user.username, user.password, user.role, user.id))
        conn.commit()
        conn.close()
        return {"success": True, "message": "User updated successfully"}
    except sqlite3.IntegrityError:
        conn.commit()
        conn.close()
        return {"success": False, "message": "Username already exists or the user doesn't exist"}


def delete_one_user(user: UserDelete):
    try:
        conn = sqlite3.connect(configs.db_file)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM USERS WHERE ID = ?',
                       (user.id,))
        conn.commit()
        conn.close()
        if cursor.rowcount == 1:
            return {"success": True, "message": "User deleted successfully"}
        else:
            return {"success": False, "message": "User not found"}
    except sqlite3.Error as e:
        return {"success": False, "message": "An error occurred while deleting the user: " + str(e)}

# Marks Related Functions


def add_new_marks(marks: MarksCreate):
    try:
        conn = sqlite3.connect(configs.db_file)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO MARKS (SUBJECT_ID,STUDENT_ID,MONTH,MARKS_TOTAL,MARKS_OBTAINED)"
            "VALUES (?,?,?,?,?)",
            (marks.subject_id,
             marks.student_id,
             marks.month,
             marks.marks_total,
             marks.marks_obtained
             ))
        conn.commit()
        conn.close()
        return {"success": True, "message": "Marks added successfully"}
    except sqlite3.IntegrityError:
        conn.commit()
        conn.close()
        return {"success": False, "message": "Marks already exists"}

def get_all_subject_months(subject_id:int):
    conn = sqlite3.connect(configs.db_file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(f"SELECT DISTINCT MONTH FROM MARKS WHERE SUBJECT_ID = ? ",(subject_id,))
    all_months = cursor.fetchall()
    conn.close()
    if all_months:
        print(all_months[0]['MONTH'])

    
    # print(all_months)

# Students Related Functions


def add_new_student(student: Student):
    try:
        conn = sqlite3.connect(configs.db_file)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO STUDENTS (STUDENT_NAME, CAMPUS_ID, ROLL_NO, BATCH, DATE_JOINED, PARENT_NAME,PARENT_CONTACT_NUMBER,'GROUP',LAST_CLASS_PERCENTAGE,REFERENCE) "
            "VALUES (?,?,?,?,?,?,?,?,?,?)",

            (student.student_name,
             student.campus_id,
             student.roll_no,
             student.batch,
             student.date_joined,
             student.parent_name,
             student.parent_contact,
             student.group,
             student.last_class_percentage,
             student.reference
             ))
        conn.commit()
        conn.close()
        return {"success": True, "message": "Student added successfully"}
    except sqlite3.IntegrityError:
        conn.commit()
        conn.close()
        return {"success": False, "message": "Student already exists"}


def update_student(student: Student):
    try:
        conn = sqlite3.connect(configs.db_file)
        cursor = conn.cursor()
        cursor.execute('UPDATE STUDENTS SET CAMPUS_ID = ?, NAME = ?, ROLL_NO = ? , BATCH = ?, DATE_JOINED = ? , IMAGE = ? WHERE ID = ?',
                       (student.CAMPUS_ID, student.NAME, student.ROLL_NO, student.BATCH, student.DATE_JOINED, student.IMAGE, student.STUDENT_ID))
        conn.commit()
        conn.close()
        return {"success": True, "message": "Student updated successfully"}
    except sqlite3.IntegrityError:
        conn.commit()
        conn.close()
        return {"success": False, "message": "Student already exists or the student doesn't exist"}


def get_student(student: Student):
    conn = sqlite3.connect(configs.db_file)
    conn.row_factory = sqlite3.row
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM STUDENTS WHERE ROLL_NO = ?', (student.ROLL_NO))
    student = cursor.fetchone()
    conn.close()

    if student:
        student_data = {'campus_id': student["campus_id"],
                        'name': student["name"],
                        'roll_no': student["roll_no"],
                        'batch': student["batch"],
                        'date_joined': student["date_joined"],
                        'image': student["image"]}
        return Student(**student_data)


def get_all_students():
    conn = sqlite3.connect(configs.db_file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM STUDENTS')
    all_students = cursor.fetchall()
    conn.close()

    if all_students:
        all_students = [Student(**{
            "student_id": student["student_id"],
            "student_name": student["student_name"],
            "campus_id": student["campus_id"],
            "roll_no": student["roll_no"],
            "batch": student["batch"],
            "date_joined": student["date_joined"],
            "parent_name": student["parent_name"],
            "parent_contact": student["parent_contact_number"],
            "group": student["group"],
            "last_class_percentage": student["last_class_percentage"],
            "reference": student["reference"]

        }) for student in all_students]
    return all_students


def get_student_id_by_name(student_name: str):
    conn = sqlite3.connect(configs.db_file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        'SELECT STUDENT_ID FROM STUDENTS WHERE STUDENT_NAME = ?', (student_name,))
    student = cursor.fetchone()
    conn.close()

    if student:
        return student['student_id']

# Campus Related Functions


def add_new_campus(campus: CampusCreate):
    try:

        conn = sqlite3.connect(configs.db_file)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO CAMPUS (CAMPUS_NAME,ADDRESS,CAMPUS_IN_CHARGE,ADMIN,COO,HEAD_EB,CONTACT_NUMBER) VALUES (?,?,?,?,?,?,?)',
                       (campus.campus_name,
                        campus.address,
                        campus.incharge,
                        campus.admin,
                        campus.coo,
                        campus.head_eb,
                        campus.contact_number))
        conn.commit()
        conn.close()
        return {"success": True, "message": "Campus added successfully"}
    except sqlite3.IntegrityError:
        conn.commit()
        conn.close()
        return {"success": False, "message": "Campus already exists"}


def update_and_save_campus(campus: Campus):
    try:
        conn = sqlite3.connect(configs.db_file)
        cursor = conn.cursor()
        cursor.execute('UPDATE CAMPUS SET CAMPUS_NAME = ?, ADDRESS = ?, CAMPUS_IN_CHARGE = ?, ADMIN = ?,COO = ?, HEAD_EB = ?, CONTACT_NUMBER = ? WHERE CAMPUS_ID = ?',
                       (
                           campus.campus_name,
                           campus.address,
                           campus.incharge,
                           campus.admin,
                           campus.coo,
                           campus.head_eb,
                           campus.contact_number,
                           campus.campus_id))
        conn.commit()
        conn.close()
        return {"success": True, "message": "Campus updated successfully"}
    except sqlite3.IntegrityError:
        conn.commit()
        conn.close()
        return {"success": False, "message": "Campus Name already exists or the campus doesn't exist"}


def get_all_campuses():
    conn = sqlite3.connect(configs.db_file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM CAMPUS')
    all_campuses = cursor.fetchall()
    conn.close()

    if all_campuses:
        all_campuses = [Campus(**{
            "campus_id": campus['campus_id'],
            "campus_name": campus['campus_name'],
            "address": campus['address'],
            "incharge": campus['campus_in_charge'],
            "admin": campus['admin'],
            "coo": campus['coo'],
            "head_eb": campus['head_eb'],
            "contact_number": campus['contact_number']

        }) for campus in all_campuses]
    return all_campuses


def delete_one_campus(campus: CampusDelete):
    try:
        conn = sqlite3.connect(configs.db_file)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM CAMPUS WHERE CAMPUS_ID = ?',
                       (campus.campus_id,))
        conn.commit()
        conn.close()
        if cursor.rowcount == 1:
            return {"success": True, "message": "Campus deleted successfully"}
        else:
            return {"success": False, "message": "Campus not found"}
    except sqlite3.Error as e:
        return {"success": False, "message": "An error occurred while deleting the campus: " + str(e)}


def get_one_campus(campus_id: int):
    conn = sqlite3.connect(configs.db_file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM CAMPUS WHERE CAMPUS_ID = ?', (campus_id,))
    campus = cursor.fetchone()
    conn.close()

    if campus:
        campus_dtl = {
            "campus_id": campus['campus_id'],
            "campus_name": campus['campus_name'],
            "address": campus['address'],
            "incharge": campus['campus_in_charge'],
            "admin": campus['admin'],
            "coo": campus['coo'],
            "head_eb": campus['head_eb'],
            "contact_number": campus['contact_number']

        }
        return Campus(**campus_dtl)


def get_campus_id_by_name(campus_name: str):
    conn = sqlite3.connect(configs.db_file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        'SELECT CAMPUS_ID FROM CAMPUS WHERE CAMPUS_NAME = ?', (campus_name,))
    campus = cursor.fetchone()
    conn.close()

    if campus:
        return campus['campus_id']

# Subject Related Functions


def get_all_subjects():
    conn = sqlite3.connect(configs.db_file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM SUBJECTS')
    all_subjects = cursor.fetchall()
    conn.close()

    if all_subjects:
        all_subjects = [Subject(**{
            "subject_id": subject['subject_id'],
            "subject_name": subject['subject_name'],
            "total_lecture_units": subject["total_lecture_units"]

        }) for subject in all_subjects]
    return all_subjects


def add_new_subject(subject: SubjectCreate):
    try:
        conn = sqlite3.connect(configs.db_file)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO SUBJECTS (SUBJECT_NAME, TOTAL_LECTURE_UNITS) VALUES (?, ?)',
                       (subject.subject_name, subject.total_lecture_units))
        conn.commit()
        conn.close()
        return {"success": True, "message": "Subject added successfully"}
    except sqlite3.IntegrityError:
        conn.commit()
        conn.close()
        return {"success": False, "message": "Subject already exists"}


def get_one_subject(subject_id: int):
    conn = sqlite3.connect(configs.db_file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM SUBJECTS WHERE SUBJECT_ID = ?', (subject_id,))
    subject = cursor.fetchone()
    conn.close()

    if subject:
        subject_dtl = {
            "subject_id": subject['subject_id'],
            "subject_name": subject['subject_name'],
            "total_lecture_units": subject['total_lecture_units']
        }
        return Subject(**subject_dtl)


def update_and_save_subject(subject: Subject):
    try:
        conn = sqlite3.connect(configs.db_file)
        cursor = conn.cursor()
        cursor.execute('UPDATE SUBJECTS SET SUBJECT_NAME = ?, TOTAL_LECTURE_UNITS = ? WHERE SUBJECT_ID = ?',
                       (
                           subject.subject_name,
                           subject.total_lecture_units,
                           subject.subject_id
                       ))

        return {"success": True, "message": "Subject updated successfully"}
    except sqlite3.IntegrityError:

        return {"success": False, "message": "Subject Name already exists or the subject doesn't exist"}
    finally:
        conn.commit()
        conn.close()


def get_subject_id_by_name(subject_name: str):
    conn = sqlite3.connect(configs.db_file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        'SELECT SUBJECT_ID FROM SUBJECTS WHERE SUBJECT_NAME = ?', (subject_name,))
    subject = cursor.fetchone()
    conn.close()

    if subject:
        return subject['subject_id']


def main():
    conn = sqlite3.connect('SystemDB.db')
    create_table(conn, schemas.users_schema)
    create_table(conn, schemas.student_schema)
    create_table(conn, schemas.campus_schema)
    create_table(conn, schemas.lecture_unit_schema)
    create_table(conn, schemas.marks_schema)
    create_table(conn, schemas.subject_schema)
    create_table(conn, schemas.subject_status_schema)
    create_table(conn, schemas.teachers_schema)
    create_table(conn, schemas.sessions_schema)


if __name__ == "__main__":
    pass
    # main()
    # print(get_user(UserLogin(username="imranabbas", password="@dminsyed")))
    # print(update_user(UserUpdate(username="ibrahim",password="@syed",role="coo",id=3)))
    # print(delete_user(UserDelete(id=2)))
    # print(get_all_users())
    # print(get_student(Student()))
    get_all_subject_months(1)