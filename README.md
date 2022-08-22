# ipfs-ethereum-python  
*Sudeep Hazra @Mar, 2022*

Using Python 3.7 to work with IPFS and Ethereum on a Windows 10 machine  
  
## Installation  
  
### Ethereum Blockchain  
For a local development blockchain, we will use Ganache. This can be downloaded and installed from https://trufflesuite.com/ganache/index.html  

Once Ganache is installed, we will need to create a new Ethereum workspace with any name of our choice.
  
### Smart Contracts  
We will be using Solidity to code the Smart Contracts. Solidity can be locally developed on Remix IDE and deployed on the local Ganache Blockchain   
  
#### Remix IDE  
https://remix.ethereum.org/  
  
On the Remix IDe page, we need to enable RemixD  
  
To connect Remix IDE with a local Ganache instance, we need to install the NPM library remixd by using the command ```npm i -g @remix-project/remixd```  
  
Then we need to run the command ```remixd -s "C:\ipfs-staging" --remix-ide https://remix.ethereum.org```  
  
Now we need to come to the Remix IDE, compile our contract and deploy it to the local Ganache HTTP address.  

Once the contract is compiled, we need the ABI. This can be obtained from the compilation tab. We will need to go to https://w3percentagecalculator.com/json-to-one-line-converter/ and then have the ABI converted to a single line JSON
  
Once the contract is deployed, we will see a new transaction with the tag "Contract Creation" in Ganache. This will be the first transaction on the blockchain.  We will need to know the contract deployed address for the next part of the development.
  
### Python  
Create a new project using PyCharm Community Edition.  
  
Then we need to install the IPFS modules  
- pip install setuptools wheel  
- pip install ipfshttpclient  
  
We will need to compile the web3 Python modules and need a build tool for that. Please install the Microsoft C++ build tools from https://visualstudio.microsoft.com/visual-cpp-build-tools/  
  
Please install the "Desktop Development with C++" component set. This is around a 6GB install. Once the install is done, we need to add the location ```C:\Program Files (x86)\Windows Kits\10\bin\10.0.19041.0\x64``` to our PATH variable.  
  
Then install the Web3 Python module  
- pip install ipython web3  
  
The following optional module is kept on-hold due to breaking changes in the underlying pyeth module  
- pip install "web3[tester]"  
  
### IPFS  
  
We will run IPFS inside Docker. For that, please download and install Docker Desktop.  
  
Once done, please run the following command to pull the docker image  
```docker pull ipfs/go-ipfs:v0.8.0```  
  
Once the image is downloaded, we need to start the container. For that, please run the following command  
```  
mkdir C:\ipfs-staging  
mkdir C:\ipfs-data  
  
docker run -d --name ipfs_host -v C:\ipfs-staging\export -v C:\ipfs-data\data\ipfs -p 4001:4001 -p 127.0.0.1:8080:8080 -p 127.0.0.1:5001:5001 ipfs/go-ipfs:v0.8.0  
```  
The container is up and running when we see the following in the Docker logs  
```  
Swarm announcing /ip4/172.17.0.2/udp/4001/quic  
API server listening on /ip4/0.0.0.0/tcp/5001  
WebUI: http://0.0.0.0:5001/webui  
Gateway (readonly) server listening on /ip4/0.0.0.0/tcp/8080  
Daemon is ready  
```  
To check the IPFS instance, we need to go to http://localhost:5001/webui and check the status  
  
Please note: *Now we are accessing the global IPFS network. Any file stored here will be available globally with all the available peers. This is not recommended for confidential data.*  
  
## Process Flow

The primary data flow can be summarized as below

*CDR is not in scope for this document and needs to be looked at separately.*

### POST Request
1. A transaction is initiated from any user of the system to store data. An optional can be used to convert data into FHIR format
2. The data is stored in the IPFS node and a hash is generated corresponding to the data
3. This hash is intercepted by the Python API 
4. A transaction is sent to the Smart Contract 
5. The Smart Contract returns a transaction receipt for the transaction

*N.B.* - All interactions between the IPFS and Blockchain are stored in an off-chain PostgreSQL database

