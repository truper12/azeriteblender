from ..config import blz_client_key, blz_secret_key
from app.main.service.meta_service import get_inventory_types
import requests

def get_item_info(item_id):
    inventory = get_inventory_types()
    try:
        d = requests.post('https://kr.battle.net/oauth/token', data={'grant_type':'client_credentials'}, auth=(blz_client_key,blz_secret_key)).json()
        headers = {'Authorization': 'Bearer %s' % (d['access_token'],)}
        item = requests.get('https://kr.api.blizzard.com/wow/item/%s' % (item_id,), data={'region':'kr','locale':'ko_KR'},headers=headers).json()
        if 'azeriteClassPowers' in item:
            azerite_powers = item['azeriteClassPowers']
            data = {
                'id': item['id'],
                'name': item['name'],
                'inventoryType': item['inventoryType'],
                'inventoryName': inventory[item['inventoryType']][0],
                'slotTo': inventory[item['inventoryType']][1],
                'availableClasses': [int(class_id) for class_id in azerite_powers.keys()],
                'azeriteClassPowers': azerite_powers
            }

            return data
        response_object = {
            'status': 'fail',
            'message': 'Unable to get azerite item information'
        }
        return response_object, 404
    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': 'Error occurs when connecting the Blizzard API Service'
        }
        return response_object, 500

def get_item_info_with_spell(item_id, class_id):
    inventory = get_inventory_types()
    try:
        d = requests.post('https://kr.battle.net/oauth/token', data={'grant_type':'client_credentials'}, auth=(blz_client_key,blz_secret_key)).json()
        headers = {'Authorization': 'Bearer %s' % (d['access_token'],)}
        item = requests.get('https://kr.api.blizzard.com/wow/item/%s' % (item_id,), data={'region':'kr','locale':'ko_KR'},headers=headers).json()
        if 'azeriteClassPowers' in item:
            azerite_powers = item['azeriteClassPowers']
            if class_id in azerite_powers:
                for azerite_power in azerite_powers[class_id]:
                    spell = requests.get('https://kr.api.blizzard.com/wow/spell/%s' % (azerite_power['spellId'],), data={'region':'kr','locale':'ko_KR'},headers=headers).json()
                    azerite_power['spellName'] = spell['name']
                data = {
                    'id': item['id'],
                    'name': item['name'],
                    'inventoryType': item['inventoryType'],
                    'inventoryName': inventory[item['inventoryType']][0],
                    'slotTo': inventory[item['inventoryType']][1],
                    'azeritePowers': azerite_powers[class_id]
                }

                return data
        response_object = {
            'status': 'fail',
            'message': 'Unable to get azerite item information'
        }
        return response_object, 404
    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': 'Error occurs when connecting the Blizzard API Service'
        }
        return response_object, 500

def get_spell_info(spell_id):
    try:
        d = requests.post('https://kr.battle.net/oauth/token', data={'grant_type':'client_credentials'}, auth=(blz_client_key,blz_secret_key)).json()
        headers = {'Authorization': 'Bearer %s' % (d['access_token'],)}
        spell = requests.get('https://kr.api.blizzard.com/wow/spell/%s' % (spell_id,), data={'region':'kr','locale':'ko_KR'},headers=headers).json()
        if 'id' in spell:
            return spell
        else:
            response_object = {
                'status': 'fail',
                'message': 'Unable to get spell information'
            }
            return response_object, 404
    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': 'Error occurs when connecting the Blizzard API Service'
        }
        return response_object, 500
    