from flask import request
from flask_restplus import Resource

from ..util.dto import ItemDto
from ..service.item_info_service import get_item_info
from ..util.decorator import token_required

api = ItemDto.api

@api.route('/<item_id>')
@api.param('item_id', 'The Azerite Item ID')
class Item(Resource):
    @api.doc('get a azerite item information')
    def get(self, item_id):
        """get a azerite item given its identifier"""
        return get_item_info(item_id)