from django.contrib.auth.models import User

from guardian.shortcuts import assign_perm
from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username']


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Message
        fields = '__all__'
        extra_kwargs = {
            'creator': {'read_only': True},
            'parent': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        message = models.Message.objects.create(
            title=validated_data['title'],
            message_body=validated_data['message_body'],
            creator=request.user,
            send_type=validated_data['send_type'],
        )
        user = message.creator
        # model permissions
        assign_perm('message.view_message', user)
        assign_perm('message.add_message', user)
        assign_perm('message.change_message', user)
        assign_perm('message.delete_message', user)
        # object permission
        assign_perm('view_message', user, message)
        assign_perm('change_message', user, message)
        assign_perm('delete_message', user, message)
        return message


class SendGroupMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SentGroupMessage
        fields = '__all__'
        extra_kwargs = {
            'sender': {'read_only': True},
        }

    def create(self, validated_data):
        request = self.context.get('request')
        send_message = models.SentGroupMessage.objects.create(
            message_id=validated_data['message_id'],
            group_id=validated_data['group_id'],
            sender=request.user
        )

        message = send_message.message_id
        if message.is_draft:
            message.is_draft = False
            message.save()

        user = send_message.sender
        # model permissions
        assign_perm('message.view_sentgroupmessage', user)
        assign_perm('message.add_sentgroupmessage', user)
        assign_perm('message.change_sentgroupmessage', user)
        assign_perm('message.delete_sentgroupmessage', user)

        assign_perm('message.view_message', send_message.group_id)
        # object permission
        assign_perm('view_sentgroupmessage', user, send_message)
        assign_perm('change_sentgroupmessage', user, send_message)
        assign_perm('delete_sentgroupmessage', user, send_message)

        assign_perm('view_message', send_message.group_id, send_message.message_id)
        return send_message


class SendUserMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SentUserMessage
        fields = '__all__'
        extra_kwargs = {
            'sender': {'read_only': True},
        }

    def create(self, validated_data):
        request = self.context.get('request')
        send_message = models.SentUserMessage.objects.create(
            message_id=validated_data['message_id'],
            user_id=validated_data['user_id'],
            sender=request.user
        )

        message = send_message.message_id
        if message.is_draft:
            message.is_draft = False
            message.save()

        user = send_message.sender
        # model permissions
        assign_perm('message.view_sentusermessage', user)
        assign_perm('message.add_sentusermessage', user)
        assign_perm('message.change_sentusermessage', user)
        assign_perm('message.delete_sentusermessage', user)

        assign_perm('message.view_message', send_message.user_id)
        # object permission
        assign_perm('view_sentusermessage', user, send_message)
        assign_perm('change_sentusermessage', user, send_message)
        assign_perm('delete_sentusermessage', user, send_message)

        assign_perm('view_message', send_message.user_id, send_message)
        return send_message


class SentMessagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Message
        fields = '__all__'


class DetailMessageSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    seen_status = serializers.SerializerMethodField()

    class Meta:
        model = models.Message
        fields = ['id', 'title', 'message_body', 'creator', 'send_type', 'is_draft', 'updated_at', 'seen_status']

    def get_seen_status(self, obj):
        request = self.context['request']
        try:
            models.SeenMessage.objects.get(message_id=obj, user_id=request.user, type='seen')
        except models.SeenMessage.DoesNotExist:
            models.SeenMessage.objects.create(message_id=obj, user_id=request.user, type='seen')


class UnreadMessagesSerializer(serializers.Serializer):
    unread_message = serializers.SerializerMethodField()

    def get_unread_message(self, obj):
        user = self.context['request'].user
        user_message = models.SentUserMessage.objects.filter(
            user_id=user
        ).values_list('message_id_id', flat=True)

        group_message = models.SentGroupMessage.objects.filter(
            group_id__in=user.groups.all()
        ).values_list('message_id_id', flat=True)

        message = user_message.union(group_message).count()
        seen_message = models.SeenMessage.objects.filter(user_id=user).count()
        unread_message = message - seen_message
        return unread_message


class ReplyMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Message
        fields = '__all__'
        extra_kwargs = {
            'creator': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        message = models.Message.objects.create(
            title=validated_data['title'],
            message_body=validated_data['message_body'],
            creator=request.user,
            send_type=validated_data['send_type'],
            parent=validated_data['parent']
        )
        user = message.creator
        # model permissions
        assign_perm('message.view_message', user)
        assign_perm('message.add_message', user)
        assign_perm('message.change_message', user)
        assign_perm('message.delete_message', user)
        # object permission
        assign_perm('view_message', user, message)
        assign_perm('change_message', user, message)
        assign_perm('delete_message', user, message)
        return message
