from django.core import mail
from django.test import TestCase


class MailSubscribe(TestCase):
    def setUp(self):
        data = dict(name='Ritomar Torquato', cpf='12345678909',
                    email='ritomar@gmail.com', phone='(86)99516-6006')
        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]


    def test_subscription_subject(self):
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, self.email.subject)


    def test_subscription_from(self):
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, self.email.from_email)


    def test_subscription_to(self):
        expect = ['contato@eventex.com.br', 'ritomar@gmail.com']
        self.assertEqual(expect, self.email.to)


    def test_subscription_body(self):
        contents = (
            'Ritomar Torquato',
            '12345678909',
            'ritomar@gmail.com',
            '(86)99516-6006'
        )
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)

