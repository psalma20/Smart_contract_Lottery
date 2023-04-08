//SPDX-License-Identifier:MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is Ownable {
    // what fxns must we will use

    address payable[] public players;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    //This means that we have a new type called lottery state with 3 positions
    //0
    //1
    //2
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }

    LOTTERY_STATE public lottery_state;

    constructor(address _priceFeedAddress) public {
        //Need to convert $50 to $50 in ETH
        usdEntryFee = 50 * (10 ** 18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        //AS LOTTERY_STATE are represented by NUMBERS we can easily state them aslo by
        //lottery_state=1(CLOSED)
        lottery_state = LOTTERY_STATE.CLOSED;
    }

    function enter() public payable {
        //$50 min for any player to enter the lottery
        require(msg.value >= getEntranceFee(), "Not Enough ETH!!");
        require(lottery_state == LOTTERY_STATE.OPEN);

        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        //getthePrice Fxn from AggregatorV3
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10 ** 10; //18 decimals
        //Setting the price $50, 1ETH=$2000
        //50/2000
        uint256 costToEnter = (usdEntryFee * 10 ** 18) / adjustedPrice;
        return costToEnter;
    }

    //Only admin can call
    function startLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "Cant Start the lottery yet!"
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        //We get To know a random winner
        //Randomness
        //Blockchain is a deterministic system
        //getting a random number in a deterministic system is actually impossible
        //Having a exploitable randomness will doom you especially anything related to finance (LOTTERY)
        //ITS AN EASY SPOT FOR HACKERS
        /////////////////////////
        //1. This Vunrable method cant be used by any production used cases
        //insecure variables will do that they will use a globally varaible(ex: msg.sender /msg.value)and hash it
    
        // uint256(
        //     keccak256(
        //         abi.encodePacked(
        //             nonce,// nonce is predictable 
        //             msg.sender,// msg.sender is predictable 
        //             block.difficulty,// can be manipulated by the minners gives the miners to win the lottery 
        //             block.timestamp//Timestamp is predictable 
        //         )
        //     )
        // ) % players.length;
    }
}
