from app.main import db
import requests
import datetime

def crawl():
    print("crawler started at %s " % datetime.datetime.now())
    conn = db.connect()
    cursor = conn.cursor()

    cursor.execute("select id, name_en from m_fight_style")
    fight_styles = cursor.fetchall()

    sql = """
    select
        c.id, c.name_en, s.id, s.name_en
    from m_class as c
    inner join m_class_specialization as s
        on c.id = s.class_id
    where
        s.available = 1
    """
    cursor.execute(sql)
    class_specializations = cursor.fetchall()
    for class_id, class_name_en, sp_id, sp_name_en in class_specializations:
        for fight_style_id, fight_style_name_en in fight_styles:
            try:
                sql = """
                insert into crawler (
                    class_id, specialization_id, fight_style_id, updated_datetime, created_datetime)
                values (
                    %s, %s, %s, now(), now())
                on duplicate key update
                    updated_datetime = values(updated_datetime)
                """
                cursor.execute(sql, (class_id, sp_id, fight_style_id))
                crawler_id = cursor.lastrowid
                url = "https://bloodmallet.com/json/azerite_traits/%s_%s_%s.json" % (class_name_en, sp_name_en, fight_style_name_en)
                bm_json = requests.get(url).json()
                baseline = bm_json['data']['baseline']
                values = []
                for spell in bm_json['data']:
                    if spell != 'baseline':
                        spell_id = bm_json['spell_ids'][spell]
                        if '+' in spell:
                            sub_spell_name = ''
                            sub_spell_id = ''
                            for sub_spell in spell.split('+')[1:]:
                                sub_spell_name += '+%s' % sub_spell
                                sub_spell_id += '+%s' % bm_json['spell_ids'][sub_spell]
                        else:
                            sub_spell_name = ''
                            sub_spell_id = None

                        for count_ilvl in bm_json['data'][spell]:
                            count, ilvl = count_ilvl.split('_')
                            if '1_%s'%ilvl in baseline:
                                values.append((crawler_id, spell_id, sub_spell_name, sub_spell_id, count, ilvl, bm_json['data'][spell][count_ilvl] - baseline['1_%s'%ilvl]))
                cursor.execute("delete from crawler_score where crawler_id = %s", (crawler_id,))
                cursor.executemany("insert into crawler_score (crawler_id, spell_id, sub_spell_name, sub_spell_id, count, item_level, score, created_datetime) values (%s, %s, %s, %s, %s, %s, %s, now())", values)
                cursor.execute("update crawler set timestamp = %s where id = %s", (bm_json['timestamp'], crawler_id,))
                conn.commit()
            except Exception as e:
                print("error occurs during crawling %s %s %s, %s" % (class_name_en, sp_name_en, fight_style_name_en, e))
    cursor.close()
    conn.close()
    print("crawler finished at %s " % datetime.datetime.now())