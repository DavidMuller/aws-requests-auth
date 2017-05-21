import datetime
import mock
import unittest

from aws_requests_auth.aws_auth import AWSRequestsAuth


class TestAWSRequestsAuth(unittest.TestCase):
    """
    Tests for AWSRequestsAuth
    """

    def test_no_query_params(self):
        """
        Assert we generate the 'correct' cannonical query string
        and canonical path for a request with no query params

        Correct is relative here b/c 'correct' simply means what
        the AWS Elasticsearch service expects
        """
        url = 'http://search-foo.us-east-1.es.amazonaws.com:80/'
        mock_request = mock.Mock()
        mock_request.url = url
        self.assertEqual('/', AWSRequestsAuth.get_canonical_path(mock_request))
        self.assertEqual('', AWSRequestsAuth.get_canonical_querystring(mock_request))

    def test_characters_escaped_in_path(self):
        """
        Assert we generate the 'correct' cannonical query string
        and path a request with characters that need to be escaped
        """
        url = 'http://search-foo.us-east-1.es.amazonaws.com:80/+foo.*/_stats'
        mock_request = mock.Mock()
        mock_request.url = url
        self.assertEqual('/%2Bfoo.%2A/_stats', AWSRequestsAuth.get_canonical_path(mock_request))
        self.assertEqual('', AWSRequestsAuth.get_canonical_querystring(mock_request))

    def test_path_with_querystring(self):
        """
        Assert we generate the 'correct' cannonical query string
        and path for request that includes a query stirng
        """
        url = 'http://search-foo.us-east-1.es.amazonaws.com:80/my_index/?pretty=True'
        mock_request = mock.Mock()
        mock_request.url = url
        self.assertEqual('/my_index/', AWSRequestsAuth.get_canonical_path(mock_request))
        self.assertEqual('pretty=True', AWSRequestsAuth.get_canonical_querystring(mock_request))

    def test_multiple_get_params(self):
        """
        Assert we generate the 'correct' cannonical query string
        for request that includes more than one query parameter
        """
        url = 'http://search-foo.us-east-1.es.amazonaws.com:80/index/type/_search?scroll=5m&search_type=scan'
        mock_request = mock.Mock()
        mock_request.url = url
        self.assertEqual('scroll=5m&search_type=scan', AWSRequestsAuth.get_canonical_querystring(mock_request))

    def test_post_request_with_get_param(self):
        """
        Assert we generate the 'correct' cannonical query string
        for a post request that includes GET-parameters
        """
        url = 'http://search-foo.us-east-1.es.amazonaws.com:80/index/type/1/_update?version=1'
        mock_request = mock.Mock()
        mock_request.url = url
        mock_request.method = "POST"
        self.assertEqual('version=1', AWSRequestsAuth.get_canonical_querystring(mock_request))

    def test_auth_for_get(self):
        auth = AWSRequestsAuth(aws_access_key='YOURKEY',
                               aws_secret_access_key='YOURSECRET',
                               aws_host='search-foo.us-east-1.es.amazonaws.com',
                               aws_region='us-east-1',
                               aws_service='es')
        url = 'http://search-foo.us-east-1.es.amazonaws.com:80/'
        mock_request = mock.Mock()
        mock_request.url = url
        mock_request.method = "GET"
        mock_request.body = None
        mock_request.headers = {}

        frozen_datetime = datetime.datetime(2016, 6, 18, 22, 4, 5)
        with mock.patch('datetime.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = frozen_datetime
            auth(mock_request)
        self.assertEqual({
            'Authorization': 'AWS4-HMAC-SHA256 Credential=YOURKEY/20160618/us-east-1/es/aws4_request, '
                             'SignedHeaders=host;x-amz-date, '
                             'Signature=ca0a856286efce2a4bd96a978ca6c8966057e53184776c0685169d08abd74739',
            'x-amz-date': '20160618T220405Z',

        }, mock_request.headers)

    def test_auth_for_post(self):
        auth = AWSRequestsAuth(aws_access_key='YOURKEY',
                               aws_secret_access_key='YOURSECRET',
                               aws_host='search-foo.us-east-1.es.amazonaws.com',
                               aws_region='us-east-1',
                               aws_service='es')
        url = 'http://search-foo.us-east-1.es.amazonaws.com:80/'
        mock_request = mock.Mock()
        mock_request.url = url
        mock_request.method = "POST"
        mock_request.body = b'foo=bar'
        mock_request.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        frozen_datetime = datetime.datetime(2016, 6, 18, 22, 4, 5)
        with mock.patch('datetime.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = frozen_datetime
            auth(mock_request)
        self.assertEqual({
            'Authorization': 'AWS4-HMAC-SHA256 Credential=YOURKEY/20160618/us-east-1/es/aws4_request, '
                             'SignedHeaders=host;x-amz-date, '
                             'Signature=a6fd88e5f5c43e005482894001d9b05b43f6710e96be6098bcfcfccdeb8ed812',
            'Content-Type': 'application/x-www-form-urlencoded',
            'x-amz-date': '20160618T220405Z',

        }, mock_request.headers)

    def test_auth_for_post_with_str_body(self):
        auth = AWSRequestsAuth(aws_access_key='YOURKEY',
                               aws_secret_access_key='YOURSECRET',
                               aws_host='search-foo.us-east-1.es.amazonaws.com',
                               aws_region='us-east-1',
                               aws_service='es')
        url = 'http://search-foo.us-east-1.es.amazonaws.com:80/'
        mock_request = mock.Mock()
        mock_request.url = url
        mock_request.method = "POST"
        mock_request.body = 'foo=bar'
        mock_request.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        frozen_datetime = datetime.datetime(2016, 6, 18, 22, 4, 5)
        with mock.patch('datetime.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = frozen_datetime
            auth(mock_request)
        self.assertEqual({
            'Authorization': 'AWS4-HMAC-SHA256 Credential=YOURKEY/20160618/us-east-1/es/aws4_request, '
                             'SignedHeaders=host;x-amz-date, '
                             'Signature=a6fd88e5f5c43e005482894001d9b05b43f6710e96be6098bcfcfccdeb8ed812',
            'Content-Type': 'application/x-www-form-urlencoded',
            'x-amz-date': '20160618T220405Z',

        }, mock_request.headers)
