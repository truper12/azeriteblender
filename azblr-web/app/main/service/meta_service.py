from app.main import db

def get_available_class_specializations():
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("select id, name from m_class")
    classes = {row[0]: {'name':row[1], 'specializations': []} for row in cursor}

    cursor.execute("select id, class_id, name from m_class_specialization where available = 1")
    for row in cursor: classes[row[1]]['specializations'].append({row[0]:{'name':row[2]}})
    cursor.close()
    conn.close()

    return classes

def get_inventory_types():
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("select id, name from m_inventory_type")
    inventory = {row[0]: row[1] for row in cursor}
    cursor.close()
    conn.close()
    return inventory

def get_fight_styles():
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("select id, name from m_fight_style ")
    fight_style = {row[0]: row[1] for row in cursor}
    cursor.close()
    conn.close()
    return fight_style