# $50 =0.026
# 0.026 ETH =26000000000000000 wei
from brownie import Lottery,accounts,config,network,exceptions
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS,get_account,fund_with_link
from web3 import Web3 
import pytest

def test_get_entrance_fee(): 
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    #Arange 
    lottery=deploy_lottery()
    #Act
    ##once the mock is deployed 
    ##starting value is 2000 eth/usd 
    #usdEntryFee is $50
    # = 50/2000 == 0.025 eth/usd 


    expected_entrance_fee =Web3.toWei(0.025,"ether")
    entrance_fee = lottery.getEntranceFee()
    #Assert
    assert expected_entrance_fee == entrance_fee
    
def test_cant_enter_unless_started():
     #Arange onlyowner fxn 
     if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
     lottery=deploy_lottery()
     #Act /Assert
     with pytest.raises(exceptions.VirtualMachineError):
         lottery.enter({"from":get_account(),"value":lottery.getEntranceFee()})

def test_can_start_and_enter_lottery():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    account = get_account()
    lottery = deploy_lottery()
    # Act
    with pytest.raises(exceptions.VirtualMachineError):
         lottery.enter({"from":get_account(),"value":lottery.getEntranceFee()})
    # Assert
    assert lottery.players(0) == account

def test_can_enter_lottery():
     # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    account = get_account()
    lottery = deploy_lottery()
    lottery.startLottery({"from":account})
    lottery.enter({"from":account,"value":lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from":account})
    assert lottery.lottery_state()== 2

#testing our fulfill fxn does it correctly chose a winner and reset
# VRFCoordinatorMock fxn called callBack with Randomness(prtenting to be a chainlink node )
def test_can_pick_winner():
     # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    account = get_account()
    lottery = deploy_lottery()
    lottery.startLottery({"from":account})
    lottery.enter({"from":account,"value":lottery.getEntranceFee()})
    lottery.enter({"from":get_account(index=1),"value":lottery.getEntranceFee()})
    lottery.enter({"from":get_account(index=2),"value":lottery.getEntranceFee()})
    fund_with_link(lottery)
    #Choose a winner and get the request id 
    transaction=lottery.endLottery({"from":account})
    request_id=transaction.events["RequestedRandomness"]["requestId"]
    #Pretend to be the chainlink node (mock version )
    #callBackWithRandomness constructor is the fulfill fxn of the moch contract 
    #GET THE RANDOM NUMBER 
    STATIC_RNG=777
    get_account("vrf_coordinator").callBackWithRandomness(request_id,STATIC_RNG,lottery.address,{"from":account})
    starting_balance_of_account = account.balance()
    blanace_of_lottery =lottery.balance()

    # 980 % 3 = 2 is the winner 
    assert account.balance() == starting_balance_of_account + blanace_of_lottery
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0


     
    

      
