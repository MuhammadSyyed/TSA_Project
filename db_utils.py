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

# Students Related Functions


def add_student(student: Student):
    try:
        conn = sqlite3.connect(configs.db_file)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO STUDENTS (CAMPUS_ID, NAME, ROLL_NO, BATCH, DATE_JOINED, IMAGE) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (student.campus_id,
             student.name,
             student.roll_no,
             student.batch,
             student.date_joined,
             student.image
             ))
        conn.commit()
        conn.close()
        return {"success": True, "message": "Student added successfully"}
    except sqlite3.IntegrityError:
        conn.commit()
        conn.close()
        return {"success": False, "message": "Student already exists"}


def update_student(student: UpdateStudent):
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
    main()
    # print(get_user(UserLogin(username="imranabbas", password="@dminsyed")))
    # print(update_user(UserUpdate(username="ibrahim",password="@syed",role="coo",id=3)))
    # print(delete_user(UserDelete(id=2)))
    # print(get_all_users())
    # print(get_student(Student()))
