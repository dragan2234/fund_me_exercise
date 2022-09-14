from brownie import FundMe, TransparentUpgradeableProxy
from scripts.helpful_scripts import get_account


def fund():
    proxy_fund_me = TransparentUpgradeableProxy[-1]
    account = get_account()
    entrance_fee = proxy_fund_me.getEntranceFee()
    print(entrance_fee)
    print(f"The current entry fee is {entrance_fee}")
    print("Funding")
    proxy_fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    proxy_fund_me = TransparentUpgradeableProxy[-1]
    account = get_account()
    proxy_fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
