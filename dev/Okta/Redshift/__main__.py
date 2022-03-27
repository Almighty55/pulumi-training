"""A Python Pulumi program"""

import pulumi
import pulumi_okta as okta
import csv

with open('redshift_clients.csv', 'r') as redshift_clients_csv:
    # store all the clients into a dictionary
    csvDict = csv.DictReader(redshift_clients_csv)
    # loop through each client entry from the csv
    # each run will create a new zone for that client
    for client in csvDict :
        fullInfo = client["users"].split(",")
        for user in fullInfo:
            displayName = user.split('\\')[0]
            #TODO: check if firstname or lastname is greater than 1 to handle users like "de Los Reyes"
            firstName = user.split('\\')[0].split(' ')[0]
            lastName = user.split('\\')[0].split(' ')[1]
            email = user.split('\\')[1]
        # use unique resource name here since multiple users can have the exact same name, but not email  
        users = okta.user.User((client['group']+"_"+email.replace(" ","_")),
                               display_name=displayName,
                               first_name=firstName,
                               last_name=lastName,
                               email=email,
                               login=email)
                                
        redshiftGroup = okta.group.Group(client["group"],
                                  name = client["group"],
                                  description = "Managed by Pulumi")
        
        # for userID in users:
        #     userList += okta.user.get_user(searches=[okta.user.GetUserSearchArgs(
        #         name="profile.firstName",
        #         value=users.firstName),])
            
        # testList = okta.user.get_user(searches=[
        #     okta.user.GetUserSearchArgs(
        #         name="profile.firstName",
        #         value="Adam",
        #         )
        #     ])    
        
        # memberships = okta.GroupMemberships((client["group"]+"_membership"),
        #                                     group_id = redshiftGroup.id,
        #                                     #TODO: Gather list of user id's created above
        #                                     users = [testList.id])
        #print(testList.id)