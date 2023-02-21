from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import *
from web3 import Web3


def deploy_fund_me():
    account = get_account()
    print(f"Deploying FundMe contract from account {account}")
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        # 这里需要部署一个MockV3Aggregator合约，因为在开发环境中，我们没有办法部署一个chainlink的合约，所以我们需要部署一个mock合约，这个合约的作用就是模拟chainlink的合约，我们可以通过这个合约来获取到我们想要的价格,合约放在contracts的test文件夹中
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()