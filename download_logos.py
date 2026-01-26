import requests
import os

# Create assets/logos directory
os.makedirs('assets/logos', exist_ok=True)

# Logo sources with high-fidelity fallbacks
logos = {
    # Crypto (TrustWallet / DefiLlama / CryptoIcons)
    'btc.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/btc.png',
    'eth.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/eth.png',
    'sol.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/sol.png',
    'usdc.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/usdc.png',
    'usdt.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/usdt.png',
    'bnb.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/bnb.png',
    'jup.png': 'https://assets.coingecko.com/coins/images/29288/large/jupiter-ag-logo.png',
    'ray.png': 'https://icons.llama.fi/raydium.png',
    'jito.png': 'https://icons.llama.fi/jito.png',
    'msol.png': 'https://assets.coingecko.com/coins/images/17767/large/marinade-sol.png',
    'xrp.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/xrp.png',
    'ada.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/ada.png',
    'avax.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/avax.png',
    'link.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/link.png',
    'dot.png': 'https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/dot.png',
    'kamino.png': 'https://assets.coingecko.com/coins/images/37397/large/KMNO.png',
    'orca.png': 'https://assets.coingecko.com/coins/images/17547/large/Orca_Logo.png',
    'marinade.png': 'https://assets.coingecko.com/coins/images/17767/large/marinade-sol.png',
    'solend.png': 'https://assets.coingecko.com/coins/images/19572/large/solend-logo.png',
    'marginfi.png': 'https://icons.llama.fi/marginfi.png',
    'pyth.png': 'https://assets.coingecko.com/coins/images/31924/large/pyth.png',
    'bonk.png': 'https://assets.coingecko.com/coins/images/28600/large/bonk.png',
    
    # Major US Stocks (Financial Modeling Prep)
    'aapl.png': 'https://financialmodelingprep.com/image-stock/AAPL.png',
    'msft.png': 'https://financialmodelingprep.com/image-stock/MSFT.png',
    'nvda.png': 'https://financialmodelingprep.com/image-stock/NVDA.png',
    'googl.png': 'https://financialmodelingprep.com/image-stock/GOOGL.png',
    'amzn.png': 'https://financialmodelingprep.com/image-stock/AMZN.png',
    'meta.png': 'https://financialmodelingprep.com/image-stock/META.png',
    'tsla.png': 'https://financialmodelingprep.com/image-stock/TSLA.png',
    'brk-b.png': 'https://financialmodelingprep.com/image-stock/BRK-B.png',
    'v.png': 'https://financialmodelingprep.com/image-stock/V.png',
    'ma.png': 'https://financialmodelingprep.com/image-stock/MA.png',
    'unh.png': 'https://financialmodelingprep.com/image-stock/UNH.png',
    'jnj.png': 'https://financialmodelingprep.com/image-stock/JNJ.png',
    'jpm.png': 'https://financialmodelingprep.com/image-stock/JPM.png',
    'wmt.png': 'https://financialmodelingprep.com/image-stock/WMT.png',
    'xom.png': 'https://financialmodelingprep.com/image-stock/XOM.png',
    'cvx.png': 'https://financialmodelingprep.com/image-stock/CVX.png',
    'amd.png': 'https://financialmodelingprep.com/image-stock/AMD.png',
    'nflx.png': 'https://financialmodelingprep.com/image-stock/NFLX.png',
    'dis.png': 'https://financialmodelingprep.com/image-stock/DIS.png',
    'cost.png': 'https://financialmodelingprep.com/image-stock/COST.png',
    'gs.png': 'https://financialmodelingprep.com/image-stock/GS.png',
    'hd.png': 'https://financialmodelingprep.com/image-stock/HD.png',
    'pep.png': 'https://financialmodelingprep.com/image-stock/PEP.png',
    'ko.png': 'https://financialmodelingprep.com/image-stock/KO.png',
    
    # Global Stocks
    'asml.png': 'https://financialmodelingprep.com/image-stock/ASML.png',
    'mc.png': 'https://financialmodelingprep.com/image-stock/MC.PA.png', # LVMH
    'sap.png': 'https://financialmodelingprep.com/image-stock/SAP.png',
    'tm.png': 'https://financialmodelingprep.com/image-stock/TM.png', # Toyota
    'samsung.png': 'https://financialmodelingprep.com/image-stock/005930.KS.png',
    'sony.png': 'https://financialmodelingprep.com/image-stock/SONY.png',
    'hsba.png': 'https://financialmodelingprep.com/image-stock/HSBA.L.png', # HSBC
    'bp.png': 'https://financialmodelingprep.com/image-stock/BP.L.png',
    
    # ETFs
    'vti.png': 'https://financialmodelingprep.com/image-stock/VTI.png',
    'spy.png': 'https://financialmodelingprep.com/image-stock/SPY.png',
    'qqq.png': 'https://financialmodelingprep.com/image-stock/QQQ.png',
    'dia.png': 'https://financialmodelingprep.com/image-stock/DIA.png',
    'vnq.png': 'https://financialmodelingprep.com/image-stock/VNQ.png',
    'vwo.png': 'https://financialmodelingprep.com/image-stock/VWO.png',
    'efa.png': 'https://financialmodelingprep.com/image-stock/EFA.png',
    'ewj.png': 'https://financialmodelingprep.com/image-stock/EWJ.png',
    'ewg.png': 'https://financialmodelingprep.com/image-stock/EWG.png',
    'ivv.png': 'https://financialmodelingprep.com/image-stock/IVV.png',
    'voo.png': 'https://financialmodelingprep.com/image-stock/VOO.png',
    'tlt.png': 'https://financialmodelingprep.com/image-stock/TLT.png',
    'bnd.png': 'https://financialmodelingprep.com/image-stock/BND.png',
    'uso.png': 'https://financialmodelingprep.com/image-stock/USO.png',
    'gdx.png': 'https://financialmodelingprep.com/image-stock/GDX.png',
    'vt.png': 'https://financialmodelingprep.com/image-stock/VT.png',
    'gld.png': 'https://financialmodelingprep.com/image-stock/GLD.png',
    
    # Commodities / Currencies (Mapped to icons)
    'gold.png': 'https://financialmodelingprep.com/image-stock/GLD.png',
    'silver.png': 'https://financialmodelingprep.com/image-stock/SLV.png',
    'oil.png': 'https://financialmodelingprep.com/image-stock/USO.png',
    'eur.png': 'https://raw.githubusercontent.com/transferwise/currency-flags/master/src/flags/eur.png',
    'gbp.png': 'https://raw.githubusercontent.com/transferwise/currency-flags/master/src/flags/gbp.png',
    'jpy.png': 'https://raw.githubusercontent.com/transferwise/currency-flags/master/src/flags/jpy.png',
    'ngn.png': 'https://raw.githubusercontent.com/transferwise/currency-flags/master/src/flags/ngn.png'
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
