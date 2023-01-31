import pytest
import brownie
from brownie import (
    ZERO_ADDRESS,
    CatalystSwapPool
)

from tests.catalyst.fixtures.pools import MAX_POOL_ASSETS


@pytest.fixture(scope="module")
def swap_pool_template_idx(swap_pool_type):
    return 0 if swap_pool_type == "volatile" else 1



# Main setup parametrized test **************************************************************************************************
# Test that all provided pool configs get deployed correctly
def test_setup(
    pool_config,
    pool_tokens,
    swap_factory,
    amplification,
    swap_pool_template_idx,
    deployer
):

    for i, token in enumerate(pool_tokens):
        token.approve(swap_factory, pool_config["init_balances"][i])
    
    tx = swap_factory.deploy_swappool(
        swap_pool_template_idx,
        pool_tokens,
        pool_config["init_balances"],
        pool_config["weights"],
        amplification,
        pool_config["name"],
        pool_config["symbol"],
        ZERO_ADDRESS,
        {"from": deployer}
    )

    # TODO verify that all parameters are saved correctly on-chain



# Tokens and weights *************************************************************************************************************

# TODO do we want deployment of a pool with no tokens to fail? (currently it does not fail)
# def test_setup_no_tokens(deploy_swappool, deployer):
#     sp = deploy_swappool(
#         [],
#         [],
#         [],
#         10**18,
#         "",
#         "",
#         deployer=deployer,
#     )


@pytest.mark.parametrize("asset_count", range(1, MAX_POOL_ASSETS+1))
def test_setup_valid_token_count(
    tokens,
    swap_factory,
    amplification,
    swap_pool_template_idx,
    deployer,
    asset_count
):

    for token in tokens[:asset_count]:
        token.approve(swap_factory, 10**8)

    swap_factory.deploy_swappool(
        swap_pool_template_idx,
        tokens[:asset_count],
        [10**8]*asset_count,
        [1]*asset_count,
        amplification,
        "",
        "",
        ZERO_ADDRESS,
        {"from": deployer}
    )


def test_setup_too_many_tokens(
    tokens,
    swap_factory,
    amplification,
    swap_pool_template_idx,
    deployer,
    max_pool_assets
):
    asset_count = max_pool_assets + 1

    for token in tokens[:asset_count]:
        token.approve(swap_factory, 10**8)

    with brownie.reverts():     #TODO add dev revert message
        swap_factory.deploy_swappool(
            swap_pool_template_idx,
            tokens[:asset_count],
            [10**8]*asset_count,
            [1]*asset_count,
            amplification,
            "",
            "",
            ZERO_ADDRESS,
            {"from": deployer}
        )


def test_setup_no_balance_set(
    tokens,
    swap_factory,
    amplification,
    swap_pool_template_idx,
    deployer,
    max_pool_assets
):
    asset_count = max_pool_assets

    for token in tokens[:asset_count]:
        token.approve(swap_factory, 10**8)


    with brownie.reverts():     #TODO add dev revert message
        swap_factory.deploy_swappool(
            swap_pool_template_idx,
            tokens[:asset_count],
            [10**8]*(asset_count-1) + [0],  # ! Last balance argument set to 0
            [1]*asset_count,
            amplification,
            "",
            "",
            ZERO_ADDRESS,
            {"from": deployer}
        )


def test_setup_no_weight_set(
    tokens,
    swap_factory,
    amplification,
    swap_pool_template_idx,
    deployer,
    max_pool_assets
):
    asset_count = max_pool_assets

    for token in tokens[:asset_count]:
        token.approve(swap_factory, 10**8)


    with brownie.reverts(dev_revert_msg="dev: invalid 0-valued weight provided"):
        swap_factory.deploy_swappool(
            swap_pool_template_idx,
            tokens[:asset_count],
            [10**8]*asset_count,
            [1]*(asset_count-1) + [0],  # ! Last weight argument set to 0
            amplification,
            "",
            "",
            ZERO_ADDRESS,
            {"from": deployer}
        )


def test_setup_without_funds(
    tokens,
    swap_factory,
    amplification,
    swap_pool_template_idx,
    deployer,
    max_pool_assets
):
    asset_count = max_pool_assets

    # ! Not approving tokens to the factory on purpose

    with brownie.reverts():     #TODO add dev revert message
        swap_factory.deploy_swappool(
            swap_pool_template_idx,
            tokens[:asset_count],
            [10**8]*asset_count,
            [1]*asset_count,
            amplification,
            "",
            "",
            ZERO_ADDRESS,
            {"from": deployer}
        )



