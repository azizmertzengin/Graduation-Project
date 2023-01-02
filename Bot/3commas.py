import requests
import re
from py3cw.request import Py3CW
from time import sleep


apiKey = "YOUR 3COMMAS API KEY HERE"
apiSecret = "YOUR 3COMMAS API SECRET HERE"
botID = "YOUR 3COMMAS BOT ID HERE"


p3cw = Py3CW(
    key=apiKey, 
    secret=apiSecret,
    request_options={
        'request_timeout': 10,
        'nr_of_retries': 1,
        'retry_status_codes': [502]
    }
)

url = "https://ngtcraft.store/cryptoBot/listCoins.php"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.206"}

idPattern = 'ID: (.*?) coinName: (.*?) isCompleted: 0'

coinIds = []

def newTrade(coinName):
    error, data  = p3cw.request(
        entity='bots', 
        action='start_new_deal', 
        action_id=botID,
        payload={
            "pair": coinName
        }
    )


def getCoins():
    getIDs = requests.get(url).text
    coins = re.findall(idPattern, getIDs, re.MULTILINE | re.DOTALL)
    if len(coins) > 0:
        for coin in coins:
            if coin[0] not in coinIds:
                newTrade("USDT_" + coin[1].replace("USDT", "").replace("$", ""))
                print("USDT_" + coin[1].replace("USDT", "").replace("$", ""))
                coinIds.append(coin[0])
                sleep(0.1)
    else:
        if len(coinIds) > 0:
            coinIds.clear()

while True:
    getCoins()
    sleep(2.5)