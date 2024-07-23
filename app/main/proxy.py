import random

import requests
from bs4 import BeautifulSoup
# from common.log import log_error
from fake_useragent import UserAgent

ua = UserAgent()
proxies = []


def set_proxy():
    try:
        # Retrieve latest proxies
        response = requests.get('https://www.sslproxies.org/', headers={'User-Agent': ua.random}, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        proxiesTable = soup.find("div", {"class": "table-responsive"})

        # Save proxies in the array
        if not isinstance(proxiesTable, type(None)):
            for row in proxiesTable.tbody.find_all('tr'):
                proxies.append({
                    'ip_address': row.find_all('td')[0].string,
                    'port': row.find_all('td')[1].string
                })

                # proxies_to_save = {
                #     'ip_address': row.find_all('td')[0].string,
                #     'port': row.find_all('td')[1].string,
                #     'code': row.find_all('td')[2].string,
                #     'country': row.find_all('td')[3].string
                # }
                # db.insert_update_proxies(proxies_to_save)
    except Exception as e:
        pass
        # log_error('+++++ Proxy: Set proxy +++++')
        # log_error(str(e))


def get_proxy():
    if len(proxies) == 0:
        set_proxy()

    # If proxy server is down, get it from local db
    # if len(proxies) == 0:
    #     proxy_data = db.get_proxy_from_db()
    #     for proxy in proxy_data:
    #         proxies.append({
    #             'ip_address': proxy[0],
    #             'port': proxy[1]
    #         })

    # Choose a random proxy
    proxy_index = random_proxy()
    proxy = proxies[proxy_index]
    req_proxies = {
        'http': 'http://' + proxy['ip_address'] + ':' + str(proxy['port']),
        'https': 'https://' + proxy['ip_address'] + ':' + str(proxy['port'])
    }
    proxies.pop(proxy_index)

    return req_proxies

    # Retrieve a random index proxy (we need the index to delete it if not working)


def random_proxy():
    if len(proxies) > 1:
        return random.randint(0, len(proxies) - 1)
    return 0


def get_user_agent():
    pass
    # Fake user agents
    # software_names = [SoftwareName.CHROME.value]
    # operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    # user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    # return user_agent_rotator.get_random_user_agent()
