#!/usr/bin/python
import configparser
from IPFSFile import IPFSFile
from Ethereum import Ethereum
from web3 import Web3
from tqdm import tqdm
from time import sleep
from web3.auto import w3

# ======================= IPFS =======================
# Get IPFS connection parameters
# ipfs_connection = config['IPFS']

# Create IPFS client
# ipfsFile = IPFSFile(str(ipfs_connection['host']), ipfs_connection['port'])

# Store file in IPFS
# result = ipfsFile.store_data(r'C:\ipfs-staging\truffle-logo.png')
# print(result)
# Output: QmNZJYiGnG8GwvztP2xSMqsckoqAh8j8NFsctNtErjQuvo

# Retrieve file from IPFS using hash
# ipfsFile.get_data("QmNZJYiGnG8GwvztP2xSMqsckoqAh8j8NFsctNtErjQuvo")

# ======================= Blockchain =======================
# Get Blockchain connection parameters
# web3_connection = config['BLOCKCHAIN']

# Create Blockchain client
# web3_client = Ethereum(str(web3_connection['host']), web3_connection['port'])
# web3_client = Web3(Web3.HTTPProvider('http://' + '127.0.0.1' + ":" + '7545'))
# address = "0xF59c68c12f19Da5d21580C3A177d909f78C67Cdd"
# abi = '[{"inputs": [{"internalType": "uint256","name": "num","type": "uint256"}],"name": "store","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [],"name": "retrieve","outputs": [{"internalType": "uint256","name": "",	"type": "uint256"}],"stateMutability": "view","type": "function"}]'
# store_var_contract = web3_client.eth.contract(address=address, abi=abi)
# gas = store_var_contract.functions.store(0).estimateGas()
# print(gas)

# tx_hash = store_var_contract.functions.store(100).transact({'from': '0x31E4b4Fc78ADEacDF0D92B52DBd43Fd1fc102d57'})
# receipt = web3_client.eth.wait_for_transaction_receipt(tx_hash)
# print("Transaction receipt mined:")
# pprint.pprint(dict(receipt))
# print("\nWas transaction successful?")
# pprint.pprint(receipt["status"])


# res = store_var_contract.functions.retrieve().call()
# print(res)

