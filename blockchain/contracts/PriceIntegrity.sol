// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract PriceIntegrity {

    struct Record {
        string dataHash;
        uint256 timestamp;
        address sender;
    }

    mapping(uint256 => Record) public records;
    uint256 public recordCount;

    event HashStored(
        uint256 indexed id,
        string dataHash,
        uint256 timestamp,
        address sender
    );

    function storeHash(string memory _hash) public {

        records[recordCount] = Record(
            _hash,
            block.timestamp,
            msg.sender
        );

        emit HashStored(
            recordCount,
            _hash,
            block.timestamp,
            msg.sender
        );

        recordCount++;
    }

    function getRecord(uint256 index)
        public
        view
        returns (
            string memory,
            uint256,
            address
        )
    {
        Record memory r = records[index];
        return (r.dataHash, r.timestamp, r.sender);
    }
}
