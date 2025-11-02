from django.core.cache import cache
from .models import Property
import logging
from django_redis import get_redis_connection

# Set up a logger
logger = logging.getLogger(__name__)

def get_all_properties():
    # Try to get the cached queryset from Redis
    cached_properties = cache.get('all_properties')
    
    if cached_properties is None:
        # If not found in the cache, fetch from the database
        cached_properties = Property.objects.all()
        # Cache the queryset for 1 hour (3600 seconds)
        cache.set('all_properties', cached_properties, 3600)
    
    return cached_properties


def get_redis_cache_metrics():
    try:
        # Connect to Redis using django_redis
        redis_conn = get_redis_connection('default')  # 'default' refers to the default cache in settings.py
        
        # Get Redis INFO command for cache stats
        info = redis_conn.info('stats')  # Retrieves statistics about the Redis instance
        
        # Extract keyspace_hits and keyspace_misses from the info
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)
        
        # Calculate the hit ratio
        total_accesses = keyspace_hits + keyspace_misses
        hit_ratio = keyspace_hits / total_accesses if total_accesses > 0 else 0
        
        # Log the metrics
        logger.info(f"Redis Cache Metrics - Hits: {keyspace_hits}, Misses: {keyspace_misses}, Hit Ratio: {hit_ratio:.2f}")
        
        # Return the metrics as a dictionary
        return {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'hit_ratio': hit_ratio
        }
    
    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {str(e)}")
        return {
            'error': f"Error retrieving Redis cache metrics: {str(e)}"
        }
