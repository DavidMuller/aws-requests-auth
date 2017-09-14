import os
import unittest

import mock

from aws_requests_auth.aws_auth import AWSRequestsAuth
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
        mock_request = mock.Mock()
        with mock.patch.object(AWSRequestsAuth, '__call__') as parent_class_call_method:
            boto_auth_inst(mock_request)  # dummy call to __call__ method
            parent_class_call_method.assert_called_with(
                mock_request,
                aws_access_key='test-AWS_ACCESS_KEY_ID',
                aws_secret_access_key='test-AWS_SECRET_ACCESS_KEY',
                aws_token='test-AWS_SESSION_TOKEN',
            )
