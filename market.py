"""
ArthaMind AI — Market Data Module
===================================
Fetches live gold, silver, and currency exchange rates from
free APIs with multi-source fallback and caching.
"""

import time
from datetime import datetime
from typing import Any, Optional

import requests

from config import settings
from utils import logger, timer


# ═══════════════════════════════════════════════════════════════
#  CACHE
# ═══════════════════════════════════════════════════════════════

class DataCache:
    """Simple time-based cache for API responses."""

    def __init__(self, ttl_seconds: int = 600):
        self._cache: dict[str, dict[str, Any]] = {}
        self._ttl = ttl_seconds

    def get(self, key: str) -> Optional[Any]:
        """Retrieve a cached value if still valid."""
        entry = self._cache.get(key)
        if entry and (time.time() - entry["timestamp"]) < self._ttl:
            logger.debug(f"Cache hit for '{key}'")
            return entry["data"]
        return None

    def set(self, key: str, data: Any) -> None:
        """Store a value in cache with current timestamp."""
        self._cache[key] = {"data": data, "timestamp": time.time()}

    def clear(self) -> None:
        """Clear all cached data."""
        self._cache.clear()


# Module-level cache (10-minute TTL)
_cache = DataCache(ttl_seconds=600)


# ═══════════════════════════════════════════════════════════════
#  GOLD & SILVER PRICES
# ═══════════════════════════════════════════════════════════════

