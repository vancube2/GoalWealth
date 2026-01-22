from opik import track

@track(project_name="goalwealth", tags=["opportunities"])
def check_opportunities(user_profile):
    """
    Check for investment opportunities based on market conditions and user profile
    
    Args:
        user_profile: Dict with 'age', 'risk_tolerance', 'capital'
    
    Returns:
        List of opportunity dicts with type, asset, reason, action, risk
    """
    
    opportunities = []
    
    try:
        # Try to get live market data
        from market_data import get_crypto_prices
        
        crypto_prices = get_crypto_prices(['solana', 'bitcoin', 'ethereum'])
        
        sol_price = crypto_prices.get('solana', {}).get('price', 0)
        sol_change = crypto_prices.get('solana', {}).get('change_24h', 0)
        btc_change = crypto_prices.get('bitcoin', {}).get('change_24h', 0)
        
        # Opportunity 1: Solana Dip Buy
        if sol_change < -5:
            opportunities.append({
                'type': 'BUY_DIP',
                'asset': 'Solana (SOL)',
                'reason': f'SOL is down {abs(sol_change):.1f}% in 24h - potential buy opportunity',
                'action': f'Consider buying at ${sol_price:.2f} and dollar-cost averaging',
                'risk': 'Medium'
            })
        
        # Opportunity 2: Market Volatility = Staking Time
        if abs(sol_change) > 3:
            opportunities.append({
                'type': 'YIELD_FARMING',
                'asset': 'Jito Staking',
                'reason': f'Market volatility ({abs(sol_change):.1f}%) - lock in stable 8-9% APY',
                'action': 'Stake SOL on Jito (jito.network) for MEV rewards',
                'risk': 'Low'
            })
        
        # Opportunity 3: High Risk Tolerance = DeFi
        if user_profile.get('risk_tolerance') == 'High':
            opportunities.append({
                'type': 'DEFI_POOLS',
                'asset': 'Raydium Liquidity Pools',
                'reason': 'High risk tolerance - eligible for 20-25% APY liquidity pools',
                'action': 'Provide SOL-USDC liquidity on Raydium (raydium.io)',
                'risk': 'High (Impermanent Loss)'
            })
        
        # Opportunity 4: Large Capital = Kamino Vaults
        if user_profile.get('capital', 0) > 5000 and user_profile.get('risk_tolerance') in ['Medium', 'High']:
            opportunities.append({
                'type': 'AUTOMATED_VAULTS',
                'asset': 'Kamino Finance Vaults',
                'reason': f'Capital of ${user_profile["capital"]:,} can benefit from automated strategies',
                'action': 'Explore Kamino vaults (kamino.finance) for 25-35% APY',
                'risk': 'High (Leverage Risk)'
            })
        
        # Opportunity 5: Bitcoin Dip (for conservative investors)
        if btc_change < -3 and user_profile.get('risk_tolerance') in ['Low', 'Medium']:
            opportunities.append({
                'type': 'BTC_DCA',
                'asset': 'Bitcoin (BTC)',
                'reason': f'BTC down {abs(btc_change):.1f}% - good time to dollar-cost average',
                'action': 'Add to Bitcoin holdings as digital gold hedge',
                'risk': 'Medium'
            })
        
        # Opportunity 6: Rebalancing Alert
        if user_profile.get('age', 30) < 35 and user_profile.get('risk_tolerance') != 'High':
            opportunities.append({
                'type': 'REBALANCE',
                'asset': 'Portfolio Rebalance',
                'reason': 'Young age + long timeline - consider increasing growth allocation',
                'action': 'Review portfolio: Target 70% stocks, 20% crypto, 10% bonds',
                'risk': 'Low'
            })
        
    except Exception as e:
        # Fallback opportunities if market data fails
        opportunities = [
            {
                'type': 'JITO_STAKING',
                'asset': 'Jito Liquid Staking',
                'reason': 'Earn stable 8-9% APY with low risk',
                'action': 'Visit jito.network to stake SOL',
                'risk': 'Low'
            },
            {
                'type': 'EDUCATION',
                'asset': 'Learning Resources',
                'reason': 'Build your knowledge before investing',
                'action': 'Check the Resources tab for guides',
                'risk': 'None'
            }
        ]
    
    return opportunities


# For testing
if __name__ == "__main__":
    test_profile = {
        'age': 30,
        'risk_tolerance': 'High',
        'capital': 15000
    }
    
    opps = check_opportunities(test_profile)
    
    print(f"\nFound {len(opps)} opportunities:\n")
    for i, opp in enumerate(opps, 1):
        print(f"{i}. {opp['type']}: {opp['asset']}")
        print(f"   Reason: {opp['reason']}")
        print(f"   Action: {opp['action']}")
        print(f"   Risk: {opp['risk']}\n")