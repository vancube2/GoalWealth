import requests
import os

# Create assets/logos directory
os.makedirs('assets/logos', exist_ok=True)

# Logo sources that we verified work
logos = {
    'btc.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/btc.png',
    'eth.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/eth.png',
    'sol.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/sol.png',
    'usdc.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/usdc.png',
    'usdt.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/usdt.png',
    'bnb.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/bnb.png',
    'vti.png': 'https://financialmodelingprep.com/image-stock/VTI.png',
    'spy.png': 'https://financialmodelingprep.com/image-stock/SPY.png',
    'qqq.png': 'https://financialmodelingprep.com/image-stock/QQQ.png',
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
