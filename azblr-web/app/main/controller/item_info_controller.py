from flask import request
from flask_restplus import Resource

from ..util.dto import ItemDto
from ..service.item_info_service import get_item_info_with_spell, get_item_info_with_spell_by_name

api = ItemDto.api
_item_name = ItemDto.item_name

@api.route('/<item_id>/class/<class_id>')
@api.param('item_id', 'The Azerite Item ID')
@api.param('class_id', 'Class ID')
class ItemClass(Resource):
    @api.doc('get a azerite item information with class power detailed')
    def get(self, item_id, class_id):
        """get a azerite item with azerite power details of the given class id"""
        return get_item_info_with_spell(item_id, class_id)

@api.route('/class/<class_id>')
# @api.param('item_name', 'The Azerite Item ID')
@api.param('class_id', 'Class ID')
class ItemClassByName(Resource):
    @api.doc('get a azerite item information with class power detailed')
    @api.expect(_item_name)
    def post(self, class_id):
        """get a azerite item with azerite power details of the given class id"""
        return get_item_info_with_spell_by_name(request.json['item_name'], class_id)