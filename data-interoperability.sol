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

    event DocumentCreated(address indexed owner, Document document);

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

        emit DocumentCreated(msg.sender, mappedDocument[_id]);
    }

    function grant_view(uint256 _documentId, address _requestor) public returns (Document memory) {
        mappedDocument[_documentId]._documentReaders.push(_requestor);
        return mappedDocument[_documentId];

    }

    function getDocument(uint _documentId) public view returns (Document memory) {
        return mappedDocument[_documentId];
    }

    function getAllDocument(address _owner) public view returns (Document[] memory) {
        return ownedDocuments[_owner];
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

    function check_if_owner(uint256 _documentId, address _requestor) public view returns(bool) {
        address _owner = mappedDocument[_documentId]._documentOwner;
        bool isOwner = false;
        if (_requestor == _owner) {
            isOwner = true;
        }
        return isOwner;
    }

}