from connectAPI import client
import os
import json
import requests
from time import sleep, time
import datetime

# VARIABLES STARTING
cost = float(input("Kaç usdt ile işleme girilsin? (Default: 20.00 - Min: 12.00): "))
if cost < 12.00:
    cost = 20.00
costr = round(cost,2)
if costr > cost:
    cost = costr - 0.01
print(cost)

takeProfit = float(input("Kar yüzde kaç olunca realize edilsin? (Default: 2.00 - Min: 0.2): "))
if takeProfit < 0.2:
    takeProfit = 2.00
print(takeProfit)

stopLoss = float(input("Zarar yüzde kaç olunca pozisyon kapatılsın? (0: Stop yok) (Default: 1.00): "))
if stopLoss < 0:
    stopLoss = 0.99
elif stopLoss == 0:
    stopLoss = 0.00
else:
    stopLoss = float(100 - stopLoss)/100
print(stopLoss)
mesaj = "Sistem başlatılıyor"
for i in range(0,3):
    mesaj = mesaj + "."
    print(mesaj)
    sleep(0.75)
headers = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.487"
# VARIABLES ENDING




def masterRemover():
    os.remove("masterUSDT.json")
    os.rename("tempUSDT.json", "masterUSDT.json")


def getMasters():
    hodler = []

    masterJson = json.loads((requests.get("https://api.binance.com/api/v3/ticker/24hr").text))
    for i in range ((len(masterJson))):
        if ("USDT" in str(masterJson[i]["symbol"]) and "UP" not in str(masterJson[i]["symbol"]) and "DOWN" not in str(masterJson[i]["symbol"]) and "BULL" not in str(masterJson[i]["symbol"]) and "BEAR" not in str(masterJson[i]["symbol"]) and "TRY" not in str(masterJson[i]["symbol"]) and "BUSDUSDT" not in str(masterJson[i]["symbol"]) and "USDCUSDT" not in str(masterJson[i]["symbol"]) and "TUSDUSDT" not in str(masterJson[i]["symbol"]) and "USDSBUSDT" not in str(masterJson[i]["symbol"])):
            hodler.append(json.dumps(masterJson[i]))
    with open("masterUSDT.json", "w", encoding="utf-8") as txt_file:
        txt_file.write(str(hodler))

def getTemps():
    hodler = []

    tempJson = json.loads((requests.get("https://api.binance.com/api/v3/ticker/24hr").text))
    for i in range ((len(tempJson))):
        if ("USDT" in str(tempJson[i]["symbol"]) and "UP" not in str(tempJson[i]["symbol"]) and "DOWN" not in str(tempJson[i]["symbol"]) and "BULL" not in str(tempJson[i]["symbol"]) and "BEAR" not in str(tempJson[i]["symbol"]) and "TRY" not in str(tempJson[i]["symbol"]) and "BUSDUSDT" not in str(tempJson[i]["symbol"]) and "USDCUSDT" not in str(tempJson[i]["symbol"]) and "TUSDUSDT" not in str(tempJson[i]["symbol"]) and "USDSBUSDT" not in str(tempJson[i]["symbol"])):
            hodler.append(json.dumps(tempJson[i]))
    with open("tempUSDT.json", "w", encoding="utf-8") as txt_file:
        txt_file.write(str(hodler))


def sendSignalUSDT():
    masterJson = json.loads(open("masterUSDT.json").read().replace("'",""))
    tempJson = json.loads(open("tempUSDT.json").read().replace("'",""))
    print("Coin aranıyor")
    for i in range ((len(masterJson))):
        # if (((float(tempJson[i]["quoteVolume"]) + float(masterJson[i]["quoteVolume"])/2) <= 5000000) and float(tempJson[i]["quoteVolume"]) >= float(masterJson[i]["quoteVolume"])*1.00):
        if ((float(masterJson[i]["quoteVolume"]) >= 12000000) and float(tempJson[i]["quoteVolume"]) >= float(masterJson[i]["quoteVolume"])*1.00):
            if (float(tempJson[i]["lastPrice"]) >= float(masterJson[i]["lastPrice"])*1.01):
                sym = str(tempJson[i]["symbol"])
                price = float(tempJson[i]["lastPrice"])
                signal = (sym + " AL " + str(price))

                signal = "Deneysel Pump Yakalayıcı\n" + signal + " " + str(datetime.datetime.strftime(datetime.datetime.now(),"%X"))
                print(signal)
                # comma = 6
                # while(True):
                for comma in range (6,-1,-1):
                    cash = float(client.get_asset_balance(asset='USDT')["free"])
                    if cash >= cost:
                        try:
                            print(comma)
                            order = client.order_market_buy(symbol=sym, quantity=float(round(cost/price,comma)))
                            sleep(0.5)
                            buyPrice = float(order["fills"][0]["price"])
                            qty = float(order["origQty"])
                            print("{} adet {} fiyatından {} alındı.".format(str(qty),str(buyPrice),str(sym)))
                            kacta = 1
                            print("kacta")
                            stopLossPrice = float(stopLoss*buyPrice)
                            print("stoploss")
                            takeProfitPrice = float(buyPrice*takeProfit/100) + buyPrice # TP HAZIR
                            print("tp")
                            print("Kar alma ve zarar kesme takibi başladı.")
                            while(True):
                                masterJson = json.loads((requests.get("https://api.binance.com/api/v3/ticker/24hr?symbol="+sym).text))
                                print(str(kacta)+ ". teste girdi")
                                kacta+=1
                                if (float(masterJson["lastPrice"]) < stopLossPrice):
                                    sellOrder = client.order_market_sell(symbol=sym, quantity=qty)
                                    print("stop oldu")
                                    print(sellOrder)
                                    sleep(0.5)
                                    break
                                elif (float(masterJson["lastPrice"]) >= takeProfitPrice):
                                    sellOrder = client.order_market_sell(symbol=sym, quantity=qty)
                                    print("kar aldı")
                                    print(sellOrder)
                                    sleep(0.5)
                                    break
                            break
                        except:
                            if comma > 0:
                                comma -= 1
                    else:
                        print("Yetersiz bakiye")
                        break
                break
            else:
                pass


def findPump():
    getMasters()
    while(True):
        getTemps()
        sendSignalUSDT()
        masterRemover()
        sleep(60)