from django.core import mail
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

class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='Ritomar Torquato', cpf='12345678909',
                    email='ritomar@gmail.com', phone='(86)99516-6006')
        self.response = self.client.post('/inscricao/', data)


    def test_post(self):
        """Valid POST should redirect to '/inscricao/'"""
        self.assertEqual(302, self.response.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmação de inscrição'

        self.assertEqual(expect, email.subject)

    def test_subscription_from(self):
        email = mail.outbox[0]
        expect = 'contato@eventex.com.br'

        self.assertEqual(expect, email.from_email)

    def test_subscription_to(self):
        email = mail.outbox[0]
        expect = ['eventex-ritomar@mailinator.com', 'ritomar@gmail.com']

        self.assertEqual(expect, email.to)

    def test_subscription_body(self):
        email = mail.outbox[0]

        self.assertIn('Ritomar Torquato', email.body)
        self.assertIn('12345678909', email.body)
        self.assertIn('ritomar@gmail.com', email.body)
        self.assertIn('(86)99516-6006', email.body)

class SubscribeInvalidPost(TestCase):
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


class SubscribeSuccessMessage(TestCase):
    def test_message(self):
        data = dict (name='Ritomar Torquato', cpf='12345678909',
                     email='ritomar@hotmail.com', phone='(86)99516-6006')
        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, 'Inscrição realizada com sucesso!')
