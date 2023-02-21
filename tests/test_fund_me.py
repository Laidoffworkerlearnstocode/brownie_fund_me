from scripts.helpful_scripts import *
from scripts.deploy import deploy_fund_me
from brownie import network, exceptions, accounts, config
import pytest

def test_can_fund_and_withdraw():
    # Arrange
    account = get_account()               # 获取账户
    fund_me = deploy_fund_me()            # 部署合约
    entrance_fee = fund_me.getEntranceFee() + 100        # 获取入场费
    tx = fund_me.fund({"from": account, "value": entrance_fee})     # 调用fund方法
    tx.wait(1)                            # 等待交易完成
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee     # 断言入场费是否正确
    tx2 = fund_me.withdraw({"from": account})     # 调用withdraw方法
    tx2.wait(1)                           # 等待交易完成
    assert fund_me.addressToAmountFunded(account.address) == 0     # 断言是否提现成功

def test_only_owner_can_withdraw():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS: # 如果不是本地测试环境，跳过测试
        pytest.skip("Only for local testing")
    fund_me = deploy_fund_me()          # 部署合约
    account = get_account()             # 获取账户
    bad_actor = accounts.add()          # 添加一个账户
    print(f"Bad actor: {bad_actor}")    # 打印账户
    print(f"Owner: {account}")          # 打印账户
    with pytest.raises(exceptions.VirtualMachineError):     # 断言是否抛出异常
        fund_me.withdraw({"from": bad_actor})

