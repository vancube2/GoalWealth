import streamlit as st

def apply_custom_styles():
    """Apply premium financial dashboard styling (Dark/Glassmorphism)"""
    st.markdown("""
    <style>
    /* Import Professional Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Global Variables */
    :root {
        --bg-dark: #0B1120;
        --bg-card: rgba(30, 41, 59, 0.7);
        --bg-glass: rgba(15, 23, 42, 0.5);
        --primary: #3B82F6;
        --primary-gradient: linear-gradient(135deg, #3B82F6 0%, #6366F1 100%);
        --accent: #10B981;
        --text-primary: #F8FAFC;
        --text-secondary: #94A3B8;
        --border-color: rgba(255, 255, 255, 0.1);
        --card-border: 1px solid rgba(255, 255, 255, 0.1);
        --glow: 0 0 20px rgba(59, 130, 246, 0.1);
    }
    
    /* Global Styles */
    .stApp {
        background-color: var(--bg-dark);
        transition: background 0.8s ease-in-out;
    }
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Apply font to text elements but exclude icons if possible */
    h1, h2, h3, h4, h5, h6, p, span, div, label, button, input, textarea, li, a {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }
    
    p, label, span {
        color: var(--text-secondary) !important;
    }
    
    /* Card/Container Styles (Streamlit Containers) */
    .element-container, .stExpander {
        background: transparent;
    }
    
    /* Metric Cards */
    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0F1218;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Buttons - Refined for stability */
    .stButton > button {
        background: rgba(255, 255, 255, 0.05) !important;
        color: var(--text-primary) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: all 0.2s ease;
        white-space: nowrap !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
    }
    
    .stButton > button[kind="primary"] {
        background: var(--primary-gradient) !important;
        border: none !important;
        color: white !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stButton > button:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
        transform: translateY(-1px);
    }

    /* Inputs - Force Dark Theme */
    /* CRITICAL INPUT FIX */
    /* Target ALL input types specifically and aggressively */
    input, textarea, select,
    input[type="text"], input[type="number"], input[type="password"], input[type="email"],
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > input {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        caret-color: #3B82F6 !important;
        background-color: #1E293B !important; /* Solid dark background - No Transparency */
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }

    /* Target specific Streamlit/BaseWeb wrappers to ensure they are also solid */
    div[data-baseweb="input"], 
    div[data-baseweb="base-input"], 
    div[data-baseweb="select"] > div {
        background-color: #1E293B !important;
        border: none !important;
    }

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div,
    div[data-baseweb="base-input"] > input,
    input.st-ai,
    textarea.st-ai {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #F8FAFC !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    div[data-baseweb="input"] input {
        color: #F8FAFC !important;
    }
    
    div[data-baseweb="select"] span {
        color: #F8FAFC !important;
    }
    
    ::placeholder {
        color: rgba(255, 255, 255, 0.4) !important;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: var(--text-secondary);
        background-color: transparent;
        border: none;
        padding-bottom: 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--primary);
        border-bottom: 2px solid var(--primary);
    }
    
    /* Charts Background */
    .js-plotly-plot .plotly .main-svg {
        background: transparent !important;
    }

    /* Dataframes */
    [data-testid="stDataFrame"] {
        background: transparent !important;
    }
    
    /* === AI ADVISOR STYLING === */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 16px !important;
        padding: 1.25rem !important;
        margin-bottom: 1.5rem !important;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }

    [data-testid="stChatMessage"] p {
        color: #F8FAFC !important;
        line-height: 1.6;
    }
    
    [data-testid="stChatInput"] textarea {
        background-color: #1E293B !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 12px !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.1);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255,255,255,0.1);
    }
    /* Voice Recorder Customization */
    .stMicRecorder {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
    }
    
    .stMicRecorder button {
        background: rgba(59, 130, 246, 0.1) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        color: #60A5FA !important;
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        transition: all 0.3s ease !important;
    }
    
    .stMicRecorder button:hover {
        background: rgba(59, 130, 246, 0.2) !important;
        transform: scale(1.1);
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.3);
    }

    /* Small Mic for Chat */
    [data-testid="column"] .stMicRecorder button {
        width: 40px !important;
        height: 40px !important;
        margin-top: 5px;
    }
    /* Market Ticker Marquee */
    .market-ticker-container {
        width: 100%;
        overflow: hidden;
        background: rgba(15, 23, 42, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 0;
        margin: 1.5rem 0;
        backdrop-filter: blur(10px);
        white-space: nowrap;
        position: relative;
        height: 48px;
        display: flex;
        align-items: center;
        border-radius: 8px;
    }

    /* DeFi Yield Desk */
    .defi-yield-container {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        height: 380px; /* Adjusted height for vertical marquee */
        overflow: hidden;
        position: relative;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }

    .defi-yield-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding-bottom: 0.75rem;
    }

    .yield-scroll-area {
        display: flex;
        flex-direction: column;
        animation: yield-scroll 25s linear infinite;
    }

    .yield-scroll-area:hover {
        animation-play-state: paused;
    }

    .yield-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.03);
    }

    .yield-card-left {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .yield-icon {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        background: rgba(59, 130, 246, 0.1);
    }

    .yield-card:hover {
        background: rgba(59, 130, 246, 0.1);
        border-color: rgba(59, 130, 246, 0.3);
        transform: scale(1.02);
    }

    .yield-name {
        font-weight: 700;
        color: var(--text-primary);
        font-size: 0.95rem;
    }

    .yield-apy {
        color: #10B981;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 1.1rem;
    }

    .yield-tvl {
        color: var(--text-secondary);
        font-size: 0.75rem;
        font-weight: 500;
    }

    @keyframes yield-scroll {
        0% { transform: translateY(0); }
        100% { transform: translateY(-50%); }
    }

    .market-ticker {
        display: inline-flex;
        animation: marquee 120s linear infinite; /* Slower for readability with many items */
        align-items: center;
        width: max-content;
    }

    .ticker-item {
        display: inline-flex;
        align-items: center;
        margin-right: 4rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
        font-weight: 500;
        background: rgba(255, 255, 255, 0.02);
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
    }

    .ticker-icon {
        width: 18px;
        height: 18px;
        margin-right: 0.75rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.9rem;
    }

    .ticker-symbol {
        color: var(--text-primary);
        font-weight: 700;
        margin-right: 0.75rem;
    }

    .ticker-price {
        color: #fff;
        margin-right: 0.75rem;
        opacity: 0.9;
    }

    .ticker-change {
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 0.2rem;
    }

    .change-up { 
        color: #10B981 !important; 
        text-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
    }
    .change-down { 
        color: #EF4444 !important; 
        text-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
    }

    @keyframes marquee {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }
    
    </style>
    """, unsafe_allow_html=True)


