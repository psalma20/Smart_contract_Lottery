from brownie import Lottery,MockV3Aggregator,config,network,accounts,Contract
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
 else:
  return accounts.add(config["wallets"]["from_key"]
            )
 
 
 
  #DEVELOPMENT
### WHICH MEANS WHENEVER We see eth_usd_price_feed you know that we will get the MockV3Aggregator

contract_to_mock={"eth_usd_price_feed":MockV3Aggregator
 
}
def get_contract(contract_name ):
 """This fxn will grab the contract addresses from the brownie config  if defiened 
 Otherwise,it will deoloy a mock version of the contract, and 
 return the mock contract.

 Args:
     contract_name (string)
 Returns:
     brownie.network.contract.ProjectContract: The most recently deployed 
     version of  this contract.
     example :Mock3Aggregator[-1]

 """
 contract_type = contract_to_mock[contract_name]
 if network.show_active()in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
  if len(contract_type)<=0:
   #MockV3Aggregator.length
   deploy_mocks()
   #MockV3Aggregator[-1]
   contract = contract_type[-1]
  else:
   contract_address=config["networks"][network.show_active()][contract_name]
   contract=Contract.from_abi(contract_type._name,contract_address,contract_type.abi)
  return contract


   
   
 

 def deploy_mocks(decimals=DECIMALS,initial_value=STARTING_PRICE):
    account=get_account()
    MockV3Aggregator.deploy(decimals,initial_value,{"from":account})

    print("Deployed!!")
  
 