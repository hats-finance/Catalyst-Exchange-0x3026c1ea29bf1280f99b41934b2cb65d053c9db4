import pytest
from brownie import reverts
from brownie.test import given, strategy


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


@given(swap_amount=strategy("uint256", max_value=2000*10**18))
def test_local_swap(swappool, token1, token2, berg, deployer, compute_expected_swap, swap_amount):
    token1.transfer(berg, swap_amount, {'from': deployer})
    token1.approve(swappool, swap_amount, {'from': berg})
    
    y = compute_expected_swap(swap_amount, token1, token2, swappool)
    
    tx = swappool.localswap(
         token1, token2, swap_amount, 0, {'from': berg}
    )
    assert token1.balanceOf(berg) == 0
    
    if swap_amount/(token1.balanceOf(swappool)-swap_amount) < 1e-06:
        assert tx.return_value <= int(y*1.000001), "Swap returns more than theoretical"
    else:
        assert tx.return_value <= int(y*1.000001), "Swap returns more than theoretical"
        assert (y * 9 /10) <= tx.return_value, "Swap returns less than 9/10 theoretical"
    
    assert tx.return_value == token2.balanceOf(berg)
    
    

@given(swap_amount=strategy("uint256", max_value=2000*10**18))
def test_local_swap_approx(swappool, token1, token2, berg, deployer, compute_expected_swap, swap_amount):
    token1.transfer(berg, swap_amount, {'from': deployer})
    token1.approve(swappool, swap_amount, {'from': berg})
    
    y = compute_expected_swap(swap_amount, token1, token2, swappool)
    
    if swap_amount/(token1.balanceOf(swappool)-swap_amount) < 1e-02:
        tx = swappool.localswap(
            token1, token2, swap_amount, 0, True, {'from': berg}
        )
        assert tx.return_value <= int(y*1.000001), "Swap returns more than theoretical"
    else:
        tx = swappool.localswap(
            token1, token2, swap_amount, (y * 9 /10), True, {'from': berg}
        )
        assert tx.return_value <= int(y*1.000001), "Swap returns more than theoretical"
        assert (y * 9 /10) <= tx.return_value, "Swap returns less than 9/10 theoretical"
    
    
@given(swap_amount=strategy("uint256", min_value=1*10**18, max_value=2000*10**18))
def test_local_swap_minout_always_fails(swappool, token1, token2, berg, deployer, compute_expected_swap, swap_amount):
    token1.transfer(berg, swap_amount, {'from': deployer})
    token1.approve(swappool, swap_amount, {'from': berg})
    
    y = compute_expected_swap(swap_amount, token1, token2, swappool)
    
    with reverts("Insufficient Return"):
        tx = swappool.localswap(
            token1, token2, swap_amount, y*1.1, {'from': berg}
        )


@given(swap_amount=strategy("uint256", max_value=2000*10**18), min_out=strategy("uint256", max_value=2000*10**18))
def test_local_swap_minout(swappool, token1, token2, berg, deployer, swap_amount, min_out):
    token1.transfer(berg, swap_amount, {'from': deployer})
    token1.approve(swappool, swap_amount, {'from': berg})
    
    simulated_swap_return = swappool.dry_swap_both(token1, token2, swap_amount, False)
    
    if simulated_swap_return < min_out:
        with reverts("Insufficient Return"):
            tx = swappool.localswap(
                token1, token2, swap_amount, min_out, False, {'from': berg}
            )
    else:
        tx = swappool.localswap(
            token1, token2, swap_amount, min_out, False, {'from': berg}
        )
        assert min_out <= tx.return_value
    