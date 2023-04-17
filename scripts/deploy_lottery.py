import time
from scripts.helpful_scripts import get_account,get_contract,fund_with_link
from brownie import Lottery,config,network

 ##All what we have in the lottery.sol constructor 
 ## publish_source is verifing the contract and false is the defualt 


    
def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        
    )
    print("Deployed lottery!")
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("The lottery is started!")

def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("You entered the lottery!")

# before we end we need to add linktoken to that fxn (request randomness)
#calling the end_lottery fxn we we are going to request to a chainlinknode 
#chainlink will response by the fulfull random fxn 


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    #fund the contract 
    tx=fund_with_link(lottery.address)
    tx.wait(1)
    #end the lottery 
    ending_tx=tx = lottery.endLottery({"from": account})
    ending_tx.wait(1)
    time.sleep(60)
    print(f"{lottery.recentWinner()} is the new Winner!")

 


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()

    