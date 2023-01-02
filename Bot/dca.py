from connectAPI import client
from time import sleep
import requests
import json

# VARIABLES STARTING
coinName = str(input("Hangi Coin/Paritede işlem yapılsın? (Default: ETHUSDT): "))
if len(coinName) <= 0:
    coinName = "ETHUSDT"
print(coinName)

baseOrder = float(input("Başlangıç emri kaç USDT olsun? (Min and Default: 12.00): "))
if (baseOrder) < 12:
    baseOrder = 12.00
print(baseOrder)

safetyOrder = float(input("Güvenlik emri kaç USDT olsun? (Min ve Default: 12.00): "))
if (safetyOrder) < 12:
    safetyOrder = 12.00
print(safetyOrder)

takeProfit = float(input("%kaç kar ile işlem kapatılsın? (Min ve Default: 0.25): "))
if (takeProfit < 0.25):
    takeProfit = 0.25
print(takeProfit)

priceDev = float(input("Giriş fiyatından %kaç düşünce güvenlik emri tetiklensin? (Min ve Default: 2.00): "))
if (priceDev < 0):
    priceDev = 2.00
print(priceDev)

maxSafety = int(input("En fazla güvenlik emri sayısı (Default: 20): "))
if (maxSafety < 0):
    maxSafety = 20
print(maxSafety)
headers = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.487"
# VARIABLES ENDING


def letsMakeMoney():
    comma = 8
    qty = 0
    buyPrice = 0
    commaChecked = -1

    while(True):
        cash = float(client.get_asset_balance("USDT")['free'])
        if (cash >= baseOrder):
            try:
                price = float(json.loads((requests.get("https://api.binance.com/api/v3/ticker/24hr?symbol=" + coinName).text))["lastPrice"])
                if commaChecked >= 0:
                    order = client.order_market_buy(symbol=coinName, quantity=float(round(baseOrder/price,commaChecked)))
                else:
                    order = client.order_market_buy(symbol=coinName, quantity=float(round(baseOrder/price,comma)))
                sleep(1)
                firstBuy = float(order["fills"][0]["price"])
                buyPrice += float(order["fills"][0]["price"])
                qty += float(order["origQty"])
                print("Toplamda {} adet {} alındı ve komisyonlar hariç fiyat ortalaması: {}".format(qty, coinName, buyPrice/qty))
                if commaChecked < 0:
                    commaChecked = comma
                
                safetyCount = 0

                while(True):
                    if (safetyCount < maxSafety):
                        try:
                            cash = float(client.get_asset_balance("USDT")['free'])
                            if cash >= safetyOrder:
                                price = float(json.loads((requests.get("https://api.binance.com/api/v3/ticker/24hr?symbol=" + coinName).text))["lastPrice"])
                                if price <= (((100-priceDev)/100)*(firstBuy)):
                                    order = client.order_market_buy(symbol=coinName, quantity=float(round(safetyOrder/price,commaChecked)))
                                    buyPrice += float(order["fills"][0]["price"])
                                    qty += float(order["origQty"])
                                    print("Toplamda {} adet {} alındı ve komisyonlar hariç fiyat ortalaması: {}".format(qty, coinName, buyPrice/qty))
                                    safetyCount +=1
                            else:
                                print("Yetersiz bakiye.")
                        except:
                            print("Sistem hata ile karşılaştı, işlem tekrar deneniyor.")

                    price = float(json.loads((requests.get("https://api.binance.com/api/v3/ticker/24hr?symbol=" + coinName).text))["lastPrice"])
                    if (price >= (((takeProfit/100) * (buyPrice/qty)) + (buyPrice/qty))):
                        try:
                            order = client.order_market_sell(symbol=coinName, quantity=qty)
                            print("Satış başarıyla gerçekleşti. {} USDT kar edildi.".format(((takeProfit/100) * (buyPrice/qty))))
                            qty = 0
                            buyPrice = 0
                            break
                        except:
                            print("Satış yapılırken hata meydana geldi. Lütfen hesabınızda kullanılabilir olarak {} adet {} olduğundan emin olun.")
            except:
                if comma > 0 and commaChecked < 0:
                    comma -= 1
        else:
            print("Yetersiz bakiye.")