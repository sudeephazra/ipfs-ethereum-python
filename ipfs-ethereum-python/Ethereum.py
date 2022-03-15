#!/usr/bin/python
from web3 import Web3


class Ethereum:

    web3_client = None
    contract_object = None

    def __init__(self, http_host, http_port):
        print(" Attempting to connect to Blockchain at " + str(http_host) + ":" + str(http_port))
        try:
            self.web3_client = Web3(Web3.HTTPProvider('http://' + http_host + ":" + http_port))
        except Exception as ex:
            print(" Unable to connect to blockchain endpoint. " + str(ex))
        else:
            if self.web3_client.isConnected():
                print(" Connected to the blockchain endpoint. " + str(http_host) + ":" + str(http_port))

    def initialize_contract_object(self, contract_address, contract_abi):
        address = contract_address
        abi = contract_abi
        self.contract_object = self.web3_client.eth.contract(address=address, abi=abi)

    def gas_estimate(self, value, read=True):
        if self.contract_object:
            if read:
                gas = self.contract_object.functions.store(value).estimateGas()
            else:
                gas = self.contract_object.functions.retrieve().estimateGas()
            return gas
        else:
            print("No contract initialized. Please run initialize_contract_object() before calling any operation")

    def store_data(self, value, from_account):
        print("Attempting to store data")
        if self.contract_object:
            tx_hash = self.contract_object.functions.store(value).transact({'from': from_account})
            receipt = self.web3_client.eth.wait_for_transaction_receipt(tx_hash)
            return receipt
        else:
            print("No contract initialized. Please run initialize_contract_object() before calling any operation")

    def retrieve_data(self):
        print("Attempting to retrieve data")
        if self.contract_object:
            result = self.contract_object.functions.retrieve().call()
            return result
        else:
            print("No contract initialized. Please run initialize_contract_object() before calling any operation")
