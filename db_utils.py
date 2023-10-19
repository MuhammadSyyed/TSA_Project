import sqlite3
from models import *
import configs
import schemas
import datetime

# Utilities


def log(head, msg):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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

def add_user(user: UserCreate):
    try:
        conn = sqlite3.connect(configs.db_file)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO USERS (USERNAME, PASSWORD, ROLE) VALUES (?, ?, ?)',
                       (user.username, user.password, user.role))
        conn.commit()
        conn.close()
        return {"message": "User added successfully"}
    except sqlite3.IntegrityError:
        return {"Error": "Username already exists"}


def get_user(user: UserLogin):
    conn = sqlite3.connect(configs.db_file)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM USERS WHERE USERNAME = ? AND PASSWORD = ?', (user.username, user.password))
    row = cursor.fetchone()
    conn.close()

    if row:
        user_data = {
            "id": row[0],
            "username": row[1],
            "role": UserRole(row[3])
        }
        return User(**user_data)


def get_all_users():
    conn = sqlite3.connect(configs.db_file)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM USERS')
    all_users = cursor.fetchall()
    conn.close()

    if all_users:
        all_users = [User(**{
            "id": user[0],
            "username": user[1],
            "role": UserRole(user[3])
        }) for user in all_users]
    return all_users


def update_user(user:UserUpdate):
    try:
        conn = sqlite3.connect(configs.db_file)
        cursor = conn.cursor()
        cursor.execute('UPDATE USERS SET USERNAME = ?, PASSWORD = ?, ROLE = ? WHERE ID = ?',
                       (user.username, user.password, user.role, user.id))
        conn.commit()
        conn.close()
        return {"message": "User updated successfully"}
    except sqlite3.IntegrityError:
        return {"error": "Username already exists or the user doesn't exist"}


def delete_user(user: UserDelete):
    try:
        conn = sqlite3.connect(configs.db_file)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM USERS WHERE ID = ?',
                       (user.id,))
        conn.commit()
        conn.close()
        if cursor.rowcount == 1:
            return {"message": "User deleted successfully"}
        else:
            return {"error": "User not found"}
    except sqlite3.Error as e:
        return {"error": "An error occurred while deleting the user: " + str(e)}

# Students Related Functions

def add_student(student: Student):
    try:
        conn = sqlite3.connect(configs.db_file)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO STUDENTS (CAMPUS_ID, NAME, ROLL_NO, BATCH, DATE_JOINED, IMAGE) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (student.CAMPUS_ID,
             student.NAME,
             student.ROLL_NO,
             student.BATCH,
             student.DATE_JOINED,
             student.IMAGE
             ))
        conn.commit()
        conn.close()
        return {"message": "Student added successfully"}
    except sqlite3.IntegrityError:
        return {"Error": "Student already exists"}


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


if __name__ == "__main__":
    pass
    # main()
    # print(get_user(UserLogin(username="imranabbas", password="@dminsyed")))
    # print(update_user(UserUpdate(username="ibrahim",password="@syed",role="coo",id=3)))
    # print(delete_user(UserDelete(id=2)))
    # print(get_all_users())
