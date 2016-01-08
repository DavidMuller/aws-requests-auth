import hmac
import urllib
import hashlib
import datetime
from urlparse import urlparse

import requests


def sign(key, msg):
    """
    Copied from https://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html
    """
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def getSignatureKey(key, dateStamp, regionName, serviceName):
    """
    Copied from https://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html
    """
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning


class AWSRequestsAuth(requests.auth.AuthBase):
    """
    Auth class that allows us to connect to AWS services
    via Amazon's signature version 4 signing process

    Adapted from https://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html
    """

    def __init__(self,
                 aws_host,
                 aws_service,
                 aws_access_key=None,
                 aws_secret_access_key=None,
                 aws_region=None,
                 headers=None):
        """
        Example usage for talking to an AWS Elasticsearch Service:

        If an access key, secret access key, or the region is not provided they will be determined
        using the same method as the aws cli

        AWSRequestsAuth(aws_host='search-service-foobar.us-east-1.es.amazonaws.com',
                        aws_service='es',
                        aws_access_key='YOURKEY',
                        aws_secret_access_key='YOURSECRET',
                        aws_region='us-east-1')
        """
        self.aws_access_key = aws_access_key
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_host = aws_host
        self.aws_region = aws_region
        self.service = aws_service
        self.headers = headers if headers else {}

        if not (aws_access_key and aws_secret_access_key):
            # Attempt to get instance role creds

            metadata_exception = TypeError("AWS credentials not provided, and they cannot be retreived from configuration")

            try:
                import botocore.session
            except ImportError:
                raise metadata_exception

            session = botocore.session.Session()
            security_creds = session.get_credentials()

            if not security_creds:
                raise metadata_exception

            self.aws_access_key = security_creds.access_key
            self.aws_secret_access_key = security_creds.secret_key

            if security_creds.token:
                self.headers['X-Amz-Security-Token'] = security_creds.token

        if not aws_region:

            try:
                import boto.session
            except ImportError:
                raise TypeError("Unable to determine region")

            session = boto.session.Session()
            self.aws_region = session.get_config_variable('region')
        else:
            self.aws_region = aws_region

    def __call__(self, r):
        """
        Adds the authorization headers required by Amazon's signature
        version 4 signing process to the request.

        Adapted from https://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html
        """
        # Create a date for headers and the credential string
        t = datetime.datetime.utcnow()
        amzdate = t.strftime('%Y%m%dT%H%M%SZ')
        datestamp = t.strftime('%Y%m%d')  # Date w/o time for credential_scope

        canonical_uri = AWSRequestsAuth.get_caononical_path(r)

        canonical_querystring = AWSRequestsAuth.get_canonical_querystring(r)

        # Create the canonical headers and signed headers. Header names
        # and value must be trimmed and lowercase, and sorted in ASCII order.
        # Note that there is a trailing \n.
        canonical_headers = ('host:' + self.aws_host + '\n' +
                             'x-amz-date:' + amzdate + '\n')

        # Create the list of signed headers. This lists the headers
        # in the canonical_headers list, delimited with ";" and in alpha order.
        # Note: The request can include any headers; canonical_headers and
        # signed_headers lists those that you want to be included in the
        # hash of the request. "Host" and "x-amz-date" are always required.
        signed_headers = 'host;x-amz-date'

        # Create payload hash (hash of the request body content). For GET
        # requests, the payload is an empty string ('').
        body = r.body if r.body else ''
        payload_hash = hashlib.sha256(body).hexdigest()

        # Combine elements to create create canonical request
        canonical_request = (r.method + '\n' + canonical_uri + '\n' +
                             canonical_querystring + '\n' + canonical_headers +
                             '\n' + signed_headers + '\n' + payload_hash)

        # Match the algorithm to the hashing algorithm you use, either SHA-1 or
        # SHA-256 (recommended)
        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = (datestamp + '/' + self.aws_region + '/' +
                            self.service +'/' + 'aws4_request')
        string_to_sign = (algorithm + '\n' + amzdate + '\n' + credential_scope +
                          '\n' + hashlib.sha256(canonical_request).hexdigest())

        # Create the signing key using the function defined above.
        signing_key = getSignatureKey(self.aws_secret_access_key,
                                      datestamp,
                                      self.aws_region,
                                      self.service)

        # Sign the string_to_sign using the signing_key
        string_to_sign_utf8 = string_to_sign.encode('utf-8')
        signature = hmac.new(signing_key,
                             string_to_sign_utf8,
                             hashlib.sha256).hexdigest()

        # The signing information can be either in a query string value or in
        # a header named Authorization. This code shows how to use a header.
        # Create authorization header and add to request headers
        authorization_header = (algorithm + ' ' + 'Credential=' + self.aws_access_key +
                                '/' + credential_scope + ', ' + 'SignedHeaders=' +
                                signed_headers + ', ' + 'Signature=' + signature)

        r.headers['Authorization'] = authorization_header
        r.headers['x-amz-date'] = amzdate
        r.headers.update(self.headers)
        return r

    @classmethod
    def get_caononical_path(cls, r):
        """
        Create canonical URI--the part of the URI from domain to query
        string (use '/' if no path)
        """
        parsedurl = urlparse(r.url)

        # safe chars adapted from boto's use of urllib.parse.quote
        # https://github.com/boto/boto/blob/d9e5cfe900e1a58717e393c76a6e3580305f217a/boto/auth.py#L393
        return urllib.quote(parsedurl.path if parsedurl.path else '/', safe='/-_.~')

    @classmethod
    def get_canonical_querystring(cls, r):
        """
        Create the canonical query string. In this example (a GET request),
        request parameters are in the query string. Query string values must
        be URL-encoded (space=%20). The parameters must be sorted by name.
        """
        canonical_querystring = ''

        parsedurl = urlparse(r.url)
        querystring_sorted = '&'.join(sorted(parsedurl.query.split('&')))

        for query_param in querystring_sorted.split('&'):
            key_val_split = query_param.split('=', 1)

            # safe chars adopted from boto source
            # https://github.com/boto/boto/blob/d9e5cfe900e1a58717e393c76a6e3580305f217a/boto/auth.py#L359-L360
            unenc_key = urllib.unquote(key_val_split[0])
            key = urllib.quote(key_val_split[0], safe='-_.~') if key_val_split[0] == unenc_key else key_val_split[0]
            try:
                unenc_val = urllib.unquote(key_val_split[1])
                val = urllib.quote(key_val_split[1], safe='-_.~') if key_val_split[1] == unenc_val else key_val_split[1]
            except IndexError:
                val = ''

            if key:
                if canonical_querystring:
                    canonical_querystring += "&"
                canonical_querystring += u'='.join([key, val])

        return canonical_querystring
