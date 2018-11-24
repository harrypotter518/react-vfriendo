from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.utils import json

from .models import Message
from .serializers import MessagesSerializer


class MessagesViewSet(viewsets.ModelViewSet):
    serializer_class = MessagesSerializer
    queryset = Message.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        latitude = request.data['latitude']
        longitude = request.data['longitude']

        # TODO: Have a learn here
        # bot_response = bot().read_input(serializer.data['contents'], latitude, longitude)

        bot_response = {
            'message': 'Hi!',
            'budget_choices': True,
        }

        return Response({
            'bot_response': bot_response,
            'message': serializer.data,
        })
