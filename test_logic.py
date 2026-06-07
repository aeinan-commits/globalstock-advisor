"""
Validate strategy screening logic with synthetic metrics (no network).
Each fake stock is crafted to hit (or miss) specific strategies.
"""
import sys
sys.path.insert(0, "/home/claude/stockadvisor")
from app import strategies as st

# Build a few synthetic stocks with full metric dicts
def base():
    return {
        "price": 100, "prev_close": 99, "change_pct": 1.0,
        "ret_1m": 5, "ret_3m": 10, "ret_6m": 8, "ret_12m": 12,
        "rsi": 55, "ema50": 95, "ema200": 90,
        "bb_lower": 92, "bb_upper": 108, "bb_mid": 100,
        "vol_today": 1e6, "vol_avg20": 9e5, "volatility_annual": 30,
        "beta": 1.1, "benchmark_ret_6m": 5,
        "pe": 20, "pb": 3, "peg": 2, "roe": 12,
        "debt_to_equity": 0.8, "rev_growth": 8, "eps_growth": 10,
        "profit_margin": 8, "dividend_yield": 1.5, "payout_ratio": 40,
    }

stocks = {}

# MOMO: strong 6m + RSI in band
s = base(); s["ret_6m"] = 35; s["rsi"] = 62; stocks["MOMO"] = s
# TREND: price>ema50>ema200
s = base(); s["price"] = 120; s["ema50"] = 110; s["ema200"] = 100; stocks["TREND"] = s
# VALUE: cheap
s = base(); s["pe"] = 9; s["pb"] = 1.1; s["roe"] = 18; stocks["VALUE"] = s
# GROWTH
s = base(); s["rev_growth"] = 25; s["eps_growth"] = 40; stocks["GROWTH"] = s
# GARP
s = base(); s["peg"] = 0.7; s["eps_growth"] = 22; stocks["GARP"] = s
# DIVIDEND
s = base(); s["dividend_yield"] = 6.2; s["payout_ratio"] = 55; stocks["DIVID"] = s
# RELSTR: beats benchmark by >15
s = base(); s["ret_6m"] = 40; s["benchmark_ret_6m"] = 10; stocks["RELST"] = s
# MEANREV: below lower BB + RSI<30
s = base(); s["price"] = 80; s["bb_lower"] = 85; s["rsi"] = 25; stocks["MEANR"] = s
# LOWVOL
s = base(); s["beta"] = 0.6; s["volatility_annual"] = 18; stocks["LOWV"] = s
# QUALITY
s = base(); s["roe"] = 25; s["profit_margin"] = 18; s["debt_to_equity"] = 0.4; stocks["QUAL"] = s
# DUD: matches nothing
stocks["DUD"] = base()

names = {k: f"{k} Corp" for k in stocks}

print(f"{'STRATEGY':<14} {'MATCHES':<8} TICKERS")
print("-" * 50)
for sid in st.STRATEGIES:
    res = st.screen(sid, stocks, names)
    tickers = ", ".join(r["symbol"] for r in res)
    print(f"{sid:<14} {len(res):<8} {tickers}")

print("\nDetail sample — momentum match:")
for r in st.screen("momentum", stocks, names):
    print(" ", r)
