#!/usr/bin/python
import ipfshttpclient


class IPFSFile:

    client = None

    def __init__(self, ipfs_host, ipfs_port):
        print("Attempting to connect to IPFS at " + str(ipfs_host) + ":" + str(ipfs_port))
        try:
            self.client = ipfshttpclient.connect(session=True)
        except Exception as ex:
            print("Unable to connect to IPFS. " + str(ex))
        else:
            print("Connected to the IPFS endpoint. " + str(ipfs_host) + ":" + str(ipfs_port))

    # This method accepts a file and then stores it into the IPFS node
    def upload_file_ipfs(self, filename):
        try:
            result = self.client.add(filename)
        except Exception as ex:
            print("Unable to store file to IPFS. " + str(ex))
        else:
            return result
        return None

    # This method accepts a JSON and then stores it into the IPFS node
    def upload_json_ipfs(self, json_data):
        try:
            result = self.client.add_json(json_data)
        except Exception as ex:
            print("Unable to store JSON to IPFS. " + str(ex))
        else:
            return result
        return None

    # This method saves a file into IPFS and then creates an hash to store the file metadata into IPFS
    def store_data(self, filename):
        ipfs_details = self.upload_file_ipfs(filename)
        file = ipfs_details['Name']
        file_hash = ipfs_details['Hash']
        size = ipfs_details['Size']
        file_metadata = {"file_name": file, "file_hash": file_hash, "file_size": size}
        try:
            result = self.client.add_json(file_metadata)
        except Exception as ex:
            print("Unable to store metadata in IPFS")
        else:
            return result
        return None

    def store_json(self, json_data):
        try:
            ipfs_details = self.upload_json_ipfs(json_data)
        except Exception as ex:
            print("Unable to store metadata in IPFS")
        else:
            return ipfs_details
        return None

    def get_data(self, json_hash):
        try:
            json_data = self.client.get_json(json_hash)
        except Exception as ex:
            print("Unable to get data from IPFS")
        else:
            self.get_file_ipfs(json_data["file_hash"], json_data["file_name"])
        return None

    def get_json(self, json_hash):
        try:
            json_data = self.client.get_json(json_hash)
        except Exception as ex:
            print("Unable to get data from IPFS")
        else:
            return json_data
        return None

    # This method retrieves the data for a given file hash and saves it as a give file
    def get_file_ipfs(self, file_hash, file_name):
        try:
            result = self.client.cat(str(file_hash))
        except Exception as ex:
            print("Unable to get file from IPFS. " + str(ex))
        else:
            f = open(file_name, "wb")
            f.write(result)
            f.close()
        return None

    def get_data_ipfs(self, file_hash):
        try:
            result = self.client.cat(str(file_hash))
            # result = file_hash
        except Exception as ex:
            print("Unable to get file from IPFS. " + str(ex))
        else:
            return result.decode('utf8', 'strict')
        return None
