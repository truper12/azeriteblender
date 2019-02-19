import requests
from app.main.config import blz_client_key, blz_secret_key

def a():
    r = requests.post('https://kr.battle.net/oauth/token', data={'grant_type':'client_credentials'}, auth=(blz_client_key,blz_secret_key))
    d = r.json()
    print(r.json())
    r2 = requests.get('https://kr.api.blizzard.com/wow/spell/280555', data={'region':'kr','locale':'ko_KR'},headers={'Authorization': 'Bearer %s' % (d['access_token'],)})
    # r2 = requests.get('https://kr.api.blizzard.com/wow/item/160630?namespace=static-kr', data={'region':'kr','locale':'ko_KR'},headers={'Authorization': 'Bearer %s' % (d['access_token'],)})
    # r2 = requests.get('https://kr.api.blizzard.com/data/wow/token/?namespace=dynamic-kr', headers={'Authorization': 'Bearer %s' % (d['access_token'],)})
    print(r2.json())
    return

if __name__ == "__main__":
    a()