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


def get_login_cookies(session, baseUrl):
    """
        Get PHPSESSID cookie to use the API
    """
    credentials = config('loginCredentials')

    print("start login")
    loginPage = session.get(baseUrl + '/login')
    soup = BeautifulSoup(loginPage.text, "html.parser")
    csrf = soup.find("input", type="hidden")
    print(csrf)
    # Get user and password from config.ini file
    credentials = config('loginCredentials')

    payload = {'_username': credentials['user'],
               '_password': credentials['password'],
               '_csrf_token': csrf['value'],
               }

    # Fake browser header
    headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36"}
    loginCheck = session.post(baseUrl + '/login_check',
                              data=payload,
                              headers=headers,
                              cookies=loginPage.cookies)
   # Response ok or not?
    if loginCheck.status_code == 200:
        securePage = session.get('https://amsterdam.apptimizeplatform.nl/api/inspectionround/area/rounds/planning', headers=headers)
        # Check for name in html page which is only visible after login
        if securePage.status_code == 200:
            print("login succeeded!")
            return loginCheck.cookies
    if loginCheck.status_code == 401 or loginCheck == 403:
        print('login failed!')


def getListofRounds(session, baseApiUrl, cookies):
    roundsIds = []
    apiUrls = ['area', 'object']

    for apiUrl in apiUrls:

        rounds = session.get(baseApiUrl + '/' + apiUrl + '/rounds/planning', cookies=cookies)
        roundsJson = rounds.json()


        roundsItems = [{'id': r['id'], 'name': r['name'].replace('/', '-'), 'type': apiUrl} for r in roundsJson]
        roundsIds.extend(roundsItems)
    print(roundsIds)
    return roundsIds


def getXLSofRounds(session, roundsIds, baseApiUrl, cookies, resultsFolder):
    for roundsId in roundsIds:
        apiUrl = baseApiUrl + '/' + roundsId['type'] + '/rounds/' + str(roundsId['id']) + '/report/results/excel'
        print(apiUrl)
        resp = session.get(apiUrl, cookies=cookies, stream=True)
        resp.raw.decode_content = True

        if resp.status_code == 200:
            with open(resultsFolder + '/' + roundsId['name'] + '.xlsx', 'wb') as output:
                shutil.copyfileobj(resp.raw, output)


def main(resultsFolder):
    hostName = 'https://amsterdam.apptimizeplatform.nl'
    baseApiUrl = hostName + '/api/inspectionround'

    with requests.Session() as session:
        cookies = get_login_cookies(session, hostName)
        roundsIds = getListofRounds(session, baseApiUrl, cookies)
        getXLSofRounds(session, roundsIds, baseApiUrl, cookies, resultsFolder)


if __name__ == '__main__':
    desc = "download all xls crow measurements"
    parser = argparse.ArgumentParser(desc)
    parser.add_argument('resultsFolder', type=str,
                        help='Add results folder name.', nargs=1)
    args = parser.parse_args()

    main(args.resultsFolder[0])
