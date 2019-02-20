from ..config import blz_client_key, blz_secret_key
import requests

def get_item_info(item_id):
    try:
        d = requests.post('https://kr.battle.net/oauth/token', data={'grant_type':'client_credentials'}, auth=(blz_client_key,blz_secret_key)).json()
        headers = {'Authorization': 'Bearer %s' % (d['access_token'],)}
        item = requests.get('https://kr.api.blizzard.com/wow/item/%s' % (item_id,), data={'region':'kr','locale':'ko_KR'},headers=headers).json()
        if 'azeriteClassPowers' in item:
            azerite_powers = item['azeriteClassPowers']
            # for class_id in azerite_powers:
            #     for azerite_power in azerite_powers[class_id]:
            #         spell = requests.get('https://kr.api.blizzard.com/wow/spell/%s' % (azerite_power['spellId'],), data={'region':'kr','locale':'ko_KR'},headers=headers).json()
            #         azerite_power['spell'] = spell
            data = {
                'id': item['id'],
                'name': item['name'],
                'inventoryType': item['inventoryType'],
                'availableClasses': list(azerite_powers.keys()),
                'azeriteClassPowers': azerite_powers
            }

            return {
                'status': 'success',
                'message': '',
                'data': data
            }, 200
        else:
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
            return {
                'status': 'success',
                'message': '',
                'data': spell
            }, 200
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
    