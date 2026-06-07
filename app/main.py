"""
GlobalStock Advisor — backend API (FastAPI).

Endpoints
---------
GET  /                      health check
GET  /markets               list of available markets for the dropdown
GET  /strategies            list of available strategy models
GET  /scan?market=&strategy=   run a screen, return ranked matches

Caching
-------
A scan for a (market, strategy) pair is expensive (downloads prices for the
whole universe). We cache the *raw metrics* per market for CACHE_TTL seconds,
so switching strategies on the same market is instant, and repeated scans
within the TTL window don't re-hit yfinance.
"""

import time
import threading

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from . import markets as mk
from . import data as dt
from . import strategies as st

CACHE_TTL = 900  # 15 minutes

app = FastAPI(title="GlobalStock Advisor API", version="0.1.0")

# Allow the mobile app (any origin) to call us
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# market_id -> {"ts": epoch, "metrics": {...}, "names": {...}}
_cache = {}
_lock = threading.Lock()

DISCLAIMER = (
    "This application provides information for educational purposes only and "
    "does not constitute investment advice, a recommendation, or an offer to "
    "buy or sell any security. Markets carry risk. Always do your own research "
    "and consult a licensed financial advisor. You trade at your own risk."
)


def _get_metrics(market_id, use_fundamentals):
    """Return cached metrics for a market, refreshing if stale."""
    now = time.time()
    with _lock:
        entry = _cache.get(market_id)
        if entry and (now - entry["ts"] < CACHE_TTL) and \
           entry.get("fund") == use_fundamentals:
            return entry["metrics"], entry["names"]

    symbols = mk.get_symbols(market_id)
    metrics, names = dt.compute_metrics(symbols, market_id, use_fundamentals)

    with _lock:
        _cache[market_id] = {
            "ts": now, "metrics": metrics, "names": names,
            "fund": use_fundamentals,
        }
    return metrics, names


@app.get("/")
def health():
    return {"status": "ok", "service": "GlobalStock Advisor API"}


@app.get("/disclaimer")
def disclaimer():
    return {"disclaimer": DISCLAIMER}


@app.get("/markets")
def list_markets():
    return {"markets": mk.get_market_list()}


@app.get("/strategies")
def list_strategies():
    return {"strategies": st.STRATEGY_CATALOG}


@app.get("/scan")
def scan(
    market: str = Query(..., description="Market id, e.g. BIST100"),
    strategy: str = Query(..., description="Strategy id, e.g. momentum"),
    limit: int = Query(25, ge=1, le=100),
):
    if market not in mk.MARKETS:
        return {"error": f"Unknown market '{market}'", "markets": list(mk.MARKETS.keys())}
    if strategy not in st.STRATEGIES:
        return {"error": f"Unknown strategy '{strategy}'", "strategies": list(st.STRATEGIES.keys())}

    # Does this strategy need fundamentals?
    cat = next((c for c in st.STRATEGY_CATALOG if c["id"] == strategy), {})
    needs_fund = cat.get("requires") in ("fundamental", "mixed")

    metrics, names = _get_metrics(market, use_fundamentals=needs_fund)
    results = st.screen(strategy, metrics, names)

    return {
        "market": market,
        "strategy": strategy,
        "count": len(results),
        "results": results[:limit],
        "disclaimer": DISCLAIMER,
        "cached_at": _cache.get(market, {}).get("ts"),
    }
