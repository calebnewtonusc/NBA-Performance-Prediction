"""
Redis Caching Layer for NBA Predictions

Provides high-performance caching for predictions, features, and model results
"""

import json
import hashlib
from typing import Any, Optional, Dict
from datetime import timedelta

try:
    import redis
    from redis.exceptions import RedisError

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    print("[exclamationmark.triangle]  Redis not installed. Install with: pip install redis")


class RedisCache:
    """Redis cache manager for predictions and features"""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        default_ttl: int = 3600,
    ):
        """
        Initialize Redis cache

        Args:
            host: Redis host
            port: Redis port
            db: Redis database number
            password: Redis password (if required)
            default_ttl: Default time-to-live in seconds (1 hour default)
        """
        if not REDIS_AVAILABLE:
            raise ImportError("Redis package not installed")

        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
        )
        self.default_ttl = default_ttl

        # Statistics
        self.hits = 0
        self.misses = 0

    def _generate_key(self, prefix: str, data: Dict) -> str:
        """Generate cache key from data"""
        # Sort keys for consistent hashing
        data_str = json.dumps(data, sort_keys=True)
        hash_obj = hashlib.sha256(data_str.encode())
        return f"{prefix}:{hash_obj.hexdigest()}"

    def health_check(self) -> bool:
        """Check Redis connectivity"""
        try:
            return self.client.ping()
        except RedisError:
            return False

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            value = self.client.get(key)
            if value:
                self.hits += 1
                return json.loads(value)
            self.misses += 1
            return None
        except RedisError as e:
            print(f"Redis error on get: {e}")
            self.misses += 1
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache"""
        try:
            ttl = ttl or self.default_ttl
            value_json = json.dumps(value)
            return self.client.setex(key, ttl, value_json)
        except RedisError as e:
            print(f"Redis error on set: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            return bool(self.client.delete(key))
        except RedisError as e:
            print(f"Redis error on delete: {e}")
            return False

    def clear_all(self) -> bool:
        """Clear all keys (use with caution!)"""
        try:
            return self.client.flushdb()
        except RedisError as e:
            print(f"Redis error on clear: {e}")
            return False

    def cache_prediction(
        self, model_name: str, model_version: str, features: Dict, prediction: Dict, ttl: int = 300
    ) -> bool:
        """
        Cache prediction result

        Args:
            model_name: Model name
            model_version: Model version
            features: Input features
            prediction: Prediction result
            ttl: Cache TTL in seconds (5 minutes default)
        """
        cache_data = {"model_name": model_name, "model_version": model_version, **features}

        key = self._generate_key("prediction", cache_data)
        return self.set(key, prediction, ttl)

    def get_cached_prediction(
        self, model_name: str, model_version: str, features: Dict
    ) -> Optional[Dict]:
        """Get cached prediction"""
        cache_data = {"model_name": model_name, "model_version": model_version, **features}

        key = self._generate_key("prediction", cache_data)
        return self.get(key)

    def cache_features(self, game_id: str, features: Dict, ttl: int = 3600) -> bool:
        """Cache game features (1 hour default)"""
        key = f"features:{game_id}"
        return self.set(key, features, ttl)

    def get_cached_features(self, game_id: str) -> Optional[Dict]:
        """Get cached game features"""
        key = f"features:{game_id}"
        return self.get(key)

    def cache_model_metadata(self, model_name: str, model_version: str, metadata: Dict) -> bool:
        """Cache model metadata (no expiry)"""
        key = f"model_metadata:{model_name}:{model_version}"
        return self.set(key, metadata, ttl=86400)  # 24 hours

    def get_model_metadata(self, model_name: str, model_version: str) -> Optional[Dict]:
        """Get cached model metadata"""
        key = f"model_metadata:{model_name}:{model_version}"
        return self.get(key)

    def increment_counter(self, counter_name: str) -> int:
        """Increment a counter"""
        try:
            return self.client.incr(counter_name)
        except RedisError:
            return 0

    def get_counter(self, counter_name: str) -> int:
        """Get counter value"""
        try:
            value = self.client.get(counter_name)
            return int(value) if value else 0
        except (RedisError, ValueError):
            return 0

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0

        try:
            info = self.client.info("stats")
            memory = self.client.info("memory")

            return {
                "hits": self.hits,
                "misses": self.misses,
                "hit_rate_percent": round(hit_rate, 2),
                "total_keys": self.client.dbsize(),
                "used_memory_mb": round(memory.get("used_memory", 0) / 1024 / 1024, 2),
                "connected_clients": info.get("connected_clients", 0),
                "total_commands_processed": info.get("total_commands_processed", 0),
            }
        except RedisError:
            return {
                "hits": self.hits,
                "misses": self.misses,
                "hit_rate_percent": round(hit_rate, 2),
                "error": "Could not retrieve Redis stats",
            }

    def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching pattern"""
        try:
            keys = self.client.keys(pattern)
            if keys:
                return self.client.delete(*keys)
            return 0
        except RedisError as e:
            print(f"Redis error on invalidate_pattern: {e}")
            return 0


class InMemoryCache:
    """Fallback in-memory cache when Redis is unavailable (thread-safe)"""

    def __init__(self, max_size: int = 1000):
        """
        Initialize in-memory cache

        Args:
            max_size: Maximum number of items to cache
        """
        import threading

        self.cache: Dict[str, Any] = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
        self.lock = threading.RLock()  # Thread-safe lock

    def health_check(self) -> bool:
        """Always healthy for in-memory cache"""
        return True

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache (thread-safe)"""
        with self.lock:
            if key in self.cache:
                self.hits += 1
                return self.cache[key]
            self.misses += 1
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache (thread-safe, ignores TTL for simplicity)"""
        with self.lock:
            if len(self.cache) >= self.max_size:
                # Remove oldest item (simple FIFO)
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]

            self.cache[key] = value
            return True

    def delete(self, key: str) -> bool:
        """Delete key from cache (thread-safe)"""
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                return True
            return False

    def clear_all(self) -> bool:
        """Clear all keys (thread-safe)"""
        with self.lock:
            self.cache.clear()
            return True

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics (thread-safe)"""
        with self.lock:
            total_requests = self.hits + self.misses
            hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0

            return {
                "hits": self.hits,
                "misses": self.misses,
                "hit_rate_percent": round(hit_rate, 2),
                "total_keys": len(self.cache),
                "cache_type": "in-memory",
            }


def get_cache(use_redis: bool = True, **kwargs) -> Any:
    """
    Get cache instance (Redis or in-memory fallback)

    Args:
        use_redis: Whether to try Redis first
        **kwargs: Arguments for RedisCache

    Returns:
        Cache instance
    """
    if use_redis and REDIS_AVAILABLE:
        try:
            cache = RedisCache(**kwargs)
            if cache.health_check():
                print("[checkmark.circle] Redis cache connected")
                return cache
            print("[exclamationmark.triangle]  Redis not available, falling back to in-memory cache")
        except Exception as e:
            print(f"[exclamationmark.triangle]  Redis connection failed: {e}, falling back to in-memory cache")

    return InMemoryCache()
