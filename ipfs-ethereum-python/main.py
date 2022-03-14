#!/usr/bin/python
import configparser
from IPFSFile import IPFSFile

# Read the configuration file
config = configparser.ConfigParser()
config.read('config.ini')
ipfs_connection = config['IPFS']

# Create IPFS client
ipfsFile = IPFSFile(str(ipfs_connection['host']), ipfs_connection['port'])

# Store file in IPFS
# result = ipfsFile.store_data(r'C:\ipfs-staging\truffle-logo.png')
# print(result)
# Output: QmNZJYiGnG8GwvztP2xSMqsckoqAh8j8NFsctNtErjQuvo

# Retrieve file from IPFS using hash
ipfsFile.get_data("QmNZJYiGnG8GwvztP2xSMqsckoqAh8j8NFsctNtErjQuvo")






