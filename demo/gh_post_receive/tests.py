from django.test import TestCase
from django.test import Client
from django.conf import settings


class RedeployTest(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_valid_id(self):
        valid_id = 'valid'
        settings.REDEPLOY_IDS.append(valid_id)
        response = self.client.get('/redeploy/?redeploy_id=' + valid_id)
        self.assertEqual('ok', response.content)

    def test_missing_id(self):
        response = self.client.get('/redeploy/')
        self.assertNotEqual('ok', response.content)

    def test_invalid_id(self):
        response = self.client.get('/redeploy/?redeploy_id=invalid')
        self.assertNotEqual('ok', response.content)
