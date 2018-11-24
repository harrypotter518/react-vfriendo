from rest_framework import serializers

from .models import Message


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'contents', 'created_at')
        read_only_fields = ('created_at',)
