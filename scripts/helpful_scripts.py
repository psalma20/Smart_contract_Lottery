from brownie import Lottery,MockV3Aggregator,VRFCoordinatorMock,config,network,accounts,Contract,LinkToken,interface 
from web3 import Web3


LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development","ganache-local"]
FORKED_LOCAL_ENVIROMENTS=["networks","mainnet-fork-dev"]
DECIMALS = 8
STARTING_PRICE = 200000000000



def get_account(index=None, id=None ):
    #accounts[0] brownie ganache accounts
    #accounts.add("env") our enviroments 
    #accounts.load("id")"id in the termenial"

 if index:
   return accounts[index]
 if id:
  return accounts.loads(id)
 if(
   network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or 
   network.show_active() in FORKED_LOCAL_ENVIROMENTS
 ) :
  return accounts[0]
 ##Default
 return accounts.add(config["wallets"]["from_key"]
            )
 
 
 
  #DEVELOPMENT
### WHICH MEANS WHENEVER We see eth_usd_price_feed you know that we will get the MockV3Aggregator

contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}

def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config
    if defined, otherwise, it will deploy a mock version of that contract, and
    return that mock contract.
        Args:
            contract_name (string)
        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed
            version of this contract.
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            # MockV3Aggregator.length
            deploy_mocks()
        contract = contract_type[-1]
        # MockV3Aggregator[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # address
        # ABI
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
        # MockV3Aggregator.abi
    return contract
   
   
 

def deploy_mocks(decimals=DECIMALS,initial_value=STARTING_PRICE):
    
    account=get_account()
    #1.pricefeed
    MockV3Aggregator.deploy(decimals,initial_value,{"from":account})
    #2. Link token 
    link_token=LinkToken.deploy({"from":account})
    #3.VRFCoordinator
    #4. Lottery deployed 
    VRFCoordinatorMock.deploy(link_token.address,{"from":account})


    print("Deployed!!")
  
def fund_with_link(contract_address,account=None,link_token=None,amount=250000000000000000): #0.25 Link 
   
   account=account if account else get_account()
   link_token=link_token if link_token else get_contract("link_token")

   #WAY1
   tx= link_token.transfer(contract_address,amount,{"from":account})
   #WAY2 from brownie interface
   #link_token_contract=interface.LinkTokenInterface(link_token.address)
   #tx=link_token_contract.transfer(contract_address,amount,{"from":account})
   tx.wait(1)
   print("Contract is funded!! ")
   return tx


    
 