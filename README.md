# ipfs-ethereum-python

Using Python 3.7 to work with IPFS and Ethereum on a Windows 10 machine

## Installation

### Ethereum Blockchain
For a local development blockchain, we will use Ganache. This can be downloaded and installed from https://trufflesuite.com/ganache/index.html

### Smart Contracts
We will be using Solidity to code the Smart Contracts. Solidity can be locally developed and deployed on the local Ganache Blockchain 

#### Remix IDE
https://remix.ethereum.org/

### Python
Create a new project using PyCharm Community Edition.

Then we need to install the IPFS modules
- pip install setuptools wheel
- pip install ipfs-api
- pip install ipfshttpclient **

We will need to compile the web3 Python modules and need a build tool for that. Please install the Microsoft C++ build tools from https://visualstudio.microsoft.com/visual-cpp-build-tools/

Please install the "Desktop Development with C++" component set. This is around a 6GB install. Once the install is done, we need to add the location ```C:\Program Files (x86)\Windows Kits\10\bin\10.0.19041.0\x64``` to our PATH variable.

Then install the Web3 Python module
- pip install ipython web3

The following optional module is kept on-hold due to breaking changes in the underlying pyeth module
- pip install "web3[tester]"

### IPFS

We will run IPFS inside Docker. For that, please download and install Docker Desktop.

Once done, please run the following command to pull the docker image
```docker pull ipfs/go-ipfs```

Once the image is downloaded, we need to start the container. For that, please run the following command

```
mkdir C:\ipfs-staging
mkdir C:\ipfs-data

docker run -d --name ipfs_host -v C:\ipfs-staging\export -v C:\ipfs-data\data\ipfs -p 4001:4001 -p 127.0.0.1:8080:8080 -p 127.0.0.1:5001:5001 ipfs/go-ipfs:latest
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

Please note: **Now we are accessing the global IPFS network. Any file stored here will be available globally with all the available peers. This is not recommended for confidential data.**


## Development
We need to be able to do the following
- Accept a file and add it to IPFS
  - Add the hash of the file to the Blockchain
- Retrieve the hash of a file from the Blockchain
  - Retrieve the file from IPFS
- Validate the authenticity of a file in IPFS and a transaction in Blockchain

The basic level of tasks can be broken down into the following

|Task|Status|
| --- | --- |
|Setup Development Blockchain|Completed|
|Setup Development IPFS|In-Progress|
|Setup Python|Completed|
|Setup Python Libraries|In-Progress|
|Connect Python to Blockchain||
|Connect Python to IPFS|In-Progress|
|Develop Smart Contracts||
|Connect Python to Smart Contracts||
|Setup web interface|In-Progress|
|Develop interconnecting interface||
|Functional Testing ||
|Non-functional Testing||
|Documentation|In-Progress|


## Testing
- Happy Path
- Sad Path

## Resources

### Blockchain 
https://medium.com/@kacharlabhargav21/using-ganache-with-remix-and-metamask-446fe5748ccf

### Ethereum Python
https://ethereum.org/en/developers/docs/programming-languages/python/
https://snakecharmers.ethereum.org/a-developers-guide-to-ethereum-pt-1/
https://medium.com/coinmonks/web3-py-from-ganache-to-infura-3c16aadb0a0
https://web3py.readthedocs.io/en/latest/quickstart.html

### Docker IPFS
https://hub.docker.com/r/ipfs/go-ipfs

### IPFS Ethereum
https://www.quicknode.com/guides/web3-sdks/how-to-integrate-ipfs-with-ethereum
