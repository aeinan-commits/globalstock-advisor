"""
Global market index constituents.

These are SEED lists (hand-curated starting points). In production the
backend refreshes them automatically from Wikipedia / exchange sources
via the update_indices() routine in updater.py.

Each market entry:
  - name:     display name shown in the app
  - flag:     emoji flag for the UI
  - suffix:   yfinance ticker suffix ("" for US)
  - symbols:  list of FULL yfinance tickers (suffix already applied)
"""

MARKETS = {
    # ------------------------------------------------------------------
    # AMERICAS
    # ------------------------------------------------------------------
    "SP500": {
        "name": "USA — S&P 500 (top liquid)",
        "flag": "🇺🇸",
        "suffix": "",
        "symbols": [
            "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "NVDA", "META", "TSLA",
            "BRK-B", "JPM", "V", "MA", "UNH", "HD", "PG", "JNJ", "XOM", "CVX",
            "LLY", "ABBV", "AVGO", "COST", "PEP", "KO", "WMT", "MRK", "BAC",
            "ADBE", "CRM", "NFLX", "AMD", "TMO", "ACN", "MCD", "CSCO", "ABT",
            "DHR", "WFC", "TXN", "DIS", "INTC", "VZ", "QCOM", "PM", "INTU",
            "CAT", "IBM", "GE", "AMGN", "NKE", "HON", "UNP", "LOW", "SPGI",
            "GS", "BA", "PFE", "AMAT", "BKNG", "ELV", "SYK", "BLK", "T",
            "PLD", "GILD", "MDT", "ADI", "MMC", "LRCX", "VRTX", "REGN", "C",
            "CB", "NOW", "ISRG", "TJX", "ZTS", "MU", "ETN", "BSX", "PGR",
            "SO", "CME", "DUK", "MO", "SLB", "EOG", "BDX", "ITW", "AON",
            "CSX", "APD", "WM", "FCX", "MCK", "NSC", "EMR", "GD", "FDX",
        ],
    },
    "NASDAQ100": {
        "name": "USA — NASDAQ 100",
        "flag": "🇺🇸",
        "suffix": "",
        "symbols": [
            "AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "GOOG", "TSLA",
            "AVGO", "COST", "PEP", "ADBE", "NFLX", "AMD", "CSCO", "TMUS",
            "INTC", "QCOM", "INTU", "AMAT", "TXN", "ISRG", "BKNG", "HON",
            "VRTX", "ADP", "REGN", "LRCX", "MU", "PANW", "GILD", "SBUX",
            "MDLZ", "KLAC", "SNPS", "CDNS", "MRVL", "CRWD", "ABNB", "ORLY",
            "CSX", "FTNT", "ADI", "MELI", "PYPL", "MAR", "MNST", "CTAS",
            "WDAY", "NXPI", "ROP", "PCAR", "ADSK", "CPRT", "ROST", "DXCM",
            "PAYX", "AEP", "KDP", "ODFL", "FAST", "EA", "VRSK", "KHC",
            "EXC", "CTSH", "GEHC", "CCEP", "LULU", "DDOG", "BKR", "XEL",
            "IDXX", "ON", "ZS", "TTD", "CSGP", "ANSS", "DLTR", "MDB",
            "WBD", "TEAM", "ILMN", "MRNA", "WBA", "SIRI",
        ],
    },
    "DOW30": {
        "name": "USA — Dow Jones 30",
        "flag": "🇺🇸",
        "suffix": "",
        "symbols": [
            "AAPL", "MSFT", "JPM", "V", "UNH", "HD", "PG", "JNJ", "CVX",
            "MRK", "WMT", "CRM", "MCD", "CSCO", "DIS", "VZ", "IBM", "CAT",
            "GS", "BA", "AMGN", "NKE", "HON", "AXP", "TRV", "MMM", "KO",
            "DOW", "WBA", "INTC",
        ],
    },
    "IBOV": {
        "name": "Brazil — Bovespa",
        "flag": "🇧🇷",
        "suffix": ".SA",
        "symbols": [
            "PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "B3SA3.SA",
            "ABEV3.SA", "BBAS3.SA", "WEGE3.SA", "RENT3.SA", "SUZB3.SA",
            "ITSA4.SA", "JBSS3.SA", "EQTL3.SA", "RDOR3.SA", "PRIO3.SA",
            "ELET3.SA", "RADL3.SA", "GGBR4.SA", "VBBR3.SA", "HAPV3.SA",
            "LREN3.SA", "RAIL3.SA", "CSAN3.SA", "EMBR3.SA", "UGPA3.SA",
        ],
    },
    "TSX": {
        "name": "Canada — TSX (top)",
        "flag": "🇨🇦",
        "suffix": ".TO",
        "symbols": [
            "RY.TO", "TD.TO", "ENB.TO", "BN.TO", "CNR.TO", "BMO.TO",
            "CP.TO", "CNQ.TO", "BNS.TO", "TRP.TO", "SHOP.TO", "SU.TO",
            "MFC.TO", "CM.TO", "ATD.TO", "NTR.TO", "FNV.TO", "WCN.TO",
            "TRI.TO", "GIB-A.TO",
        ],
    },
    "MEX": {
        "name": "Mexico — IPC (top)",
        "flag": "🇲🇽",
        "suffix": ".MX",
        "symbols": [
            "WALMEX.MX", "FEMSAUBD.MX", "GFNORTEO.MX", "GMEXICOB.MX",
            "AMXB.MX", "BIMBOA.MX", "CEMEXCPO.MX", "TLEVISACPO.MX",
            "KIMBERA.MX", "ALFAA.MX", "GAPB.MX", "ASURB.MX", "PINFRA.MX",
        ],
    },

    # ------------------------------------------------------------------
    # EUROPE
    # ------------------------------------------------------------------
    "DAX40": {
        "name": "Germany — DAX 40",
        "flag": "🇩🇪",
        "suffix": ".DE",
        "symbols": [
            "SAP.DE", "SIE.DE", "ALV.DE", "DTE.DE", "AIR.DE", "MRK.DE",
            "MBG.DE", "BMW.DE", "BAS.DE", "BAYN.DE", "VOW3.DE", "ADS.DE",
            "DB1.DE", "MUV2.DE", "IFX.DE", "RWE.DE", "EOAN.DE", "DBK.DE",
            "HEN3.DE", "BEI.DE", "VNA.DE", "DHL.DE", "FRE.DE", "CON.DE",
            "HEI.DE", "SY1.DE", "BNR.DE", "QIA.DE", "RHM.DE", "ZAL.DE",
            "P911.DE", "CBK.DE", "MTX.DE", "HNR1.DE", "SHL.DE", "ENR.DE",
            "FME.DE", "1COV.DE", "PAH3.DE", "SRT3.DE",
        ],
    },
    "FTSE100": {
        "name": "UK — FTSE 100 (top)",
        "flag": "🇬🇧",
        "suffix": ".L",
        "symbols": [
            "AZN.L", "SHEL.L", "HSBA.L", "ULVR.L", "BP.L", "RIO.L",
            "GSK.L", "DGE.L", "REL.L", "GLEN.L", "BATS.L", "LSEG.L",
            "NG.L", "RR.L", "BARC.L", "AAL.L", "PRU.L", "VOD.L",
            "LLOY.L", "NWG.L", "TSCO.L", "BA.L", "IMB.L", "CPG.L",
            "AHT.L", "STAN.L", "SSE.L", "EXPN.L", "ANTO.L", "AV.L",
        ],
    },
    "CAC40": {
        "name": "France — CAC 40",
        "flag": "🇫🇷",
        "suffix": ".PA",
        "symbols": [
            "MC.PA", "OR.PA", "TTE.PA", "SAN.PA", "AIR.PA", "SU.PA",
            "AI.PA", "EL.PA", "BNP.PA", "CS.PA", "DG.PA", "SAF.PA",
            "RMS.PA", "BN.PA", "KER.PA", "STLAP.PA", "CAP.PA", "DSY.PA",
            "ENGI.PA", "VIE.PA", "ACA.PA", "ORA.PA", "GLE.PA", "ML.PA",
            "LR.PA", "PUB.PA", "RI.PA", "HO.PA", "STMPA.PA", "TEP.PA",
        ],
    },
    "IBEX35": {
        "name": "Spain — IBEX 35 (top)",
        "flag": "🇪🇸",
        "suffix": ".MC",
        "symbols": [
            "ITX.MC", "IBE.MC", "SAN.MC", "BBVA.MC", "AMS.MC", "CABK.MC",
            "TEF.MC", "FER.MC", "AENA.MC", "REP.MC", "ELE.MC", "NTGY.MC",
            "RED.MC", "ACS.MC", "MAP.MC", "GRF.MC", "ANA.MC", "SAB.MC",
        ],
    },
    "FTSEMIB": {
        "name": "Italy — FTSE MIB (top)",
        "flag": "🇮🇹",
        "suffix": ".MI",
        "symbols": [
            "ENI.MI", "ISP.MI", "UCG.MI", "ENEL.MI", "STLAM.MI", "RACE.MI",
            "G.MI", "PRY.MI", "MONC.MI", "TIT.MI", "STM.MI", "BMED.MI",
            "FBK.MI", "LDO.MI", "TRN.MI", "SRG.MI", "BAMI.MI", "MB.MI",
        ],
    },
    "AEX": {
        "name": "Netherlands — AEX",
        "flag": "🇳🇱",
        "suffix": ".AS",
        "symbols": [
            "ASML.AS", "PRX.AS", "INGA.AS", "ADYEN.AS", "AD.AS", "PHIA.AS",
            "WKL.AS", "HEIA.AS", "ABN.AS", "ASRNL.AS", "AKZA.AS", "DSFIR.AS",
            "MT.AS", "RAND.AS", "KPN.AS", "NN.AS", "BESI.AS", "IMCD.AS",
        ],
    },
    "SMI": {
        "name": "Switzerland — SMI",
        "flag": "🇨🇭",
        "suffix": ".SW",
        "symbols": [
            "NESN.SW", "ROG.SW", "NOVN.SW", "UBSG.SW", "ZURN.SW", "ABBN.SW",
            "LONN.SW", "SIKA.SW", "GIVN.SW", "CFR.SW", "SREN.SW", "ALC.SW",
            "GEBN.SW", "SLHN.SW", "HOLN.SW", "PGHN.SW", "SCMN.SW", "LOGN.SW",
        ],
    },

    # ------------------------------------------------------------------
    # ASIA-PACIFIC
    # ------------------------------------------------------------------
    "NIKKEI": {
        "name": "Japan — Nikkei (top)",
        "flag": "🇯🇵",
        "suffix": ".T",
        "symbols": [
            "7203.T", "6758.T", "6861.T", "8306.T", "9984.T", "6098.T",
            "9433.T", "8035.T", "4063.T", "6501.T", "7974.T", "9432.T",
            "8058.T", "8001.T", "6902.T", "4519.T", "6594.T", "7741.T",
            "8316.T", "6367.T", "9020.T", "4502.T", "6981.T", "8031.T",
            "7267.T", "6273.T", "4661.T", "8766.T", "6954.T", "6752.T",
        ],
    },
    "HANGSENG": {
        "name": "Hong Kong — Hang Seng (top)",
        "flag": "🇭🇰",
        "suffix": ".HK",
        "symbols": [
            "0700.HK", "0941.HK", "0939.HK", "1299.HK", "0005.HK", "9988.HK",
            "3690.HK", "1810.HK", "2318.HK", "0388.HK", "1398.HK", "0883.HK",
            "0016.HK", "2628.HK", "0001.HK", "0027.HK", "0386.HK", "1113.HK",
            "2020.HK", "9618.HK", "9999.HK", "0288.HK", "1024.HK", "2269.HK",
        ],
    },
    "NIFTY50": {
        "name": "India — Nifty 50 (top)",
        "flag": "🇮🇳",
        "suffix": ".NS",
        "symbols": [
            "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS",
            "INFY.NS", "BHARTIARTL.NS", "SBIN.NS", "LT.NS", "ITC.NS",
            "HINDUNILVR.NS", "BAJFINANCE.NS", "KOTAKBANK.NS", "AXISBANK.NS",
            "ASIANPAINT.NS", "MARUTI.NS", "SUNPHARMA.NS", "TITAN.NS",
            "ULTRACEMCO.NS", "WIPRO.NS", "NESTLEIND.NS", "ONGC.NS",
            "NTPC.NS", "POWERGRID.NS", "M&M.NS", "TATAMOTORS.NS",
            "HCLTECH.NS", "TATASTEEL.NS", "ADANIENT.NS", "JSWSTEEL.NS",
            "COALINDIA.NS",
        ],
    },
    "KOSPI": {
        "name": "South Korea — KOSPI (top)",
        "flag": "🇰🇷",
        "suffix": ".KS",
        "symbols": [
            "005930.KS", "000660.KS", "373220.KS", "207940.KS", "005380.KS",
            "005490.KS", "051910.KS", "035420.KS", "006400.KS", "000270.KS",
            "012330.KS", "068270.KS", "035720.KS", "105560.KS", "055550.KS",
            "066570.KS", "003670.KS", "096770.KS", "017670.KS", "034730.KS",
        ],
    },
    "TWSE": {
        "name": "Taiwan — TWSE (top)",
        "flag": "🇹🇼",
        "suffix": ".TW",
        "symbols": [
            "2330.TW", "2317.TW", "2454.TW", "2308.TW", "2382.TW",
            "2412.TW", "2881.TW", "2882.TW", "1303.TW", "1301.TW",
            "2303.TW", "3711.TW", "2891.TW", "2886.TW", "5880.TW",
            "2884.TW", "3008.TW", "2002.TW", "2207.TW", "1216.TW",
        ],
    },

    # ------------------------------------------------------------------
    # SOUTHEAST ASIA / EMERGING
    # ------------------------------------------------------------------
    "BIST100": {
        "name": "Turkey — BIST 100 (top)",
        "flag": "🇹🇷",
        "suffix": ".IS",
        "symbols": [
            "THYAO.IS", "ASELS.IS", "GARAN.IS", "AKBNK.IS", "ISCTR.IS",
            "KCHOL.IS", "BIMAS.IS", "SAHOL.IS", "EREGL.IS", "FROTO.IS",
            "TUPRS.IS", "SISE.IS", "YKBNK.IS", "TCELL.IS", "PGSUS.IS",
            "ASTOR.IS", "KOZAL.IS", "TOASO.IS", "HEKTS.IS", "SASA.IS",
            "ENKAI.IS", "PETKM.IS", "KONTR.IS", "OYAKC.IS", "VESTL.IS",
            "TAVHL.IS", "MGROS.IS", "ARCLK.IS", "GUBRF.IS", "ALARK.IS",
            "EKGYO.IS", "TTKOM.IS", "DOAS.IS", "ULKER.IS", "AEFES.IS",
            "BRSAN.IS", "KOZAA.IS", "TKFEN.IS", "CIMSA.IS", "SOKM.IS",
        ],
    },
    "SET50": {
        "name": "Thailand — SET50 (top)",
        "flag": "🇹🇭",
        "suffix": ".BK",
        "symbols": [
            "PTT.BK", "AOT.BK", "CPALL.BK", "ADVANC.BK", "GULF.BK",
            "PTTEP.BK", "SCB.BK", "BBL.BK", "KBANK.BK", "CPN.BK",
            "BDMS.BK", "SCC.BK", "DELTA.BK", "INTUCH.BK", "TRUE.BK",
            "KTB.BK", "MINT.BK", "CRC.BK", "OR.BK", "BH.BK",
        ],
    },
    "IDX": {
        "name": "Indonesia — IDX (top)",
        "flag": "🇮🇩",
        "suffix": ".JK",
        "symbols": [
            "BBCA.JK", "BBRI.JK", "BMRI.JK", "TLKM.JK", "ASII.JK",
            "BBNI.JK", "UNVR.JK", "ICBP.JK", "GOTO.JK", "ADRO.JK",
            "AMRT.JK", "KLBF.JK", "INDF.JK", "CPIN.JK", "SMGR.JK",
            "UNTR.JK", "MDKA.JK", "ANTM.JK", "PGAS.JK", "TPIA.JK",
        ],
    },
    "KLSE": {
        "name": "Malaysia — Bursa (top)",
        "flag": "🇲🇾",
        "suffix": ".KL",
        "symbols": [
            "1155.KL", "5347.KL", "1023.KL", "6888.KL", "1295.KL",
            "5183.KL", "6033.KL", "3816.KL", "1066.KL", "4863.KL",
            "5681.KL", "6947.KL", "1961.KL", "2445.KL", "4677.KL",
        ],
    },
    "PSE": {
        "name": "Philippines — PSEi (top)",
        "flag": "🇵🇭",
        "suffix": ".PS",
        "symbols": [
            "SM.PS", "BDO.PS", "SMPH.PS", "ALI.PS", "BPI.PS",
            "AC.PS", "JGS.PS", "ICT.PS", "MBT.PS", "TEL.PS",
            "URC.PS", "GTCAP.PS", "MER.PS", "AEV.PS", "JFC.PS",
        ],
    },

    # ------------------------------------------------------------------
    # MIDDLE EAST / AFRICA / OCEANIA
    # ------------------------------------------------------------------
    "TASI": {
        "name": "Saudi Arabia — Tadawul (top)",
        "flag": "🇸🇦",
        "suffix": ".SR",
        "symbols": [
            "2222.SR", "1120.SR", "2010.SR", "7010.SR", "1180.SR",
            "2350.SR", "1010.SR", "1211.SR", "2280.SR", "4001.SR",
            "1150.SR", "7020.SR", "2380.SR", "1060.SR", "4013.SR",
        ],
    },
    "JSE": {
        "name": "South Africa — JSE (top)",
        "flag": "🇿🇦",
        "suffix": ".JO",
        "symbols": [
            "NPN.JO", "PRX.JO", "FSR.JO", "SBK.JO", "ABG.JO",
            "MTN.JO", "VOD.JO", "AGL.JO", "BTI.JO", "CFR.JO",
            "SLM.JO", "SOL.JO", "GFI.JO", "ANG.JO", "IMP.JO",
        ],
    },
    "ASX": {
        "name": "Australia — ASX (top)",
        "flag": "🇦🇺",
        "suffix": ".AX",
        "symbols": [
            "BHP.AX", "CBA.AX", "CSL.AX", "NAB.AX", "WBC.AX",
            "ANZ.AX", "MQG.AX", "WES.AX", "GMG.AX", "FMG.AX",
            "WOW.AX", "TLS.AX", "RIO.AX", "TCL.AX", "WDS.AX",
            "STO.AX", "QBE.AX", "COL.AX", "REA.AX", "ALL.AX",
        ],
    },
}


def get_market_list():
    """Return lightweight market metadata for the app's dropdown."""
    return [
        {"id": k, "name": v["name"], "flag": v["flag"], "count": len(v["symbols"])}
        for k, v in MARKETS.items()
    ]


def get_symbols(market_id):
    """Return the ticker list for a market id, or empty list if unknown."""
    m = MARKETS.get(market_id)
    return m["symbols"] if m else []


if __name__ == "__main__":
    total = sum(len(v["symbols"]) for v in MARKETS.values())
    print(f"Markets: {len(MARKETS)} | Total symbols: {total}")
    for mid, m in MARKETS.items():
        print(f"  {m['flag']} {mid:10s} {len(m['symbols']):3d}  {m['name']}")
