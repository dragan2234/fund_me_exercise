from brownie import (
    FundMe,
    MockV3Aggregator,
    network,
    TransparentUpgradeableProxy,
    ProxyAdmin,
    config,
    Contract,
    FundMeV2,
)
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    encode_function_data,
    upgrade
)
from web3 import Web3

def deploy_fund_me():
    print(f"AAAA current netowrk is {network.show_active()}")
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        print("didmockAAAAAAAAAAAAAAAAAAA")
        price_feed_address = MockV3Aggregator[-1].address


    
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    # Optional, deploy the ProxyAdmin and use that as the admin contract
    proxy_admin = ProxyAdmin.deploy(
        {"from": account},
    )


    fund_me_encoded_initializer_function = encode_function_data(fund_me.set_price_feed_address, price_feed_address)
    # box_encoded_initializer_function = encode_function_data(initializer=box.store, 1)
    proxy = TransparentUpgradeableProxy.deploy(
        fund_me.address,
        proxy_admin.address,
        fund_me_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )
    print(f"Proxy deployed to {proxy} ! You can now upgrade it to FundMeV2!")
    proxy_fund_me = Contract.from_abi("FundMe", proxy.address, FundMe.abi)
    print(f"Here is the initial value in the FundMe: {proxy_fund_me.getEntranceFee()}")
    
    print(f"Contract deployed to {fund_me.address}")




    account = get_account()
    print(f"Deploying to {network.show_active()}")
    fund_me_v2 = FundMeV2.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    proxy = TransparentUpgradeableProxy[-1]
    proxy_admin = ProxyAdmin[-1]
    upgrade(account, proxy, fund_me_v2, proxy_admin_contract=proxy_admin)
    print("Proxy has been upgraded!")
    proxy_fund_me = Contract.from_abi("FundMeV2", proxy.address, FundMeV2.abi)
    print(f"Starting value {proxy_fund_me.getEntranceFee()}")
    return proxy_fund_me

def main():
    deploy_fund_me()