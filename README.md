# AWS Signature Version 4 Signing Process with python requests

This package allows you to authenticate to AWS with Amazon's [signature version 4 signing process](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html) with the python [requests](http://docs.python-requests.org/en/latest/) library.

Developed and tested with python `2.7.10`.

# Installation

```
pip install requests-auth-aws
```

# Usage

```python
from aws_requests_auth.aws_auth import AWSRequestsAuth

# let's talk to our AWS Elasticsearch cluster
auth = AWSRequestsAuth(aws_access_key='YOURKEY',
                       aws_secret_acces_key='YOURSECRET',
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

## Motivation

This code came about because Amazon's Elasticsearch Service [does not currently support VPC](https://forums.aws.amazon.com/thread.jspa?threadID=217059&tstart=0). This authentication class allows us to talk to our Elasticsearch cluster via [IAM](https://aws.amazon.com/iam/).

Conceivably, though, the authentication class is flexible enough to be used with any AWS service that supports the signature version 4 signing process.

### elasticsearch-py Client Usage Example

It's possible to inject the `AWSRequestsAuth` class directly into the [elasticsearch-py](https://elasticsearch-py.readthedocs.org/en/master/) library so you can talk to your Amazon AWS cluster directly through the elasticsearch-py client.

```python
from aws_requests_auth.aws_auth import AWSRequestsAuth
from elasticsearch import Elasticsearch, RequestsHttpConnection

es_host = 'search-service-foobar.us-east-1.es.amazonaws.com'
auth = AWSRequestsAuth(aws_access_key='YOURKEY',
                       aws_secret_acces_key='YOURSECRET',
                       aws_host=es_host,
                       aws_region='us-east-1',
                       aws_service='es')

# use the requests connection_class and pass in our custom auth class
es_client = Elasticsearch(hosts=es_host,
                          port=80,
                          connection_class=RequestsHttpConnection,
                          http_auth=auth)
print es_client.info()
```