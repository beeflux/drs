import io
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.views.generic import TemplateView
from rest_framework import views, serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from openspace.models import Space


class SpaceSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Space
        exclude = ()

    def get_distance(self, obj):
        a = float(''.join([x for x in str(obj.distance) if x != 'm']).strip()) / 1000

        return str("{0:.3f}".format(a)) + 'km'

class OpenSpaceView(TemplateView):
    def get_context_data(self, ** kwargs):
        data = super(OpenSpaceView, self).get_context_data(**kwargs)
        data['maps'] = []
        return data
    template_name = "openspace/dashboard.html"


class HazardResourceViewSet(views.APIView):
    permission_classes=[]

    def get(self,request,*args,**kwargs):
        params = self.request.query_params
        longitude = params['long']
        latitude = params['lat']

        user_location = GEOSGeometry('POINT({} {})'.format(longitude,latitude), srid=4326)

        api_json = {}
        resource_queryset=Space.objects.filter(location__distance_lte=(user_location,D(km=5000)))\
        .annotate(distance=Distance('location', user_location)) \
        .order_by('distance')[:10]
        resource_json= SpaceSerializer(resource_queryset, many=True)
        json = JSONRenderer().render(resource_json.data)
        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)
        return Response(data)