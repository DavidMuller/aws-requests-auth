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
        auth = BotoAWSRequestsAuth(aws_host='search-foo.us-east-1.es.amazonaws.com',
                                   aws_region='us-east-1',
                                   aws_service='es')
        mock_request = mock.Mock()
        mock_request.url = 'search-foo.us-east-1.es.amazonaws.com'
        mock_request.method = 'GET'
        mock_request.body = None
        mock_request.headers = {}
        auth(mock_request)  # dummy call to __call__ method
        self.assertEqual(auth.aws_access_key, 'test-AWS_ACCESS_KEY_ID')
        self.assertEqual(auth.aws_secret_access_key, 'test-AWS_SECRET_ACCESS_KEY')
        self.assertEqual(auth.aws_token, 'test-AWS_SESSION_TOKEN')
