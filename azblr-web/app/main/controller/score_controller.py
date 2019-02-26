from flask import request
from flask_restplus import Resource

from ..util.dto import ScoreDto
from ..service.score_service import score

api = ScoreDto.api

@api.route('')
class Item(Resource):
    @api.doc('get classes and specialization meta data')
    def get(self):
        """get a azerite item given its identifier"""
        return score(request.json)