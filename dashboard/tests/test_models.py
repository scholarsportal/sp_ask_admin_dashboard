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


"""
___  ___          _      _
|  \/  |         | |    | |
| .  . | ___   __| | ___| |___
| |\/| |/ _ \ / _` |/ _ \ / __|
| |  | | (_) | (_| |  __/ \__ \
\_|  |_/\___/ \__,_|\___|_|___/
MVP model tests --- it's not extensive
"""

from dashboard.models import ReferenceQuestion


class TestModel(TestCase):
    def test_model_reference_question_content(self):
        message = "Is the library open?"
        rq = ReferenceQuestion.objects.create(message=message)
        assert rq.message == message, "Should be: Is the library open?"


"""
______     _       _   _                 _     _
| ___ \   | |     | | (_)               | |   (_)
| |_/ /___| | __ _| |_ _  ___  _ __  ___| |__  _ _ __  ___
|    // _ \ |/ _` | __| |/ _ \| '_ \/ __| '_ \| | '_ \/ __|
| |\ \  __/ | (_| | |_| | (_) | | | \__ \ | | | | |_) \__ \
\_| \_\___|_|\__,_|\__|_|\___/|_| |_|___/_| |_|_| .__/|___/
                                                | |
                                                |_|
"""
