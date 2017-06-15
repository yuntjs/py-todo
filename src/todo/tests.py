# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from todo.models import TodoItem
from django.test import TestCase

# Create your tests here.
def createItem(client):
    url = reverse('todoitem-list')
    data = {'title': 'walk the dog'}
    return client.post(url, data, format='json')

class TestCreateTodoItem(APITestCase):
    """
    Ensure we can create a new todo item
    """
    def setUp(self):
        self.response = createItem(self.client)

    def test_received_201_created_status_code(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_received_location_header_hyperlink(self):
        self.assertRegexpMatches(self.response['Location'], '^http://.+/todos/[\d]+$')

class TestDeleteTodoItem(APITestCase):
    """
    Ensure we can delete a todo item
    """
    def setUp(self):
        response = createItem(self.client)
        self.assertEqual(TodoItem.objects.count(), 1)
        url = response['Location']
        self.response = self.client.delete(url)

    def test_received_204_no_content_status_code(self):
        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)

    def test_the_item_was_deleted(self):
        self.assertEqual(TodoItem.objects.count(), 0)
