"""
Functions in this file are included as a convenience for working with AWSRequestsAuth.
External libraries, like boto, that this file imports are not a strict requirement for the
aws-requests-auth package.
"""

import boto3


def get_credentials():
    """
    Interacts with boto to retrieve AWS credentials, and returns a dictionary of
    kwargs to be used in AWSRequestsAuth. boto automatically pulls AWS credentials from 
    a variety of sources including but not limited to credentials files and IAM role.
    AWS credentials are pulled in the order listed here: 
    http://boto3.readthedocs.io/en/latest/guide/configuration.html#configuring-credentials
    """
    credentials_obj = boto3.Session().get_credentials()
    return {
        'aws_access_key': credentials_obj.access_key,
        'aws_secret_access_key': credentials_obj.secret_key,
        'aws_token': credentials_obj.token,
    }
