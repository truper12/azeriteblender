from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flaskext.mysql import MySQL
from config import Config

app = Flask(__name__)
api = Api(app)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = Config.DATABASE_USER
app.config['MYSQL_DATABASE_PASSWORD'] = Config.DATABASE_PASSWORD
app.config['MYSQL_DATABASE_DB'] = Config.DATABASE_DB
app.config['MYSQL_DATABASE_HOST'] = Config.DATABASE_HOST
app.config['MYSQL_DATABASE_PORT'] = Config.DATABASE_PORT
mysql.init_app(app)

class CreateUser(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('login_id', type=str)
            parser.add_argument('password', type=str)
            args = parser.parse_args()

            __loginId = args['login_id']
            __password = args['password']

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute("insert into user (login_id, password, created_datetime) values (%s, %s, now())", (__loginId, __password))

            conn.commit()
            cursor.close()
            conn.close()

            return {'status': '200', 'message': 'success'}
        except Exception as e:
            return {'error': str(e)}

api.add_resource(CreateUser, '/user')

if __name__ == '__main__':
    app.run(debug=True)