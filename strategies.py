"""
Investment strategy definitions and screening logic.

Each strategy is a function that receives a `metrics` dict (computed once
per ticker in data.py) and returns either:
    None                      -> ticker does NOT match the strategy
    {"score": float, ...}     -> ticker matches; dict holds display fields

The `metrics` dict carries everything a strategy might need:
    price, prev_close, change_pct
    ret_1m, ret_3m, ret_6m, ret_12m         (% returns)
    rsi, ema50, ema200, sma200
    bb_lower, bb_upper, bb_mid              (Bollinger 20,2)
    vol_avg20, vol_today
    beta, volatility_annual                 (stddev of daily ret * sqrt(252))
    benchmark_ret_6m                        (the market index 6m return)
    # fundamentals (may be None if FMP missing the data):
    pe, pb, peg, roe, debt_to_equity,
    rev_growth, eps_growth, profit_margin,
    dividend_yield, payout_ratio
"""

# Display catalogue shown to the app. `requires` lists which data the model
# needs so the UI can warn if FMP is unavailable for fundamental models.
STRATEGY_CATALOG = [
    {"id": "momentum",    "name": "Momentum",          "icon": "trending-up",  "requires": "technical"},
    {"id": "trend",       "name": "Trend Following",   "icon": "route",        "requires": "technical"},
    {"id": "value",       "name": "Value",             "icon": "diamond",      "requires": "fundamental"},
    {"id": "growth",      "name": "Growth",            "icon": "plant-2",      "requires": "fundamental"},
    {"id": "garp",        "name": "GARP",              "icon": "scale",        "requires": "fundamental"},
    {"id": "dividend",    "name": "Dividend",          "icon": "coins",        "requires": "mixed"},
    {"id": "rel_strength","name": "Relative Strength", "icon": "flame",        "requires": "technical"},
    {"id": "mean_rev",    "name": "Mean Reversion",    "icon": "arrows-down-up","requires": "technical"},
    {"id": "low_vol",     "name": "Low Volatility",    "icon": "shield-check", "requires": "technical"},
    {"id": "quality",     "name": "Quality",           "icon": "award",        "requires": "fundamental"},
]


def _has(*vals):
    """True only if every value is present (not None)."""
    return all(v is not None for v in vals)


# ----------------------------------------------------------------------
# TECHNICAL STRATEGIES (yfinance only)
# ----------------------------------------------------------------------

def s_momentum(m):
    """Strong 6-month performance, not yet overbought."""
    if not _has(m["ret_6m"], m["rsi"]):
        return None
    if m["ret_6m"] > 20 and 50 <= m["rsi"] <= 70:
        return {
            "score": round(m["ret_6m"], 1),
            "tags": [f"6M {m['ret_6m']:+.0f}%", f"RSI {m['rsi']:.0f}"],
        }
    return None


def s_trend(m):
    """Uptrend stack: price > EMA50 > EMA200, with positive 3M momentum.

    The EMA stack alone can flag stocks that are merely drifting; requiring a
    positive 3-month return ensures the trend is actually being pushed.
    """
    if not _has(m["price"], m["ema50"], m["ema200"], m["ret_3m"]):
        return None
    if m["price"] > m["ema50"] > m["ema200"] and m["ret_3m"] > 0:
        gap = (m["price"] / m["ema200"] - 1) * 100
        return {
            "score": round(gap, 1),
            "tags": ["Above EMA50/200", f"3M {m['ret_3m']:+.0f}%"],
        }
    return None


def s_rel_strength(m):
    """Stock outperforming its market benchmark over 6 months by >15pp."""
    if not _has(m["ret_6m"], m["benchmark_ret_6m"]):
        return None
    rs = m["ret_6m"] - m["benchmark_ret_6m"]
    if rs > 15:
        return {
            "score": round(rs, 1),
            "tags": [f"+{rs:.0f}pp vs index", f"6M {m['ret_6m']:+.0f}%"],
        }
    return None


def s_mean_rev(m):
    """Oversold bounce candidate: below lower Bollinger band and RSI < 30."""
    if not _has(m["price"], m["bb_lower"], m["rsi"]):
        return None
    if m["price"] < m["bb_lower"] and m["rsi"] < 30:
        depth = (m["bb_lower"] / m["price"] - 1) * 100
        return {
            "score": round(depth, 1),
            "tags": [f"RSI {m['rsi']:.0f}", "Below lower BB"],
        }
    return None


