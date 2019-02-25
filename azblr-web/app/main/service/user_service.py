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
    specialization_ids = data['specialization_ids']
    item_ids = data['item_ids']

    conn = db.connect()
    cursor = conn.cursor()
    sql = """
    insert into user_class (
        user_id, class_id, updated_datetime, created_datetime)
    values (
        %s, %s, now(), now())
    on duplicate key update
        updated_datetime = values(updated_datetime)
    """
    cursor.execute(sql, (user_id, class_id))
    user_class_id = cursor.lastrowid

    cursor.execute("delete from user_class_specialization where user_class_id = %s", (user_class_id,))
    sql = """
    insert into user_class_specialization (
        user_class_id, specialization_id, priority, created_datetime
    ) values (%s, %s, %s, now())
    """
    print([(user_class_id, val, idx) for idx, val in enumerate(specialization_ids)])
    cursor.executemany(sql, [(user_class_id, val, idx) for idx, val in enumerate(specialization_ids)])

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

def get_user_class(user_id, class_id):
    ret = {}

    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("select id from user_class where user_id = %s and class_id = %s", (user_id, class_id))
    row = cursor.fetchone()
    if row is not None:
        user_class_id = row[0]
        cursor.execute("select specialization_id from user_class_specialization where user_class_id = %s order by priority asc", (user_class_id,))
        sp_rows = cursor.fetchall()

        cursor.execute("select item_id from user_class_item where user_class_id = %s", (user_class_id,))
        item_rows = cursor.fetchall()

        ret['class_id'] = class_id
        ret['specialization_ids'] = [r[0] for r in sp_rows]
        ret['item_ids'] = [r[0] for r in item_rows]

    cursor.close()
    conn.close()
    return ret


# def get_all_users():
#     ret = []
#     conn = db.connect()
#     cursor = conn.cursor()

#     cursor.execute("select id, login_id, password, last_login, created_datetime from user")
#     rows = cursor.fetchall()
#     for row in rows:
#         r = {}
#         r['id'] = row[0]
#         r['login_id'] = row[1]
#         r['password'] = row[2]
#         r['last_login'] = row[3]
#         r['created_datetime'] = row[4]
#         ret.append(r)

#     conn.commit()
#     cursor.close()
#     conn.close()
#     return ret


# def get_a_user(login_id):
#     ret = {}

#     conn = db.connect()
#     cursor = conn.cursor()
#     cursor.execute("select id, login_id, password, last_login, created_datetime from user where login_id = %s", (login_id, ))
#     rows = cursor.fetchall()
#     if rows is not None and len():
#         ret['id'] = rows[0][0]
#         ret['login_id'] = rows[0][1]
#         ret['password'] = rows[0][2]
#         ret['last_login'] = rows[0][3]
#         ret['created_datetime'] = rows[0][4]

#     conn.commit()
#     cursor.close()
#     conn.close()
#     return ret