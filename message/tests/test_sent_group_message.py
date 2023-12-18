from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from model_bakery import baker

from message.models import SentGroupMessage, Message


class SentGroupMessageTests(APITestCase):
    def setUp(self):
        self.user = baker.make(get_user_model())
        self.client.force_login(self.user)
        self.group = baker.make(Group)
        self.message = baker.make(Message, creator=self.user)

    def test_send_group_message_success(self):
        url = reverse('message:send-group-message')
        data = {
            'message_id': self.message.id,
            'group_id': self.group.id,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertGreaterEqual(SentGroupMessage.objects.all().count(), 1)

