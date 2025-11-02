from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from .models import Property
from serializers import PropertySerializer

# Cache the property list view for 15 minutes (900 seconds)
@api_view(['GET'])
@cache_page(60 * 15)
def property_list(request):
    # Retrieve all properties from the database
    properties = Property.objects.all()
    serializer = PropertySerializer(properties, many=True)
    return Response(serializer.data)