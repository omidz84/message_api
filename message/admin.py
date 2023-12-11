from django.contrib import admin

from . import models

# Register your models here.


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'send_type', 'is_draft', 'updated_at']


@admin.register(models.SentGroupMessage)
class SentGroupMessageAdmin(admin.ModelAdmin):
    list_display = ['message_id', 'group_id', 'sender', 'created_at']


@admin.register(models.SentUserMessage)
class SentUserMessageAdmin(admin.ModelAdmin):
    list_display = ['message_id', 'user_id', 'sender', 'created_at']


@admin.register(models.SeenMessage)
class SeenMessageAdmin(admin.ModelAdmin):
    list_display = ['message_id', 'user_id', 'type', 'created_at']


@admin.register(models.ReplyMessage)
class ReplyMessageAdmin(admin.ModelAdmin):
    list_display = ['message_id', 'title', 'sender', 'updated_at']
