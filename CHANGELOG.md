Changelog (aws-requests-auth)
==================

0.3.0
------------------
- Add python3 support -- thanks to @jlaine, and @anantasty
   - See https://github.com/DavidMuller/aws-requests-auth/pull/16

0.2.5
------------------
- Stop urlencoding query params in get_canonical_querystring(). The urlencoding in get_canonical_querystring() was causing "double encoding issues" because elasticsearch-py already apperas to urlencode query params
    - If you are using a client other than elasticsearch-py, you will need to be sure that your client urlecondes your query params before they are passed to the `AWSRequests` auth class
    - See https://github.com/DavidMuller/aws-requests-auth/pull/13 for more details

0.2.4
------------------
- Add support for [AWS STS](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html) using the `aws_token` keyword argument to `AWSRequestsAuth`
    - See [issue #9](https://github.com/DavidMuller/aws-requests-auth/issues/9) and [PR #11](https://github.com/DavidMuller/aws-requests-auth/pull/11 for) for additional details

0.2.3
------------------
- Fix handling of multiple query parameters
    - For example, the two `pretty=True` query paramaters in the following url
      `http://search-service-foobar.us-east-1.es.amazonaws.com?pretty=True&pretty=True`
      are now handled properly
    - see https://github.com/DavidMuller/aws-requests-auth/pull/7


0.2.2
------------------
- Update url quoting for canonical uri and canonical query string


0.2.1
------------------
- Fix bug where cannonical uri and query string was not url encoded appropriately for the signing process


0.2.0
------------------
- Fix typos of `aws_secret_access_key` : https://github.com/DavidMuller/aws-requests-auth/pull/1
    - This is a breaking change. The `AWSRequestsAuth` constructor now expects the kwarg `aws_secret_access_key` (instead of the incorrectly spelled `aws_secret_acces_key`).


0.1.0
------------------
Initial release
