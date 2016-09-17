from datetime import datetime

from django.test import TestCase
from eventex.subscriptions.models import Subscription


class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.test_object = Subscription(
            name='Ritomar',
            cpf='12345678909',
            email='ritomar@hotmail.com',
            phone='(86)99999-1010'
        )
        self.test_object.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_ad(self):
        """Subscription must have an auto created date attribute."""
        self.assertIsInstance(self.test_object.created_at, datetime)

    def test_str(self):
        self.assertEqual('Ritomar', str(self.test_object))