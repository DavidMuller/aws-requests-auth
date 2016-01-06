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
        self.assertEqual('/', AWSRequestsAuth.get_caononical_path(mock_request))
        self.assertEqual('', AWSRequestsAuth.get_canonical_querystring(mock_request))

    def test_characters_escaped_in_path(self):
        """
        Assert we generate the 'correct' cannonical query string
        and path a request with characters that need to be escaped
        """
        url = 'http://search-foo.us-east-1.es.amazonaws.com:80/+foo.*/_stats'
        mock_request = mock.Mock()
        mock_request.url = url
        self.assertEqual('/%2Bfoo.%2A/_stats', AWSRequestsAuth.get_caononical_path(mock_request))
        self.assertEqual('', AWSRequestsAuth.get_canonical_querystring(mock_request))

    def test_path_with_querystring(self):
        """
        Assert we generate the 'correct' cannonical query string
        and path for request that includes a query stirng
        """
        url = 'http://search-foo.us-east-1.es.amazonaws.com:80/my_index/?pretty=True'
        mock_request = mock.Mock()
        mock_request.url = url
        self.assertEqual('/my_index/', AWSRequestsAuth.get_caononical_path(mock_request))
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
