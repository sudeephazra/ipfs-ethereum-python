// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;

contract DataInteroperability {

    struct Document {
        uint256 _documentId;
        string _documentIpfsHash;
        address _documentOwner;
        uint256 _createdDate;
        address[] _documentReaders;
    }

    Document[] public _documents;
    mapping(uint256 => Document) public mappedDocument;
    mapping(address => Document[]) public ownedDocuments;

    function save_document(string memory _documentIpfsHash, address _documentOwner) public {
        // Document memory _document;
        uint256 _id = _documents.length + 1;
        mappedDocument[_id]._documentId = _id;
        mappedDocument[_id]._documentIpfsHash = _documentIpfsHash;
        mappedDocument[_id]._documentOwner = msg.sender;
        mappedDocument[_id]._createdDate = block.timestamp;
        mappedDocument[_id]._documentReaders.push(msg.sender);
        mappedDocument[_id]._documentReaders.push(_documentOwner);

        ownedDocuments[msg.sender].push(mappedDocument[_id]);

        _documents.push(mappedDocument[_id]);

    }

    function getDocument(uint _documentId) public view returns (Document memory) {
        require(check_if_reader(_documentId, msg.sender) == true, "You dont have permissions to view the record");
        return mappedDocument[_documentId];
    }

    function getAllDocument(address _owner) public view returns (Document[] memory) {
        return ownedDocuments[_owner];
    }

    function grant_view(uint256 _documentId, address _requestor) public {
        require(mappedDocument[_documentId]._documentOwner == msg.sender, "Only owner can grant permissions");

        mappedDocument[_documentId]._documentReaders.push(_requestor);
    }

    function check_if_reader(uint256 _documentId, address _requestor) public view returns(bool) {
        address[] memory _readers = mappedDocument[_documentId]._documentReaders;
        bool isReader = false;
        for (uint i=0; i < _readers.length; i++) {
            if (_requestor == _readers[i]) {
                isReader = true;
            }
        }

        return isReader;
    }

}