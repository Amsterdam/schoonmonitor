# utf-8
import requests
import requests_cache
from bs4 import BeautifulSoup
from config import config
import json

# save requests into sqlite db for reducing network requests
requests_cache.install_cache('containers_cache')


def get_login_cookies(session, baseUrl):
    """
        Get PHPSESSID cookie to use the API
    """

    loginPage = session.get(baseUrl + '/login')
    soup = BeautifulSoup(loginPage.text, "html.parser")
    csrf = soup.find("input", type="hidden")

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

    if loginCheck.status_code == 200:
        soup = BeautifulSoup(loginCheck.text, "html.parser")
        # Check for name in html page which is only visible after login
        if 'dashboard' in soup.title.string.lower():
            print("login succeeded!")
            return loginCheck.cookies
    if loginCheck.status_code == 401 or loginCheck == 403:
        print('login failed!')


def getContainer(session, cookies, containerId):
    """
        Get The container date
    """
    containerURI = session.get(baseUrl + '/api/containers/' + str(containerId) + '.json', cookies=cookies)
    containerData = containerURI.json()
    return containerData


def main(baseUrl):
    """
        Get Containers
    """

    with requests.Session() as session:
        containers = []
        n = 1
        cookies = get_login_cookies(session, baseUrl)
        containerListURI = session.get(baseUrl + '/api/containers.json', cookies=cookies)
        containerList = containerListURI.json()
        #print(containerList['containers'][0])
        containerIdList = [container['id'] for container in containerList['containers']]
        print(len(containerIdList), ' containers')
        for containerId in containerIdList:
            container = getContainer(session, cookies, containerId)
            state = '{} of {}'.format(str(n), str(len(containerIdList)))
            print(state)
            containers.append(container)
            n += 1
    with open('afvalcontainers.json', 'w') as outFile:
        json.dump(containers, outFile, indent=2)
    print('Done!')


if __name__ == '__main__':
    desc = "download all containers from Bammens Api, for more info: https://bammensservice.nl/api/doc"
    baseUrl = 'https://bammensservice.nl'
    main(baseUrl)
