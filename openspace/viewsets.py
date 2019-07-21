import io
import json
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry, Point
from django.contrib.gis.measure import D
from django.core.serializers import serialize
from rest_framework import views, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from openspace.models import Space
from openspace.serializer import SpaceCreateSerializer, SpaceSerializer


class NearSpaceViewSet(views.APIView):
    permission_classes=[]

    def get(self, request):
        params = request.query_params
        longitude = params['long']
        latitude = params['lat']

        user_location = GEOSGeometry('POINT({} {})'.format(longitude, latitude), srid=4326)

        resource_queryset=Space.objects.filter(
            location__distance_lte=(user_location, D(km=5000))).annotate(
            distance=Distance('location', user_location)).order_by('distance')[:10]
        resource_json= SpaceSerializer(resource_queryset, many=True)
        json_data = JSONRenderer().render(resource_json.data)
        stream = io.BytesIO(json_data)
        data = JSONParser().parse(stream)
        return Response(data)


class SpaceGeojsonViewSet(views.APIView):
    permission_classes = []

    def get(self, request):
        serializers = serialize('geojson', Space.objects.all(),
                                geometry_field='location', fields=('pk', 'name', 'location', 'address', 'city'))
        geojson = json.loads(serializers)
        return Response(geojson)


class SpaceViewSet(viewsets.ModelViewSet):
    queryset = Space.objects.all()[0:0]
    serializer_class = SpaceCreateSerializer

    def create(self, request, *args, **kwargs):
        name = self.request.data.get('name')
        address = self.request.data.get('address')
        city = self.request.data.get('city')
        lat = self.request.data.get('lat')
        long = self.request.data.get('long')
        location = Point(float(long), float(lat), srid=4326)
        s = Space(name=name, address=address, city=city, location=location)
        s.save()
        return Response({"message": "Sucess"})
