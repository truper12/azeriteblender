from app.main import db
from app.main.service.meta_service import get_inventory_types, get_fight_styles
from itertools import product

def score(data):
    inventory_types = get_inventory_types()
    fight_styles = get_fight_styles()

    conn = db.connect()
    cursor = conn.cursor()

    class_id = data['class_id']
    specialization_id = data['specialization_id']
    items = data['items']
    grouped_items = {}
    for item in items:
        grouped_powers = {}
        cursor.execute("select id from crawler where class_id = %s and specialization_id = %s", (class_id, specialization_id))
        crawer_ids = [r[0] for r in cursor]
        for azeritePower in item['azeritePowers']:
            sql = "select sub_spell_name, sub_spell_id from crawler_score where crawler_id in "+str(tuple(crawer_ids))+" and spell_id = %s group by sub_spell_name"
            cursor.execute(sql, azeritePower['spellId'])
            for r in cursor:
                power = {'spellId': azeritePower['spellId'], 'spellName': azeritePower['spellName'], 'subSpellName': r[0], 'subSpellId': r[1], 'tier': azeritePower['tier']}
                if azeritePower['tier'] in grouped_powers:
                    grouped_powers[azeritePower['tier']].append(power)
                else:
                    grouped_powers[azeritePower['tier']] = [power,]
        
        item['groupedPowers'] = grouped_powers
        
        if item['inventoryType'] in grouped_items:
            grouped_items[item['inventoryType']].append(item)
        else:
            grouped_items[item['inventoryType']] = [item,]
        
        del item['azeritePowers'] ###
    
    for p_items in product(*grouped_items.values()):
        for p_powers in product(*[p['groupedPowers'].values() for p in p_items]):
            print(p_powers)


    # ret = {
    #     'class_id': 3,
    #     'specialization_id': 255,
    #     'scores': [ {
    #        '<fight_style_id>': [ {
    #            '<inventory_type_id>': {
    #                'id': 160630,
    #                'name': '불멸의 환영의 벼슬',
    #                'name_unique': '불멸의 환영의 벼슬 1'
    #            }
    #        } ]
    #     } ]
    # }

    return grouped_items