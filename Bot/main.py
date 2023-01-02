import os
from time import sleep

os.system("cls")
print("KULLANACAĞINIZ APILERIN KEYLERİNİ VE DİĞER GEREKSİNİMLERİNİ EKLEMEYİ UNUTMAYIN!!! (3commas.py / connectAPI.py)")
secim = int(input("İşlem yapmak istediğiniz türü seçin:\n1. Pump\n2. Buffett's DCA\n3. 3Commas\n4. Continuous DCA\n5. Çıkış\n"))


if (secim == 1):
    os.system("cls")
    from pump import findPump
    findPump()

elif (secim == 2):
    os.system("cls")
    from buffett import dontSellThem
    dontSellThem()

elif (secim == 3):
    os.system("cls")
    os.system("3commas.bat")

elif (secim == 4):
    os.system("cls")
    from dca import letsMakeMoney
    letsMakeMoney()

else:
    print("Görüşürüz.")
    sleep(1)
    exit()


