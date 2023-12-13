from django.contrib.auth.models import User, Group
from django.db import models

# Create your models here.


class Message(models.Model):

    type = {
        'sms': 'sms',
        'web': 'web',
    }

    title = models.CharField(max_length=300, db_index=True, verbose_name='title')
    message_body = models.TextField(verbose_name='message body')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='creator')
    send_type = models.CharField(max_length=15, choices=type)
    is_draft = models.BooleanField(verbose_name='is draft', default=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='parent', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} | {self.creator.username} | {self.is_draft}'

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'messages'


class SentGroupMessage(models.Model):
    message_id = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='message')
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='group')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='sender')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.message_id.__str__()} | {self.group_id.name} | {self.sender.username}'

    class Meta:
        verbose_name = 'sent group message'
        verbose_name_plural = 'sent group messages'


class SentUserMessage(models.Model):
    message_id = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='message')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user', related_name='user')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='sender', related_name='sender')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.message_id.__str__()} | {self.user_id.username} | {self.sender.username}'

    class Meta:
        verbose_name = 'sent user message'
        verbose_name_plural = 'sent user messages'


class SeenMessage(models.Model):

    s_type = {
        'seen': 'seen',
        'ownDelete': 'ownDelete',
    }

    message_id = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='message')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    type = models.CharField(max_length=15, choices=s_type)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.message_id.__str__()} | {self.user_id.username} | {self.type}'

    class Meta:
        verbose_name = 'seen message'
        verbose_name_plural = 'seen messages'
