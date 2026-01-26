import requests
import os

# Create assets/logos directory
os.makedirs('assets/logos', exist_ok=True)

# Logo sources that we verified work
logos = {
    # Crypto
    'btc.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/btc.png',
    'eth.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/eth.png',
    'sol.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/sol.png',
    'usdc.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/usdc.png',
    'usdt.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/usdt.png',
    'bnb.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/bnb.png',
    'jup.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/jup.png',
    'ray.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/ray.png',
    'jito.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/jito.png',
    'xrp.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/xrp.png',
    'ada.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/ada.png',
    'avax.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/avax.png',
    'link.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/link.png',
    'dot.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/dot.png',
    
    # Stocks & ETFs
    'vti.png': 'https://financialmodelingprep.com/image-stock/VTI.png',
    'spy.png': 'https://financialmodelingprep.com/image-stock/SPY.png',
    'qqq.png': 'https://financialmodelingprep.com/image-stock/QQQ.png',
    'aapl.png': 'https://financialmodelingprep.com/image-stock/AAPL.png',
    'nvda.png': 'https://financialmodelingprep.com/image-stock/NVDA.png',
    'tsla.png': 'https://financialmodelingprep.com/image-stock/TSLA.png',
    'msft.png': 'https://financialmodelingprep.com/image-stock/MSFT.png',
    'amzn.png': 'https://financialmodelingprep.com/image-stock/AMZN.png',
    'googl.png': 'https://financialmodelingprep.com/image-stock/GOOGL.png',
    'meta.png': 'https://financialmodelingprep.com/image-stock/META.png',
    'nflx.png': 'https://financialmodelingprep.com/image-stock/NFLX.png',
    'amd.png': 'https://financialmodelingprep.com/image-stock/AMD.png',
    'intc.png': 'https://financialmodelingprep.com/image-stock/INTC.png',
    'jpm.png': 'https://financialmodelingprep.com/image-stock/JPM.png',
    'gs.png': 'https://financialmodelingprep.com/image-stock/GS.png',
    'xom.png': 'https://financialmodelingprep.com/image-stock/XOM.png',
    'cvx.png': 'https://financialmodelingprep.com/image-stock/CVX.png',
    'dia.png': 'https://financialmodelingprep.com/image-stock/DIA.png',
    'vnq.png': 'https://financialmodelingprep.com/image-stock/VNQ.png',
    'uso.png': 'https://financialmodelingprep.com/image-stock/USO.png',
    'gdx.png': 'https://financialmodelingprep.com/image-stock/GDX.png',
    'vt.png': 'https://financialmodelingprep.com/image-stock/VT.png',
    'tlt.png': 'https://financialmodelingprep.com/image-stock/TLT.png',
    'gold.png': 'https://www.gold.org/sites/default/files/gold_market_icons_digital_gold.png'
}

for filename, url in logos.items():
    try:
        print(f"Downloading {filename}...")
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(f'assets/logos/{filename}', 'wb') as f:
                f.write(response.content)
            print(f"✓ Saved {filename}")
        else:
            print(f"✗ Failed {filename}: {response.status_code}")
    except Exception as e:
        print(f"✗ Error {filename}: {e}")

print("\nDone! Logos saved to assets/logos/")
