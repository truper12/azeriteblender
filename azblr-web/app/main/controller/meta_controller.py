from flask import request
from flask_restplus import Resource

from ..util.dto import MetaDto
from ..service.meta_service import get_available_class_specializations

api = MetaDto.api

@api.route('/class')
class Item(Resource):
    @api.doc('get classes and specialization meta data')
    def get(self):
        """get a azerite item given its identifier"""
        return get_available_class_specializations()