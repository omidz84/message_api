from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from guardian.shortcuts import assign_perm

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from model_bakery import baker

from message.models import Message, SentUserMessage, SentGroupMessage, SeenMessage


class UnreadMessageTests(APITestCase):
    def setUp(self):
        self.user = baker.make(get_user_model())
        self.client.force_login(self.user)
        self.sender = baker.make(get_user_model())
        self.group = baker.make(Group)
        self.group.user_set.add(self.user)
        self.message = baker.make(Message, _quantity=8)
        self.send_user = baker.make(SentUserMessage, sender=self.sender, user_id=self.user, _quantity=4)
        self.send_group = baker.make(SentGroupMessage, sender=self.sender, group_id=self.group, _quantity=4)

    def test_unread_message_success(self):
        url = reverse('message:unread-message')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['unread_message'], 8)


class DeleteMessageTests(APITestCase):
    def setUp(self):
        self.user = baker.make(get_user_model())
        self.client.force_login(self.user)
        self.message = baker.make(Message)
        self.seen_message = baker.make(SeenMessage, message_id=self.message, user_id=self.user)

        assign_perm('message.view_seenmessage', self.user)
        assign_perm('message.change_seenmessage', self.user)
        assign_perm('message.view_seenmessage', self.user, self.seen_message)
        assign_perm('message.change_seenmessage', self.user, self.seen_message)

    def test_delete_message_success(self):
        url = reverse('message:delete-message', args=[self.seen_message.id])

        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['type'], 'ownDelete')

