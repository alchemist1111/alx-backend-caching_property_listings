from django.core.cache import cache
from .models import Property

def get_all_properties():
    # Try to get the cached queryset from Redis
    cached_properties = cache.get('all_properties')
    
    if cached_properties is None:
        # If not found in the cache, fetch from the database
        cached_properties = Property.objects.all()
        # Cache the queryset for 1 hour (3600 seconds)
        cache.set('all_properties', cached_properties, 3600)
    
    return cached_properties
