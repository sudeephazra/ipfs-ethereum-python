#!/usr/bin/python
from web3 import Web3
import logging


class Ethereum:

    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    web3_client = None
    contract_object = None

    def __init__(self, http_host, http_port):
        logging.info("Attempting to connect to Blockchain at " + str(http_host) + ":" + str(http_port))
        try:
            self.web3_client = Web3(Web3.HTTPProvider('http://' + http_host + ":" + http_port))
        except Exception as ex:
            logging.error("Unable to connect to blockchain endpoint. " + str(ex))
        else:
            if self.web3_client.isConnected():
                logging.info("Connected to the blockchain endpoint. " + str(http_host) + ":" + str(http_port))

    def initialize_contract_object(self, contract_address, contract_abi):
        logging.info("Initializing connection with the Smart Contract")
        address = contract_address
        abi = contract_abi
        try:
            self.contract_object = self.web3_client.eth.contract(address=address, abi=abi)
        except Exception as ex:
            logging.error("Unable to initialize connection with the Smart Contract")
        else:
            logging.info("Initialized connection with the Smart Contract")

    def gas_estimate(self, document_id, value, read=True):
        logging.info("Attempting to estimate the gas requirement for a transaction")
        if self.contract_object:
            if read:
                gas = self.contract_object.functions.retrieve(document_id).estimateGas()
            else:
                gas = self.contract_object.functions.store(document_id, value.encode('utf-8')).estimateGas()
            return gas
        else:
            logging.error("No contract initialized. Please run initialize_contract_object() before calling any operation")

    def store_data(self, document_id, value, from_account):
        logging.info("Attempting to store data through the Smart Contract into the Blockchain")
        if self.contract_object:
            tx_hash = self.contract_object.functions.store(int(document_id), value).transact({'from': from_account})
            receipt = self.web3_client.eth.wait_for_transaction_receipt(tx_hash)
            logging.info("Transaction submitted and receipt provided")
            return receipt
        else:
            logging.error("No contract initialized. Please run initialize_contract_object() before calling any operation")

    def retrieve_data(self, document_id):
        logging.info("Attempting to retrieve data")
        if self.contract_object:
            try:
                result = self.contract_object.functions.retrieve(int(document_id)).call()
            except Exception as ex:
                logging.error("Unable to retrieve the value from the Blockchain")
            else:
                logging.info("Received value from the Blockchain")
                return result
        else:
            logging.error("No contract initialized. Please run initialize_contract_object() before calling any operation")

    def get_transaction_data(self, tx_hash):
        logging.info("Getting transaction details")
        data = self.web3_client.eth.get_transaction(tx_hash)
        tx_data = data['input'].hex()
        print(tx_data)
        if tx_data is not None:
            return tx_data
        else:
            logging.error("No transaction data found")
            return None

