from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from model_bakery import baker

from message.models import Message, SentUserMessage


class ReplyMessageTests(APITestCase):
    def setUp(self):
        self.user = baker.make(get_user_model())
        self.client.force_login(self.user)
        self.sender = baker.make(get_user_model())
        self.message = baker.make(Message, creator=self.sender)
        baker.make(SentUserMessage, sender=self.sender, user_id=self.user)

    def test_reply_message_success(self):
        url = reverse('message:reply-message')
        data = {
            'title': 'hello',
            'message_body': 'test reply',
            'send_type': 'web',
            'parent': self.message.id,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertGreaterEqual(Message.objects.all().count(), 2)


class ShowReplyMessageTests(APITestCase):
    def setUp(self):
        self.user = baker.make(get_user_model())
        self.client.force_login(self.user)
        self.message = baker.make(Message)
        self.reply_message = baker.make(Message, parent=self.message, _quantity=10)

    def test_show_reply_message_success(self):
        url = reverse('message:show-reply-message', args=[self.message.id])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

