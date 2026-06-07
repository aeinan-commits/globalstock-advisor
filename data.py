"""
Data acquisition + metrics computation.

Technical data  -> yfinance (free, no key)
Fundamental data -> Financial Modeling Prep (FMP) free tier (needs API key)

Everything funnels into compute_metrics() which returns the dict consumed
by strategies.py.

Set the FMP key via environment variable:  FMP_API_KEY
If absent, fundamental fields are None and fundamental strategies simply
return no matches (technical strategies keep working).
"""

import os
import time
import math
import requests

import numpy as np
import pandas as pd
import yfinance as yf

FMP_API_KEY = os.environ.get("FMP_API_KEY", "")
FMP_BASE = "https://financialmodelingprep.com/api/v3"

# Benchmark ticker per market id (used by Relative Strength)
BENCHMARK = {
    "SP500": "^GSPC", "NASDAQ100": "^NDX", "DOW30": "^DJI",
    "IBOV": "^BVSP", "TSX": "^GSPTSE", "MEX": "^MXX",
    "DAX40": "^GDAXI", "FTSE100": "^FTSE", "CAC40": "^FCHI",
    "IBEX35": "^IBEX", "FTSEMIB": "FTSEMIB.MI", "AEX": "^AEX", "SMI": "^SSMI",
    "NIKKEI": "^N225", "HANGSENG": "^HSI", "NIFTY50": "^NSEI",
    "KOSPI": "^KS11", "TWSE": "^TWII",
    "BIST100": "XU100.IS", "SET50": "^SET.BK", "IDX": "^JKSE",
    "KLSE": "^KLSE", "PSE": "^PSI", "TASI": "^TASI.SR",
    "JSE": "^J203.JO", "ASX": "^AXJO",
}


# ----------------------------------------------------------------------
# Technical indicators
# ----------------------------------------------------------------------

def _rsi(close, period=14):
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def _ema(close, span):
    return close.ewm(span=span, adjust=False).mean()


def _pct_return(close, days):
    if len(close) <= days:
        return None
    old = close.iloc[-days - 1]
    new = close.iloc[-1]
    if old == 0 or pd.isna(old):
        return None
    return (new / old - 1) * 100


def compute_technical(hist):
    """Compute technical metrics from a yfinance history DataFrame."""
    if hist is None or hist.empty or len(hist) < 30:
        return None

    close = hist["Close"].dropna()
    vol = hist["Volume"].dropna()
    if len(close) < 30:
        return None

    price = float(close.iloc[-1])
    prev = float(close.iloc[-2]) if len(close) > 1 else price

    rsi_series = _rsi(close)
    rsi = float(rsi_series.iloc[-1]) if not pd.isna(rsi_series.iloc[-1]) else None

    ema50 = float(_ema(close, 50).iloc[-1]) if len(close) >= 50 else None
    ema200 = float(_ema(close, 200).iloc[-1]) if len(close) >= 200 else None

    # Bollinger 20, 2
    if len(close) >= 20:
        mid = close.rolling(20).mean().iloc[-1]
        std = close.rolling(20).std().iloc[-1]
        bb_mid = float(mid)
        bb_lower = float(mid - 2 * std)
        bb_upper = float(mid + 2 * std)
    else:
        bb_mid = bb_lower = bb_upper = None

    daily_ret = close.pct_change().dropna()
    vol_annual = float(daily_ret.std() * math.sqrt(252) * 100) if len(daily_ret) > 5 else None

    return {
        "price": round(price, 2),
        "prev_close": round(prev, 2),
        "change_pct": round((price / prev - 1) * 100, 2) if prev else None,
        "ret_1m": _pct_return(close, 21),
        "ret_3m": _pct_return(close, 63),
        "ret_6m": _pct_return(close, 126),
        "ret_12m": _pct_return(close, 252),
        "rsi": round(rsi, 1) if rsi is not None else None,
        "ema50": round(ema50, 2) if ema50 else None,
        "ema200": round(ema200, 2) if ema200 else None,
        "bb_lower": round(bb_lower, 2) if bb_lower else None,
        "bb_upper": round(bb_upper, 2) if bb_upper else None,
        "bb_mid": round(bb_mid, 2) if bb_mid else None,
        "vol_today": float(vol.iloc[-1]) if len(vol) else None,
        "vol_avg20": float(vol.rolling(20).mean().iloc[-1]) if len(vol) >= 20 else None,
        "volatility_annual": round(vol_annual, 1) if vol_annual else None,
    }


# ----------------------------------------------------------------------
# Bulk price download (one call for the whole universe = fast)
# ----------------------------------------------------------------------

