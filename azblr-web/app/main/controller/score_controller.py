from flask import request
from flask_restplus import Resource

from ..util.dto import ScoreDto
from ..service.score_service import score

api = ScoreDto.api
_score = ScoreDto.score

@api.route('')
class Item(Resource):
    @api.doc('get scores')
    @api.expect(_score)
    def post(self):
        """get scores"""
        return score(request.json)