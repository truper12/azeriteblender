import uuid
import datetime
from .. import flask_bcrypt
from app.main.service.auth_helper import Auth
from app.main import db

def save_new_user(data):
    conn = db.connect()
    cursor = conn.cursor()

    cursor.execute("select id from user where login_id=%s", (data['login_id'], ))
    rows = cursor.fetchall()
    if len(rows) == 0:
        hashed_password = flask_bcrypt.generate_password_hash(data['password']).decode('utf-8')
        cursor.execute("insert into user (login_id, password, created_datetime) values (%s, %s, now())", (data['login_id'], hashed_password, ))
        cursor.execute("select id from user where login_id = %s", (data['login_id'],))
        rows = cursor.fetchall()
        
        user_id = rows[0][0]
        auth_token = Auth.generate_auth_token(user_id)
        cursor.execute("update user set token = %s, last_login = now() where id=%s", (auth_token.decode(), user_id,))
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
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

def save_user_class(user_id, data):
    class_id = data['class_id']
    specialization_id = data['specialization_id']
    item_ids = data['item_ids']

    conn = db.connect()
    cursor = conn.cursor()
    sql = """
    insert into user_class (
        user_id, class_id, specialization_id, updated_datetime, created_datetime)
    values (
        %s, %s, %s, now(), now())
    on duplicate key update
        updated_datetime = values(updated_datetime)
    """
    cursor.execute(sql, (user_id, class_id, specialization_id))
    user_class_id = cursor.lastrowid

    cursor.execute("delete from user_class_item where user_class_id = %s", (user_class_id,))
    sql = """
    insert into user_class_item (
        user_class_id, item_id, created_datetime
    ) values (%s, %s, now())
    """
    cursor.executemany(sql, [(user_class_id, val) for val in item_ids])
    
    response_object = {
        'status': 'success',
        'message': 'Successfully saved.'
    }

    conn.commit()
    cursor.close()
    conn.close()
    return response_object, 200

def get_user_class(user_id, class_id, specialization_id):
    ret = {}

    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("select id from user_class where user_id = %s and class_id = %s and specialization_id = %s", (user_id, class_id, specialization_id))
    row = cursor.fetchone()
    if row is not None:
        user_class_id = row[0]

        cursor.execute("select item_id from user_class_item where user_class_id = %s", (user_class_id,))
        item_rows = cursor.fetchall()

        ret['class_id'] = class_id
        ret['specialization_id'] = specialization_id
        ret['item_ids'] = [r[0] for r in item_rows]

    cursor.close()
    conn.close()
    return ret