def download_histories(symbols, period="1y"):
    """
    Download daily history for many tickers in a single batched request.
    Returns { symbol: DataFrame }.
    """
    if not symbols:
        return {}

    data = yf.download(
        tickers=" ".join(symbols),
        period=period,
        interval="1d",
        group_by="ticker",
        auto_adjust=True,
        threads=True,
        progress=False,
    )

    out = {}
    if len(symbols) == 1:
        out[symbols[0]] = data
        return out

    for sym in symbols:
        try:
            df = data[sym].dropna(how="all")
            if not df.empty:
                out[sym] = df
        except (KeyError, Exception):
            continue
    return out


def get_info_batch(symbols):
    """
    Pull lightweight per-ticker info (name, beta, dividend yield, P/E, P/B)
    from yfinance. Slower than price download, so used sparingly.
    """
    info = {}
    for sym in symbols:
        try:
            t = yf.Ticker(sym)
            fi = t.fast_info
            inf = {}
            try:
                inf = t.info or {}
            except Exception:
                inf = {}
            info[sym] = {
                "name": inf.get("shortName") or inf.get("longName") or sym,
                "beta": inf.get("beta"),
                "pe": inf.get("trailingPE"),
                "pb": inf.get("priceToBook"),
                "dividend_yield": (inf.get("dividendYield") or 0) * 100 if inf.get("dividendYield") else None,
                "payout_ratio": (inf.get("payoutRatio") or 0) * 100 if inf.get("payoutRatio") else None,
                "profit_margin": (inf.get("profitMargins") or 0) * 100 if inf.get("profitMargins") else None,
            }
        except Exception:
            info[sym] = {"name": sym}
        time.sleep(0.05)
    return info


# ----------------------------------------------------------------------
# FMP fundamentals (optional)
# ----------------------------------------------------------------------

def get_fmp_fundamentals(symbol):
    """Fetch fundamental ratios from FMP. Returns {} on any failure."""
    if not FMP_API_KEY:
        return {}
    try:
        r = requests.get(
            f"{FMP_BASE}/ratios-ttm/{symbol}",
            params={"apikey": FMP_API_KEY}, timeout=10,
        )
        ratios = r.json()
        r2 = requests.get(
            f"{FMP_BASE}/financial-growth/{symbol}",
            params={"apikey": FMP_API_KEY, "limit": 1}, timeout=10,
        )
        growth = r2.json()

        ratios = ratios[0] if isinstance(ratios, list) and ratios else {}
        growth = growth[0] if isinstance(growth, list) and growth else {}

        def pct(x):
            return round(x * 100, 1) if isinstance(x, (int, float)) else None

        return {
            "pe": ratios.get("peRatioTTM"),
            "pb": ratios.get("priceToBookRatioTTM"),
            "peg": ratios.get("pegRatioTTM"),
            "roe": pct(ratios.get("returnOnEquityTTM")),
            "debt_to_equity": ratios.get("debtEquityRatioTTM"),
            "profit_margin": pct(ratios.get("netProfitMarginTTM")),
            "dividend_yield": pct(ratios.get("dividendYieldTTM")),
            "payout_ratio": pct(ratios.get("payoutRatioTTM")),
            "rev_growth": pct(growth.get("revenueGrowth")),
            "eps_growth": pct(growth.get("epsgrowth")),
        }
    except Exception:
        return {}


# ----------------------------------------------------------------------
# Master assembler
# ----------------------------------------------------------------------

def compute_metrics(symbols, market_id, use_fundamentals=False):
    """
    Build the metrics dict for every symbol in `symbols`.
    Returns (metrics_by_symbol, names_by_symbol).
    """
    histories = download_histories(symbols, period="1y")

    # Benchmark 6m return for relative strength
    bench_ret_6m = None
    bench = BENCHMARK.get(market_id)
    if bench:
        bh = download_histories([bench], period="1y").get(bench)
        if bh is not None and not bh.empty:
            bench_ret_6m = _pct_return(bh["Close"].dropna(), 126)

    info = get_info_batch(symbols)

    metrics = {}
    names = {}
    for sym in symbols:
        names[sym] = info.get(sym, {}).get("name", sym)
        tech = compute_technical(histories.get(sym))
        if tech is None:
            metrics[sym] = None
            continue

        inf = info.get(sym, {})
        m = dict(tech)
        m["beta"] = inf.get("beta")
        m["benchmark_ret_6m"] = bench_ret_6m

        # default fundamentals from yfinance info
        m["pe"] = inf.get("pe")
        m["pb"] = inf.get("pb")
        m["peg"] = None
        m["roe"] = None
        m["debt_to_equity"] = None
        m["rev_growth"] = None
        m["eps_growth"] = None
        m["profit_margin"] = inf.get("profit_margin")
        m["dividend_yield"] = inf.get("dividend_yield")
        m["payout_ratio"] = inf.get("payout_ratio")

        # override with richer FMP data if requested + available
        if use_fundamentals and FMP_API_KEY:
            fmp = get_fmp_fundamentals(sym)
            for k, v in fmp.items():
                if v is not None:
                    m[k] = v

        metrics[sym] = m

    return metrics, names
