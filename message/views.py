from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response

from . import serializers, models
from .permissions import CustomObjectPermissions, CustomModelPermissions


class CreateMessageView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer


class SendGroupMessageView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.SentGroupMessage.objects.all()
    serializer_class = serializers.SendGroupMessageSerializer


class SendUserMessageView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.SentUserMessage.objects.all()
    serializer_class = serializers.SendUserMessageSerializer


class SentMessagesView(generics.ListAPIView):
    permission_classes = [CustomModelPermissions]
    queryset = models.Message.objects.all()
    serializer_class = serializers.SentMessagesSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return models.Message.objects.all()
        return models.Message.objects.filter(creator=user)


class ReplyMessageView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.ReplyMessage.objects.all()
    serializer_class = serializers.ReplyMessageSerializer


class DetailReplyMessageView(generics.RetrieveAPIView):
    permission_classes = [CustomObjectPermissions]
    queryset = models.ReplyMessage.objects.all()
    serializer_class = serializers.DetailReplyMessageSerializer


class ReceivedMessagesView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.MessageSerializer

    def get_queryset(self):
        user = self.request.user

        user_message = models.SentUserMessage.objects.filter(
            user_id=user
        ).values_list('message_id_id', flat=True)

        group_message = models.SentGroupMessage.objects.filter(
            group_id__in=user.groups.all()
        ).values_list('message_id_id', flat=True)

        message = user_message.union(group_message)
        return models.Message.objects.filter(id__in=message)


class DetailMessageView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.Message.objects.all()
    serializer_class = serializers.DetailMessageSerializer


class UpdateMessageView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [CustomObjectPermissions]
    queryset = models.Message.objects.all()
    serializer_class = serializers.DetailMessageSerializer


class UnreadMessagesCountView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.UnreadMessagesSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.data, context={'request': request})
        return Response(serializer.data)

