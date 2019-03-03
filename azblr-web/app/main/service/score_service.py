from app.main import db
from app.main.service.meta_service import get_inventory_types, get_fight_styles
from itertools import product

def score(data):
    fight_styles = get_fight_styles()

    conn = db.connect()
    cursor = conn.cursor()

    class_id = data['class_id']
    specialization_id = data['specialization_id']
    items = data['items']
    selected_items = {}
    for item in items:
        grouped_powers = {}
        cursor.execute("select id from crawler where class_id = %s and specialization_id = %s", (class_id, specialization_id))
        crawler_ids = [r[0] for r in cursor]
        for azeritePower in item['azeritePowers']:
            sql = "select sub_spell_name, sub_spell_id from crawler_score where crawler_id in "+str(tuple(crawler_ids))+" and spell_id = %s group by sub_spell_name, sub_spell_id"
            cursor.execute(sql, azeritePower['spellId'])
            for r in cursor:
                power = {'spellId': azeritePower['spellId'], 'spellName': azeritePower['spellName'], 'subSpellName': r[0], 'subSpellId': r[1], 'tier': azeritePower['tier']}
                if azeritePower['tier'] in grouped_powers:
                    grouped_powers[azeritePower['tier']].append(power)
                else:
                    grouped_powers[azeritePower['tier']] = [power,]
        
        del item['azeritePowers'] ###
        for power_comb in product(*grouped_powers.values()):
            selected_item = {
                "id": item['id'],
                "name": item['name'],
                "inventoryType": item['inventoryType'],
                "inventoryName": item['inventoryName'],
                "selectedPower": power_comb
            }
            if item['inventoryType'] in selected_items:
                selected_items[item['inventoryType']].append(selected_item)
            else:
                selected_items[item['inventoryType']] = [selected_item,]

    ret = {
        "class_id": class_id,
        "specialization_id": specialization_id,
        "score_order": {}
    }
    scored_items = []
    for item_comb in product(*selected_items.values()):
        item_set = {"items": item_comb}
        power_set = {}
        for item in item_comb:
            for power in item['selectedPower']:
                power_key = "%s %s" % (power['spellId'], power['subSpellName'])
                if power_key in power_set:
                    power_set[power_key] += 1
                else:
                    power_set[power_key] = 1
        ##scoring
        # import random
        item_set["score"] = {}
        for p in power_set:
            spell_id, sub_spell_name = p.split(" ")
            for fight_style_id in fight_styles:
                cursor.execute("select id from crawler where class_id=%s and specialization_id=%s and fight_style_id=%s",
                (class_id, specialization_id, fight_style_id))
                crawler_id = cursor.fetchone()[0]
                cursor.execute("select score from crawler_score where crawler_id = %s and spell_id = %s and sub_spell_name = %s and count <= %s order by count desc, item_level desc limit 1",
                (crawler_id, spell_id, sub_spell_name, power_set[p]))
                row = cursor.fetchone()
                if row is not None:
                    score = row[0]
                else:
                    score = 0

                if fight_styles[fight_style_id] in item_set["score"]:
                    item_set["score"][fight_style_id] += score
                else:
                    item_set["score"][fight_style_id] = score
        item_set["score"][3] = sum(item_set["score"].values())
        scored_items.append(item_set)
        
    ret["scored_items"] = scored_items
    # ret["scored_items"] = sorted(scored_items, key=lambda i: i["score"], reverse=True)
    ret["score_order"]["단일"] = sorted(scored_items, key=lambda i: i["score"][1], reverse=True)[:5]
    ret["score_order"]["다중"] = sorted(scored_items, key=lambda i: i["score"][2], reverse=True)[:5]
    ret["score_order"]["단일+다중"] = sorted(scored_items, key=lambda i: i["score"][3], reverse=True)[:5]

    return ret