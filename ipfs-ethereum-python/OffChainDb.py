#!/usr/bin/python
import psycopg2
import logging


class OffChainDb:

    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    def __init__(self, host, port, database, user, password):
        logging.info("Initializing the off-chain database connection")
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        logging.info('Connecting to the PostgreSQL database...')
        try:
            conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        except Exception as ex:
            logging.error("Unable to connect to the off chain database")
            self.conn = None
        else:
            self.conn = conn

    def store_new_document(self, ipfs_hash):
        logging.info("Storing a new document to the off-chain database")
        query = "insert into data_interoperability ( ipfs_hash)" \
                "values(%s)"
        cur = self.conn.cursor()
        try:
            cur.execute(query, [ipfs_hash])
        except Exception as ex:
            logging.error("Unable to insert to the off chain database")
        else:
            self.conn.commit()

    def get_document_from_ipfshash(self, ipfs_hash):
        logging.info("Getting document ID from off-chain database using ipfs hash")
        query = "select id from data_interoperability where transaction_hash is null and ipfs_hash = '" + str(ipfs_hash) + "'"
        print("Sample: " + query)
        cur = self.conn.cursor()
        try:
            cur.execute(query)
        except Exception as ex:
            logging.error("Unable to get data from the off chain database")
        else:
            if cur.rowcount >= 1:
                print("Found " + str(cur.rowcount) + " record(s)")
                return cur.fetchone()
            else:
                print("No records found from get_document_from_ipfshash(ipfs_hash)")
                return None

    def update_transaction_for_document(self, document_id, transaction_hash):
        logging.info("Updating document on the off-chain db with the transaction hash")
        query = "update data_interoperability " \
                "set transaction_hash = '" + transaction_hash + "' where id = " + str(document_id)
        cur = self.conn.cursor()
        try:
            cur.execute(query, [transaction_hash, document_id])
        except Exception as ex:
            logging.error("Unable to update the off chain database")
        else:
            self.conn.commit()

    def get_document(self, document_id):
        logging.info("Getting a specific document from the off-chain database")
        query = "select * from data_interoperability where transaction_hash is not null and id = " + str(document_id)
        cur = self.conn.cursor()
        cur.execute(query)
        if cur.rowcount >= 1:
            print("Found " + str(cur.rowcount) + " record(s) for document ID " + str(document_id))
            return cur.fetchone()
        else:
            print("No records found from get_document(document_id)")
            return None

    def get_all_documents(self):
        logging.info("Getting documents from the off-chain database")
        query = "select * from data_interoperability"
        cur = self.conn.cursor()
        cur.execute(query)
        if cur.rowcount >= 1:
            print("Found " + str(cur.rowcount) + " record(s)")
            return cur.fetchall()
        else:
            print("No records found")
            return None