def s_low_vol(m):
    """Low beta and low realised volatility."""
    if not _has(m["beta"], m["volatility_annual"]):
        return None
    if m["beta"] < 0.8 and m["volatility_annual"] < 25:
        return {
            "score": round(-m["volatility_annual"], 1),  # lower vol -> higher rank
            "tags": [f"β {m['beta']:.2f}", f"Vol {m['volatility_annual']:.0f}%"],
        }
    return None


# ----------------------------------------------------------------------
# FUNDAMENTAL STRATEGIES (need FMP)
# ----------------------------------------------------------------------

def s_value(m):
    """Cheap on P/E and P/B with decent profitability."""
    if not _has(m["pe"], m["pb"], m["roe"]):
        return None
    if 0 < m["pe"] < 15 and 0 < m["pb"] < 1.5 and m["roe"] > 10:
        return {
            "score": round(100 - m["pe"], 1),  # cheaper -> higher rank
            "tags": [f"P/E {m['pe']:.1f}", f"P/B {m['pb']:.1f}", f"ROE {m['roe']:.0f}%"],
        }
    return None


def s_growth(m):
    """Fast top-line and earnings growth."""
    if not _has(m["rev_growth"], m["eps_growth"]):
        return None
    if m["rev_growth"] > 15 and m["eps_growth"] > 20:
        return {
            "score": round(m["eps_growth"], 1),
            "tags": [f"Rev {m['rev_growth']:+.0f}%", f"EPS {m['eps_growth']:+.0f}%"],
        }
    return None


def s_garp(m):
    """Growth at a reasonable price: low PEG with real earnings growth."""
    if not _has(m["peg"], m["eps_growth"]):
        return None
    if 0 < m["peg"] < 1.0 and m["eps_growth"] > 10:
        return {
            "score": round(1 / m["peg"], 2),  # lower PEG -> higher rank
            "tags": [f"PEG {m['peg']:.2f}", f"EPS {m['eps_growth']:+.0f}%"],
        }
    return None


def s_dividend(m):
    """Solid dividend yield with a sustainable payout ratio."""
    if not _has(m["dividend_yield"]):
        return None
    payout_ok = (m["payout_ratio"] is None) or (0 < m["payout_ratio"] < 70)
    if m["dividend_yield"] > 4 and payout_ok:
        tags = [f"Yield {m['dividend_yield']:.1f}%"]
        if m["payout_ratio"] is not None:
            tags.append(f"Payout {m['payout_ratio']:.0f}%")
        return {"score": round(m["dividend_yield"], 1), "tags": tags}
    return None


def s_quality(m):
    """High ROE, low leverage, healthy margins."""
    if not _has(m["roe"], m["profit_margin"]):
        return None
    de_ok = (m["debt_to_equity"] is None) or (m["debt_to_equity"] < 1.0)
    if m["roe"] > 15 and m["profit_margin"] > 10 and de_ok:
        return {
            "score": round(m["roe"], 1),
            "tags": [f"ROE {m['roe']:.0f}%", f"Margin {m['profit_margin']:.0f}%"],
        }
    return None


# Registry mapping strategy id -> screening function
STRATEGIES = {
    "momentum":     s_momentum,
    "trend":        s_trend,
    "value":        s_value,
    "growth":       s_growth,
    "garp":         s_garp,
    "dividend":     s_dividend,
    "rel_strength": s_rel_strength,
    "mean_rev":     s_mean_rev,
    "low_vol":      s_low_vol,
    "quality":      s_quality,
}


def screen(strategy_id, metrics_by_symbol, names_by_symbol):
    """
    Apply one strategy across all symbols, return ranked list of matches.

    metrics_by_symbol: { "AAPL": {metrics...}, ... }
    names_by_symbol:   { "AAPL": "Apple Inc.", ... }
    """
    fn = STRATEGIES.get(strategy_id)
    if fn is None:
        return []

    results = []
    for sym, m in metrics_by_symbol.items():
        if m is None:
            continue
        try:
            hit = fn(m)
        except Exception:
            hit = None
        if hit:
            results.append({
                "symbol": sym,
                "name": names_by_symbol.get(sym, sym),
                "price": m.get("price"),
                "change_pct": m.get("change_pct"),
                "score": hit["score"],
                "tags": hit["tags"],
            })

    results.sort(key=lambda r: r["score"], reverse=True)
    return results
