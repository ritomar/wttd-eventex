from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/')

    def test_get(self):
        """Get '/inscricao/' must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """GET must use 'subscriptions/subscription_form.html' """
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_html(self):
        """Html must contains input tags"""
        self.assertContains(self.response, '<form action="." method="post"', 1)
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="submit"', 1)

    def test_csrf(self):
        """HTML must have contains csrf token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        form = self.response.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))

