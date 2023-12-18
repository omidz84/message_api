from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from model_bakery import baker

from message.models import SentUserMessage, Message


class SentUserMessageTests(APITestCase):
    def setUp(self):
        self.user = baker.make(get_user_model())
        self.client.force_login(self.user)
        self.user_message = baker.make(get_user_model())
        self.message = baker.make(Message, creator=self.user)

    def test_send_user_message_success(self):
        url = reverse('message:send-user-message')
        data = {
            'message_id': self.message.id,
            'user_id': self.user_message.id,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertGreaterEqual(SentUserMessage.objects.all().count(), 1)

