"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws_native import s3

# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket( "adev-pulumi-bucket", # this is the standard needed name, but if we just use this name then pulumi 
                   # will append random  stuff to the end  to avoid collisions
                    bucket_name="adev-pulumi-bucket", # this allows us to retain the actual bucket name
                    tags=[
                        {'key':'Type','value':'Dev'}, # each tag needs it's own key & value set in the array
                        {'key':'PHI','value':'no'}
                        ]
                   )

# Export the name of the bucket
# create an Ec2 example and pull the public IP once the machine is created
pulumi.export("bucket_name", bucket.id)