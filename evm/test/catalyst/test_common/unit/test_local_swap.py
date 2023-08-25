import pytest
from brownie import reverts
from brownie.test import given
from hypothesis.strategies import floats
from hypothesis import example
import re

from tests.catalyst.utils.common_utils import assert_abs_relative_error


@example(swap_amount_percentage=0.1)
@given(
    swap_amount_percentage=floats(min_value=0, max_value=1)
)  # From 0 to 1x the tokens hold by the vault
def test_local_swap(
    vault,
    vault_tokens,
    berg,
    deployer,
    compute_expected_local_swap,
    swap_amount_percentage,
):
    if len(vault_tokens) < 2:
        pytest.skip("Need at least 2 tokens within a vault to run a local swap.")

    source_token = vault_tokens[0]
    target_token = vault_tokens[1]

    init_vault_source_balance = source_token.balanceOf(vault)
    init_vault_target_balance = target_token.balanceOf(vault)

    swap_amount = swap_amount_percentage * init_vault_source_balance

    assert target_token.balanceOf(berg) == 0

    source_token.transfer(berg, swap_amount, {"from": deployer})
    source_token.approve(vault, swap_amount, {"from": berg})

    y = compute_expected_local_swap(swap_amount, source_token, target_token)[
        "to_amount"
    ]

    tx = vault.localSwap(source_token, target_token, swap_amount, 0, {"from": berg})

    assert tx.return_value <= int(y * 1.000001), "Swap returns more than theoretical"
    assert (y * 9 / 10) <= tx.return_value, "Swap returns less than 9/10 theoretical"

    # Verify user token balances
    assert source_token.balanceOf(berg) == 0
    assert target_token.balanceOf(berg) == tx.return_value

    # Verify vault token balances
    assert source_token.balanceOf(vault) == init_vault_source_balance + swap_amount
    assert target_token.balanceOf(vault) == init_vault_target_balance - tx.return_value


@example(swap_amount_percentage=0.1)
@given(
    swap_amount_percentage=floats(min_value=0.1, max_value=1)
)  # From 0.1x to 1x the tokens hold by the vault
def test_local_swap_minout_always_fails(
    vault,
    vault_tokens,
    berg,
    deployer,
    compute_expected_local_swap,
    swap_amount_percentage,
):
    if len(vault_tokens) < 2:
        pytest.skip("Need at least 2 tokens within a vault to run a local swap.")

    source_token = vault_tokens[0]
    target_token = vault_tokens[1]

    swap_amount = swap_amount_percentage * source_token.balanceOf(vault)

    source_token.transfer(berg, swap_amount, {"from": deployer})
    source_token.approve(vault, swap_amount, {"from": berg})

    y = compute_expected_local_swap(swap_amount, source_token, target_token)[
        "to_amount"
    ]

    with reverts(revert_pattern=re.compile("typed error: 0x24557f05.*")):
        vault.localSwap(
            source_token, target_token, swap_amount, y * 1.1, {"from": berg}
        )


@example(swap_amount_percentage=0.1, min_out_percentage=0.2)
@example(swap_amount_percentage=0.0, min_out_percentage=0.05)
@given(
    swap_amount_percentage=floats(min_value=0, max_value=1),
    min_out_percentage=floats(min_value=0, max_value=1),
)
def test_local_swap_minout(
    vault, vault_tokens, berg, deployer, swap_amount_percentage, min_out_percentage
):
    if len(vault_tokens) < 2:
        pytest.skip("Need at least 2 tokens within a vault to run a local swap.")

    source_token = vault_tokens[0]
    target_token = vault_tokens[1]

    swap_amount = swap_amount_percentage * source_token.balanceOf(vault)
    min_out = min_out_percentage * target_token.balanceOf(vault)

    source_token.transfer(berg, swap_amount, {"from": deployer})
    source_token.approve(vault, swap_amount, {"from": berg})

    simulated_swap_return = vault.calcLocalSwap(source_token, target_token, swap_amount)

    if simulated_swap_return < min_out:
        with reverts(revert_pattern=re.compile("typed error: 0x24557f05.*")):
            vault.localSwap(
                source_token, target_token, swap_amount, min_out, {"from": berg}
            )
    else:
        tx = vault.localSwap(
            source_token, target_token, swap_amount, min_out, {"from": berg}
        )
        assert min_out <= tx.return_value


