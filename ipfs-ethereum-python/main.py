#!/usr/bin/python
import configparser
from IPFSFile import IPFSFile
from Ethereum import Ethereum
from OffChainDb import OffChainDb
from tabulate import tabulate
from flask import Flask, request, make_response
from flask_restful import Api
import json
from http import HTTPStatus
import logging

# Initialize the Flask application
app = Flask(__name__)
api = Api(app)

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
# 1. Get IPFS and Blockchain connection details
# 2. Check connection with IPFS and Blockchain
# 3. Upload a file to IPFS and get the hash
# 4. Initialize a transaction in Blockchain with the hash from the previous step as an input
# 5. Get the transaction receipt and store it in an OLTP data source

# Read the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Configure IPFS
ipfs_connection = config['IPFS']
ipfsFile = IPFSFile(str(ipfs_connection['host']), ipfs_connection['port'])
# Configure Blockchain
web3_connection = config['BLOCKCHAIN']
web3_client = Ethereum(str(web3_connection['host']), web3_connection['port'])
web3_client.initialize_contract_object(web3_connection['contract_address'], web3_connection['abi'])
#
db_connection = config['DATABASE']
db_client = OffChainDb(str(db_connection['host']), str(db_connection['port']), str(db_connection['database']),
                       str(db_connection['user']), str(db_connection['password']))


@app.route('/api/v1/medication/<int:document_id>', methods=['GET'])
def get_data(document_id):
    logging.info("Servicing /medication/<document_id> GET request for document " + str(document_id))
    headers = {"Content-Type": "application/json"}
    try:
        ipfs_file_hash = web3_client.retrieve_data(document_id)
        if ipfs_file_hash is None:
            return make_response('No data found', HTTPStatus.NO_CONTENT, headers)
        else:
            json_data = json.loads(ipfsFile.get_json(ipfs_file_hash))
    except Exception as ex:
        return make_response(ex, HTTPStatus.INTERNAL_SERVER_ERROR, headers)
    else:
        return make_response({'data': json_data}, HTTPStatus.OK, headers)


@app.route('/api/v1/medication', methods=['POST'])
def store_data():
    headers = {"Content-Type": "application/json"}
    try:
        if request.is_json:
            medication_data = request.get_json()
            ipfs_hash = ipfsFile.store_json(medication_data["data"])
            db_client.store_new_document(ipfs_hash)
            db_record = db_client.get_document_from_ipfshash(ipfs_hash)
            receipt = web3_client.store_data(db_record[0], ipfs_hash, medication_data["account"])
            db_client.update_transaction_for_document(db_record[0], str(receipt['transactionHash'].hex()))
    except Exception as ex:
        return make_response(ex, HTTPStatus.INTERNAL_SERVER_ERROR, headers)
    else:
        return make_response({"transaction_receipt": str(receipt['transactionHash'].hex())}, HTTPStatus.OK, headers)


if __name__ == '__main__':
    app.run()  # run our Flask app





