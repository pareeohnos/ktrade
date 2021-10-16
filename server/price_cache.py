import logging

from server.singleton_meta import SingletonMeta

log = logging.getLogger(__name__)

class PriceCache(metaclass=SingletonMeta):
  def __init__(self):
    log.debug("[PriceCache] Init new price cache")
    self.price_cache = {}

  def init_cache_for_ticker(self, watched_ticker_id):
    log.info(f"[PriceCache] Init cache for watched ticker {watched_ticker_id}")
    if self.price_cache.get(watched_ticker_id):
      return

    self.price_cache[watched_ticker_id] = {
      "high": None,
      "low": None,
      "price": None
    }

  def cached_prices_for_ticker(self, watched_ticker_id):
    return self.price_cache.get(watched_ticker_id)

  def cached_price(self, watched_ticker_id, key):
    cache = self.price_cache.get(watched_ticker_id)
    if not cache:
      return None
    
    log.info(f"[PriceCache] Getting {key} for {watched_ticker_id}: {cache[key]}")
    return cache[key]

  def update_cached_price(self, watched_ticker_id, key, val):
    log.info(f"[PriceCache] Updating {key} price for {watched_ticker_id}: {val}")
    self.price_cache[watched_ticker_id][key] = val

  def delete_watched_ticker(self, watched_ticker_id):
    log.info(f"[PriceCache] Deleting cache for {watched_ticker_id}")
    del self.price_cache[watched_ticker_id]

  def reset_cached_values(self):
    for prices in self.price_cache:
      prices["low"] = None
      prices["high"] = None
      prices["price"] = None