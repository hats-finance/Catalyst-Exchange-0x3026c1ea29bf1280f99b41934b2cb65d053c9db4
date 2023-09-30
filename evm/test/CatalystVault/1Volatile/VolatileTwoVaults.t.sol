// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "../../../src/ICatalystV1Vault.sol";

import "../Invariant.t.sol";
import {TestSendAsset} from "../SendAsset.t.sol";
import {TestReceiveAsset} from "../ReceiveAsset.t.sol";
import "../non-exploits/CrossSwap.SwapWorthlessToken.t.sol";

contract TestVolatileInvariant2 is TestInvariant, TestSendAsset, TestReceiveAsset, TestSwapWorthlessTokenCrossChain {

    address[] _vaults;

    function setUp() virtual override public {
        super.setUp();

        amplified = false;

        address[] memory assets = getTokens(2);
        uint256[] memory init_balances = new uint256[](2);
        init_balances[0] = 10 * 10**18; init_balances[1] = 100 * 10**18;
        uint256[] memory weights = new uint256[](2);
        weights[0] = 3; weights[1] = 2;

        address vault1 = deployVault(assets, init_balances, weights, 10**18, 0);

        _vaults.push(vault1);

        assets = getTokens(1);
        init_balances = new uint256[](1);
        init_balances[0] = 10 * 10**18;
        weights = new uint256[](1);
        weights[0] = 2;

        address vault2 = deployVault(assets, init_balances, weights, 10**18, 0);

        _vaults.push(vault2);

    }
    function getLargestSwap(address fromVault, address toVault, address fromAsset, address toAsset) view override internal returns(uint256 amount) {
        return getLargestSwap(fromVault, toVault, fromAsset, toAsset, false);
    }

    function getLargestSwap(address fromVault, address toVault, address fromAsset, address toAsset, bool securityLimit) view override internal returns(uint256 amount) {
        if (securityLimit) {
            amount = Token(fromAsset).balanceOf(fromVault) / 2;
        } else {
            amount = Token(fromAsset).balanceOf(fromVault) * 1000;
        }
        uint256 amount2 = Token(fromAsset).balanceOf(address(this));
        if (amount2 < amount) amount = amount2;
    }
    
    function invariant(address[] memory vaults) view internal override returns(uint256 inv) {
        (uint256[] memory balances, uint256[] memory weights) = getBalances(vaults);

        balances = logArray(balances);

        balances = xProduct(balances, weights);

        inv = getSum(balances);
    }

    function getTestConfig() internal override view returns(address[] memory vaults) {
        return vaults = _vaults;
    }
}
