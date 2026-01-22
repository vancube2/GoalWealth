import streamlit as st

def apply_custom_styles():
    """Apply professional custom styling"""
    st.markdown("""
    <style>
    /* Main container */
    .main {
        padding-top: 2rem;
    }
    
    /* Headers */
    h1 {
        color: #1E3A8A;
        font-weight: 700;
        padding-bottom: 1rem;
        border-bottom: 3px solid #3B82F6;
    }
    
    h2 {
        color: #1E40AF;
        margin-top: 2rem;
    }
    
    h3 {
        color: #2563EB;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 600;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 1rem;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid #3B82F6;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #F3F4F6;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #F9FAFB;
    }
    
    /* Tables */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Chat messages */
    [data-testid="stChatMessage"] {
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background-color: #D1FAE5;
        border-left: 4px solid #10B981;
        border-radius: 8px;
    }
    
    .stError {
        background-color: #FEE2E2;
        border-left: 4px solid #EF4444;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)


def create_success_banner(message):
    """Create a success banner"""
    return f"""
    <div style="
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    ">
        ✓ {message}
    </div>
    """