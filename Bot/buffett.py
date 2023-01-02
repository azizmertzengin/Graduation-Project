from connectAPI import client
from time import sleep
import requests
import json

# VARIABLES STARTING
commaChecked = -1
coinName = str(input("Hangi Coin/Paritede işlem yapılsın? (Default: ETHUSDT): "))
if len(coinName) <= 0:
    coinName = "ETHUSDT"
print(coinName)

sleepSec = int(input("İki alım arasında kaç saniye beklensin? Tam sayı olarak girin. (Default: 604800 Min: 2): "))
if sleepSec < 2:
    sleepSec = 604800
print(sleepSec)

cost = float(input("Her bir alım kaç dolar olsun? (Min ve Default: 12.00): "))
if cost < 12:
    cost = 12.00
print(cost)

wallet = float(input("Toplamda kaç dolarlık alım yapılsın? (0: Nakit olduğu sürece zamanı gelince alım yapar.) (Default: Tek alımlık): "))
if (wallet < cost and wallet > 0) or wallet < 0:
    wallet = cost
print(wallet)
headers = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.487"
# VARIABLES ENDING


def toInfinityAndBeyond():
    comma = 8
    qty = 0
    buyPrice = 0
    while(True):
        cash = float(client.get_asset_balance("USDT")['free'])
        if cash >= cost:
            while(True):
                try:
                    price = float(json.loads((requests.get("https://api.binance.com/api/v3/ticker/24hr?symbol=" + coinName).text))["lastPrice"])
                    order = client.order_market_buy(symbol=coinName, quantity=float(round(cost/price,comma)))
                    # print(round(cash/price,6))
                    # print(order["fills"][0]["price"]) # aldığı fiyatı yazıyor.
                    sleep(1)
                    buyPrice += float(order["fills"][0]["price"])
                    qty += float(order["origQty"])
                    print("Toplamda {} adet {} alındı ve komisyonlar hariç fiyat ortalaması: {}".format(qty, coinName, buyPrice/qty))
                    if commaChecked < 0:
                        commaChecked = comma
                    sleep(sleepSec - 1)
                    break

                except:
                    if comma > 0 and commaChecked < 0:
                        comma -= 1
        else:
            print("Yetersiz bakiye. 30 saniye sonra tekrar denenecek.")
            sleep(30)



def youAreMyFavoriteDeputy(wallet):
    comma = 8
    qty = 0
    buyPrice = 0
    i = 0
    while (i < int(wallet/cost)):
        cash = float(client.get_asset_balance("USDT")['free'])
        if cash >= cost:
            while (True):
                try:
                    price = float(json.loads((requests.get("https://api.binance.com/api/v3/ticker/24hr?symbol=" + coinName).text))["lastPrice"])
                    order = client.order_market_buy(symbol=coinName, quantity=float(round(cost/price,comma)))
                    # print(round(cash/price,6))
                    # print(order["fills"][0]["price"]) # aldığı fiyatı yazıyor.
                    sleep(1)
                    buyPrice += float(order["fills"][0]["price"])
                    qty += float(order["origQty"])
                    print("Toplamda {} adet {} alındı ve komisyonlar hariç fiyat ortalaması: {}\nTamamlanan satın alım sayısı: {}".format(qty, coinName, buyPrice/qty, i+1))
                    i = i+1
                    if commaChecked < 0:
                        commaChecked = comma
                    sleep(sleepSec - 1)
                    break

                except:
                    if comma > 0 and commaChecked < 0:
                        comma -= 1
        else:
            print("Yetersiz bakiye. 30 saniye sonra tekrar denenecek.")
            sleep(30)


def dontSellThem():
    if wallet > 0 or wallet < 0:
        youAreMyFavoriteDeputy(wallet)
    elif wallet == 0:
        toInfinityAndBeyond()