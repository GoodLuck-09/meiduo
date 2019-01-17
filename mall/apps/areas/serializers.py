from rest_framework import serializers
from .models import Area


class AreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = ['id', 'name']


class SubAreaSerializer(serializers.ModelSerializer):
    subs = AreaSerializer(many=True)

    class Meta:

        model = Area
        fields = ['subs', 'name', 'id']

