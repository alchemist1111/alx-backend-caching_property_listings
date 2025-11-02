from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property

# Signal handler for post_save - called after a Property is created or updated
@receiver(post_save, sender=Property)
def invalidate_property_cache_on_save(sender, instance, **kwargs):
    # Invalidate the cached 'all_properties' key after a property is created or updated
    cache.delete('all_properties')

# Signal handler for post_delete - called after a Property is deleted
@receiver(post_delete, sender=Property)
def invalidate_property_cache_on_delete(sender, instance, **kwargs):
    # Invalidate the cached 'all_properties' key after a property is deleted
    cache.delete('all_properties')
