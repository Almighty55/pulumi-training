"""A Python Pulumi program"""

import pulumi
import pulumi_okta as okta
import csv

with open('clients.csv', 'r') as clients_csv:
    # store all the clients into a dictionary
    csvDict = csv.DictReader(clients_csv)
    # loop through each client entry from the csv
    # each run will create a new zone for that client
    for client in csvDict :
      network = okta.network.Zone((client["name"]+"_Zone"), # resource name required
                                # specify true name here
                                name = client["name"],
                                # use the split here since gateways requires a list
                                gateways = (client['gateways'].split(",")), 
                                #type will always be IP and not dynamic
                                type = "IP",
                                opts=pulumi.ResourceOptions(delete_before_replace=True))
      signOn = okta.policy.Signon((client["name"]+"_SignOn"),
                                # Limit this field to 50 characters
                                name = client["name"],
                                # this call leverages the ID which can vary from display name
                                # this ID is for org:company which was created by the webapp
                                #! groups_includeds is actually a typo in Pulumi's SDK
                                #! https://github.com/pulumi/pulumi-okta/issues/140
                                groups_includeds = [(okta.group.get_group(name="org:company")).id], 
                                status = "ACTIVE",
                                opts=pulumi.ResourceOptions(delete_before_replace=True,
                                depends_on=[network]))
      signOnRule = okta.policy.RuleSignon((client["name"]+"_SignOnRule"),
                                name="IP Whitelist",
                                network_connection = "ZONE",
                                network_includes = [network.id],
                                policy_id = signOn.id,
                                status="ACTIVE",
                                risc_level = "", # okta gets angry without this being set
                                opts=pulumi.ResourceOptions(delete_before_replace=True,
                                depends_on=[signOn]))
      
# group = okta.group.get_group(name="org:company")

# Export the name of the bucket
# pulumi.export("Group", group)