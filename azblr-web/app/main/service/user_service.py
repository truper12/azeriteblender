import uuid
import datetime
from .. import flask_bcrypt
from app.main import db

def save_new_user(data):
    conn = db.connect()
    cursor = conn.cursor()

    cursor.execute("select id from user where login_id=%s", (data['login_id'], ))
    rows = cursor.fetchall()
    if len(rows) == 0:
        hashed_password = flask_bcrypt.generate_password_hash(data['password']).decode('utf-8')
        cursor.execute("insert into user (login_id, password, created_datetime) values (%s, %s, now())", (data['login_id'], hashed_password, ))
        
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }

        conn.commit()
        cursor.close()
        conn.close()
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }

        cursor.close()
        conn.close()
        return response_object, 409

def get_all_users():
    ret = []
    conn = db.connect()
    cursor = conn.cursor()

    cursor.execute("select id, login_id, password, created_datetime from user")
    rows = cursor.fetchall()
    for row in rows:
        r = {}
        r['id'] = row[0]
        r['login_id'] = row[1]
        r['password'] = row[2]
        r['created_datetime'] = row[3]
        ret.append(r)

    conn.commit()
    cursor.close()
    conn.close()
    return ret


def get_a_user(login_id):
    ret = {}

    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("select id, login_id, password, created_datetime from user where login_id = %s", (login_id, ))
    rows = cursor.fetchall()
    if rows is not None and len():
        ret['id'] = rows[0][0]
        ret['login_id'] = rows[0][1]
        ret['password'] = rows[0][2]
        ret['created_datetime'] = rows[0][3]

    conn.commit()
    cursor.close()
    conn.close()
    return ret