# Misc **************************************************************************************************************************

def test_setup_invalid_template(
    tokens,
    swap_factory,
    amplification,
    deployer,
    max_pool_assets,
    swap_pool_type
):
    asset_count = max_pool_assets

    for token in tokens[:asset_count]:
        token.approve(swap_factory, 10**8)
    
    with brownie.reverts():     #TODO add dev revert message
        swap_factory.deploy_swappool(
            1 if swap_pool_type == "volatile" else 0,          # ! Invalid template selected on purpose
            tokens[:asset_count],
            [10**8]*asset_count,
            [1]*asset_count,
            amplification,
            "",
            "",
            ZERO_ADDRESS,
            {"from": deployer}
        )


def test_setup_pool_token_mint(
    tokens,
    swap_factory,
    amplification,
    swap_pool_template_idx,
    deployer,
    max_pool_assets
):
    asset_count = max_pool_assets

    for token in tokens[:asset_count]:
        token.approve(swap_factory, 10**8)
    
    tx = swap_factory.deploy_swappool(
        swap_pool_template_idx,
        tokens[:asset_count],
        [10**8]*asset_count,
        [1]*asset_count,
        amplification,
        "",
        "",
        ZERO_ADDRESS,
        {"from": deployer}
    )

    sp = CatalystSwapPool.at(tx.return_value)

    # Verify pool tokens have been minted for the deployer
    assert sp.balanceOf(deployer) == 10**18



def test_setup_call_setup_external(
    tokens,
    swap_factory,
    amplification,
    swap_pool_template_idx,
    deployer,
    max_pool_assets
):
    asset_count = max_pool_assets

    for token in tokens[:asset_count]:
        token.approve(swap_factory, 10**8)
    
    tx = swap_factory.deploy_swappool(
        swap_pool_template_idx,
        tokens[:asset_count],
        [10**8]*asset_count,
        [1]*asset_count,
        amplification,
        "",
        "",
        ZERO_ADDRESS,
        {"from": deployer}
    )

    sp = CatalystSwapPool.at(tx.return_value)

    # Call setup again
    with brownie.reverts(dev_revert_msg="dev: Pool Already setup."):
        sp.setup(
            "",
            "",
            ZERO_ADDRESS,
            0,
            0,
            ZERO_ADDRESS,
            deployer,
            {"from": deployer}
        )



def test_setup_call_initialize_swap_curves_external(
    tokens,
    swap_factory,
    amplification,
    swap_pool_template_idx,
    deployer,
    max_pool_assets
):
    asset_count = max_pool_assets

    for token in tokens[:asset_count]:
        token.approve(swap_factory, 10**8)
    
    tx = swap_factory.deploy_swappool(
        swap_pool_template_idx,
        tokens[:asset_count],
        [10**8]*asset_count,
        [1]*asset_count,
        amplification,
        "",
        "",
        ZERO_ADDRESS,
        {"from": deployer}
    )

    sp = CatalystSwapPool.at(tx.return_value)

    # Call initializeSwapCurves again
    with brownie.reverts(dev_revert_msg="dev: swap curves may only be initialized once by the factory"):
        sp.initializeSwapCurves(
            tokens[:asset_count],
            [1]*asset_count,
            10**18,
            deployer,
            {"from": deployer}
        )



@pytest.mark.parametrize("onlyLocal", [True, False])
def test_setup_only_local(
    tokens,
    swap_factory,
    cross_chain_interface,
    amplification,
    swap_pool_template_idx,
    deployer,
    max_pool_assets,
    onlyLocal
):
    asset_count = max_pool_assets

    for token in tokens[:asset_count]:
        token.approve(swap_factory, 10**8)
    
    tx = swap_factory.deploy_swappool(
        swap_pool_template_idx,
        tokens[:asset_count],
        [10**8]*asset_count,
        [1]*asset_count,
        amplification,
        "",
        "",
        ZERO_ADDRESS if onlyLocal else cross_chain_interface,
        {"from": deployer}
    )

    sp = CatalystSwapPool.at(tx.return_value)

    assert sp.onlyLocal() == onlyLocal
