import time
from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import ast

import json
import config as config
from web3 import Web3
import bscscan
from bscscan import BscScan
import asyncio
import math



async def getABI(contract_id):
    global contract_abi


    async with BscScan('7ED9HIVQEPDXWD598A5H514ZAMHAQR9AFY') as bsc:
        contract_abi = (await bsc.get_contract_abi(contract_id))

        print("abi string:", contract_abi)
        return contract_abi

#CONSTANTS

API_KEY = '7ED9HIVQEPDXWD598A5H514ZAMHAQR9AFY'

bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))
print("web3 is connected:", web3.isConnected())

contract_address = "0xf8a0bf9cf54bb92f17374d9e9a321e6a111a51bd"


private_key = "0x87f2e0bb908bf802a9fa5ac455fdc33feb798e08492f09a5d8d1b8db0b7c9610"



#this will be an argument of the function
#contract_address = '0xf8a0bf9cf54bb92f17374d9e9a321e6a111a51bd'
#buyRating = 0.01


contract_id = web3.toChecksumAddress(contract_address)




# My own address to swap from
sender_address = "0xc24CB0ED70DA1aC54f1926C2bceBD796Dbd38D38"

# This is global Pancake V2 Swap router address
router_address = "0x10ED43C718714eb63d5aA57B78B54704E256024E"

# always spend using Wrapped BNB
# I guess you want to use other coins to swap you can do that, but for me I used Wrapped BNB
spend = web3.toChecksumAddress("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c")

# This is your private key info
private = "0x87f2e0bb908bf802a9fa5ac455fdc33feb798e08492f09a5d8d1b8db0b7c9610"

# Print out your balances just for checking


balance = web3.eth.get_balance(sender_address)
print(balance)

humanReadable = web3.fromWei(balance, 'ether')
print(humanReadable)




tokenABI = asyncio.run(getABI(contract_id))
tokenContractObject = web3.eth.contract(address=contract_id, abi=tokenABI)

tokensToSell = web3.fromWei(tokenContractObject.functions.balanceOf(sender_address).call(), 'ether')
tokensToSell = float(tokensToSell)
weiTokensToSell = web3.toWei(tokensToSell, 'ether')
print(tokensToSell)
ticker = tokenContractObject.functions.symbol().call()
print(ticker)


print("Address has", tokensToSell, ticker, "tokens to sell from contract ID", contract_id)
nonce = web3.eth.get_transaction_count(sender_address)

start = time.time()
print("0.02 bnb toWei:", web3.toWei('0.02', 'ether'))





pancakeABI = asyncio.run(getABI(router_address))
contract = web3.eth.contract(address=router_address, abi=pancakeABI)
'''
approve = tokenContractObject.functions.approve(router_address, weiTokensToSell).buildTransaction({
    'from': sender_address,
    'gas': 350000,
    'gasPrice': web3.toWei('10', 'gwei'),
    'nonce': web3.eth.get_transaction_count(sender_address),
})

signed_txn = web3.eth.account.sign_transaction(approve, private_key=private)
tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("Approved: " + web3.toHex(tx_token))
time.sleep(3)

print(f"Swapping {tokensToSell} {ticker} for BNB")
'''




pancakeswap2_txn = contract.functions.swapExactTokensForETH(
    weiTokensToSell,
    0,
    [contract_id, spend],
    sender_address,
    (int(time.time()) + 1000000)

).buildTransaction({
    'from': sender_address,
    'gasPrice': web3.toWei('5', 'gwei'),
    'nonce': web3.eth.get_transaction_count(sender_address),
})

signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=private)
tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
print(f"Sold {ticker}: " + web3.toHex(tx_token))
