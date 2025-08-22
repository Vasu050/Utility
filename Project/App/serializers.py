from rest_framework import serializers
from .models import AgentData
class AgentDataSerializer(serializers.ModelSerializer):
    timestamp = serializers.SerializerMethodField()
    system_details = serializers.SerializerMethodField()
    process_details = serializers.SerializerMethodField()

    class Meta:
        model = AgentData
        fields = ["hostname", "timestamp", "system_details", "process_details","created_at"]

    def get_timestamp(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_system_details(self, obj):
        return obj.data.get("system_details", {})

    def get_process_details(self, obj):
        return obj.data.get("process_details", [])
