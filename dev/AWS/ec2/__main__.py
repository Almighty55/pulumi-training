# Copyright 2016-2018, Pulumi Corporation.  All rights reserved.

import pulumi
import pulumi_aws as aws

ami = aws.ec2.get_ami(most_recent=True,
                  owners=["137112412989"],
                  filters=[aws.GetAmiFilterArgs(name="name", values=["amzn-ami-hvm-*"])])

sg = aws.ec2.SecurityGroup('webAccesss',
    name='webAccess',
    description='Enable HTTP access',
    ingress=[aws.ec2.SecurityGroupIngressArgs(
        protocol='tcp',
        from_port=80,
        to_port=80,
        cidr_blocks=['0.0.0.0/0'],
        )
    ]
)

user_data = """
#!/bin/bash
echo "George you paying attention?" > index.html
nohup python -m SimpleHTTPServer 80 &
"""

server = aws.ec2.Instance('web-server-www',
    instance_type='t2.micro',
    vpc_security_group_ids=[sg.id],
    # had to run this in the cli for default VPC
    # aws ec2 create-default-vpc    
    user_data=user_data,
    ami=ami.id)

pulumi.export('public_ip', server.public_ip)
pulumi.export('public_dns', server.public_dns)