// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;

contract IPFS {

    mapping(uint256 => string) public mappedDocument;

    function store(uint _documentId, string memory _documentHash) public {
        mappedDocument[_documentId] = _documentHash;
    }

    function retrieve(uint _documentId) public view returns (string memory) {
        return mappedDocument[_documentId];
    }
}