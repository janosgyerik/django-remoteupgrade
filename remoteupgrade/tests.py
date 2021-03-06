from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test import Client
from django.utils import simplejson as json


class RemoteUpgradeTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.baseurl = reverse('remoteupgrade')
        
    def assertSuccess(self, response):
        self.assertTrue(json.loads(response.content)['success'])

    def assertFailure(self, response):
        self.assertFalse(json.loads(response.content)['success'])

    def test_valid_id(self):
        valid_id = 'valid'
        settings.REMOTEUPGRADE_IDS.append(valid_id)
        url = self.baseurl + '?id=' + valid_id
        response = self.client.get(url)
        self.assertSuccess(response)

    def test_missing_id(self):
        url = self.baseurl
        response = self.client.get(url)
        self.assertFailure(response)

    def test_invalid_id(self):
        url = self.baseurl + '?id=invalid'
        response = self.client.get(url)
        self.assertFailure(response)

    def test_missing_script(self):
        backup = settings.REMOTEUPGRADE_SCRIPT
        settings.REMOTEUPGRADE_SCRIPT = '/path/to/nonexistent'
        self.assertRaises(OSError, self.test_valid_id)
        settings.REMOTEUPGRADE_SCRIPT = backup
