#!/usr/bin/python
import configparser
from IPFSFile import IPFSFile
from Ethereum import Ethereum

# 1. Get IPFS and Blockchain connection details
# 2. Check connection with IPFS and Blockchain
# 3. Upload a file to IPFS and get the hash
# 4. Initialize a transaction in Blockchain with the hash from the previous step as an input
# 5. Get the transaction receipt and store it in an OLTP data source
# 6. To verify the state of the transaction, take the receipt from the OLTP datasource and check status on Blockchain
# 7. *** Verify the Merkle proof of the transaction hash
# 8.

# Read the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Configure
ipfs_connection = config['IPFS']
ipfsFile = IPFSFile(str(ipfs_connection['host']), ipfs_connection['port'])
web3_connection = config['BLOCKCHAIN']
web3_client = Ethereum(str(web3_connection['host']), web3_connection['port'])
web3_client.initialize_contract_object(web3_connection['address'], web3_connection['abi'])

# Upload file
# result = ipfsFile.store_data(r'C:\ipfs-staging\truffle-logo.png')
# print(" JSON transaction hash: " + result)
# gastimate = web3_client.gas_estimate(result)
# print(gastimate)
# receipt = web3_client.store_data(result, "0x37EbED421820Cb5830c67C9750120d0658604759")
# print(dict(receipt))

# Download file
ipfs_file_hash = web3_client.retrieve_data()
ipfsFile.get_data(ipfs_file_hash)