class MetalPriceFetcher:
    """Fetches gold and silver prices in INR with fallback sources."""

    @staticmethod
    @timer
    def get_gold_price() -> dict[str, Any]:
        """Fetch current gold prices in INR.

        Tries GoldAPI.io first, then falls back to approximate values.

        Returns:
            Dictionary with price_per_gram_24k, price_per_gram_22k, etc.
        """
        cached = _cache.get("gold_price")
        if cached:
            return cached

        result = MetalPriceFetcher._fetch_from_goldapi("XAU")
        if result:
            _cache.set("gold_price", result)
            return result

        # Fallback: approximate values
        fallback = {
            "price_per_gram_24k": "N/A",
            "price_per_gram_22k": "N/A",
            "price_per_10g_24k": "N/A",
            "price_per_10g_22k": "N/A",
            "price_per_ounce": "N/A",
            "source": "Unavailable — API key not configured",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "fallback",
        }
        return fallback

    @staticmethod
    @timer
    def get_silver_price() -> dict[str, Any]:
        """Fetch current silver prices in INR.

        Returns:
            Dictionary with price_per_gram, price_per_kg, etc.
        """
        cached = _cache.get("silver_price")
        if cached:
            return cached

        result = MetalPriceFetcher._fetch_from_goldapi("XAG")
        if result:
            _cache.set("silver_price", result)
            return result

        fallback = {
            "price_per_gram": "N/A",
            "price_per_kg": "N/A",
            "price_per_ounce": "N/A",
            "source": "Unavailable — API key not configured",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "fallback",
        }
        return fallback

    @staticmethod
    def _fetch_from_goldapi(symbol: str) -> Optional[dict[str, Any]]:
        """Fetch metal price from GoldAPI.io.

        Args:
            symbol: Metal symbol — 'XAU' for gold, 'XAG' for silver.

        Returns:
            Parsed price data or None on failure.
        """
        if not settings.GOLDAPI_KEY:
            logger.info(f"GoldAPI key not configured, skipping {symbol} fetch")
            return None

        try:
            url = f"https://www.goldapi.io/api/{symbol}/INR"
            headers = {
                "x-access-token": settings.GOLDAPI_KEY,
                "Content-Type": "application/json",
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if symbol == "XAU":
                price_24k = data.get("price_gram_24k", 0)
                price_22k = data.get("price_gram_22k", 0)
                return {
                    "price_per_gram_24k": round(price_24k, 2),
                    "price_per_gram_22k": round(price_22k, 2),
                    "price_per_10g_24k": round(price_24k * 10, 2),
                    "price_per_10g_22k": round(price_22k * 10, 2),
                    "price_per_ounce": round(data.get("price", 0), 2),
                    "source": "GoldAPI.io",
                    "timestamp": timestamp,
                    "status": "live",
                }
            else:  # XAG — Silver
                price_gram = data.get("price_gram_24k", data.get("price", 0) / 31.1035)
                return {
                    "price_per_gram": round(price_gram, 2),
                    "price_per_kg": round(price_gram * 1000, 2),
                    "price_per_ounce": round(data.get("price", 0), 2),
                    "source": "GoldAPI.io",
                    "timestamp": timestamp,
                    "status": "live",
                }

        except requests.RequestException as exc:
            logger.warning(f"GoldAPI request failed for {symbol}: {exc}")
            return None
        except (KeyError, ValueError) as exc:
            logger.warning(f"GoldAPI parse error for {symbol}: {exc}")
            return None


# ═══════════════════════════════════════════════════════════════
#  CURRENCY EXCHANGE
# ═══════════════════════════════════════════════════════════════

class CurrencyConverter:
    """Currency conversion using the free Frankfurter API (ECB data)."""

    BASE_URL = "https://api.frankfurter.app/v1"

    @staticmethod
    @timer
    def get_exchange_rates(base: str = "INR") -> dict[str, Any]:
        """Fetch latest exchange rates for INR.

        Args:
            base: Base currency code.

        Returns:
            Dictionary with exchange rates and metadata.
        """
        cache_key = f"exchange_rates_{base}"
        cached = _cache.get(cache_key)
        if cached:
            return cached

        try:
            symbols = ",".join(settings.CURRENCIES)
            url = f"{CurrencyConverter.BASE_URL}/latest"
            params = {"base": base, "symbols": symbols}

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            result = {
                "base": base,
                "rates": data.get("rates", {}),
                "date": data.get("date", ""),
                "source": "European Central Bank (via Frankfurter)",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "live",
            }

            _cache.set(cache_key, result)
            return result

        except requests.RequestException as exc:
            logger.warning(f"Currency API request failed: {exc}")
            return {
                "base": base,
                "rates": {},
                "source": "Unavailable",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "error",
                "error": str(exc),
            }

    @staticmethod
    def convert(amount: float, from_currency: str, to_currency: str) -> dict[str, Any]:
        """Convert an amount between two currencies.

        Args:
            amount: Amount to convert.
            from_currency: Source currency code (e.g. 'INR').
            to_currency: Target currency code (e.g. 'USD').

        Returns:
            Dictionary with converted amount and rate.
        """
        try:
            url = f"{CurrencyConverter.BASE_URL}/latest"
            params = {"base": from_currency, "symbols": to_currency, "amount": amount}

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            rate = data.get("rates", {}).get(to_currency, 0)
            converted_amount = rate  # Frankfurter returns the converted amount directly when 'amount' is passed

            return {
                "from": from_currency,
                "to": to_currency,
                "original_amount": amount,
                "converted_amount": round(converted_amount, 2) if converted_amount else 0,
                "rate": round(data.get("rates", {}).get(to_currency, 0) / amount, 6) if amount else 0,
                "date": data.get("date", ""),
                "status": "success",
            }

        except requests.RequestException as exc:
            logger.warning(f"Currency conversion failed: {exc}")
            return {
                "from": from_currency,
                "to": to_currency,
                "original_amount": amount,
                "converted_amount": 0,
                "status": "error",
                "error": str(exc),
            }


# ═══════════════════════════════════════════════════════════════
#  MARKET DATA AGGREGATOR
# ═══════════════════════════════════════════════════════════════

class MarketDataFetcher:
    """Aggregated market data interface for the UI layer."""

    def __init__(self):
        self.metal_fetcher = MetalPriceFetcher()
        self.currency_converter = CurrencyConverter()

    def get_all_market_data(self) -> dict[str, Any]:
        """Fetch all available market data.

        Returns:
            Dictionary with gold, silver, and currency data.
        """
        return {
            "gold": MetalPriceFetcher.get_gold_price(),
            "silver": MetalPriceFetcher.get_silver_price(),
            "currency": CurrencyConverter.get_exchange_rates(),
        }

    def refresh(self) -> dict[str, Any]:
        """Force refresh all market data by clearing cache.

        Returns:
            Fresh market data.
        """
        _cache.clear()
        return self.get_all_market_data()
