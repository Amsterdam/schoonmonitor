# utf-8
import requests
from requests import session
from bs4 import BeautifulSoup
from config import config
import json
from pprint import pprint
import shutil
import parser
import argparse


def get_login_cookies(pastedPHPSESSID):
    """ 
        Get PHPSESSID cookie to use the API
    """
    credentials = config('loginCredentials')

    login_url = "https://amsterdam.apptimizeplatform.nl/login"
    s = requests.session()
    r = s.get(login_url)
    # print(r.cookies)

    loginPage = r.text
    soup = BeautifulSoup(loginPage, "html.parser")
    csrf = soup.find("input", type="hidden")
    csrf_token = csrf['value']

    # print('crsf=' + csrf_token)

    payload = {'_username': credentials['user'],
               '_password': credentials['password'],
               '_csrf_token': csrf_token,
               }

    r = s.post(login_url, data=payload)
    print(r.cookies)
    #print(r.headers)
    
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Host': 'amsterdam.apptimizeplatform.nl',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://amsterdam.apptimizeplatform.nl/schouwronde/rapportage/data_export',
        'Cookie': 'PHPSESSID='+ pastedPHPSESSID + ';',
        'Connection': "keep-alive"}

    test = requests.get('https://amsterdam.apptimizeplatform.nl/api/inspectionround/area/rounds/planning', headers=headers)
    if test.status_code == 200:
        print('login succeeded!')
        return headers

    if test.status_code == 401:
        print('login failed! Insert PHPSESSID number from Cookie page from your webbrowser after you login')


def getListofRounds(baseApiUrl, headers):
    roundsIds = []
    apiUrls = ['area', 'object']

    for apiUrl in apiUrls:

        rounds = requests.get(baseApiUrl + '/' + apiUrl + '/rounds/planning', headers=headers)
        roundsJson = rounds.json()


        roundsItems = [{'id': r['id'], 'name': r['name'].replace('/','-'), 'type': apiUrl} for r in roundsJson]
        roundsIds.extend(roundsItems)
    print(roundsIds)
    return roundsIds


def getXLSofRounds(roundsIds, baseApiUrl, headers):
    for roundsId in roundsIds:
        apiUrl = baseApiUrl + '/' + roundsId['type'] + '/rounds/' + str(roundsId['id']) + '/report/results/excel'
        print(apiUrl)
        resp = requests.get(apiUrl, headers=headers, stream=True)
        resp.raw.decode_content = True

        if resp.status_code == 200:
            with open('results/' + roundsId['name'] + '.xlsx', 'wb') as output:
                shutil.copyfileobj(resp.raw, output)


def main(pastedPHPSESSID):
    hostName = 'amsterdam.apptimizeplatform.nl'
    baseApiUrl = 'https://' + hostName + '/api/inspectionround'
    headers = get_login_cookies(pastedPHPSESSID)
    roundsIds = getListofRounds(baseApiUrl, headers)
    getXLSofRounds(roundsIds, baseApiUrl, headers)


if __name__ == '__main__':
    desc = "download all xls crow measurements"
    parser = argparse.ArgumentParser(desc)
    parser.add_argument('phpsessid', type=str,
                        help='paste phphsessid key here from web browser', nargs=1)
    args = parser.parse_args()
    main(args.phpsessid[0])
