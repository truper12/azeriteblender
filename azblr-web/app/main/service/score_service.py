from app.main import db
from app.main.service.meta_service import get_inventory_types, get_fight_styles

def score(data):
    inventory_types = get_inventory_types()
    fight_styles = get_fight_styles()

    class_id = data['class_id']
    spcializations = data['specialiazations']
    items = data['item']


    return