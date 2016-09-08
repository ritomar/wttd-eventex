from django.test import TestCase

""" HomeTest é um cenário de teste pois herda de TestCase """

class HomeTest(TestCase):
    def setUp(self):
        # response é um atributo da classe HomeTest
        self.response = self.client.get('/')

    def test_get(self):
        """ GET '/ must return status code 200 """
        # self.client faz requisições HTTP diretas para o django
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """ Must use 'index.html' """
        self.assertTemplateUsed(self.response, 'index.html')