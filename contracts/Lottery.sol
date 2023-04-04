//SPDX-License-Identifier:MIT
pragma solidity ^0.6.6;

import"@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract Lottery{
    // what fxns must we will use 

    address payable[] public players;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;

    constructor(address _priceFeedAddress) public {
        //Need to convert $50 to $50 in ETH
        usdEntryFee= 50 * (10**18); 
        ethUsdPriceFeed=AggregatorV3Interface(_priceFeedAddress);
    }


    function enter() public payable{
        //$50 min for any player to enter the lottery 

        
        players.push(msg.sender);
    }
    
    function getEntranceFee() public view returns (uint256){

    }

    //Only admin can call
    function startLottery() public{}
    function endLottery() public{}
}

