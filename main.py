from telethon.sync import TelegramClient, events
import LIQ_MCAP_CHECKER
import bsc
import time
from selenium import webdriver
import asyncio
import time
import logging
import urllib
import urllib.request
import json


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)




name = 'anon' 
api_id = '12270514'
api_hash = "4b0fb9f8967b9c33ebe70280f35fbabd"
chat = -1001747146328
client = TelegramClient('anon', api_id, api_hash)


#judge if a token is ok to buy





@client.on(events.NewMessage)
async def my_event_handler(event):
    NEW = event.raw_text
    print(NEW)
    if "poocoin.app/tokens/" in NEW:

        address = NEW[NEW.index("poocoin.app/tokens/") + len("poocoin.app/tokens/"):NEW.index("0x") + len("0xba5eab68a7203c9ff72e07b708991f07f55ef40e")]
        print("token address: " + address)

        if LIQ_MCAP_CHECKER.OK_TO_BUY(address):


            text = (open("file.txt", "r").read())
            y = json.loads(text)

            text = (open("tax.txt", "r").read())
            taxMultiplier = float(text)


            buyRating = LIQ_MCAP_CHECKER.buyRating(y["MCAP"], y["liquidity"], taxMultiplier)
            print("the token address is ok to buy. proceeding to buy with a buy rating of " + str(buyRating))

            bsc.buyToken(contract_address=address, buyRating=buyRating)

        else:
            print("Something is wrong with this token: Either the market cap is too high, the liquidity is too low, or it's been flagged as a honeypot.")









client.start()
print("client is bot: ", client.is_bot())

client.run_until_disconnected()


