"""A Python Pulumi program"""

import pulumi
from pulumi_aws import s3

# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket('my-webserver')

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)