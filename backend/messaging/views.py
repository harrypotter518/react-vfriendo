from rest_framework import viewsets

from .models import Message
from .serializers import MessagesSerializer


class MessagesViewSet(viewsets.ModelViewSet):
    serializer_class = MessagesSerializer
    queryset = Message.objects.all()

    def create(self, request, *args, **kwargs):
        message = super().create(request, *args, **kwargs)

        # TODO: Have a learn here, message.contents is the message contents

        return message