#### Sample Request
```
POST /api/v1/medication HTTP/1.1
Host: localhost:5000
Content-Type: application/json
Content-Length: 918

{
    "fileBase64": "data:@file/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAYFBMVEWAgID///97e3vCwsL4+Pitra2QkJDMzMx5eXnl5eWLi4t9fX3IyMh2dnbPz8/V1dXw8PDc3Nzj4+P19fWEhITs7OydnZ2jo6OUlJSwsLC4uLiurq6+vr6ZmZmSkpKhoaE0a0TUAAAGzUlEQVR4nO3dWXuiMBQG4CRCjYRVQNRq+///5QT3BXJOUCdL893MTRnzPkCArIQqEx1Sl2XZyiz7VIcUl+THzNP7zDTzcHiaX3P9reNvy0Is+uLIUh3LpySQIdZi1+3XX0nSNESw7D58JOzdGfshmfsCMdI0ydfXvpsthqzPwmWXcCZkiEvpC8x4smlBYb7mbtHuIhj7XSqFyyRz2HeIyH7LUWH9zVz39REkHxGWCTNduDeFbwaFlWN1iyr8d0BY+HICD2Gr6FFY+XMCD2GrB+HCM6Ak/t4J68Y74aW6OQp/vboJT+H5VZhy06X5SJryLIz8u0QPEd1ZuPHxGu2TLY/C0tNTKE/i6iic+XoK5SOjPQi/vD2HhH33wsrPivSYJJLCjb+nUD4TKylsTJfik2E7SqrMdCk+GVmbEo9rUhmR+C4kjfdCEvkuFN4LuffCLAidT1YGoevJ2iB0PX9AuAzCwYhT3l+gt4dPEAqRrLo4jrvVVyOsvwB4pSsUYlVcOq7qattYbtQVChEv7jrJaTSzu1NHUyiSnD6l7Wwm6gnZ6nm0Sp",
    "creator_account": "0x31E4b4Fc78ADEacDF0D92B52DBd43Fd1fc102d57",
    "owner_account": "0x589B94e83A2345f33eaF34567be1c465D71870ef"
}
```
#### Sample Response Body
```
{
    "transaction_receipt": "AttributeDict(
      {
        'transactionHash': HexBytes('0x15c0712216947d677b210dc18a399274ddc40e88afd09ec94e6744700635e090'), 
        'transactionIndex': 0, 
        'blockHash': HexBytes('0x09482b831e9d05b2f365872de7034af198a97214aad4ca86b4c7378f71d4c980'), 
        'blockNumber': 92, 'from': '0x589B94e83A2345f33eaF34567be1c465D71870ef', 
        'to': '0xF381d0b5F150CD8B18b19Adac1C7798E7185fe4C', 
        'gasUsed': 605973, 
        'cumulativeGasUsed': 605973, 
        'contractAddress': None, 
        'logs': [], 
        'status': 1, 
        'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
      }
    )"
}
```

### GET Request (Individual Document)
1. Any user submits a request to retrieve data from the Blockchain using an identifier
2. The request is redirected to the Smart Contract
3. The relevant data hash is extracted from the Blockchain
4. The data corresponding to this hash os retrieved from IPFS
5. The data is sent back to the Python API
6. The JSON data from IPFS is sent back to the user

#### Sample Request 
```
GET /api/v1/medication/7 HTTP/1.1
Host: localhost:5000
Content-Type: application/json
Content-Length: 68

{
    "account_id": "0x31E4b4Fc78ADEacDF0D92B52DBd43Fd1fc102d57"
}
```
#### Sample Response Body
```
{
    "content": "\"Hello World\"",
    "data": [
        7,
        "QmSXfamUcvkEyYbtGdQdwZ4TrnVbneKrY5zNx7eGV5ckyq",
        "0x589B94e83A2345f33eaF34567be1c465D71870ef",
        1661083172,
        [
            "0x589B94e83A2345f33eaF34567be1c465D71870ef",
            "0x31E4b4Fc78ADEacDF0D92B52DBd43Fd1fc102d57"
        ]
    ]
}
```

#### Errors
You will get a 403 FORBIDDEN response if the user account does not have permissions to read the document.


### GET Request (All Documents)

#### Sample Request 
```
GET /api/v1/medications HTTP/1.1
Host: localhost:5000
Content-Type: application/json
Content-Length: 68

{
    "account_id": "0x589B94e83A2345f33eaF34567be1c465D71870ef"
}
```
#### Sample Response Body
```
{
    "data": [
        [
            1,
            "QmYiJpPZ2ySmRmdY2EVXeEsQbtCjrq375EFPMTnRLqU4k8",
            "0x589B94e83A2345f33eaF34567be1c465D71870ef",
            1660915072,
            [
                "0x589B94e83A2345f33eaF34567be1c465D71870ef",
                "0x31E4b4Fc78ADEacDF0D92B52DBd43Fd1fc102d57"
            ]
        ],
        [
            2,
            "QmSaqh7sEyj3rCiECEza4twh56RLqdygiX4imuSajiE7tq",
            "0x589B94e83A2345f33eaF34567be1c465D71870ef",
            1660915485,
            [
                "0x589B94e83A2345f33eaF34567be1c465D71870ef",
                "0x31E4b4Fc78ADEacDF0D92B52DBd43Fd1fc102d57"
            ]
        ]
    ]
}
```




  
## Resources  
  
### Blockchain 
https://medium.com/@kacharlabhargav21/using-ganache-with-remix-and-metamask-446fe5748ccf  
https://www.programcreek.com/python/example/99233/ethereum.transactions.Transaction  
https://medium.com/authereum/debugging-solidity-with-a-gui-remix-and-ganache-c6c16488fcfd  
  
### Ethereum Python  
https://ethereum.org/en/developers/docs/programming-languages/python/  
https://snakecharmers.ethereum.org/a-developers-guide-to-ethereum-pt-1/  
https://medium.com/coinmonks/web3-py-from-ganache-to-infura-3c16aadb0a0  
https://web3py.readthedocs.io/en/latest/quickstart.html  
https://blog.logrocket.com/web3-py-tutorial-guide-ethereum-blockchain-development-with-python/  
https://medium.com/python-pandemonium/getting-started-with-python-and-ipfs-94d14fdffd10
  
### Docker IPFS  
https://hub.docker.com/r/ipfs/go-ipfs  
  
### IPFS Ethereum  
https://www.quicknode.com/guides/web3-sdks/how-to-integrate-ipfs-with-ethereum  
https://www.freecodecamp.org/news/technical-guide-to-ipfs-decentralized-storage-of-web3/  
