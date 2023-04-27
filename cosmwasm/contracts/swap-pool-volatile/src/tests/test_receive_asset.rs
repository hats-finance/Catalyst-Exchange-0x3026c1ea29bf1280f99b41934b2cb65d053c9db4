mod test_volatile_receive_asset {
    use cosmwasm_std::{Uint128, Addr};
    use cw_multi_test::{App, Executor};
    use ethnum::{U256, uint};
    use swap_pool_common::ContractError;

    use crate::{msg::VolatileExecuteMsg, tests::{helpers::{mock_instantiate, deploy_test_tokens, WAD, mock_initialize_pool, query_token_balance, get_response_attribute, mock_set_pool_connection, CHANNEL_ID, SWAPPER_B, compute_expected_receive_asset, CHAIN_INTERFACE}, math_helpers::{uint128_to_f64, f64_to_uint128}}};

    //TODO check event

    #[test]
    fn test_receive_asset_calculation() {

        let mut app = App::default();

        // Instantiate and initialize vault
        let vault = mock_instantiate(&mut app, Some(Addr::unchecked(CHAIN_INTERFACE)));
        let vault_tokens = deploy_test_tokens(&mut app, None, None);
        let vault_config = mock_initialize_pool(
            &mut app,
            vault.clone(),
            vault_tokens.iter().map(|token_addr| token_addr.to_string()).collect(),
            vec![Uint128::from(1u64) * WAD, Uint128::from(2u64) * WAD, Uint128::from(3u64) * WAD],
            vec![1u64, 1u64, 1u64]
        );

        // Connect pool with a mock pool
        let from_pool = Addr::unchecked("from_pool");
        mock_set_pool_connection(
            &mut app,
            vault.clone(),
            CHANNEL_ID.to_string(),
            from_pool.as_bytes().to_vec(),
            true
        );

        // Define the receive asset configuration
        let to_asset_idx = 0;
        let to_asset = vault_tokens[to_asset_idx].clone();
        let to_weight = vault_config.weights[to_asset_idx];
        let to_balance = vault_config.assets_balances[to_asset_idx];
        
        let swap_units = uint!("500000000000000000");



        // Tested action: receive asset
        let response = app.execute_contract(
            Addr::unchecked(CHAIN_INTERFACE),
            vault.clone(),
            &VolatileExecuteMsg::ReceiveAsset {
                channel_id: CHANNEL_ID.to_string(),
                from_pool: from_pool.as_bytes().to_vec(),
                to_asset_index: to_asset_idx as u8,
                to_account: SWAPPER_B.to_string(),
                u: swap_units,
                min_out: Uint128::zero(),
                swap_hash: b"1aefweftegnedtwdwaagwwetgajyrgwd".to_vec(),
                calldata: vec![]
            },
            &[]
        ).unwrap();



        // Verify the swap return
        let expected_return = compute_expected_receive_asset(
            swap_units,
            to_weight,
            to_balance
        );

        let observed_return = get_response_attribute::<Uint128>(response.events[1].clone(), "to_amount").unwrap();
    
        assert!(uint128_to_f64(observed_return) <= expected_return.to_amount * 1.000001);
        assert!(uint128_to_f64(observed_return) >= expected_return.to_amount * 0.999999);

        // Verify the output assets have been transferred to the swapper
        let vault_to_asset_balance = query_token_balance(&mut app, to_asset.clone(), vault.to_string());
        assert_eq!(
            vault_to_asset_balance,
            vault_config.assets_balances[to_asset_idx] - observed_return
        );

        // Verify the output assets have been received by the swapper
        let swapper_to_asset_balance = query_token_balance(&mut app, to_asset.clone(), SWAPPER_B.to_string());
        assert_eq!(
            swapper_to_asset_balance,
            observed_return
        );

    }


    //TODO this test currently fails as transferring a zero-valued amount of a token is not allowed. Do we want this?
    #[test]
    #[ignore]
    fn test_receive_asset_zero_amount() {

        let mut app = App::default();

        // Instantiate and initialize vault
        let vault = mock_instantiate(&mut app, Some(Addr::unchecked(CHAIN_INTERFACE)));
        let vault_tokens = deploy_test_tokens(&mut app, None, None);
        let vault_config = mock_initialize_pool(
            &mut app,
            vault.clone(),
            vault_tokens.iter().map(|token_addr| token_addr.to_string()).collect(),
            vec![Uint128::from(1u64) * WAD, Uint128::from(2u64) * WAD, Uint128::from(3u64) * WAD],
            vec![1u64, 1u64, 1u64]
        );

        // Connect pool with a mock pool
        let from_pool = Addr::unchecked("from_pool");
        mock_set_pool_connection(
            &mut app,
            vault.clone(),
            CHANNEL_ID.to_string(),
            from_pool.as_bytes().to_vec(),
            true
        );

        // Define the receive asset configuration
        let to_asset_idx = 0;
        let to_asset = vault_tokens[to_asset_idx].clone();
        
        let swap_units = U256::ZERO;



        // Tested action: receive asset
        let response = app.execute_contract(
            Addr::unchecked(CHAIN_INTERFACE),
            vault.clone(),
            &VolatileExecuteMsg::ReceiveAsset {
                channel_id: CHANNEL_ID.to_string(),
                from_pool: from_pool.as_bytes().to_vec(),
                to_asset_index: to_asset_idx as u8,
                to_account: SWAPPER_B.to_string(),
                u: swap_units,
                min_out: Uint128::zero(),
                swap_hash: b"1aefweftegnedtwdwaagwwetgajyrgwd".to_vec(),
                calldata: vec![]
            },
            &[]
        ).unwrap();



        // Verify the swap return
        let observed_return = get_response_attribute::<Uint128>(response.events[1].clone(), "to_amount").unwrap();
        assert!(uint128_to_f64(observed_return) == 0.);

        // Verify the vault asset balance remains unchanged
        let vault_to_asset_balance = query_token_balance(&mut app, to_asset.clone(), vault.to_string());
        assert_eq!(
            vault_to_asset_balance,
            vault_config.assets_balances[to_asset_idx]
        );

        // Verify the swapper asset balance remains unchanged
        let swapper_to_asset_balance = query_token_balance(&mut app, to_asset.clone(), SWAPPER_B.to_string());
        assert_eq!(
            swapper_to_asset_balance,
            Uint128::zero()
        );

    }



    #[test]
    fn test_receive_asset_minout() {

        let mut app = App::default();

        // Instantiate and initialize vault
        let vault = mock_instantiate(&mut app, Some(Addr::unchecked(CHAIN_INTERFACE)));
        let vault_tokens = deploy_test_tokens(&mut app, None, None);
        let vault_config = mock_initialize_pool(
            &mut app,
            vault.clone(),
            vault_tokens.iter().map(|token_addr| token_addr.to_string()).collect(),
            vec![Uint128::from(1u64) * WAD, Uint128::from(2u64) * WAD, Uint128::from(3u64) * WAD],
            vec![1u64, 1u64, 1u64]
        );

        // Connect pool with a mock pool
        let from_pool = Addr::unchecked("from_pool");
        mock_set_pool_connection(
            &mut app,
            vault.clone(),
            CHANNEL_ID.to_string(),
            from_pool.as_bytes().to_vec(),
            true
        );

        // Define the receive asset configuration
        let to_asset_idx = 0;
        let to_weight = vault_config.weights[to_asset_idx];
        let to_balance = vault_config.assets_balances[to_asset_idx];
        
        let swap_units = uint!("500000000000000000");
        
        // Compute the expected return
        let expected_return = compute_expected_receive_asset(
            swap_units,
            to_weight,
            to_balance
        ).to_amount;

        // Set min_out_valid to be slightly smaller than the expected return
        let min_out_valid = f64_to_uint128(expected_return * 0.99).unwrap();

        // Set min_out_invalid to be slightly larger than the expected return
        let min_out_invalid = f64_to_uint128(expected_return * 1.01).unwrap();



        // Tested action 1: receive asset with min_out > expected_return fails
        let response_result = app.execute_contract(
            Addr::unchecked(CHAIN_INTERFACE),
            vault.clone(),
            &VolatileExecuteMsg::ReceiveAsset {
                channel_id: CHANNEL_ID.to_string(),
                from_pool: from_pool.as_bytes().to_vec(),
                to_asset_index: to_asset_idx as u8,
                to_account: SWAPPER_B.to_string(),
                u: swap_units,
                min_out: min_out_invalid,
                swap_hash: b"1aefweftegnedtwdwaagwwetgajyrgwd".to_vec(),
                calldata: vec![]
            },
            &[]
        );



        // Make sure the transaction fails
        assert!(matches!(
            response_result.err().unwrap().downcast::<ContractError>().unwrap(),
            ContractError::ReturnInsufficient { min_out: err_min_out, out: err_out}
                if err_min_out == min_out_invalid && err_out < err_min_out
        ));
        


        // Tested action 2: receive asset with min_out <= expected_return succeeds
        app.execute_contract(
            Addr::unchecked(CHAIN_INTERFACE),
            vault.clone(),
            &VolatileExecuteMsg::ReceiveAsset {
                channel_id: CHANNEL_ID.to_string(),
                from_pool: from_pool.as_bytes().to_vec(),
                to_asset_index: to_asset_idx as u8,
                to_account: SWAPPER_B.to_string(),
                u: swap_units,
                min_out: min_out_valid,
                swap_hash: b"1aefweftegnedtwdwaagwwetgajyrgwd".to_vec(),
                calldata: vec![]
            },
            &[]
        ).unwrap();

    }


    #[test]
    fn test_receive_asset_not_connected_pool() {

        let mut app = App::default();

        // Instantiate and initialize vault
        let vault = mock_instantiate(&mut app, Some(Addr::unchecked(CHAIN_INTERFACE)));
        let vault_tokens = deploy_test_tokens(&mut app, None, None);
        mock_initialize_pool(
            &mut app,
            vault.clone(),
            vault_tokens.iter().map(|token_addr| token_addr.to_string()).collect(),
            vec![Uint128::from(1u64) * WAD, Uint128::from(2u64) * WAD, Uint128::from(3u64) * WAD],
            vec![1u64, 1u64, 1u64]
        );

        // ! Do not connect the pool with the mock source pool
        let from_pool = Addr::unchecked("from_pool");

        // Define the receive asset configuration
        let to_asset_idx = 0;
        let swap_units = uint!("500000000000000000");



        // Tested action: receive asset
        let response_result = app.execute_contract(
            Addr::unchecked(CHAIN_INTERFACE),
            vault.clone(),
            &VolatileExecuteMsg::ReceiveAsset {
                channel_id: CHANNEL_ID.to_string(),
                from_pool: from_pool.as_bytes().to_vec(),
                to_asset_index: to_asset_idx as u8,
                to_account: SWAPPER_B.to_string(),
                u: swap_units,
                min_out: Uint128::zero(),
                swap_hash: b"1aefweftegnedtwdwaagwwetgajyrgwd".to_vec(),
                calldata: vec![]
            },
            &[]
        );



        // Make sure the transaction fails
        assert!(matches!(
            response_result.err().unwrap().downcast().unwrap(),
            ContractError::PoolNotConnected { channel_id: err_channel_id, pool: err_pool }
                if err_channel_id == CHANNEL_ID && err_pool == from_pool.as_bytes().to_vec()
        ));

    }


    #[test]
    fn test_receive_asset_invalid_to_asset_index() {

        let mut app = App::default();

        // Instantiate and initialize vault
        let vault = mock_instantiate(&mut app, Some(Addr::unchecked(CHAIN_INTERFACE)));
        let vault_tokens = deploy_test_tokens(&mut app, None, None);
        mock_initialize_pool(
            &mut app,
            vault.clone(),
            vault_tokens.iter().map(|token_addr| token_addr.to_string()).collect(),
            vec![Uint128::from(1u64) * WAD, Uint128::from(2u64) * WAD, Uint128::from(3u64) * WAD],
            vec![1u64, 1u64, 1u64]
        );

        // Connect pool with a mock pool
        let from_pool = Addr::unchecked("from_pool");
        mock_set_pool_connection(
            &mut app,
            vault.clone(),
            CHANNEL_ID.to_string(),
            from_pool.as_bytes().to_vec(),
            true
        );

        // Define the receive asset configuration
        let to_asset_idx = 3;   // ! Invalid index (index 3 = 4th asset)
        let swap_units = uint!("500000000000000000");



        // Tested action: receive asset
        let response_result = app.execute_contract(
            Addr::unchecked(CHAIN_INTERFACE),
            vault.clone(),
            &VolatileExecuteMsg::ReceiveAsset {
                channel_id: CHANNEL_ID.to_string(),
                from_pool: from_pool.as_bytes().to_vec(),
                to_asset_index: to_asset_idx as u8,
                to_account: SWAPPER_B.to_string(),
                u: swap_units,
                min_out: Uint128::zero(),
                swap_hash: b"1aefweftegnedtwdwaagwwetgajyrgwd".to_vec(),
                calldata: vec![]
            },
            &[]
        );



        // Make sure the transaction fails
        assert!(matches!(
            response_result.err().unwrap().downcast().unwrap(),
            ContractError::GenericError {}      //TODO error
        ));

    }


    #[test]
    fn test_receive_asset_caller_not_interface() {

        let mut app = App::default();

        // Instantiate and initialize vault
        let vault = mock_instantiate(&mut app, Some(Addr::unchecked(CHAIN_INTERFACE)));
        let vault_tokens = deploy_test_tokens(&mut app, None, None);
        mock_initialize_pool(
            &mut app,
            vault.clone(),
            vault_tokens.iter().map(|token_addr| token_addr.to_string()).collect(),
            vec![Uint128::from(1u64) * WAD, Uint128::from(2u64) * WAD, Uint128::from(3u64) * WAD],
            vec![1u64, 1u64, 1u64]
        );

        // Connect pool with a mock pool
        let from_pool = Addr::unchecked("from_pool");
        mock_set_pool_connection(
            &mut app,
            vault.clone(),
            CHANNEL_ID.to_string(),
            from_pool.as_bytes().to_vec(),
            true
        );

        // Define the receive asset configuration
        let to_asset_idx = 0;
        let swap_units = uint!("500000000000000000");



        // Tested action: receive asset
        let response_result = app.execute_contract(
            Addr::unchecked("not_chain_interface"),     // ! Caller is not CHAIN_INTERFACE
            vault.clone(),
            &VolatileExecuteMsg::ReceiveAsset {
                channel_id: CHANNEL_ID.to_string(),
                from_pool: from_pool.as_bytes().to_vec(),
                to_asset_index: to_asset_idx as u8,
                to_account: SWAPPER_B.to_string(),
                u: swap_units,
                min_out: Uint128::zero(),
                swap_hash: b"1aefweftegnedtwdwaagwwetgajyrgwd".to_vec(),
                calldata: vec![]
            },
            &[]
        );



        // Make sure the transaction fails
        assert!(matches!(
            response_result.err().unwrap().downcast().unwrap(),
            ContractError::Unauthorized {}
        ));

    }

}