import streamlit as st
from planner_agent import create_investment_plan
from styles import apply_custom_styles, create_success_banner
import time

# Apply custom styling
apply_custom_styles()

st.set_page_config(
    page_title="GoalWealth - Investment Planning Platform",
    page_icon="📈",
    layout="wide"
)

# Welcome banner (only show once per session)
if 'welcomed' not in st.session_state:
    st.session_state.welcomed = True
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
    ">
        <h2 style="margin: 0; color: white; border: none;">👋 Welcome to GoalWealth!</h2>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem;">
            Your AI-powered companion for multi-channel investment planning.
            Get started by filling out your profile in the sidebar! →
        </p>
    </div>
    """, unsafe_allow_html=True)

st.title("GoalWealth")
st.subheader("Multi-Channel Investment Planner")
st.markdown("*Traditional Markets | Cryptocurrency | Solana DeFi | Alternative Assets*")
st.markdown("---")

st.sidebar.header("Your Profile")
st.sidebar.markdown("Tell us about yourself:")

currency = st.sidebar.selectbox(
    "Currency",
    ["USD ($)", "EUR (€)", "GBP (£)", "NGN (₦)", "JPY (¥)", "CAD ($)", "AUD ($)", "INR (₹)"],
    index=0
)

currency_symbol = currency.split("(")[1].split(")")[0]
currency_code = currency.split(" ")[0]

age = st.sidebar.number_input("Age", min_value=18, max_value=80, value=30)
income = st.sidebar.number_input(f"Annual Income ({currency_symbol})", min_value=0, max_value=10000000, value=60000, step=5000)
capital = st.sidebar.number_input(f"Starting Capital ({currency_symbol})", min_value=0, max_value=100000000, value=10000, step=1000)
monthly = st.sidebar.number_input(f"Monthly Investment ({currency_symbol})", min_value=0, max_value=1000000, value=500, step=100)
timeline = st.sidebar.slider("Investment Timeline (years)", min_value=1, max_value=50, value=30)
risk_tolerance = st.sidebar.selectbox("Risk Tolerance", ["Low", "Medium", "High"])
goal = st.sidebar.text_area("Investment Goal", "Build wealth for retirement")

# Opportunities Section in Sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("💡 Opportunities")

from opportunities import check_opportunities

user_profile_opportunities = {
    'age': age,
    'risk_tolerance': risk_tolerance,
    'capital': capital
}

try:
    opportunities = check_opportunities(user_profile_opportunities)
    
    if opportunities:
        for idx, opp in enumerate(opportunities[:2], 1):  # Show top 2
            with st.sidebar.expander(f"💡 Opportunity {idx}: {opp['type']}", expanded=False):
                st.write(f"**{opp['asset']}**")
                st.write(opp['reason'])
                st.write(f"*Action:* {opp['action']}")
                st.caption(f"Risk: {opp['risk']}")
    else:
        st.sidebar.info("No special opportunities at the moment")
except Exception as e:
    st.sidebar.caption("Opportunities loading...")

# Tips & Shortcuts
with st.expander("⌨️ Quick Tips & Navigation"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **Getting Started:**
        - Fill out your profile →
        - Generate your plan
        - Track your portfolio
        - Ask questions anytime
        """)
    with col2:
        st.markdown("""
        **Tab Navigation:**
        - **Tab 1:** Create investment plan
        - **Tab 2:** Track live portfolio
        - **Tab 3:** Ask the AI advisor
        - **Tab 4:** Learn with guides
        """)
    with col3:
        st.markdown("""
        **Pro Tips:**
        - Download your plans
        - Generate learning guides
        - Check opportunity alerts
        - Review strategy templates
        """)

tab1, tab2, tab3, tab4 = st.tabs(["Create Plan", "Portfolio Tracker", "Advisor Chat", "Resources"])

