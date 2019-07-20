from django.shortcuts import render
from django.views.generic import TemplateView


class OpenSpaceView(TemplateView):
    def get_context_data(self, ** kwargs):
        data = super(OpenSpaceView, self).get_context_data(**kwargs)
        data['maps'] = []
        return data
    template_name = "openspace/dashboard.html"

class HazardResourceViewSet(views.APIView):
    permission_classes=[]

    def get(self,request,*args,**kwargs):
        longitude = self.kwargs['long']
        latitude =self.kwargs['lat']
        hazard_title = self.kwargs['hazard']
        try:
            distance_parm= self.kwargs['distance']
        except:
            distance_parm=5000
        try:
            count= int(self.kwargs['count'])
        except:
            count=20

        user_location =GEOSGeometry('POINT({} {})'.format(longitude,latitude), srid=4326)

        #Hazard_object = Hazard.objects.get(title=hazard_title)
        #Hresources = Hazard_object.hazardresources_set.all()
        api_json = {}

        if(hazard_title=='flood'):
            resource_array=['Hospital','School','Policestation','Bridge']
        elif (hazard_title=='landslide'):
            resource_array=['Policestation','Hospital','School']
        elif (hazard_title=='fire'):
            resource_array=['Policestation','Hospital','School','MarketCenter']
        elif (hazard_title=='earthquake'):
            resource_array=['Policestation','Hospital','School']



        resource_object=[]
        print(distance_parm)
        for resource in resource_array:
            model_x= apps.get_model('risk_profile', resource)
            print("model_x",model_x)
            resource_queryset=model_x.objects \
            .filter(location__distance_lte=(user_location,D(km=distance_parm))) \
            .annotate(distance=Distance('location',user_location)) \
            .order_by('distance')[0:count]
            print(resource_queryset)
            resource_json= HospitalSerializer(resource_queryset,many=True)
            json = JSONRenderer().render(resource_json.data)
            stream = io.BytesIO(json)
            data = JSONParser().parse(stream)
            api_json[resource] =data

        return Response(api_json)