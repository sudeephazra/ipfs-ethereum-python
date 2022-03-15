// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;

contract IPFS {
    string ipfsHash;

    function store(string memory x) public {
        ipfsHash = x;
    }

    function retrieve() public view returns (string memory) {
        return ipfsHash;
    }
}