[![Build Status](https://travis-ci.org/DavidMuller/aws-requests-auth.svg?branch=master)](https://travis-ci.org/DavidMuller/aws-requests-auth)

# AWS Signature Version 4 Signing Process with python requests

This package allows you to authenticate to AWS with Amazon's [signature version 4 signing process](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html) with the python [requests](http://docs.python-requests.org/en/latest/) library.

Tested with both python `2.7` and `3.4`.

# Installation

```
pip install aws-requests-auth
```

# Motivation

This code came about because Amazon's Elasticsearch Service [does not currently support VPC](https://forums.aws.amazon.com/thread.jspa?threadID=217059&tstart=0). This authentication class allows us to talk to our Elasticsearch cluster via [IAM](https://aws.amazon.com/iam/).

Conceivably, the authentication class is flexible enough to be used with any AWS service that supports the signature version 4 signing process.  However, I've only tested it with the Elasticsearch service.


# Usage

```python
import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth

# let's talk to our AWS Elasticsearch cluster
auth = AWSRequestsAuth(aws_access_key='YOURKEY',
                       aws_secret_access_key='YOURSECRET',
                       aws_host='search-service-foobar.us-east-1.es.amazonaws.com',
                       aws_region='us-east-1',
                       aws_service='es')

response = requests.get('http://search-service-foobar.us-east-1.es.amazonaws.com',
                        auth=auth)
print response.content

{
  "status" : 200,
  "name" : "Stevie Hunter",
  "cluster_name" : "elasticsearch",
  "version" : {
    "number" : "1.5.2",
    etc....
  },
  "tagline" : "You Know, for Search"
}
```

## elasticsearch-py Client Usage Example

It's possible to inject the `AWSRequestsAuth` class directly into the [elasticsearch-py](https://elasticsearch-py.readthedocs.org/en/master/) library so you can talk to your Amazon AWS cluster directly through the elasticsearch-py client.

```python
from aws_requests_auth.aws_auth import AWSRequestsAuth
from elasticsearch import Elasticsearch, RequestsHttpConnection

es_host = 'search-service-foobar.us-east-1.es.amazonaws.com'
auth = AWSRequestsAuth(aws_access_key='YOURKEY',
                       aws_secret_access_key='YOURSECRET',
                       aws_host=es_host,
                       aws_region='us-east-1',
                       aws_service='es')

# use the requests connection_class and pass in our custom auth class
es_client = Elasticsearch(host=es_host,
                          port=80,
                          connection_class=RequestsHttpConnection,
                          http_auth=auth)
print es_client.info()
```

## Temporary Security Credentials
If you are using [AWS STS](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html) to grant temporary access to your Elasticsearch resource, you can use the `aws_token` keyword argument to include your credentials in `AWSRequestsAuth`.  See [issue #9](https://github.com/DavidMuller/aws-requests-auth/issues/9) and [PR #11](https://github.com/DavidMuller/aws-requests-auth/pull/11 for) for additional details. 