def create_glass_card():
    """Returns CSS style string for a glassmorphism card"""
    return "background: rgba(22, 27, 34, 0.7); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);"


import base64
import os

def get_img_as_base64(file_path):
    """Reads an image and returns a base64 string"""
    try:
        # Use absolute path resolution for robustness in cloud environments
        abs_path = os.path.abspath(file_path)
        if not os.path.exists(abs_path):
            # Try relative to the script location as a secondary fallback
            abs_path = os.path.join(os.path.dirname(__file__), file_path)
            
        with open(abs_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception as e:
        # Log to console for debugging in cloud logs
        print(f"Error loading image {file_path}: {e}")
        return ""

def create_hero_section():
    """Create premium hero section"""
    img_path = os.path.join("assets", "hero_bg.png")
    img_base64 = get_img_as_base64(img_path)
    
    # Fallback gradient if image fails
    bg_style = "background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(99, 102, 241, 0.15) 100%);"
    
    if img_base64:
        bg_style = f"background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.8)), url('data:image/png;base64,{img_base64}'); background-size: cover; background-position: center;"

    return f"""<div style="
        {bg_style}
        border: 1px solid rgba(59, 130, 246, 0.2); 
        backdrop-filter: blur(10px); 
        border-radius: 20px; 
        padding: 4rem 2rem; 
        margin-bottom: 3rem; 
        text-align: center; 
        position: relative; 
        overflow: hidden;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
    ">
        <div style="position: relative; z-index: 1;">
            <h1 style="font-size: 4rem; margin: 0; background: linear-gradient(to right, #fff, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0 0 30px rgba(59, 130, 246, 0.3); letter-spacing: -0.04em;">GOALWEALTH</h1>
            <p style="font-size: 1.2rem; color: #E2E8F0; margin-top: 1rem; font-weight: 400; letter-spacing: 0.1em; text-transform: uppercase;">Professional Asset Management</p>
        </div>
    </div>"""

def get_section_background(section_name):
    """Returns CSS to apply a specific background image to the whole app based on the section"""
    images = {
        "DASHBOARD": "hero_bg.png",
        "PORTFOLIO": "portfolio_header.png",
        "AI ADVISOR": "hero_bg.png",
        "EDUCATION": "education_header.png"
    }
    
    img_name = images.get(section_name, "hero_bg.png")
    img_base64 = get_img_as_base64(os.path.join("assets", img_name))
    
    if not img_base64:
        return ""
        
    return f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(11, 14, 20, 0.7), rgba(11, 14, 20, 0.85)), url('data:image/png;base64,{img_base64}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """

def apply_tab_backgrounds():
    """Injects CSS to apply specific backgrounds to the Portfolio and Education tabs"""
    # Deprecated in favor of get_section_background, keeping for now
    pass


def create_stat_card(title, value, change=None, sub_change=None):
    """Create a glassmorphic stat card"""
    change_html = ""
    if change is not None:
        color = "#10B981" if change >= 0 else "#EF4444"
        arrow = "↗" if change >= 0 else "↘"
        bg_color = "rgba(16, 185, 129, 0.1)" if change >= 0 else "rgba(239, 68, 68, 0.1)"
        change_html = f"<div style='display: inline-flex; align-items: center; padding: 4px 10px; background: {bg_color}; border-radius: 20px; color: {color}; font-size: 0.8rem; font-weight: 600; border: 1px solid {color}33;'>{arrow} {abs(change):.2f}%</div>"

    return f"""<div style="{create_glass_card()}">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem; flex-wrap: wrap; gap: 0.5rem;">
            <div style="color: #94A3B8; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; white-space: nowrap;">{title}</div>
            {change_html}
        </div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.6rem; color: #fff; font-weight: 700; letter-spacing: -0.02em; overflow-wrap: break-word;">{value}</div>
    </div>"""

def create_metric_card_large(title, value, change=None):
    """Same as stat card but potentially emphasized"""
    return create_stat_card(title, value, change)

def create_success_banner(message):
    return f"""
    <div style="
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.2);
        color: #10B981;
        padding: 1rem;
        border-radius: 12px;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 1rem 0;
    ">
        <span style="font-size: 1.2rem;">✓</span>
        <span style="font-weight: 500;">{message}</span>
    </div>
    """

