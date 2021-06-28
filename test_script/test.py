
import requests
import config

res = requests.get(config.TEST_URL).json()
print(res)
if 'error' in res:
    print(res['error'])
    exit(1)

exit(0)
