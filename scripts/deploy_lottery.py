
from brownie import Lottery,MockV3Aggregator,config,network
from scripts.helpful_scripts import get_account,deploy_mocks,LOCAL_BLOCKCHAIN_ENVIRONMENTS
def deploy_lottery():
    account=get_account()
    ##All what we have in the constructor 
    lottery=Lottery.deploy()


def main():
    deploy_lottery()