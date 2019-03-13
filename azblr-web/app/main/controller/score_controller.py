from flask import request
from flask_restplus import Resource

from ..util.dto import ScoreDto
from ..service.score_service import score

api = ScoreDto.api
_score = ScoreDto.score

@api.route('')
class Item(Resource):
    @api.doc('get classes and specialization meta data')
    @api.expect(_score)
    def post(self):
        """get a azerite item given its identifier"""
        return score(request.json)