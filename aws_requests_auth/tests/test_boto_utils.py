import datetime
import hashlib
import os
import unittest

import mock

from aws_requests_auth.boto_utils import BotoAWSRequestsAuth, get_credentials


class TestBotoUtils(unittest.TestCase):
    """
    Tests for boto_utils module.
    """

    def setUp(self):
        self.saved_env = {}
        for var in ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_SESSION_TOKEN']:
            self.saved_env[var] = os.environ.get(var)
            os.environ[var] = 'test-%s' % var

    def tearDown(self):
        for k, v in self.saved_env.items():
            if v is None:
                os.environ.pop(k)
            else:
                os.environ[k] = v

    def test_get_credentials(self):
        creds = get_credentials()  # botocore should discover these from os.environ
        self.assertEqual(creds['aws_access_key'], 'test-AWS_ACCESS_KEY_ID')
        self.assertEqual(creds['aws_secret_access_key'], 'test-AWS_SECRET_ACCESS_KEY')
        self.assertEqual(creds['aws_token'], 'test-AWS_SESSION_TOKEN')

    def test_boto_class(self):
        boto_auth_inst = BotoAWSRequestsAuth(
            aws_host='search-foo.us-east-1.es.amazonaws.com',
            aws_region='us-east-1',
            aws_service='es',
        )
        url = 'http://search-foo.us-east-1.es.amazonaws.com:80/'
        mock_request = mock.Mock()
        mock_request.url = url
        mock_request.method = "GET"
        mock_request.body = None
        mock_request.headers = {}

        frozen_datetime = datetime.datetime(2016, 6, 18, 22, 4, 5)
        with mock.patch('datetime.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = frozen_datetime
            boto_auth_inst(mock_request)
        self.assertEqual({
            'Authorization': 'AWS4-HMAC-SHA256 Credential=test-AWS_ACCESS_KEY_ID/20160618/us-east-1/es/aws4_request, '
                             'SignedHeaders=host;x-amz-date;x-amz-security-token, '
                             'Signature=9d35f096395c7aa5061e69aca897417dd41bb8fb01a465bb78343624f8f123bf',
            'x-amz-date': '20160618T220405Z',
            'X-Amz-Security-Token': 'test-AWS_SESSION_TOKEN',
            'x-amz-content-sha256': hashlib.sha256(b'').hexdigest(),

        }, mock_request.headers)
