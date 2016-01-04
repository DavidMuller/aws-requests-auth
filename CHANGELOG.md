Changelog (aws-requests-auth)
==================

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
