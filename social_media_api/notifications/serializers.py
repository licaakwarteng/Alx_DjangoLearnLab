from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    target_str = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor_username', 'verb', 'target_str', 'timestamp', 'is_read']

    def get_target_str(self, obj):
        return str(obj.target)