with tab1:
    st.header("Create Your Personalized Investment Plan")
    
    st.info("""
    Your Comprehensive Investment Strategy Includes:
    - Risk assessment and asset allocation
    - Traditional markets (Stocks, Bonds, ETFs)
    - Cryptocurrency portfolio (Bitcoin, Ethereum, Solana)
    - Solana DeFi strategies (Jito, Raydium, Kamino, Jupiter, Arcium)
    - Alternative investments (Real Estate, Gold)
    - Multi-layer passive income opportunities
    - 30-year wealth projections
    - Step-by-step implementation guide
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Age", f"{age} years")
    with col2:
        st.metric("Capital", f"{currency_symbol}{capital:,}")
    with col3:
        st.metric("Monthly", f"{currency_symbol}{monthly:,}")
    with col4:
        st.metric("Timeline", f"{timeline} years")
    
    if st.button("Generate Investment Plan", type="primary", use_container_width=True):
        
        user_profile = {
            'age': age,
            'income': income,
            'capital': capital,
            'monthly': monthly,
            'timeline': timeline,
            'risk_tolerance': risk_tolerance,
            'goal': goal,
            'currency': currency_code,
            'currency_symbol': currency_symbol
        }
        
        with st.spinner("🔄 Creating your personalized investment strategy..."):
            try:
                plan = create_investment_plan(user_profile)
                
                if plan and len(plan) > 100:  # Verify it's a real plan
                    st.markdown(create_success_banner("Your GoalWealth Investment Plan is Ready!"), unsafe_allow_html=True)
                    st.markdown("---")
                    
                    with st.expander("📋 View Complete Investment Plan", expanded=True):
                        st.markdown(plan)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="📥 Download Plan",
                            data=plan,
                            file_name=f"goalwealth_plan_{age}yo_{capital}{currency_code}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    with col2:
                        st.info("💡 Follow the implementation guide in your plan")
                    
                    # Show next steps
                    st.markdown("### 🎯 Your Next Steps")
                    st.markdown("""
                    1. ✅ Review your personalized plan carefully
                    2. 📅 Note the week-by-week execution timeline
                    3. 📊 Visit **Portfolio Tracker** to monitor investments
                    4. 💬 Use **Advisor Chat** for any questions
                    5. 📚 Check **Resources** for educational guides
                    """)
                else:
                    st.error("⚠️ Plan generation returned incomplete data. Please try again.")
                    
            except Exception as e:
                st.error(f"❌ Error generating plan: {str(e)}")
                st.info("💡 Try refreshing the page or check your internet connection.")

with tab2:
    st.header("Portfolio Tracker")
    
    st.markdown("Track your complete investment portfolio across all channels")
    
    with st.expander("Enter Your Holdings", expanded=False):
        st.subheader("Traditional Markets")
        col1, col2 = st.columns(2)
        
        with col1:
            vti_shares = st.number_input("VTI Shares", min_value=0.0, value=0.0, step=1.0)
            bnd_shares = st.number_input("BND Shares", min_value=0.0, value=0.0, step=1.0)
            vxus_shares = st.number_input("VXUS Shares", min_value=0.0, value=0.0, step=1.0)
        
        with col2:
            vnq_shares = st.number_input("VNQ Shares", min_value=0.0, value=0.0, step=1.0)
            gld_shares = st.number_input("GLD Shares", min_value=0.0, value=0.0, step=1.0)
        
        st.subheader("Cryptocurrency")
        col3, col4 = st.columns(2)
        
        with col3:
            btc_amount = st.number_input("Bitcoin (BTC)", min_value=0.0, value=0.0, step=0.01, format="%.4f")
            eth_amount = st.number_input("Ethereum (ETH)", min_value=0.0, value=0.0, step=0.1, format="%.4f")
            sol_amount = st.number_input("Solana (SOL)", min_value=0.0, value=0.0, step=1.0, format="%.2f")
        
        with col4:
            ray_amount = st.number_input("Raydium (RAY)", min_value=0.0, value=0.0, step=10.0, format="%.2f")
            jup_amount = st.number_input("Jupiter (JUP)", min_value=0.0, value=0.0, step=10.0, format="%.2f")
        
        track_button = st.button("Update Portfolio", type="primary", use_container_width=True)
    
    if track_button or any([vti_shares, bnd_shares, vxus_shares, vnq_shares, gld_shares, btc_amount, eth_amount, sol_amount, ray_amount, jup_amount]):
        
        # Progress indicator
        progress_text = st.empty()
        progress_bar = st.progress(0)
        
        try:
            progress_text.text("🔄 Fetching live market data...")
            progress_bar.progress(20)
            
            from market_data import get_stock_prices, get_crypto_prices, calculate_portfolio_value
            
            holdings = {'stocks': {}, 'crypto': {}}
            
            if vti_shares > 0:
                holdings['stocks']['VTI'] = vti_shares
            if bnd_shares > 0:
                holdings['stocks']['BND'] = bnd_shares
            if vxus_shares > 0:
                holdings['stocks']['VXUS'] = vxus_shares
            if vnq_shares > 0:
                holdings['stocks']['VNQ'] = vnq_shares
            if gld_shares > 0:
                holdings['stocks']['GLD'] = gld_shares
            
            if btc_amount > 0:
                holdings['crypto']['bitcoin'] = btc_amount
            if eth_amount > 0:
                holdings['crypto']['ethereum'] = eth_amount
            if sol_amount > 0:
                holdings['crypto']['solana'] = sol_amount
            if ray_amount > 0:
                holdings['crypto']['raydium'] = ray_amount
            if jup_amount > 0:
                holdings['crypto']['jupiter-exchange-solana'] = jup_amount
            
            progress_bar.progress(40)
            progress_text.text("📊 Calculating prices...")
            
            stock_tickers = list(holdings.get('stocks', {}).keys())
            crypto_symbols = list(holdings.get('crypto', {}).keys())
            
            stock_prices = get_stock_prices(stock_tickers) if stock_tickers else {}
            crypto_prices = get_crypto_prices(crypto_symbols) if crypto_symbols else {}
            
            progress_bar.progress(80)
            progress_text.text("📈 Building portfolio...")
            
            portfolio = calculate_portfolio_value(holdings, stock_prices, crypto_prices)
            
            progress_bar.progress(100)
            progress_text.text("✅ Portfolio updated!")
            
            # Clear progress indicators
            time.sleep(0.5)
            progress_text.empty()
            progress_bar.empty()
            
            st.markdown("---")
            col1, col2, col3, col4 = st.columns(4)
            
            total_value = portfolio['total']
            traditional_value = portfolio['traditional']
            crypto_value = portfolio['crypto']
            
            with col1:
                st.metric("Total Portfolio Value", f"{currency_symbol}{total_value:,.2f}")
            
            with col2:
                st.metric("Traditional Markets", f"{currency_symbol}{traditional_value:,.2f}", f"{(traditional_value/total_value*100) if total_value > 0 else 0:.1f}%")
            
            with col3:
                st.metric("Cryptocurrency", f"{currency_symbol}{crypto_value:,.2f}", f"{(crypto_value/total_value*100) if total_value > 0 else 0:.1f}%")
            
            with col4:
                total_change = 0
                if portfolio['details']:
                    for detail in portfolio['details']:
                        weight = detail['value'] / total_value if total_value > 0 else 0
                        total_change += detail['change'] * weight
                
                st.metric("24h Change", f"{total_change:+.2f}%", f"{currency_symbol}{(total_value * total_change / 100):+,.2f}")
            
            st.markdown("---")
            st.subheader("Your Holdings")
            
            if portfolio['details']:
                import pandas as pd
                
                df_data = []
                for detail in portfolio['details']:
                    df_data.append({
                        'Asset': detail['asset'],
                        'Ticker': detail['ticker'],
                        'Type': detail['type'].title(),
                        'Amount': f"{detail['amount']:.4f}" if detail['type'] == 'crypto' else f"{detail['amount']:.0f}",
                        'Price': f"{currency_symbol}{detail['price']:,.2f}",
                        'Value': f"{currency_symbol}{detail['value']:,.2f}",
                        '24h Change': f"{detail['change']:+.2f}%",
                        'Allocation': f"{(detail['value']/total_value*100):.1f}%"
                    })
                
                df = pd.DataFrame(df_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                st.markdown("---")
                st.subheader("Portfolio Allocation")
                
                import plotly.graph_objects as go
                
                labels = [d['asset'] for d in portfolio['details']]
                values = [d['value'] for d in portfolio['details']]
                
                fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
                fig.update_layout(title="Asset Distribution", height=500)
                st.plotly_chart(fig, use_container_width=True)
            
            else:
                st.info("No holdings to display")
                
        except Exception as e:
            if 'progress_text' in locals():
                progress_text.empty()
            if 'progress_bar' in locals():
                progress_bar.empty()
            st.error(f"❌ Error fetching portfolio data: {str(e)}")
            st.info("💡 Please check your internet connection and try again.")
    
    else:
        st.info("Enter your holdings above to see your live portfolio")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Portfolio Value", f"{currency_symbol}0.00")
        with col2:
            st.metric("Total Returns", f"{currency_symbol}0.00", "0%")
        with col3:
            st.metric("24h Change", "0%")

with tab3:
    st.header("Investment Advisor")
    
    st.markdown("Ask anything about investing, Solana DeFi, or portfolio strategy")
    
    with st.expander("Example Questions", expanded=False):
        st.markdown("""
        **General Investing:**
        - Should I buy Bitcoin or Solana right now?
        - Is it a good time to invest with current market volatility?
        
        **Solana DeFi:**
        - How does Jito staking work and is it safe?
        - What is impermanent loss in Raydium pools?
        
        **Risk Management:**
        - What are the risks of DeFi protocols?
        - How much should I allocate to crypto vs stocks?
        """)
    
    st.markdown("---")
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(chat['question'])
        with st.chat_message("assistant"):
            st.write(chat['answer'])
    
    user_question = st.chat_input("Ask your investment question...")
    
    if user_question:
        with st.chat_message("user"):
            st.write(user_question)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                from advisor_agent import get_investment_advice
                
                user_context = {
                    'age': age,
                    'risk_tolerance': risk_tolerance,
                    'portfolio_value': f"{currency_symbol}{capital:,}",
                    'timeline': timeline
                }
                
                answer = get_investment_advice(user_question, user_context)
                st.write(answer)
        
        st.session_state.chat_history.append({'question': user_question, 'answer': answer})
        st.rerun()
    
    if st.session_state.chat_history:
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

with tab4:
    st.header("Investment Resources")
    
    st.markdown("Learn about investing through AI-generated educational guides")
    
    # Guide Generator Section
    st.subheader("📚 Generate Learning Guides")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        from education_agent import AVAILABLE_GUIDES, generate_guide
        
        selected_topic = st.selectbox(
            "Select a topic to learn about:",
            list(AVAILABLE_GUIDES.keys())
        )
    
    with col2:
        user_level = st.selectbox(
            "Experience level:",
            ["Beginner", "Intermediate", "Advanced"]
        )
    
    if st.button("Generate Learning Guide", type="primary", use_container_width=True):
        with st.spinner(f"Creating personalized guide on {selected_topic}..."):
            guide = generate_guide(selected_topic, user_level.lower())
            
            st.markdown("---")
            st.success(f"Guide Created: {selected_topic}")
            
            with st.expander(f"📖 {selected_topic} - {user_level} Level", expanded=True):
                st.markdown(guide)
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "Download Guide as Text",
                    guide,
                    file_name=f"goalwealth_guide_{AVAILABLE_GUIDES[selected_topic]}_{user_level.lower()}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            with col2:
                if st.button("Generate Another Guide", use_container_width=True):
                    st.rerun()
    
    # Quick Reference Section
    st.markdown("---")
    st.subheader("📋 Quick Reference")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Traditional Investing Basics:**
        - **VTI:** Total US stock market ETF
          - Diversification: 3,500+ companies
          - Expected return: 8-10% annually
          - Risk: Medium
        
        - **BND:** Total bond market ETF
          - Stability and income focus
          - Expected return: 3-4% annually
          - Risk: Low
        
        - **VXUS:** International stocks
          - Global diversification
          - Expected return: 7-9% annually
          - Risk: Medium-High
        
        - **VNQ:** Real estate (REITs)
          - Dividend income: 3-5% annually
          - Expected return: 8-10% total
          - Risk: Medium
        
        **Cryptocurrency Fundamentals:**
        - **Bitcoin (BTC):** Digital gold, store of value
          - Market cap leader
          - Historical return: 15%+ annually (volatile)
          
        - **Ethereum (ETH):** Smart contracts platform
          - DeFi foundation
          - Staking available: 3-5% APY
          
        - **Solana (SOL):** High-speed blockchain
          - Low transaction costs
          - Growing DeFi ecosystem
        """)
    
    with col2:
        st.markdown("""
        **Solana DeFi Protocols:**
        
        **🔸 Jito (Liquid Staking)**
        - Website: jito.network
        - APY: 8-9% (with MEV rewards)
        - Risk: Low
        - Benefit: Liquid staking token (JitoSOL)
        - Best for: Passive income seekers
        
        **🔸 Raydium (DEX & Liquidity)**
        - Website: raydium.io
        - APY: 20-25% (liquidity pools)
        - Risk: Medium-High (impermanent loss)
        - Token: RAY
        - Best for: Active DeFi participants
        
        **🔸 Kamino Finance (Vaults)**
        - Website: kamino.finance
        - APY: 25-35% (automated strategies)
        - Risk: High (leverage, liquidation)
        - Best for: Experienced DeFi users
        
        **🔸 Jupiter (DEX Aggregator)**
        - Website: jup.ag
        - Function: Best swap prices
        - Token: JUP (governance)
        - Best for: All traders
        
        **🔸 Arcium (Privacy SDK)**
        - Website: arcium.io
        - Function: Confidential transactions
        - NOT an investment - it's a tool
        - Use: Private transfers between protocols
        """)
    
    # Strategy Templates
    st.markdown("---")
    st.subheader("💡 Strategy Templates")
    
    strategy_type = st.selectbox(
        "Select investment strategy type:",
        [
            "Conservative Income Focus",
            "Balanced Growth & Income", 
            "Aggressive Growth",
            "Solana DeFi Maximalist"
        ]
    )
    
    strategies = {
        "Conservative Income Focus": {
            "allocation": "60% Bonds, 30% Stocks, 10% Crypto",
            "goal": "Preserve capital and generate steady income",
            "expected_return": "4-6% annually",
            "risk": "Low",
            "implementation": [
                "60% in BND (Total Bond Market)",
                "20% in VTI (US Stocks)",
                "10% in VXUS (International)",
                "7% in Bitcoin (store of value)",
                "3% in Jito staked SOL (8% yield)"
            ]
        },
        "Balanced Growth & Income": {
            "allocation": "50% Stocks, 30% Bonds, 20% Crypto/Alts",
            "goal": "Long-term growth with income generation",
            "expected_return": "7-9% annually",
            "risk": "Medium",
            "implementation": [
                "35% in VTI (US Stocks)",
                "15% in VXUS (International)",
                "30% in BND (Bonds)",
                "10% in Bitcoin/Ethereum",
                "5% in Jito staked SOL",
                "5% in REITs (VNQ)"
            ]
        },
        "Aggressive Growth": {
            "allocation": "70% Stocks, 25% Crypto, 5% Bonds",
            "goal": "Maximum growth over long timeline",
            "expected_return": "12-15% annually",
            "risk": "High",
            "implementation": [
                "50% in VTI (US Stocks)",
                "20% in VXUS (International)",
                "15% in Bitcoin/Solana",
                "10% in Jito + Raydium",
                "5% in Bonds (stability)"
            ]
        },
        "Solana DeFi Maximalist": {
            "allocation": "60% Solana DeFi, 30% SOL/BTC/ETH, 10% Traditional",
            "goal": "Maximize returns through Solana ecosystem",
            "expected_return": "20-30% annually (high volatility)",
            "risk": "Very High",
            "implementation": [
                "25% in Jito staked SOL (8-9% APY)",
                "20% in Raydium pools (20-25% APY)",
                "15% in Kamino vaults (25-35% APY)",
                "10% in Bitcoin (hedge)",
                "10% in raw SOL (holding)",
                "10% in ETH (diversification)",
                "10% in VTI (stability)"
            ]
        }
    }
    
    selected_strategy = strategies[strategy_type]
    
    with st.expander(f"View {strategy_type} Details", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Allocation:** {selected_strategy['allocation']}")
            st.write(f"**Goal:** {selected_strategy['goal']}")
        
        with col2:
            st.write(f"**Expected Return:** {selected_strategy['expected_return']}")
            st.write(f"**Risk Level:** {selected_strategy['risk']}")
        
        st.markdown("**Implementation:**")
        for item in selected_strategy['implementation']:
            st.write(f"- {item}")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p><b>GoalWealth</b> - Advanced Investment Planning Platform</p>
    <p>Multi-Channel Diversification | Solana DeFi Integration | AI-Powered Guidance</p>
    <p>Built for Anthropic x Comet Hackathon 2025</p>
</div>
""", unsafe_allow_html=True)