from app.main import db
from app.main.service.meta_service import get_inventory_types, get_fight_styles
from itertools import product
from copy import deepcopy

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
            sql = "select sub_spell_name, sub_spell_id from crawler_score where crawler_id in "+str(tuple(crawer_ids))+" and spell_id = %s group by sub_spell_name, sub_spell_id"
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

    ret = {
        "class_id": class_id,
        "specialization_id": specialization_id
    }
    scored_items = []
    for item_comb in product(*grouped_items.values()):
        item_set = {}
        power_set = {}
        for item in item_comb:
            for power_comb in product(*item['groupedPowers'].values()):
                item_set[item['inventoryName']] = {
                    "id": item['id'],
                    "name": item['name'],
                    "inventoryType": item['inventoryType'],
                    "inventoryName": item['inventoryName'],
                    "selectedPower": power_comb
                }
                
            for power in power_comb:
                power_key = str(power['spellId'])+power['subSpellName']
                if power_key in power_set:
                    power_set[power_key] += 1
                else:
                    power_set[power_key] = 1
        ##scoring
        print(power_set)
        scored_items.append(item_set)

    ret["scored_items"] = scored_items

    return ret