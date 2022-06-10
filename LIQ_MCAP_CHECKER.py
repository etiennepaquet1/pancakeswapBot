import time
from selenium import webdriver
import os
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import urllib
from urllib import request
import ast



def buyRating(mcap, liquidity, taxRate):


    return ((((300000 - mcap) / 300000) * 1.6) - 0.3) * taxRate





def OK_TO_BUY(address):
    url = "https://poocoin.app/tokens/" + address
    honey = "https://aywt3wreda.execute-api.eu-west-1.amazonaws.com/default/IsHoneypot?chain=bsc2&token=" + address

    # if the token is judged to be ok to buy
    if (liqOK_mcapOK(url) and (notHoneypot(honey))):
        return True
    else:
        return False

def liqOK_mcapOK(token_address):

    PATH = "C:\Program Files (x86)\Google\chromedriver.exe"

    driver = webdriver.Chrome(PATH)

    driver.get(token_address)

    time.sleep(2)
    success = driver.find_elements_by_class_name("text-success")
    print(len(success))
    for l in success:

        print(l.text)


    liquidity = success[2].text
    liquidity2 = ''
    for character in liquidity:
        if character.isnumeric():
            liquidity2 += character
    liquidity = int(liquidity2)

    MCAP = success[1].text
    print(MCAP)
    MCAP2 = ''
    for character in MCAP:
        if character.isnumeric():
            MCAP2 += character
    MCAP = int(MCAP2)


    file = open("file.txt", "w")
    JSON_text = ('{ "MCAP":' + str(MCAP) + ', "liquidity": ' +  str(liquidity) + ' }')
    file.write(JSON_text)

    return (MCAP < 200000 and liquidity > MCAP/20)


#print(liqOK_mcapOK("https://poocoin.app/tokens/0x1ce0c2827e2ef14d5c4f29a091d735a204794041/"))



def notHoneypot(honey):
    PATH = "C:\Program Files (x86)\Google\chromedriver.exe"

    driver = webdriver.Chrome(PATH)

    driver.get(honey)

    h = driver.find_element_by_css_selector('body > pre').text


    print(h)

    hp = ((((h.split(", "))[0]).split(": "))[1])
    buyTax = float((((h.split(", "))[4]).split(": "))[1])
    sellTax = float((((h.split(", "))[5]).split(": "))[1])

    buyTax2 = (100 - buyTax)/100
    sellTax2 = (100 - sellTax)/100


    taxMultiplier = (buyTax2 * sellTax2)

    file = open("tax.txt", "w")
    tax = str(taxMultiplier)
    file.write(tax)



    print(hp == "false")

    return (hp == 'false')




#notHoneypot("https://aywt3wreda.execute-api.eu-west-1.amazonaws.com/default/IsHoneypot?chain=bsc2&token=0xf6058884ef0654c4c4f1f0a2010ff279df3b4b50")
