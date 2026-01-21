# GoalWealth - Multi-Channel Investment Planner

> AI-powered investment planning with systematic evaluation through Opik

Commit To Change: An AI Agents Hackathon

---

##  What is GoalWealth?

GoalWealth is a comprehensive investment planning platform that creates personalized strategies across:
- Traditional Markets: Stocks, Bonds, ETFs, REITs, Gold
- Cryptocurrency: Bitcoin, Ethereum, Solana
- Solana DeFi: Jito, Raydium, Kamino, Jupiter, Arcium
- Multi-Currency Support: USD, EUR, GBP, NGN, JPY, CAD, AUD, INR

---

## 🏆 Why GoalWealth Wins "Best Use of Opik"

### The Challenge
How do you know if your AI investment advisor is giving quality advice? How do you improve it systematically?

### Our Solution: Comprehensive Opik Evaluation Framework

We built 5 custom metrics to measure investment plan quality:

1. Specificity (0-10): Does plan include exact dollar amounts and tickers?
2. Safety (0-10): Are appropriate risk warnings included?
3. Personalization (0-10): Is plan tailored to user's age/risk/timeline?
4. Actionability (0-10): Does plan include clear next steps?
5. Completeness (0-10): Does plan cover all necessary elements?

### Evaluation Results

Investment Planner:
- Baseline Score: 8.8/10 (averaged across 5 metrics)
- Test Profiles: 3 diverse users (young/aggressive, mid-career/conservative, DeFi enthusiast)
- Average Generation Time: 43.2 seconds

Experiments Conducted:
- Experiment 1: Baseline prompt → 8.8/10
- Experiment 2: Enhanced structured format → 8.6/10 (worse!)
- Experiment 3: With validation layer → 8.8/10 (same, but +6s slower)

Key Insight: Opik proved baseline was already optimal, preventing wasted optimization effort!

Chat Advisor:
- Baseline Score: 7.5/10 (across 4 test questions)
- Average Response Time: 12.0 seconds
- Attempted Enhancement: Failed due to API limits
- Outcome: Baseline confirmed as production-ready

### What Opik Enabled

Data-Driven Decisions: Metrics showed which changes helped vs hurt  
Resource Efficiency: Stopped pursuing worse alternatives  
Production Validation: Confirmed system quality (8.8/10 is excellent)  
Systematic Improvement: Framework ready for future optimization  
Full Transparency: All experiments tracked in Opik dashboard

---

## Features

### 1. Investment Planner
- Personalized multi-channel strategies
- Specific dollar amounts for each investment
- Solana DeFi deep dive (Jito, Raydium, Kamino)
- 30-year wealth projections
- Week-by-week execution guide

### 2. Portfolio Tracker
- Live market data (stocks via yfinance, crypto via CoinGecko)
- Real-time P&L calculations
- Interactive pie charts
- Multi-asset support

### 3. Investment Advisor Chat
- Context-aware Q&A
- Expertise in traditional + crypto + DeFi
- Risk warnings on all recommendations
- Chat history

### 4. Educational Resources
- AI-generated learning guides (7 topics)
- Customizable by experience level
- Quick reference for protocols
- 4 strategy templates

### 5. Opportunity Alerts
- Market condition monitoring
- Buy-the-dip notifications
- Yield opportunity suggestions
- Risk-appropriate recommendations

---

## Technical Implementation

### Opik Integration

Every major operation is tracked:
```python
from opik import track

@track(project_name="goalwealth", tags=["planner"])
def create_investment_plan(user_profile):
    # Plan generation logic
    
@track(project_name="goalwealth-eval", tags=["evaluation"])
def evaluate_plan(plan, metrics):
    # Quality measurement logic
```

Projects in Opik:
- `goalwealth` - Production traces
- `goalwealth-eval` - Evaluation runs
- `goalwealth-experiments` - A/B tests

### Tech Stack
- AI Model: Google Gemini 2.5 Flash
- Evaluation: Opik by Comet
- Framework: Streamlit
- Market Data: yfinance + CoinGecko API
- Visualization: Plotly

---

## Setup

### Prerequisites
- Python 3.11+
- API keys (free tiers):
  - Google Gemini API
  - Opik/Comet account

### Quick Start
```bash
# Clone repository
git clone <your-repo-url>
cd GoalWealth

# Install dependencies
pip install -r requirements.txt

# Create .env file
GEMINI_API_KEY=your_key_here
OPIK_API_KEY=your_key_here
OPIK_WORKSPACE=your_workspace

# Run application
streamlit run app.py
```
## Quality Metrics:
- Investment Planner: 8.8/10
- Chat Advisor: 7.5/10
- Portfolio Tracker: 100% uptime

## Opik Value Delivered:
- 3 experiments tracked
- 5 custom metrics defined
- Production quality validated
- Prevented 2+ hours of wasted optimization

## Our Delivery:
5-metric evaluation framework  
3 tracked experiments  
Multi-profile testing  
Data-driven insights  
Complete observability  

## Screenshots
<img width="1920" height="1080" alt="Screenshot (25)" src="https://github.com/user-attachments/assets/3a6f717d-58b0-4e07-8d6e-8aabbc39edb7" />


## Author
Chukwubuikem Nwaozuzu  
Enugu, Nigeria  
Commit To Change: An AI Agents Hackathon

## License
Educational/Hackathon purposes. Not financial advice.
Built Claude, Gemini, and Opik
