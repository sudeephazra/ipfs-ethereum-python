#!/usr/bin/python
import configparser
from IPFSFile import IPFSFile
from Ethereum import Ethereum
from OffChainDb import OffChainDb
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


@app.route('/api/v1/medications', methods=['GET'])
def get_all_data():
    logging.info("Servicing /medications GET request for address")
    headers = {"Content-Type": "application/json"}
    try:
        if request.is_json:
            request_data = request.get_json()
            account_id = request_data["account_id"]
            all_documents = web3_client.get_all_documents_for_account(str(account_id))
            if all_documents is None:
                return make_response('No data found', HTTPStatus.NO_CONTENT, headers)
        else:
            return make_response('Invalid input. JSON input expected', HTTPStatus.BAD_REQUEST, headers)
    except Exception as ex:
        return make_response(ex, HTTPStatus.INTERNAL_SERVER_ERROR, headers)
    else:
        return make_response({'data': all_documents}, HTTPStatus.OK, headers)


@app.route('/api/v1/medication/<int:document_id>', methods=['GET'])
def get_data(document_id):
    logging.info("Servicing /medication/<document_id> GET request for document ")
    headers = {"Content-Type": "application/json"}
    try:
        if request.is_json:
            request_data = request.get_json()
            account_id = request_data["account_id"]
            document = web3_client.get_document(document_id, account_id)
            if document is None:
                return make_response('No data found', HTTPStatus.NO_CONTENT, headers)
        else:
            return make_response('Invalid input. JSON input expected', HTTPStatus.BAD_REQUEST, headers)
    except Exception as ex:
        return make_response(ex, HTTPStatus.PRECONDITION_FAILED, headers)
    else:
        return make_response({'data': document}, HTTPStatus.OK, headers)


@app.route('/api/v1/medication', methods=['POST'])
def store_data():
    logging.info("Servicing /api/v1/medication POST request")
    headers = {"Content-Type": "application/json"}
    try:
        if request.is_json:
            data = request.get_json()
            creator = data["creator_account"]
            owner = data["owner_account"]
            ipfs_hash = ipfsFile.store_json(data["fileBase64"])
            receipt = web3_client.store_data(ipfs_hash, creator, owner)
    except Exception as ex:
        return make_response(ex, HTTPStatus.INTERNAL_SERVER_ERROR, headers)
    else:
        # return make_response({"transaction_receipt": str(receipt['transactionHash'].hex())}, HTTPStatus.OK, headers)
        return make_response({"transaction_receipt": str(receipt)}, HTTPStatus.OK, headers)


@app.route('/api/v1/medication/permissions', methods=['POST'])
def allow_read():
    logging.info("Servicing /api/v1/permissions POST request")
    headers = {"Content-Type": "application/json"}
    try:
        if request.is_json:
            data = request.get_json()
            document = data["document_id"]
            requestor = data["requestor_account"]
            owner = data["owner_account"]
            receipt = web3_client.grant_permission(int(document), requestor, owner)
    except Exception as ex:
        return make_response(ex, HTTPStatus.INTERNAL_SERVER_ERROR, headers)
    else:
        # return make_response({"transaction_receipt": str(receipt['transactionHash'].hex())}, HTTPStatus.OK, headers)
        return make_response({"transaction_receipt": str(receipt)}, HTTPStatus.OK, headers)


if __name__ == '__main__':
    app.run(debug=True)  # run our Flask app in development mode





