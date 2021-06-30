# -*- coding: utf-8 -*-
from datetime import datetime

# Fixture package

# Test package & Utils
from django.test import TestCase
import pytest

pytestmark = pytest.mark.django_db

# models
from django.contrib.auth.models import User

from django.db import models

from django.urls import reverse
from dashboard.views.views_report import download_in_xslx_report_for_this_year

@pytest.mark.django_db
def test_view_download_in_xslx_report_for_this_year(client):
    url = reverse("download_in_xslx_report_for_this_year")
    response = client.get(url)
    #pytest.set_trace()
    assert response.status_code == 200

def test_view_chord_diagram(client):
    url = reverse("chord_diagram")
    response = client.get(url)
    #pytest.set_trace()
    assert response.status_code == 200

def test_view_daily_report(client):
    url = reverse("daily_report")
    response = client.get(url)
    assert response.status_code == 200