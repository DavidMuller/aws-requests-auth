from distutils.core import setup


setup(
    name='aws-requests-auth',
    version='0.4.2',
    author='David Muller',
    author_email='davehmuller@gmail.com',
    packages=['aws_requests_auth'],
    url='https://github.com/davidmuller/aws-requests-auth',
    description='AWS signature version 4 signing process for the python requests module',
    long_description='See https://github.com/davidmuller/aws-requests-auth for installation and usage instructions.',
    install_requires=['requests>=0.14.0'],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)
