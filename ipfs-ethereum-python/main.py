#!/usr/bin/python
import configparser
from IPFSFile import IPFSFile
from Ethereum import Ethereum
from OffChainDb import OffChainDb
from tabulate import tabulate

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

operation = None
while operation != 'x':
    records = db_client.get_all_documents()
    print(tabulate(records, headers=['Document ID', 'IPFS Hash', 'Transaction Hash'],
                   tablefmt='psql'))

    operation = input('Select your operation (Read/Write/eXit): ')

    if operation.lower() == 'r':
        print("Performing read operation")
        document_id = input("Select document id: ")
        ipfs_file_hash = web3_client.retrieve_data(document_id)
        print(ipfs_file_hash)
        if ipfs_file_hash is None:
            print("No records found for document ID: " + str(document_id))
        else:
            ipfsFile.get_data(ipfs_file_hash)

    elif operation.lower() == 'w':
        print("Performing write operation")
        file = input("Enter full file path: ")
        account = input("Enter your account: ")
        ipfsHash = ipfsFile.store_data(file)
        db_client.store_new_document(ipfsHash)
        db_record = db_client.get_document_from_ipfshash(ipfsHash)
        receipt = web3_client.store_data(db_record[0], ipfsHash, account)
        db_client.update_transaction_for_document(db_record[0], str(receipt['transactionHash'].hex()))

    elif operation.lower() == 'x':
        print("Exiting...")

    else:
        print("Invalid operation selected. Please select either of R/W/X for the corresponding operation")








