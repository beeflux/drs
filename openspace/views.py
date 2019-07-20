import io
import json
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry, Point
from django.contrib.gis.measure import D
from django.core.serializers import serialize
from django.views.generic import TemplateView
from rest_framework import views, serializers, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from openspace.models import Space


class SpaceCreateSerializer(serializers.ModelSerializer):
    lat = serializers.FloatField(write_only=True)
    long = serializers.FloatField(write_only=True)

    class Meta:
        model = Space
        exclude = ('location',)


class SpaceSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()
    lat = serializers.SerializerMethodField()
    long = serializers.SerializerMethodField()

    class Meta:
        model = Space
        exclude = ()

    def get_lat(self, obj):
        return obj.location.x

    def get_long(self, obj):
        return obj.location.y

    def get_distance(self, obj):
        a = float(''.join([x for x in str(obj.distance) if x != 'm']).strip()) / 1000

        return str("{0:.3f}".format(a)) + 'km'

class OpenSpaceView(TemplateView):
    def get_context_data(self, ** kwargs):
        data = super(OpenSpaceView, self).get_context_data(**kwargs)
        data['maps'] = []
        return data
    template_name = "openspace/dashboard.html"


class NearSpaceViewSet(views.APIView):
    permission_classes=[]

    def get(self,request,*args,**kwargs):
        params = self.request.query_params
        longitude = params['long']
        latitude = params['lat']

        user_location = GEOSGeometry('POINT({} {})'.format(longitude,latitude), srid=4326)

        resource_queryset=Space.objects.filter(location__distance_lte=(user_location,D(km=5000)))\
        .annotate(distance=Distance('location', user_location)) \
        .order_by('distance')[:10]
        resource_json= SpaceSerializer(resource_queryset, many=True)
        json = JSONRenderer().render(resource_json.data)
        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)
        return Response(data)


class SpaceGeojsonViewSet(views.APIView):
    permission_classes=[]
    def get(self,request,*args,**kwargs):
        serializers=serialize('geojson', Space.objects.all(),
                              geometry_field='location',fields=('pk','name','location','address','city'))
        Hydrogeojson=json.loads(serializers)
        return Response(Hydrogeojson)


class SpaceViewSet(viewsets.ModelViewSet):
    queryset = Space.objects.all()
    serializer_class = SpaceCreateSerializer

    def create(self, request, *args, **kwargs):
        name = self.request.data.get('name')
        address = self.request.data.get('address')
        city = self.request.data.get('city')
        lat = self.request.data.get('lat')
        long = self.request.data.get('long')
        location = Point(float(lat), float(long), srid=4326)
        s = Space(name=name, address=address, city=city, location=location)
        s.save()
        return Response({"message":"Sucess"})
