import datetime
import jwt
from .. import flask_bcrypt
from ..config import key
from app.main import db


class Auth:

    @staticmethod
    def login_user(data):
        try:
            user = {}
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute("select id, login_id, password, last_login, created_datetime from user where login_id = %s", (data.get('login_id'), ))
            rows = cursor.fetchall()
            if len(rows) == 1:
                user['id'] = rows[0][0]
                user['login_id'] = rows[0][1]
                user['password'] = rows[0][2]
                user['last_login'] = rows[0][3]
                user['created_datetime'] = rows[0][4]

            if bool(user) and flask_bcrypt.check_password_hash(user['password'], data.get('password')):
                auth_token = Auth.generate_auth_token(user['id'])

                if auth_token:
                    cursor.execute("update user set last_login = now(), token = %s where id = %s", (auth_token.decode(), user['id']))

                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'Authorization': auth_token.decode()
                    }

                    conn.commit()
                    cursor.close()
                    conn.close()
                    return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'login id or password does not match.'
                }
                cursor.close()
                conn.close()
                return response_object, 401

        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, 500

    @staticmethod
    def logout_user(data):
        ####??? Bearer??
        # if data:
        #     auth_token = data.split(" ")[1]
        # else:
        #     auth_token = ''
        auth_token = data
        if auth_token:
            resp = Auth.decode_auth_token(auth_token)

            if not isinstance(resp, str):
                conn = db.connect()
                cursor = conn.cursor()
                cursor.execute("update user set token = null where id = %s", (resp, ))

                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged out.'
                }

                conn.commit()
                cursor.close()
                conn.close()
                return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403
    
    @staticmethod
    def generate_auth_token(id):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': id
        }

        return jwt.encode(
            payload,
            key,
            algorithm='HS256'
        )

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, key)
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute("select id from user where token = %s", (str(auth_token),))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            if len(rows) == 0 or payload['sub'] != rows[0][0]:
                raise jwt.InvalidTokenError
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
    

    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = Auth.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                conn = db.connect()
                cursor = conn.cursor()
                cursor.execute("select login_id, last_login, created_datetime from user where id = %s", (resp, ))
                rows = cursor.fetchall()
                
                response_object = {
                    'status': 'success',
                    'data': {
                        'login_id': rows[0][0],
                        'last_login': str(rows[0][1]),
                        'created_datetime': str(rows[0][2])
                    }
                }

                cursor.close()
                conn.close()
                return response_object, 200
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401