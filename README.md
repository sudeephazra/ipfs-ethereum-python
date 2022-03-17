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
  
### PostgreSQL (Off-chain database)  
  
We will use Docker to run PostgreSQL. To download the image, please issue the command ```docker pull postgres```  
  
The run the image using the command ```docker run --name postgres-offchain-db -p 5432:5432 -e POSTGRES_PASSWORD=password -d postgres```  
  
Then create a table as follows  
```sql  
create table data_interoperability (  
	id serial primary key, 
	ipfs_hash varchar(255), 
	transaction_hash varchar(255)
);  
```  
  
## Development  
We need to be able to do the following  
- Accept a file and add it to IPFS  
  - Add the hash of the file to the Blockchain  
- Retrieve the hash of a file from the Blockchain  
  - Retrieve the file from IPFS  

  
The basic level of tasks can be broken down into the following  
  
|Task|Status|  
| --- | --- |  
|Setup Development Blockchain|Completed|  
|Setup Development IPFS|Completed|  
|Setup Python|Completed|  
|Setup Python Libraries|Completed|  
|Connect Python to Blockchain|Completed|  
|Connect Python to IPFS|Completed|  
|Develop Smart Contracts|Completed|  
|Connect Python to Smart Contracts|Completed|  
|Setup web interface|In-Progress|  
|Develop interconnecting interface|In-Progress|  
|Functional Testing |In-Progress|  
|Non-functional Testing|In-Progress|  
|Documentation|In-Progress|  
  
  
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
