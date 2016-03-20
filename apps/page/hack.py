import requests

RUN_URL = u'https://api.hackerearth.com/v3/code/run/'
CLIENT_SECRET = '018e27ad57f11ceee17d05c1c0e7646d7b4af856'

source = "print 'Hello World'"

data = {
    'client_secret': CLIENT_SECRET,
    'async': 0,
    'source': source,
    'lang': "PYTHON",
    'time_limit': 5,
    'memory_limit': 262144,
    'input':'',
}

"""r = requests.post(RUN_URL, data=data)
print r.json()#['run_status']['output']
"""