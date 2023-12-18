from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from guardian.shortcuts import assign_perm

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from model_bakery import baker

from message.models import Message, SentUserMessage, SentGroupMessage, SeenMessage


class NewMessageTests(APITestCase):
    def setUp(self):
        self.user = baker.make(get_user_model())
        self.client.force_login(self.user)

    def test_new_message_success(self):
        url = reverse('message:new-message')
        data = {
            'title': 'hello',
            'message_body': 'hello',
            'send_type': 'web',
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertGreaterEqual(Message.objects.all().count(), 1)

    def test_new_message_invalid_send_type(self):
        url = reverse('message:new-message')
        data = {
            'title': 'hello',
            'message_body': 'hello',
            'send_type': 'aa',
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertGreaterEqual(Message.objects.all().count(), 0)


class SentMessageTests(APITestCase):
    def setUp(self):
        self.user = baker.make(get_user_model())
        self.client.force_login(self.user)
        self.message = baker.make(Message, creator=self.user, _quantity=10)

    def test_sent_list_success(self):
        url = reverse('message:sent-message')

        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)


class ReceivedMessageTests(APITestCase):
    def setUp(self):
        self.user = baker.make(get_user_model())
        self.client.force_login(self.user)
        self.sender = baker.make(get_user_model())
        self.group = baker.make(Group)
        self.group.user_set.add(self.user)
        self.message = baker.make(Message, creator=self.sender, _quantity=10)
        baker.make(SentUserMessage, sender=self.sender, user_id=self.user, _quantity=5)
        baker.make(SentGroupMessage, sender=self.sender, group_id=self.group, _quantity=5)

    def test_received_list_success(self):
        url = reverse('message:received-message')

        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)


class DetailMessageTests(APITestCase):
    def setUp(self):
        self.user = baker.make(get_user_model())
        self.client.force_login(self.user)
        self.message = baker.make(Message)

        assign_perm('message.view_message', self.user)
        assign_perm('message.change_message', self.user)
        assign_perm('message.delete_message', self.user)
        assign_perm('message.view_message', self.user, self.message)
        assign_perm('message.change_message', self.user, self.message)
        assign_perm('message.delete_message', self.user, self.message)

    def test_detail_message_get_success(self):
        url = reverse('message:detail-message', args=[self.message.id])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.message.title)

    def test_detail_message_put_success(self):
        url = reverse('message:detail-message', args=[self.message.id])
        data = {
            'title': 'hello',
            'message_body': 'hello',
            'send_type': 'web'
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'hello')
        self.assertEqual(response.data['message_body'], 'hello')
        self.assertEqual(response.data['send_type'], 'web')
        self.assertGreaterEqual(SeenMessage.objects.all().count(), 1)

    def test_detail_message_delete_success(self):
        url = reverse('message:detail-message', args=[self.message.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertGreaterEqual(Message.objects.all().count(), 0)
