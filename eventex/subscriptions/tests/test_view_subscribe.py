from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class ViewSubscribeGet(TestCase):
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

        tags = (
            ('<form action="." method="post"', 1),
            ('<input', 6),
            ('type="text"', 3),
            ('type="email"', 1),
            ('type="submit"', 1)
        )

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        """HTML must have contains csrf token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)



class ViewSubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Ritomar Torquato', cpf='12345678909',
                    email='ritomar@gmail.com', phone='(86)99516-6006')
        self.response = self.client.post('/inscricao/', data)

    def test_post(self):
        """Valid POST should redirect to '/inscricao/'"""
        self.assertEqual(302, self.response.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))


class ViewSubscribedPostInvalid(TestCase):
    def setUp(self):
        self.response = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_erros(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)


class ViewSubscribeSuccessMessage(TestCase):
    def test_message(self):
        data = dict (name='Ritomar Torquato', cpf='12345678909',
                     email='ritomar@hotmail.com', phone='(86)99516-6006')
        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, 'Inscrição realizada com sucesso!')
