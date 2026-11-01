pragma solidity ^0.8.0;

contract ResearchOwnership {

    struct Paper {
        string paperHash;
        string owner;
        uint timestamp;
    }

    mapping(string => Paper) public papers;

    function addPaper(
        string memory _hash,
        string memory _owner
    ) public {

        papers[_hash] = Paper(
            _hash,
            _owner,
            block.timestamp
        );
    }

    function getPaper(
        string memory _hash
    ) public view returns(
        string memory,
        string memory,
        uint
    ) {

        Paper memory p = papers[_hash];

        return (
            p.paperHash,
            p.owner,
            p.timestamp
        );
    }
}