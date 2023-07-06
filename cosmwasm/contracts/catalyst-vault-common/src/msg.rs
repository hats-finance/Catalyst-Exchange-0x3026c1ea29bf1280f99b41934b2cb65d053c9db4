use cosmwasm_schema::cw_serde;

use cosmwasm_std::{Binary, Uint64, Uint128, Addr};
use cw20::Expiration;
use catalyst_types::U256;



#[cw_serde]
pub struct InstantiateMsg {
    pub name: String,       // Name for the vault token
    pub symbol: String,     // Symbol for the vault token
    pub chain_interface: Option<String>,
    pub vault_fee: Uint64,
    pub governance_fee_share: Uint64,
    pub fee_administrator: String,
    pub setup_master: String,
}


#[cw_serde]
pub enum ExecuteMsg<T> {

    InitializeSwapCurves {
        assets: Vec<String>,
        weights: Vec<Uint128>,
        amp: Uint64,
        depositor: String
    },

    FinishSetup {},

    SetVaultFee { fee: Uint64 },

    SetGovernanceFeeShare { fee: Uint64 },

    SetFeeAdministrator { administrator: String },

    SetConnection {
        channel_id: String,
        to_vault: Binary,
        state: bool
    },

    OnSendAssetSuccess {
        channel_id: String,
        to_account: Binary,
        u: U256,
        amount: Uint128,
        asset: String,
        block_number_mod: u32
    },

    OnSendAssetFailure {
        channel_id: String,
        to_account: Binary,
        u: U256,
        amount: Uint128,
        asset: String,
        block_number_mod: u32
    },

    OnSendLiquiditySuccess {
        channel_id: String,
        to_account: Binary,
        u: U256,
        amount: Uint128,
        block_number_mod: u32
    },

    OnSendLiquidityFailure {
        channel_id: String,
        to_account: Binary,
        u: U256,
        amount: Uint128,
        block_number_mod: u32
    },

    DepositMixed {
        deposit_amounts: Vec<Uint128>,  //TODO EVM MISMATCH
        min_out: Uint128
    },

    WithdrawAll {
        vault_tokens: Uint128,
        min_out: Vec<Uint128>
    },

    WithdrawMixed {
        vault_tokens: Uint128,
        withdraw_ratio: Vec<Uint64>,
        min_out: Vec<Uint128>,
    },

    LocalSwap {
        from_asset: String,
        to_asset: String,
        amount: Uint128,
        min_out: Uint128,
    },

    SendAsset {
        channel_id: String,
        to_vault: Binary,
        to_account: Binary,
        from_asset: String,
        to_asset_index: u8,
        amount: Uint128,
        min_out: U256,
        fallback_account: String,   //TODO EVM mismatch
        calldata: Binary
    },

    ReceiveAsset {
        channel_id: String,
        from_vault: Binary,
        to_asset_index: u8,
        to_account: String,
        u: U256,
        min_out: Uint128,
        from_amount: U256,
        from_asset: Binary,
        from_block_number_mod: u32,
        calldata_target: Option<Addr>,
        calldata: Option<Binary>
    },

    SendLiquidity {
        channel_id: String,
        to_vault: Binary,
        to_account: Binary,
        amount: Uint128,            //TODO EVM mismatch
        min_vault_tokens: U256,      //TODO EVM mismatch
        min_reference_asset: U256,  //TODO EVM mismatch
        fallback_account: String,   //TODO EVM mismatch
        calldata: Binary
    },

    ReceiveLiquidity {
        channel_id: String,
        from_vault: Binary,
        to_account: String,
        u: U256,
        min_vault_tokens: Uint128,
        min_reference_asset: Uint128,
        from_amount: U256,
        from_block_number_mod: u32,
        calldata_target: Option<Addr>,
        calldata: Option<Binary>
    },

    Custom (T),


    // CW20 Implementation
    Transfer { recipient: String, amount: Uint128 },
    Burn { amount: Uint128 },
    Send {
        contract: String,
        amount: Uint128,
        msg: Binary,
    },
    IncreaseAllowance {
        spender: String,
        amount: Uint128,
        expires: Option<Expiration>,
    },
    DecreaseAllowance {
        spender: String,
        amount: Uint128,
        expires: Option<Expiration>,
    },
    TransferFrom {
        owner: String,
        recipient: String,
        amount: Uint128,
    },
    SendFrom {
        owner: String,
        contract: String,
        amount: Uint128,
        msg: Binary,
    },
    BurnFrom { owner: String, amount: Uint128 },
}


#[cw_serde]
pub struct ChainInterfaceResponse {
    pub chain_interface: Option<Addr>
}

#[cw_serde]
pub struct SetupMasterResponse {
    pub setup_master: Option<Addr>
}

#[cw_serde]
pub struct FactoryResponse {
    pub factory: Addr
}

#[cw_serde]
pub struct FactoryOwnerResponse {
    pub factory_owner: Addr
}

#[cw_serde]
pub struct ReadyResponse {
    pub ready: bool
}

#[cw_serde]
pub struct OnlyLocalResponse {
    pub only_local: bool
}

#[cw_serde]
pub struct AssetsResponse {
    pub assets: Vec<Addr>
}

#[cw_serde]
pub struct WeightResponse {
    pub weight: Uint128
}

#[cw_serde]
pub struct VaultFeeResponse {
    pub fee: Uint64
}

#[cw_serde]
pub struct GovernanceFeeShareResponse {
    pub fee: Uint64
}

#[cw_serde]
pub struct FeeAdministratorResponse {
    pub administrator: Addr
}

#[cw_serde]
pub struct CalcSendAssetResponse {
    pub u: U256
}

#[cw_serde]
pub struct CalcReceiveAssetResponse {
    pub to_amount: Uint128
}

#[cw_serde]
pub struct CalcLocalSwapResponse {
    pub to_amount: Uint128
}

#[cw_serde]
pub struct GetLimitCapacityResponse {
    pub capacity: U256
}

#[cw_serde]
pub struct TotalEscrowedAssetResponse {
    pub amount: Uint128
}

#[cw_serde]
pub struct TotalEscrowedLiquidityResponse {
    pub amount: Uint128
}

#[cw_serde]
pub struct AssetEscrowResponse {
    pub fallback_account: Option<Addr>
}

#[cw_serde]
pub struct LiquidityEscrowResponse {
    pub fallback_account: Option<Addr>
}

#[cw_serde]
pub struct VaultConnectionStateResponse {
    pub state: bool
}