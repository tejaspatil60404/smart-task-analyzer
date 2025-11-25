from rest_framework import serializers

class TaskInputSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField()
    due_date = serializers.CharField(required=False, allow_blank=True)
    estimated_hours = serializers.FloatField(required=False)
    importance = serializers.IntegerField(required=False)
    dependencies = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )
