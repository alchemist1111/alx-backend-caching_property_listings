from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .utils import get_all_properties
from .serializers import PropertySerializer

# Cache the property list view for 15 minutes (900 seconds)
@cache_page(60 * 15)
def property_list(request):
    # Use the utility function to get properties (with low-level caching)
    properties = get_all_properties()
    # Serialize the properties
    serializer = PropertySerializer(properties, many=True)
    # Return the data as JSON using JsonResponse
    return JsonResponse(serializer.data, safe=False)