def test_local_swap_event(vault, vault_tokens, berg, deployer):
    """
    Test the LocalSwap event gets fired.
    """

    if len(vault_tokens) < 2:
        pytest.skip("Need at least 2 tokens within a vault to run a local swap.")

    swap_amount = 10**8

    source_token = vault_tokens[0]
    target_token = vault_tokens[1]

    source_token.transfer(
        berg, swap_amount, {"from": deployer}
    )  # Fund berg's account with tokens to swap
    source_token.approve(vault, swap_amount, {"from": berg})

    tx = vault.localSwap(source_token, target_token, swap_amount, 0, {"from": berg})

    observed_return = tx.return_value

    swap_event = tx.events["LocalSwap"]

    assert swap_event["account"] == berg
    assert swap_event["fromAsset"] == source_token
    assert swap_event["toAsset"] == target_token
    assert swap_event["fromAmount"] == swap_amount
    assert swap_event["toAmount"] == observed_return


@example(swap_amount_percentage=0.1)
@given(
    swap_amount_percentage=floats(min_value=0, max_value=1)
)  # From 0 to 1x the tokens hold by the vault
@pytest.mark.usefixtures("vault_set_fees")
def test_local_swap_fees(
    vault,
    vault_tokens,
    berg,
    deployer,
    compute_expected_local_swap,
    swap_amount_percentage,
):
    if len(vault_tokens) < 2:
        pytest.skip("Need at least 2 tokens within a vault to run a local swap.")

    source_token = vault_tokens[0]
    target_token = vault_tokens[1]

    init_vault_source_balance = source_token.balanceOf(vault)
    init_vault_target_balance = target_token.balanceOf(vault)
    init_gov_source_balance = source_token.balanceOf(
        deployer
    )  # TODO replace the 'deployer' account with a 'governance' fixture (or rename deployer to governance)

    swap_amount = swap_amount_percentage * init_vault_source_balance

    assert target_token.balanceOf(berg) == 0
    source_token.transfer(berg, swap_amount, {"from": deployer})
    source_token.approve(vault, swap_amount, {"from": berg})

    expected_swap_result = compute_expected_local_swap(
        swap_amount, source_token, target_token
    )

    tx = vault.localSwap(source_token, target_token, swap_amount, 0, {"from": berg})

    assert tx.return_value <= int(
        expected_swap_result["to_amount"] * 1.000001
    ), "Swap returns more than theoretical"
    assert tx.return_value >= int(
        expected_swap_result["to_amount"] * 9 / 10
    ), "Swap returns less than 9/10 theoretical"

    # Verify user token balances
    assert source_token.balanceOf(berg) == 0
    assert target_token.balanceOf(berg) == tx.return_value

    # Verify vault balances
    vault_fee = expected_swap_result[
        "vault_fee"
    ]  # TODO how do we verify the correctness of this? Assert change (increase) in vault invariant? Or is the expected swap return enough?
    governance_fee = expected_swap_result["governance_fee"]

    assert_abs_relative_error(
        source_token.balanceOf(vault),
        init_vault_source_balance
        + swap_amount
        - governance_fee,  # Governance fee is sent directly to the governance account
        1e-15,
    )
    assert target_token.balanceOf(vault) == init_vault_target_balance - tx.return_value

    # Verify governance balances
    assert_abs_relative_error(
        source_token.balanceOf(deployer),
        init_gov_source_balance + governance_fee,
        1e-15,
    )