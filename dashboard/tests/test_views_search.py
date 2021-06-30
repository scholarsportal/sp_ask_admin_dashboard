# -*- coding: utf-8 -*-
from datetime import datetime

# Fixture package

# Test package & Utils
from django.test import TestCase
import pytest

pytestmark = pytest.mark.django_db

# models
from django.contrib.auth.models import User
import json

from django.db import models

from django.urls import reverse
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client

class Unit_test(TestCase):
    @pytest.mark.django_db
    def test_view(self):
        url = reverse("get_operators_currently_online")
        response = self.client.get(url)
        assert response.status_code == 200

    def test_view_guest_id(self):
        url = reverse("search_chats_with_this_guestID", "text/json",            
                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = self.client.get(url)
        breakpoint()#pytest.set_trace()

        assert response.status_code == 200