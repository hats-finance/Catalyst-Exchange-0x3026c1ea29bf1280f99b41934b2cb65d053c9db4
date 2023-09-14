use cosmwasm_schema::cw_serde;
use cosmwasm_std::{Env, Binary, Coin, from_binary, BankMsg, CosmosMsg, Uint128, StdResult, Deps};

use crate::{commands::CommandResult, error::ContractError, executors::types::{Account, CoinAmount, Denom}};

pub const BIPS_BASE: Uint128 = Uint128::new(10_000u128);

#[cw_serde]
pub struct TransferCommand {
    pub amounts: Vec<CoinAmount>,
    pub recipient: Account
}

#[cw_serde]
pub struct PayPortionCommand {
    pub denoms: Vec<Denom>,
    pub bips: Vec<Uint128>,
    pub recipient: Account
}

#[cw_serde]
pub struct SweepCommand {
    pub denoms: Vec<Denom>,
    pub minimum_amounts: Vec<Uint128>,
    pub recipient: Account
}

#[cw_serde]
pub struct BalanceCheckCommand {
    pub denoms: Vec<Denom>,
    pub minimum_amounts: Vec<Uint128>,
    pub account: Account
}


pub fn execute_transfer(
    deps: &Deps,
    env: &Env,
    input: &Binary
) -> Result<CommandResult, ContractError> {
    
    let args = from_binary::<TransferCommand>(input)?;

    // Filter out zero amounts
    let coins = args.amounts.iter()
        .map(|amount| -> Result<_, _> {
            amount.get_amount(deps, env)
        })
        .filter(|map_result| {
            match map_result {
                Ok(coin) => !coin.amount.is_zero(),
                _ => true,
            }
        })
        .collect::<Result<Vec<_>, _>>()?;

    if coins.len() == 0 {
        return Ok(CommandResult::Check(Ok(())));
    }

    let msg = BankMsg::Send {
        to_address: args.recipient.get_address(deps, env)?,
        amount: coins
    };

    Ok(CommandResult::Message(
        CosmosMsg::Bank(msg)
    ))
}


pub fn execute_sweep(
    deps: &Deps,
    env: &Env,
    input: &Binary
) -> Result<CommandResult, ContractError> {
    
    let args = from_binary::<SweepCommand>(input)?;

    if args.denoms.len() != args.minimum_amounts.len() {
        return Err(ContractError::InvalidParameters {
            reason: "denoms/minimum_amounts count mismatch".to_string()
        });
    }

    let router_coins = args.denoms.iter()
        .map(|denom| {
            deps.querier.query_balance(env.contract.address.clone(), denom)
        })
        .collect::<Result<Vec<_>, _>>()?;

    let is_minimum_not_reached = router_coins.iter()
        .zip(args.minimum_amounts)
        .find_map(|(coin, minimum_amount)| {
            if coin.amount < minimum_amount {
                Some((coin, minimum_amount))
            }
            else {
                None
            }
        });

    if let Some((coin, amount)) = is_minimum_not_reached {
        let error = format!(
            "Minimum amount {} not fulfilled on sweep operation (found {}{})",
            coin,
            amount,
            coin.denom
        );
        return Ok(CommandResult::Check(Err(error)));
    }

    let send_amounts: Vec<_> = router_coins.into_iter()
        .filter(|coin| !coin.amount.is_zero())
        .collect();

    if send_amounts.len() == 0 {
        return Ok(CommandResult::Check(Ok(())));
    }

    let msg = BankMsg::Send {
        to_address: args.recipient.get_address(deps, env)?,
        amount: send_amounts
    };

    Ok(CommandResult::Message(
        CosmosMsg::Bank(msg)
    ))

}


pub fn execute_pay_portion(
    deps: &Deps,
    env: &Env,
    input: &Binary
) -> Result<CommandResult, ContractError> {
    
    let args = from_binary::<PayPortionCommand>(input)?;

    if args.denoms.len() != args.bips.len() {
        return Err(ContractError::InvalidParameters {
            reason: "denoms/bips count mismatch".to_string()
        });
    }

    let invalid_bips = args.bips.iter()
        .any(|bip| bip.is_zero() || bip > &BIPS_BASE);

    if invalid_bips {
        return Err(ContractError::InvalidParameters {
            reason: "Invalid bips.".to_string()
        });
    }

    let coins = args.denoms.iter()
        .zip(args.bips)
        .map(|(denom, bips)| -> StdResult<_> {

            let router_coin = deps.querier
                .query_balance(env.contract.address.clone(), denom)?;

            let pay_amount = router_coin.amount
                .checked_mul(bips)?
                .checked_div(BIPS_BASE)?;

            Ok(
                Coin::new(pay_amount.u128(), denom)
            )
        })
        .filter(|map_result| {
            match map_result {
                Ok(coin) => !coin.amount.is_zero(),
                _ => true,
            }
        })
        .collect::<Result<Vec<_>, _>>()?;

    if coins.len() == 0 {
        return Ok(CommandResult::Check(Ok(())));
    }

    let msg = BankMsg::Send {
        to_address: args.recipient.get_address(deps, env)?,
        amount: coins
    };

    Ok(CommandResult::Message(
        CosmosMsg::Bank(msg)
    ))

}


pub fn execute_balance_check(
    deps: &Deps,
    env: &Env,
    input: &Binary
) -> Result<CommandResult, ContractError> {
    
    let args = from_binary::<BalanceCheckCommand>(input)?;

    if args.denoms.len() != args.minimum_amounts.len() {
        return Err(ContractError::InvalidParameters {
            reason: "denoms/minimum_amounts count mismatch".to_string()
        });
    }

    let account_coins = args.denoms.iter()
        .map(|denom| {
            deps.querier.query_balance(args.account.get_address(deps, env)?, denom)
        })
        .collect::<Result<Vec<_>, _>>()?;

    let minimum_check = account_coins.iter()
        .zip(args.minimum_amounts)
        .try_for_each(|(coin, minimum_amount)| {
            if coin.amount < minimum_amount {
                Err(
                    format!(
                        "Minimum amount {} not fulfilled on balance check operation (found {}{})",
                        coin,
                        minimum_amount,
                        coin.denom
                    )
                )
            }
            else {
                Ok(())
            }
        });
    
    Ok(CommandResult::Check(minimum_check))
}
