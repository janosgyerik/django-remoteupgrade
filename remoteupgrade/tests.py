from django.conf import settings
from django.test import TestCase
from django.test import Client
from django.utils import simplejson as json


class RemoteUpgradeTest(TestCase):
    def setUp(self):
        self.client = Client()
        
    def assertSuccess(self, response):
        self.assertTrue(json.loads(response.content)['success'])

    def assertFailure(self, response):
        self.assertFalse(json.loads(response.content)['success'])

    def test_valid_id(self):
        valid_id = 'valid'
        settings.REMOTEUPGRADE_IDS.append(valid_id)
        response = self.client.get('/remoteupgrade/?id=' + valid_id)
        self.assertSuccess(response)

    def test_missing_id(self):
        response = self.client.get('/remoteupgrade/')
        self.assertFailure(response)

    def test_invalid_id(self):
        response = self.client.get('/remoteupgrade/?id=invalid')
        self.assertFailure(response)
