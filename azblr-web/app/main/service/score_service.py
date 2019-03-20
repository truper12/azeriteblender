from app.main import db
from app.main.service.meta_service import get_fight_styles
from app.main.service.item_info_service import get_spell_info
from itertools import product

def score(data):
    class_id = data['class_id']
    specialization_id = data['specialization_id']
    items = data['items']

    fight_styles = get_fight_styles()

    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("select id, fight_style_id, timestamp from crawler where class_id = %s and specialization_id = %s", (class_id, specialization_id))
    crawler_ids = []
    timestamps = {}
    for r in cursor:
        crawler_ids.append(r[0])
        timestamps[r[1]] = r[2].strftime("%Y-%m-%d %H:%M")
    # crawler_ids = tuple([r[0] for r in cursor])

    selected_items = {}
    for item in items:
        grouped_powers = {}
        
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
                "slotTo": item['slotTo'],
                "inventoryName": item['inventoryName'],
                "icon": item['icon'],
                "selectedPower": power_comb
            }
            if item['slotTo'] in selected_items:
                selected_items[item['slotTo']].append(selected_item)
            else:
                selected_items[item['slotTo']] = [selected_item,]
    
    score_data = {}
    sql = """
    select c.fight_style_id, cs.spell_id, cs.sub_spell_name, cs.count, cs.score
    from crawler_score cs inner join crawler c on cs.crawler_id = c.id
    where c.id in %s
    order by cs.count desc, cs.item_level desc """ % str(tuple(crawler_ids))
    cursor.execute(sql)
    for r in cursor:
        key = "%s %s" % (r[1], r[2])
        if r[0] in score_data:
            if key in score_data[r[0]]:
                if r[3] not in score_data[r[0]][key]:
                    score_data[r[0]][key][r[3]] = r[4]
            else:
                score_data[r[0]][key] = {r[3]: r[4]}
        else:
            score_data[r[0]] = {
                key: {
                    r[3]: r[4]
                }
            }
            
    ret = {
        "class_id": class_id,
        "specialization_id": specialization_id,
        "timestamps": timestamps,
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
        item_set["score"] = {}
        for p in power_set:
            for fight_style_id in fight_styles:
                score = 0
                if fight_style_id in score_data:
                    if p in score_data[fight_style_id]:
                        if power_set[p] in score_data[fight_style_id][p]:
                            score = score_data[fight_style_id][p][power_set[p]]

                if fight_style_id in item_set["score"]:
                    item_set["score"][fight_style_id] += score
                else:
                    item_set["score"][fight_style_id] = score
        item_set["score"][3] = sum(item_set["score"].values())
        scored_items.append(item_set)

    ## sorting
    ret["score_order"]["1"] = sorted(scored_items, key=lambda i: i["score"][1], reverse=True)[:3]
    ret["score_order"]["2"] = sorted(scored_items, key=lambda i: i["score"][2], reverse=True)[:3]
    ret["score_order"]["3"] = sorted(scored_items, key=lambda i: i["score"][3], reverse=True)[:3]

    ## get subspell name
    sub_spells = {}
    for f in ret["score_order"]:
        for s in ret["score_order"][f]:
            for i in s["items"]:
                for p in i["selectedPower"]:
                    sub_spells_ko = ""
                    if p["subSpellId"] is not None:
                        for n in p["subSpellId"].split("+"):
                            if n != "":
                                if n in sub_spells:
                                    sub_spells_ko += "+"+sub_spells[n]
                                else:
                                    ko = get_spell_info(n)['name']
                                    sub_spells_ko += "+"+ko
                                    sub_spells[n] = ko
                    p["subSpellNameKor"] = sub_spells_ko


    return ret