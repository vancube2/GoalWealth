import streamlit as st

st.set_page_config(
    page_title="GoalWealth - Investment Planning Platform",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

from planner_agent import create_investment_plan
from styles import apply_custom_styles, create_success_banner, create_hero_section, create_stat_card, create_metric_card_large, get_section_background
import time
import plotly.graph_objects as go
from streamlit_mic_recorder import mic_recorder
from voice_processor import extract_profile_from_voice, process_voice_advisor_query, transcribe_voice
from live_data import get_live_market_data, get_defi_yields, get_portfolio_growth_projection
from solana_service import get_solana_service


import base64
from pathlib import Path

def get_logo_base64(filename):
    """Load local logo and convert to base64 for embedding"""
    try:
        logo_path = Path(__file__).parent / 'assets' / 'logos' / filename
        if logo_path.exists():
            with open(logo_path, 'rb') as f:
                return base64.b64encode(f.read()).decode()
    except:
        pass
    return None

def get_asset_logo(symbol):
    """Returns local logo as base64 data URI"""
    symbol = symbol.upper()
    
    # Map symbols to local logo files - GLOBAL SCALE
    logo_map = {
        # Crypto
        'BTC': 'btc.png', 'ETH': 'eth.png', 'SOL': 'sol.png',
        'BNB': 'bnb.png', 'XRP': 'xrp.png', 'ADA': 'ada.png',
        'AVAX': 'avax.png', 'LINK': 'link.png', 'DOT': 'dot.png',
        'JUP': 'jup.png', 'RAY': 'ray.png', 'JITO': 'jito.png',
        'MSOL': 'msol.png', 'PYTH': 'pyth.png', 'BONK': 'bonk.png',
        'USDC': 'usdc.png', 'USDT': 'usdt.png',
        
        # Major US Stocks
        'AAPL': 'aapl.png', 'MSFT': 'msft.png', 'NVDA': 'nvda.png',
        'GOOGL': 'googl.png', 'AMZN': 'amzn.png', 'META': 'meta.png',
        'TSLA': 'tsla.png', 'BRK-B': 'brk-b.png', 'V': 'v.png',
        'MA': 'ma.png', 'UNH': 'unh.png', 'JNJ': 'jnj.png',
        'JPM': 'jpm.png', 'WMT': 'wmt.png', 'XOM': 'xom.png',
        'CVX': 'cvx.png', 'AMD': 'amd.png', 'NFLX': 'nflx.png',
        'DIS': 'dis.png', 'COST': 'cost.png', 'GS': 'gs.png',
        'HD': 'hd.png', 'PEP': 'pep.png', 'KO': 'ko.png',
        
        # Global Stocks
        'ASML': 'asml.png', 'SAP': 'sap.png', 'SAMSUNG': 'samsung.png',
        'TOYOTA': 'tm.png', 'SONY': 'sony.png', 'LVMH': 'mc.png',
        'HSBA': 'hsba.png', 'BP': 'bp.png',
        
        # ETFs
        'VTI': 'vti.png', 'SPY': 'spy.png', 'QQQ': 'qqq.png',
        'DIA': 'dia.png', 'VNQ': 'vnq.png', 'VWO': 'vwo.png',
        'EFA': 'efa.png', 'EWJ': 'ewj.png', 'EWG': 'ewg.png',
        'IVV': 'ivv.png', 'VOO': 'voo.png', 'TLT': 'tlt.png',
        'BND': 'bnd.png', 'USO': 'uso.png', 'GDX': 'gdx.png',
        'VT': 'vt.png', 'VXUS': 'vxus.png', 'VEA': 'vea.png',
        'GLD': 'gld.png', 'GOLD': 'gold.png',
        'SILVER': 'silver.png', 'OIL': 'oil.png',
        
        # Currencies (Mapped from icons)
        'USD': 'usdc.png', 'EUR': 'eur.png', 'GBP': 'gbp.png',
        'JPY': 'jpy.png', 'NGN': 'ngn.png'
    }
    
    filename = logo_map.get(symbol)
    if filename:
        b64 = get_logo_base64(filename)
        if b64:
            return f"data:image/png;base64,{b64}"
    
    # Fallback to emoji for assets without downloaded logos
    emoji_map = {
        'BTC': '₿', 'ETH': 'Ξ', 'SOL': '◎', 'BNB': '🔶',
        'VTI': '📊', 'BND': '📜', 'GOLD': '🟡', 'BONDS': '📜',
        'AAPL': '🍎', 'TSLA': '⚡', 'NVDA': '🟩'
    }
    return emoji_map.get(symbol, '💰')

def get_protocol_logo(name):
    """Returns protocol logo - using local files if available else emojis"""
    # Map names/symbols to files
    protocol_map = {
        'Jito Staking': 'jito.png',
        'Jitovaults': 'jito.png',
        'Raydium Pools': 'ray.png',
        'Raydium': 'ray.png',
        'Kamino Vaults': 'kamino.png',
        'Kamino': 'kamino.png',
        'Orca Whirlpools': 'orca.png',
        'Orca': 'orca.png',
        'Marinade Native': 'marinade.png',
        'Marinade': 'marinade.png',
        'Solend Lending': 'solend.png',
        'Solend': 'solend.png',
        'Marginfi Yield': 'marginfi.png',
        'Marginfi': 'marginfi.png'
    }
    
    filename = protocol_map.get(name)
    if filename:
        b64 = get_logo_base64(filename)
        if b64:
            return f"data:image/png;base64,{b64}"

    icons = {
        'Jito Staking': '🥩', 'Raydium Pools': '🔆',
        'Kamino Vaults': '⚡', 'Marinade Native': '💧',
        'Orca Whirlpools': '🐋', 'Solend Lending': '🏦'
    }
    return icons.get(name, '💰')

def render_asset_icon(icon_val, class_name="ticker-logo", style=""):
    """Helper to render either a base64 img or an emoji div correctly"""
    if isinstance(icon_val, str) and icon_val.startswith('data:image'):
        return f'<img src="{icon_val}" class="{class_name}" style="{style}">'
    else:
        # It's an emoji
        return f'<div class="ticker-icon" style="display:inline-block; {style}">{icon_val}</div>'

# Apply professional financial dashboard styling
apply_custom_styles()

# Common chart dark configuration
def get_dark_chart_layout(height=350):
    return dict(
        height=height,
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Plus Jakarta Sans', color='#94A3B8', size=12),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False),
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#F8FAFC'))
    )

# Hero section (only show once per session)
if 'welcomed' not in st.session_state:
    st.session_state.welcomed = True
if 'is_pro' not in st.session_state:
    st.session_state.is_pro = False
    st.markdown(create_hero_section(), unsafe_allow_html=True)
else:
    # Smaller header for subsequent visits
    st.markdown("""
    <div style="margin-bottom: 2rem; display: flex; align-items: center; justify-content: space-between;">
        <h2 style="margin: 0; background: linear-gradient(to right, #fff, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">GoalWealth Dashboard</h2>
        <span style="color: #94A3B8; font-family: 'JetBrains Mono'; font-size: 0.9rem;">LIVE CONNECTION ●</span>
    </div>
    """, unsafe_allow_html=True)

# Sidebar - Professional Configuration Panel
with st.sidebar:
    # Logo Display - Fixed for transparency and size
    st.image("assets/logo.png", width=200) 
    st.markdown("---")
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(99, 102, 241, 0.1) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
    ">
        <h3 style="margin: 0 0 0.5rem 0; font-size: 1.1rem; color: #fff;">PROFILE</h3>
        <p style="margin: 0; font-size: 0.85rem; color: #94A3B8;">Customize your parameters</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Voice Setup Trigger
    st.markdown("##### 🎙️ Voice Setup")
    voice_profile = mic_recorder(
        start_prompt="Start Recording",
        stop_prompt="Stop Recording",
        just_once=True,
        use_container_width=True,
        key="voice_profile"
    )
    
    if voice_profile and 'bytes' in voice_profile:
        with st.spinner("Analyzing audio..."):
            extracted = extract_profile_from_voice(voice_profile['bytes'])
            
            if extracted and "error" not in extracted:
                updated = False
                if extracted.get('age'): 
                    st.session_state['age_val'] = int(extracted['age'])
                    updated = True
                if extracted.get('income'): 
                    st.session_state['income_val'] = int(extracted['income'])
                    updated = True
                if extracted.get('capital'): 
                    st.session_state['capital_val'] = int(extracted['capital'])
                    updated = True
                if extracted.get('monthly'): 
                    st.session_state['monthly_val'] = int(extracted['monthly'])
                    updated = True
                if extracted.get('timeline'): 
                    st.session_state['timeline_val'] = int(extracted['timeline'])
                    updated = True
                if extracted.get('risk_tolerance'): 
                    st.session_state['risk_val'] = extracted['risk_tolerance']
                    updated = True
                if extracted.get('goal'): 
                    st.session_state['goal_val'] = extracted['goal']
                    updated = True
                
                if updated:
                    st.success("Profile updated via voice!")
                    st.rerun()
                else:
                    st.warning("Voice detected but no profile fields were found. Try saying: 'I am 30 years old with 50000 income'")
            else:
                error_msg = extracted.get("error") if extracted else "Unknown processing error"
                st.error(f"Voice Error: {error_msg}")
    
    st.markdown("###")
    
    # --- Membership Status ---
    if not st.session_state.is_pro:
        st.markdown(f"""
        <div style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.2); padding: 1.25rem; border-radius: 12px; margin-bottom: 2rem;">
            <div style="font-size: 0.65rem; color: #F59E0B; font-weight: 800; text-transform: uppercase; margin-bottom: 0.5rem; letter-spacing: 0.05em;">Institutional Pro</div>
            <p style="font-size: 0.8rem; color: #E2E8F0; margin-bottom: 1rem; line-height: 1.4;">Unlock strategic audits and unlimited assets for <b>$49/mo</b>.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("GO INSTITUTIONAL", use_container_width=True, type="primary"):
            st.session_state.is_pro = True
            st.rerun()
    else:
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.2); padding: 1.25rem; border-radius: 12px; margin-bottom: 2rem;">
            <div style="font-size: 0.65rem; color: #10B981; font-weight: 800; text-transform: uppercase; margin-bottom: 0.5rem; letter-spacing: 0.05em;">Membership: Active</div>
            <p style="font-size: 0.8rem; color: #E2E8F0; margin-bottom: 0; line-height: 1.4;">You have full institutional access.</p>
        </div>
        """, unsafe_allow_html=True)

    # Personal Information
    st.caption("PERSONAL DETAILS")
    col1, col2 = st.columns(2)
    with col1:
        age_val = st.session_state.get('age_val', 30)
        age = st.number_input("Age", min_value=18, max_value=80, value=age_val, key="age_input")
    with col2:
        risk_opts = ["Low", "Medium", "High"]
        risk_val = st.session_state.get('risk_val', "High")
        risk_idx = risk_opts.index(risk_val) if risk_val in risk_opts else 1
        risk_tolerance = st.selectbox("Risk", risk_opts, index=risk_idx, key="risk_input")
    
    # --- FORMAL RISK ASSESSMENT ---
    with st.expander("🛡️ FORMAL RISK AUDIT", expanded=False):
        st.caption("ANALYZE YOUR RISK PROFILE")
        q1 = st.radio("Time Horizon", ["< 5 years", "5-10 years", "10-20 years", "20+ years"])
        q2 = st.radio("Market Volatility Response", ["Sell everything", "Sell partially", "Hold firm", "Buy the dip"])
        q3 = st.radio("Investment Knowledge", ["Novice", "Intermediate", "Advanced", "Institutional"])
        
        if st.button("CALCULATE RISK TOLERANCE", use_container_width=True):
            score = 0
            if q1 == "20+ years": score += 3
            elif q1 == "10-20 years": score += 2
            
            if q2 == "Buy the dip": score += 5
            elif q2 == "Hold firm": score += 3
            
            if q3 == "Institutional": score += 4
            elif q3 == "Advanced": score += 3
            
            new_risk = "Low"
            if score >= 9: new_risk = "High"
            elif score >= 5: new_risk = "Medium"
            
            st.session_state['risk_val'] = new_risk
            st.success(f"Risk Audit Complete: {new_risk} Tolerance")
            time.sleep(1)
            st.rerun()
    
    # Financial Details
    st.markdown("###")
    st.caption("FINANCIALS")
    
    # Currency (Open for all per user request)
    currency = st.selectbox(
        "Currency",
        ["USD ($)", "EUR (€)", "GBP (£)", "NGN (₦)", "JPY (¥)", "CAD ($)", "AUD ($)", "INR (₹)"],
        index=0
    )
    
    currency_symbol = currency.split("(")[1].split(")")[0]
    currency_code = currency.split(" ")[0]
    
    # Dynamic Currency Conversion Logic
    from live_data import get_global_exchange_rates
    rates = get_global_exchange_rates()
    rate = rates.get(currency_code, 1.0)
    
    st.markdown("###")
    st.caption("FINANCIAL PARAMETERS")
    
    income_val = st.session_state.get('income_val', 60000)
    income = st.number_input(
        f"Annual Income", 
        min_value=0, 
        max_value=10000000, 
        value=income_val, 
        step=5000,
        format="%d",
        key="income_input"
    )
    
    capital_val = st.session_state.get('capital_val', 10000)
    capital = st.number_input(
        f"Starting Capital", 
        min_value=0, 
        max_value=100000000, 
        value=capital_val, 
        step=1000,
        format="%d",
        key="capital_input"
    )
    
    monthly_val = st.session_state.get('monthly_val', 500)
    monthly = st.number_input(
        f"Monthly Velocity", 
        min_value=0, 
        max_value=1000000, 
        value=monthly_val, 
        step=100,
        format="%d",
        key="monthly_input"
    )

    # --- Financial Resolution Engine ---
    st.markdown("---")
    st.markdown("##### 🏁 RESOLUTION DASHBOARD")
    
    # Quantitative Resolution Milestones
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        # Emergency Fund Milestone
        ef_target = 10000 * rate
        ef_progress = min(capital / ef_target, 1.0) if ef_target > 0 else 1.0
        st.caption("EMERGENCY FUND")
        st.progress(ef_progress)
        st.markdown(f"<p style='font-size:0.7rem; color:#94A3B8; margin-top:-0.5rem;'>{int(ef_progress*100)}% of {currency_symbol}{int(ef_target):,}</p>", unsafe_allow_html=True)
    
    with res_col2:
        # Retirement Velocity
        target_v = 5000 * rate
        velocity = min(monthly / target_v, 1.0) if target_v > 0 else 1.0
        st.caption("SAVINGS VELOCITY")
        st.progress(velocity)
        st.markdown(f"<p style='font-size:0.7rem; color:#94A3B8; margin-top:-0.5rem;'>{int(velocity*100)}% of target</p>", unsafe_allow_html=True)

    # Institutional Risk Resilience Metric
    from styles import create_health_score_dial
    
    # Simple multivariable metric: (Income Stability * 0.4) + (Capital Base * 0.3) + (Savings Rate * 0.3)
    resilience_score = min(80 + (monthly/500 * 5) + (income/100000 * 5), 99)
    st.markdown(create_health_score_dial(int(resilience_score), "RESILIENCE"), unsafe_allow_html=True)
    
    # Investment Goals
    st.markdown("###")
    st.caption("GOALS")
    timeline_val = st.session_state.get('timeline_val', 30)
    timeline = st.slider("Timeline (years)", min_value=1, max_value=50, value=timeline_val, key="timeline_input")
    goal_val = st.session_state.get('goal_val', "Build wealth for retirement")
    goal = st.text_area("Primary Goal", goal_val, height=80, key="goal_input")
    
    # Opportunities
    st.markdown("---")
    st.caption("OPPORTUNITY SCANNER")
    
    from opportunities import check_opportunities
    
    user_profile_opportunities = {
        'age': age,
        'risk_tolerance': risk_tolerance,
        'capital': capital
    }
    
    try:
        opportunities = check_opportunities(user_profile_opportunities)
        
        if opportunities:
            for idx, opp in enumerate(opportunities[:2], 1):
                # Map asset names to symbols/keys for logo lookup
                symbol_map = {
                    'Solana (SOL)': 'SOL',
                    'Jito Staking': 'Jito Staking',
                    'Raydium Liquidity Pools': 'Raydium Pools',
                    'Kamino Finance Vaults': 'Kamino Vaults',
                    'Bitcoin (BTC)': 'BTC',
                    'Portfolio Rebalance': 'BONDS'
                }
                asset_key = symbol_map.get(opp['asset'], 'SOL')
                
                # Use protocol logo helper for known protocols
                if any(p in opp['asset'] for p in ['Jito', 'Raydium', 'Kamino', 'Orca', 'Marinade', 'Solend']):
                    clean_name = opp['asset'].replace(' Liquidity Pools', '').replace(' Finance Vaults', '').replace(' Staking', '').replace(' (SOL)', '').strip()
                    # Try both variants
                    logo_url = get_protocol_logo(opp['asset']) or get_protocol_logo(clean_name)
                    if not logo_url.startswith('data:'): # Check if it returned emoji
                        logo_url = get_protocol_logo(clean_name + " Pools") or logo_url
                else:
                    logo_url = get_asset_logo(asset_key)
                
                fallback_img = "https://cdn-icons-png.flaticon.com/512/2489/2489756.png"
                
                with st.expander(f"✨ {opp['type']}", expanded=True):
                    icon_html = render_asset_icon(logo_url, style="width:20px; height:20px; margin-right:8px;")
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                        {icon_html}
                        <strong style='color:#F8FAFC'>{opp['asset']}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    st.caption(opp['reason'])
                    st.markdown(f"<div style='background:rgba(59, 130, 246, 0.2); padding:0.5rem; border-radius:6px; margin-top:0.5rem; border:1px solid rgba(59, 130, 246, 0.3); font-size:0.8rem; color:#60A5FA'>{opp['action']}</div>", unsafe_allow_html=True)
        else:
            st.info("Scanning markets...")
    except Exception as e:
        st.write("")

# Main Content Area
# Professional Navigation using Session State
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "DASHBOARD"

# Apply the dynamic background based on the active tab
st.markdown(get_section_background(st.session_state.active_tab), unsafe_allow_html=True)

# Navigation Bar - Responsive Approach
# Use a more flexible column layout for navigation
nav_cols = st.columns([1, 1, 1, 1, 1, 1])
with nav_cols[1]:
    if st.button("DASHBOARD", use_container_width=True, type="primary" if st.session_state.active_tab == "DASHBOARD" else "secondary", key="nav_dash"):
        st.session_state.active_tab = "DASHBOARD"
        st.rerun()
with nav_cols[2]:
    if st.button("PORTFOLIO", use_container_width=True, type="primary" if st.session_state.active_tab == "PORTFOLIO" else "secondary", key="nav_port"):
        st.session_state.active_tab = "PORTFOLIO"
        st.rerun()
with nav_cols[3]:
    if st.button("ADVISOR", use_container_width=True, type="primary" if st.session_state.active_tab == "AI ADVISOR" else "secondary", key="nav_adv"):
        st.session_state.active_tab = "AI ADVISOR"
        st.rerun()
with nav_cols[4]:
    if st.button("EDU", use_container_width=True, type="primary" if st.session_state.active_tab == "EDUCATION" else "secondary", key="nav_edu"):
        st.session_state.active_tab = "EDUCATION"
        st.rerun()

st.markdown("###")

# TAB Handling
active_tab = st.session_state.active_tab

# TAB 1: Investment Planner
if active_tab == "DASHBOARD":
    # Use adaptive column layout for better mobile experience
    col1, col2 = st.columns([2, 1]) if not st.session_state.get('is_mobile', False) else (st.container(), st.container())
    
    # Note: Streamlit's st.columns on mobile already stacks, but we can refine the container logic
    with col1:
        st.markdown("### Market Overview")
        
        # Consistent Live Market Ticker
        live_market = get_live_market_data()
        ticker_items = []
        for symbol, details in live_market.items():
            change_class = "change-up" if details['change_24h'] >= 0 else "change-down"
            arrow = "▲" if details['change_24h'] >= 0 else "▼"
            logo = get_asset_logo(symbol)
            icon_html = render_asset_icon(logo)
            
            # Convert price to local currency
            local_price = details["price"] * rate
            
            item_html = (
                f'<div class="ticker-item">'
                f'{icon_html}'
                f'<span class="ticker-symbol">{symbol}</span>'
                f'<span class="ticker-price">{currency_symbol}{local_price:,.2f}</span>'
                f'<span class="ticker-change {change_class}">{arrow} {abs(details["change_24h"]):.2f}%</span>'
                f'</div>'
            )
            ticker_items.append(item_html)
        
        # Repeat items to create a gapless infinite loop
        repeated_content = "".join(ticker_items) + "".join(ticker_items)
        full_ticker_html = f'<div class="market-ticker-container"><div class="market-ticker">{repeated_content}</div></div>'
        st.markdown(full_ticker_html, unsafe_allow_html=True)
        
        st.markdown("#### Performance")
        st.markdown(f"<div style='text-align:right; color:#94A3B8; font-family:JetBrains Mono;'>{currency_code} Markets Open</div>", unsafe_allow_html=True)

        # Solana Network Status
        sol_service = get_solana_service()
        tps = sol_service.get_tps()
        slot = sol_service.get_slot_height()
        
        st.markdown(f"""
        <div style="margin-top: 1rem; padding: 0.8rem; background: rgba(20, 241, 149, 0.05); border: 1px dashed rgba(20, 241, 149, 0.2); border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 8px; height: 8px; background: #14F195; border-radius: 50%; box-shadow: 0 0 8px #14F195;"></div>
                <span style="font-size: 0.8rem; color: #14F195; font-weight: 600;">Solana Mainnet</span>
            </div>
            <div style="font-family: 'JetBrains Mono'; font-size: 0.75rem; color: #94A3B8;">
                TPS: <span style="color: #E2E8F0;">{tps}</span> | Slot: {slot}
            </div>
        </div>
        """, unsafe_allow_html=True)

    
    from live_data import get_live_market_data, get_defi_yields, get_portfolio_growth_projection
    
    market_data = get_live_market_data()
    
    # Main Dashboard Metrics with Global Currency
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        btc_data = market_data['BTC']
        st.markdown(create_stat_card("BITCOIN", f"{currency_symbol}{btc_data['price']*rate:,.0f}", btc_data['change_24h'], get_asset_logo('BTC')), unsafe_allow_html=True)
    
    with col2:
        eth_data = market_data['ETH']
        st.markdown(create_stat_card("ETHEREUM", f"{currency_symbol}{eth_data['price']*rate:,.0f}", eth_data['change_24h'], get_asset_logo('ETH')), unsafe_allow_html=True)
    
    with col3:
        sol_data = market_data['SOL']
        st.markdown(create_stat_card("SOLANA", f"{currency_symbol}{sol_data['price']*rate:,.2f}", sol_data['change_24h'], get_asset_logo('SOL')), unsafe_allow_html=True)
    
    with col4:
        vti_data = market_data['VTI']
        st.markdown(create_stat_card("GLOBAL EQUITY", f"{currency_symbol}{vti_data['price']*rate:,.2f}", vti_data['change_24h'], get_asset_logo('VTI')), unsafe_allow_html=True)
    
    st.markdown("###")
    
    # Charts Row
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Market Performance")
        
        fig = go.Figure()
        colors = {'BTC': '#F7931A', 'ETH': '#627EEA', 'SOL': '#14F195'}
        
        for symbol in ['BTC', 'ETH', 'SOL']:
            data = market_data[symbol]
            dates = [d['date'] for d in data['history']]
            prices = [d['price'] for d in data['history']]
            
            initial_price = prices[0]
            normalized = [(p / initial_price - 1) * 100 for p in prices]
            
            fig.add_trace(go.Scatter(
                x=dates,
                y=normalized,
                name=symbol,
                mode='lines',
                line=dict(width=2, color=colors.get(symbol, '#fff'))
            ))
        
        layout = get_dark_chart_layout()
        layout['yaxis']['title'] = 'Change (%)'
        fig.update_layout(layout)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Live Yield Desk")
        
        defi_results = get_defi_yields()
        
        yield_items = []
        for protocol, info in defi_results.items():
            logo_url = get_protocol_logo(protocol)
            icon_html = render_asset_icon(logo_url, class_name="yield-logo", style="margin-right:12px;")
            item_html = (
                f'<div class="yield-card">'
                f'<div class="yield-card-left">'
                f'{icon_html}'
                f'<div><div class="yield-name">{protocol}</div><div class="yield-tvl">TVL: {info["tvl"]}</div></div>'
                f'</div>'
                f'<div class="yield-apy">{info["apy"]}%</div>'
                f'</div>'
            )
            yield_items.append(item_html)
            
        # Repeat for continuous vertical loop
        repeated_yields = "".join(yield_items) + "".join(yield_items)
        
        full_defi_html = (
            f'<div class="defi-yield-container">'
            f'<div class="yield-scroll-area">{repeated_yields}</div>'
            f'</div>'
        )
        st.markdown(full_defi_html, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### Global Smart Vaults")
    from live_data import get_strategy_vaults
    from styles import create_vault_card
    
    vaults = get_strategy_vaults()
    v_cols = st.columns(3)
    for i, vault in enumerate(vaults):
        with v_cols[i]:
            logo_uri = get_asset_logo(vault['logo'])
            st.markdown(create_vault_card(
                vault['name'], 
                vault['description'], 
                vault['apy'], 
                vault['risk'], 
                vault['tvl'],
                vault['status'],
                logo_uri
            ), unsafe_allow_html=True)
            
    st.markdown("---")
    
    # Projections
    st.markdown("### Wealth Projection")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        scenarios = {
            'Conservative (5%)': 0.05,
            'Moderate (8%)': 0.08,
            'Aggressive (12%)': 0.12
        }
        
        fig = go.Figure()
        scenario_colors = ['#60A5FA', '#3B82F6', '#1E40AF']
        
        for idx, (scenario_name, return_rate) in enumerate(scenarios.items()):
            projection = get_portfolio_growth_projection(capital, monthly, timeline, return_rate)
            years = [p['year'] for p in projection]
            values = [p['value'] for p in projection]
            
            fig.add_trace(go.Scatter(
                x=years,
                y=values,
                name=scenario_name,
                mode='lines',
                line=dict(width=3, color=scenario_colors[idx]),
                fill='tonexty' if idx > 0 else None,
                fillcolor=f"rgba{tuple(int(scenario_colors[idx].lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (0.1,)}"
            ))
        
        layout = get_dark_chart_layout(height=400)
        layout['yaxis']['title'] = f'Value ({currency_symbol})'
        layout['hovermode'] = 'x unified'
        fig.update_layout(layout)
        
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); padding:1.5rem; border-radius:12px;">
            <div style="font-size:0.8rem; color:#94A3B8; text-transform:uppercase; margin-bottom:0.5rem;">Target</div>
            <div style="font-size:1.3rem; font-weight:700; color:#fff; margin-bottom:1rem; word-break: break-word;">
                {currency_symbol}{get_portfolio_growth_projection(capital, monthly, timeline, 0.08)[-1]['value']:,.0f}
            </div>
            <div style="font-size:0.85rem; color:#10B981;">
                Based on Moderate (8%) growth over {timeline} years.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("###")
        if st.button("GENERATE FULL PLAN", type="primary", use_container_width=True):
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
            
            with st.spinner("Analyzing market conditions and generating strategy (this may take a moment)..."):
                try:
                    plan = create_investment_plan(user_profile)
                    
                    # Check if plan is valid and not an error message
                    if plan and len(plan) > 100 and not plan.strip().startswith("Error"):
                         st.session_state['generated_plan'] = plan
                         st.session_state['plan_error'] = None
                    else:
                        st.session_state['generated_plan'] = None
                        st.session_state['plan_error'] = plan
                        
                except Exception as e:
                    st.session_state['generated_plan'] = None
                    st.session_state['plan_error'] = str(e)

    # --- Full Width Plan Display Section (Outside Columns) ---
    if 'generated_plan' in st.session_state and st.session_state['generated_plan']:
        st.markdown("---")
        st.markdown("### 📋 Your Personalized Strategy")
        st.markdown(create_success_banner("Plan Generated Successfully"), unsafe_allow_html=True)
        
        with st.expander("VIEW FULL PLAN DOCUMENT", expanded=True):
            st.markdown(st.session_state['generated_plan'])
            
        st.download_button("DOWNLOAD PDF REPORT", st.session_state['generated_plan'], file_name="plan.txt")
        
    elif 'plan_error' in st.session_state and st.session_state['plan_error']:
        st.markdown("---")
        st.markdown("### ⚠️ Strategic Analysis Paused")
        
        # Determine if it's a quota issue
        error_msg = str(st.session_state['plan_error'])
        if "429" in error_msg or "quota" in error_msg.lower():
            st.warning("Daily capacity reached. Please try again in 24 hours or upgrade your Gemini API tier.")
        else:
            st.error("An unexpected error occurred during strategy generation.")
            
        with st.expander("Technical Insight"):
            st.caption(f"Error Code: {error_msg}")
            
        if st.button("Attempt Re-analysis"):
            st.session_state.pop('plan_error', None)
            st.rerun()

# TAB 2: Portfolio Tracker
elif active_tab == "PORTFOLIO":
    st.markdown("### Portfolio Workspace")
    
    # Initialize Portfolio in Session State
    if 'portfolio_holdings' not in st.session_state:
        st.session_state.portfolio_holdings = []
    
    # Solana Wallet Integration
    with st.expander("🔌 CONNECT SOLANA WALLET (Read-Only)"):
        sol_wallet = st.text_input("Enter Solana Wallet Address", placeholder="Address...")
        if sol_wallet:
            if st.button("Fetch On-Chain Balance"):
                with st.spinner("Querying blockchain..."):
                    sol_service = get_solana_service()
                    bal = sol_service.get_balance(sol_wallet)
                    if bal > 0:
                        # Add or Update SOL in holdings
                        existing = next((h for h in st.session_state.portfolio_holdings if h['symbol'] == 'SOL'), None)
                        if existing:
                            existing['qty'] = bal  # Update quantity
                            st.info(f"Updated SOL balance to {bal:.4f}")
                        else:
                            st.session_state.portfolio_holdings.append({
                                'symbol': 'SOL', 
                                'qty': bal, 
                                'cost': 140 # Assume generic cost basis or 0
                            })
                            st.success(f"Found {bal:.4f} SOL")
                        st.rerun()
                    else:
                        st.warning("No SOL found or invalid address.")

    
    # --- Sidebar/Management Controls ---
    col_add, col_actions = st.columns([2, 1])
    
    with col_add:
        with st.expander("➕ ADD ASSET TO PORTFOLIO", expanded=not st.session_state.portfolio_holdings):
            from live_data import get_asset_registry
            registry = get_asset_registry()
            
            # Searchable selectbox for assets
            asset_options = [f"{a['symbol']} - {a['name']} ({a['category']})" for a in registry]
            selected_asset_str = st.selectbox("Search Global Assets (Symbols, Names, Categories)", options=asset_options, key="asset_search")
            
            # Extract symbol
            selected_symbol = selected_asset_str.split(" - ")[0]
            
            col_q, col_c = st.columns(2)
            with col_q:
                qty = st.number_input("Quantity", min_value=0.0, step=0.1, key="add_qty")
            with col_c:
                avg_cost = st.number_input(f"Avg Cost ({currency_symbol})", min_value=0.0, step=1.0, key="add_cost")
            
            if st.button("ADD TO HOLDINGS", type="primary", use_container_width=True):
                # Membership Check: Capacity
                if not st.session_state.is_pro and len(st.session_state.portfolio_holdings) >= 3:
                    st.warning("⚠️ Free Tier Capacity Reached (3 Assets). Upgrade to Pro for unlimited institutional tracking.")
                else:
                    # Check if already exists
                    existing = next((item for item in st.session_state.portfolio_holdings if item['symbol'] == selected_symbol), None)
                    if existing:
                        # Update (simplified for demo: just replacing or averaging)
                        new_qty = existing['qty'] + qty
                        new_cost = ((existing['qty'] * existing['cost']) + (qty * avg_cost)) / new_qty if new_qty > 0 else 0
                        existing['qty'] = new_qty
                        existing['cost'] = new_cost
                    else:
                        st.session_state.portfolio_holdings.append({
                            'symbol': selected_symbol,
                            'qty': qty,
                            'cost': avg_cost
                        })
                    st.success(f"Added {selected_symbol} to portfolio.")
                    st.rerun()

    with col_actions:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.02); padding: 1.25rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); height: 100%;">
            <div style="font-size: 0.7rem; color: #94A3B8; text-transform: uppercase; margin-bottom: 0.5rem; letter-spacing: 0.05em;">Tactical Actions</div>
            <div style="display: flex; flex-direction: column; gap: 0.5rem;">
        """, unsafe_allow_html=True)
        if st.button("STRATEGIC AUDIT", use_container_width=True):
            st.session_state.rebalance_request = True
        if st.button("RESET DATA", use_container_width=True, type="secondary"):
            st.session_state.portfolio_holdings = []
            st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)

    # --- Portfolio Display ---
    if st.session_state.portfolio_holdings:
        st.markdown("#### Institutional Holdings")
        
        # Table Header
        header_cols = st.columns([1, 1.5, 1, 1, 1, 1, 0.5])
        header_style = "font-size: 0.65rem; color: #64748B; text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em;"
        header_cols[0].markdown(f"<div style='{header_style}'>Asset</div>", unsafe_allow_html=True)
        header_cols[1].markdown(f"<div style='{header_style}'>Position</div>", unsafe_allow_html=True)
        header_cols[2].markdown(f"<div style='{header_style}'>Avg Cost</div>", unsafe_allow_html=True)
        header_cols[3].markdown(f"<div style='{header_style}'>Price</div>", unsafe_allow_html=True)
        header_cols[4].markdown(f"<div style='{header_style}'>Value</div>", unsafe_allow_html=True)
        header_cols[5].markdown(f"<div style='{header_style}'>PnL</div>", unsafe_allow_html=True)
        
        total_market_value = 0
        total_cost_basis = 0
        
        # Get live data for holdings
        market_data = get_live_market_data()
        
        for idx, item in enumerate(st.session_state.portfolio_holdings):
            symbol = item['symbol']
            qty = item['qty']
            cost = item['cost']
            
            data = market_data.get(symbol, {'price': cost/rate if rate > 0 else cost, 'change_24h': 0.0})
            # Convert USD market price to local currency
            current_price_local = data['price'] * rate
            
            market_value = qty * current_price_local
            cost_basis = qty * cost
            unrealized_pnl = market_value - cost_basis
            pnl_pct = (unrealized_pnl / cost_basis * 100) if cost_basis > 0 else 0
            
            total_market_value += market_value
            total_cost_basis += cost_basis
            
            row_cols = st.columns([1, 1.5, 1, 1, 1, 1, 0.5])
            
            # Asset Icon & Name
            logo_uri = get_asset_logo(symbol)
            icon_html = render_asset_icon(logo_uri, style="width:24px; height:24px; margin-right:10px;")
            row_cols[0].markdown(f"<div style='display:flex; align-items:center;'>{icon_html} <b style='color:#fff;'>{symbol}</b></div>", unsafe_allow_html=True)
            
            # Position Info
            row_cols[1].markdown(f"<div style='color:#94A3B8; font-family:\"JetBrains Mono\";'>{qty:,.2f} Units</div>", unsafe_allow_html=True)
            
            # Values (Using local currency symbol and rate)
            row_cols[2].markdown(f"<div style='color:#F8FAFC;'>{currency_symbol}{cost:,.2f}</div>", unsafe_allow_html=True)
            row_cols[3].markdown(f"<div style='color:#F8FAFC;'>{currency_symbol}{current_price_local:,.2f}</div>", unsafe_allow_html=True)
            row_cols[4].markdown(f"<div style='font-weight:700; color:#fff;'>{currency_symbol}{market_value:,.2f}</div>", unsafe_allow_html=True)
            
            # PnL
            pnl_color = "#10B981" if unrealized_pnl >= 0 else "#EF4444"
            row_cols[5].markdown(f"<div style='color:{pnl_color}; font-weight:700;'>{currency_symbol}{unrealized_pnl:+,.2f} <br><small style='opacity:0.8;'>{pnl_pct:+.2f}%</small></div>", unsafe_allow_html=True)
            
            # Remove button
            if row_cols[6].button("🗑️", key=f"del_{symbol}_{idx}"):
                st.session_state.portfolio_holdings.pop(idx)
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Summary Row
        sum_col1, sum_col2, sum_col3 = st.columns([1, 1, 1.5])
        with sum_col1:
            st.markdown(create_stat_card("TOTAL MARKET VALUE", f"{currency_symbol}{total_market_value:,.2f}", 0, "💰"), unsafe_allow_html=True)
            
            # Allocation Chart with Asset Class Intelligence
            asset_registry = get_asset_registry()
            def get_category(sym):
                match = next((a for a in asset_registry if a['symbol'] == sym), None)
                return match['category'] if match else 'Other'
            
            categories = {}
            for h in st.session_state.portfolio_holdings:
                cat = get_category(h['symbol'])
                val = h['qty'] * market_data.get(h['symbol'], {'price': 0})['price'] * rate
                categories[cat] = categories.get(cat, 0) + val
                
            fig_alloc = go.Figure(data=[go.Pie(
                labels=list(categories.keys()),
                values=list(categories.values()),
                hole=.7,
                marker=dict(colors=['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']),
                textinfo='label+percent',
                hoverinfo='label+value+percent'
            )])
            fig_alloc.update_layout(get_dark_chart_layout(height=280))
            fig_alloc.update_layout(title={'text': "Asset Class Distribution", 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top', 'font': {'size': 12, 'color': '#94A3B8'}})
            fig_alloc.update_traces(showlegend=False, textfont_size=10)
            st.plotly_chart(fig_alloc, use_container_width=True, key="port_alloc_chart")

        with sum_col2:
            total_pnl = total_market_value - total_cost_basis
            total_pnl_pct = (total_pnl / total_cost_basis * 100) if total_cost_basis > 0 else 0
            st.markdown(create_stat_card("NET UNREALIZED PNL", f"{currency_symbol}{total_pnl:,.2f}", total_pnl_pct, "📈"), unsafe_allow_html=True)
            
            # Institutional Target Summary
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.02); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); margin-top: 1rem;">
                <div style="font-size: 0.75rem; color: #10B981; text-transform: uppercase; font-weight: 800; margin-bottom: 1.25rem; letter-spacing:0.05em;">Benchmark: {risk_tolerance} Global</div>
                <div style='display:flex; justify-content:space-between; font-size:0.85rem; color:#94A3B8; margin-bottom:0.75rem;'><span>Core Equity</span><span style='color:#fff; font-weight:600;'>50-60%</span></div>
                <div style='display:flex; justify-content:space-between; font-size:0.85rem; color:#94A3B8; margin-bottom:0.75rem;'><span>Digital Alpha</span><span style='color:#fff; font-weight:600;'>15-20%</span></div>
                <div style='display:flex; justify-content:space-between; font-size:0.85rem; color:#94A3B8;'><span>Yield Layer</span><span style='color:#fff; font-weight:600;'>10-15%</span></div>
                <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.05); font-size: 0.7rem; color: #64748B;">
                    Optimized via institutional-grade quantitative protocols.
                </div>
            </div>
            """, unsafe_allow_html=True)

        with sum_col3:
            # Active Rebalancing Logic
            if st.session_state.get('rebalance_request'):
                st.markdown("#### QUANTITATIVE STRATEGY")
                
                if not st.session_state.is_pro:
                    # Gated Preview UI
                    st.markdown(f"""
                    <div style="background: rgba(245, 158, 11, 0.05); border: 1px dashed rgba(245, 158, 11, 0.3); padding: 2rem; border-radius: 20px; text-align: center; margin-top: 0.5rem;">
                        <div style="font-size: 2rem; margin-bottom: 1rem;">🔒</div>
                        <h5 style="color: #F59E0B; margin-top: 0;">Institutional Audit Locked</h5>
                        <p style="color: #94A3B8; font-size: 0.85rem; line-height: 1.5;">Specific Buy/Sell execution steps and Arcium-standard tactical rebalancing are reserved for **Institutional Pro** members.</p>
                        <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.05); margin: 1.5rem 0;">
                        <p style="color: #fff; font-weight: 700; margin-bottom: 1rem;">Unlock for $49/mo</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("UPGRADE NOW", type="primary", use_container_width=True, key="gate_upgrade"):
                        st.session_state.is_pro = True
                        st.rerun()
                    if st.button("DISMISS", use_container_width=True, type="secondary"):
                        st.session_state.rebalance_request = False
                        st.rerun()
                else:
                    from portfolio_agent import analyze_portfolio_rebalance
                    
                    with st.spinner("Analyzing portfolio weightings..."):
                        user_context = {'age': age, 'goal': goal}
                        rebalance_report = analyze_portfolio_rebalance(
                            st.session_state.portfolio_holdings,
                            risk_tolerance,
                            user_context
                        )
                        
                        st.markdown(f"""
                        <div style="background: rgba(59, 130, 246, 0.05); border: 1px solid rgba(59, 130, 246, 0.2); padding: 1.5rem; border-radius: 20px; margin-top: 0.5rem; box-shadow: 0 10px 40px -10px rgba(0,0,0,0.5);">
                            <h5 style="color: #60A5FA; margin-top: 0; display:flex; align-items:center; letter-spacing:0.02em;">
                                <span style="margin-right:10px;">📉</span> STRATEGIC REBALANCING STEPS
                            </h5>
                            <div style="color: #E2E8F0; font-size: 0.9rem; line-height: 1.7; height: 320px; overflow-y: auto; padding-right:10px;">
                                {rebalance_report}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button("DISMISS REPORT", use_container_width=True, type="secondary"):
                            st.session_state.rebalance_request = False
                            st.rerun()
            else:
                st.markdown(create_stat_card("ASSET COUNT", f"{len(st.session_state.portfolio_holdings)} ACTIVATED", 0, "📂"), unsafe_allow_html=True)
                st.markdown("""
                <div style="background: rgba(255,255,255,0.02); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); margin-top: 1rem;">
                    <div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 1.5rem; line-height:1.5;">Initiate **STRATEGIC AUDIT** to generate a confidential rebalancing report.</div>
                    <div style="background: rgba(59, 130, 246, 0.1); padding: 0.75rem; border-radius: 8px; border: 1px solid rgba(59, 130, 246, 0.2); font-size: 0.75rem; color: #60A5FA;">
                        <b>Note:</b> All execution paths follow institutional multi-chain protocols.
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem; background: rgba(255,255,255,0.01); border-radius: 24px; border: 2px dashed rgba(255,255,255,0.05); margin-top: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📁</div>
            <h3 style="color: #F8FAFC; margin-bottom: 0.5rem;">Inventory Status: Offline</h3>
            <p style="color: #94A3B8; max-width: 400px; margin: 0 auto 2rem;">Add assets from our global library of 100+ institutional symbols to begin tracking and quantitative analysis.</p>
        </div>
        """, unsafe_allow_html=True)

# TAB 3: AI Advisor
elif active_tab == "AI ADVISOR":
    st.markdown("### Investment Assistant")
    
    # Chat container styling
    chat_container = st.container()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        
    with chat_container:
        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(chat['question'])
            with st.chat_message("assistant", avatar="assets/ai_avatar.png"):
                st.write(chat['answer'])
    
    col1, col2 = st.columns([6, 1])
    with col1:
        user_question = st.chat_input("Ask about your portfolio, specific assets, or market trends...")
    with col2:
        voice_query = mic_recorder(
            start_prompt="🎤",
            stop_prompt="🛑",
            just_once=True,
            key="voice_query"
        )
    
    if voice_query and 'bytes' in voice_query:
        with st.spinner("Processing voice..."):
            answer = process_voice_advisor_query(voice_query['bytes'], {
                'age': age, 'risk_tolerance': risk_tolerance, 'goal': goal
            })
            if answer and not answer.startswith("Sorry"):
                st.session_state.chat_history.append({'question': "🎤 Voice Query", 'answer': answer})
                st.rerun()
            else:
                st.error(answer or "Failed to process voice query.")

    if user_question:
        with chat_container:
            with st.chat_message("user"):
                st.write(user_question)
            
            with st.chat_message("assistant", avatar="assets/ai_avatar.png"):
                from advisor_agent import get_investment_advice
                with st.spinner("Analyzing..."):
                    answer = get_investment_advice(user_question, {})
                    st.write(answer)
        
        st.session_state.chat_history.append({'question': user_question, 'answer': answer})

# TAB 4: Education
elif active_tab == "EDUCATION":
    st.markdown("### Knowledge Base")
    # Using existing logic but cleaner layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); padding:1.5rem; border-radius:12px; height:100%;">
            <h4 style="color:white; margin-top:0;">Solana DeFi Guide</h4>
            <p style="font-size:0.9rem;">Master the high-speed ecosystem.</p>
            <ul style="padding-left:1.2rem; color:#94A3B8; font-size:0.9rem;">
                <li>Liquid Staking (Jito)</li>
                <li>DEX Aggregators (Jupiter)</li>
                <li>Liquidity Pools (Raydium)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        from education_agent import AVAILABLE_GUIDES, generate_guide
        
        c1, c2 = st.columns(2)
        with c1:
            topic = st.selectbox("Select Guide Topic", list(AVAILABLE_GUIDES.keys()))
        with c2:
            level = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])
            
        if st.button("GENERATE GUIDE"):
            with st.spinner("Writing guide..."):
                g = generate_guide(topic, level.lower())
                st.markdown(g)
