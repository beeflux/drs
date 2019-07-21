from rest_framework import views, serializers
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
        return obj.location.y

    def get_long(self, obj):
        return obj.location.x

    def get_distance(self, obj):
        a = float(''.join([x for x in str(obj.distance) if x != 'm']).strip()) / 1000
        return str("{0:.3f}".format(a)) + 'km'
