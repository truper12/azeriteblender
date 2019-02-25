from flask import request
from flask_restplus import Resource

from ..util.dto import ItemDto
from ..service.item_info_service import get_item_info, get_item_info_with_spell
from ..util.decorator import token_required

api = ItemDto.api

@api.route('/<item_id>')
@api.param('item_id', 'The Azerite Item ID')
class Item(Resource):
    @api.doc('get a azerite item information')
    def get(self, item_id):
        """get a azerite item given its identifier"""
        return get_item_info(item_id)

@api.route('/<item_id>/class/<class_id>')
@api.param('item_id', 'The Azerite Item ID')
@api.param('class_id', 'Class ID')
class ItemClass(Resource):
    @api.doc('get a azerite item information with class power detailed')
    def get(self, item_id, class_id):
        return get_item_info_with_spell(item_id, class_id)