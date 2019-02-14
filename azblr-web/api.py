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
            parser.add_argument('email', type=str)
            parser.add_argument('user_name', type=str)
            parser.add_argument('password', type=str)
            args = parser.parse_args()

            __userEmail = args['email']
            __userName = args['user_name']
            __userPassword = args['password']

            conn = mysql.connect()
            cursor = conn.cursor()
            # cursor.execute("insert into test (a, b) values (1, 'b')")

            conn.commit()
            cursor.close()
            conn.close()

            return {'status': '200', 'message': 'success'}
        except Exception as e:
            return {'error': str(e)}

api.add_resource(CreateUser, '/user')

if __name__ == '__main__':
    app.run(debug=True)