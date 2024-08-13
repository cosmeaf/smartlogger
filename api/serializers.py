from rest_framework import serializers
from .models import Maintenance

class MaintenanceUsageHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = ['usage_hours']


class MaintenanceAlarmHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = ['alarm_hours']


class MaintenanceOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = ['os']
