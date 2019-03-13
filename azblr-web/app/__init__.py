from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.item_info_controller import api as item_ns
from .main.controller.meta_controller import api as meta_ns
from .main.controller.score_controller import api as score_ns

blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )

api.add_namespace(user_ns)
api.add_namespace(auth_ns)
api.add_namespace(item_ns)
api.add_namespace(meta_ns)
api.add_namespace(score_ns)