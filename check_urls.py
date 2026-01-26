import requests
import base64

urls = {
    'BTC': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/btc.png',
    'ETH': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/eth.png',
    'SOL': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/sol.png',
    'VTI': 'https://financialmodelingprep.com/image-stock/VTI.png',
    'MSOL': 'https://assets.coincap.io/assets/icons/msol@2x.png', # Fallback to test
    'JITO': 'https://www.jito.network/favicon.ico'
}

with open('logo_data.txt', 'w', encoding='utf-8') as f:
    for name, url in urls.items():
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                b64 = base64.b64encode(r.content).decode()
                f.write(f"{name}_B64 = \"{b64}\"\n\n")
                print(f"Captured {name}")
            else:
                f.write(f"{name}_B64 = \"\" # FAILED {r.status_code}\n\n")
                print(f"Failed {name}: {r.status_code}")
        except Exception as e:
            f.write(f"{name}_B64 = \"\" # ERROR {e}\n\n")
            print(f"Error {name}: {e}")
