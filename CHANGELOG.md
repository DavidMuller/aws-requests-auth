Changelog (aws-requests-auth)
==================

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
