
# coding: utf-8

# In[1]:

import json
import sys
import globus_sdk

jsonFile = "globus_task_list.json"


# In[2]:

CLIENT_ID='2826c2c1-2bdf-4ea4-8f3a-d25487ad9c4c'
client = globus_sdk.NativeAppAuthClient(CLIENT_ID)
client.oauth2_start_flow_native_app()

authorize_url = client.oauth2_get_authorize_url()
print('Please go to this URL and login: {0}'.format(authorize_url))

# this is to work on Python2 and Python3 -- you can just use raw_input() or
# input() for your specific version
get_input = getattr(__builtins__, 'raw_input', input)
auth_code = get_input(
    'Please enter the code you get after login here: ').strip()
token_response = client.oauth2_exchange_code_for_tokens(auth_code)

globus_auth_data = token_response.by_resource_server['auth.globus.org']
globus_transfer_data = token_response.by_resource_server['transfer.api.globus.org']

# most specifically, you want these tokens as strings
AUTH_TOKEN = globus_auth_data['access_token']
TRANSFER_TOKEN = globus_transfer_data['access_token']


# In[3]:

# a GlobusAuthorizer is an auxiliary object we use to wrap the token. In
# more advanced scenarios, other types of GlobusAuthorizers give us
# expressive power
authorizer = globus_sdk.AccessTokenAuthorizer(TRANSFER_TOKEN)
tc = globus_sdk.TransferClient(authorizer=authorizer)

# high level interface; provides iterators for list responses
print("My Endpoints:")
for ep in tc.endpoint_search(filter_scope="my-endpoints"):
    print("[{}] {}".format(ep["id"], ep["display_name"]))


# In[ ]:

f= open(jsonFile)
data= json.load(f)


# In[4]:

print("My Last 25 Tasks:")
# `filter` to get Delete Tasks (default is just Transfer Tasks)
for task in tc.task_list(num_results=25, filter="type:TRANSFER,DELETE"):
    print(task["task_id"], task["type"], task["status"])


# In[5]:

#for transfer in data['DATA']:
for transfer in tc.task_list(num_results=5):
    print("=================================================================")
    print("task_id=(",transfer['task_id'],')',transfer['source_endpoint_display_name'],"=>",transfer['destination_endpoint_display_name'])
    print("request_time",transfer['request_time'])
    print("completed   ",transfer['completion_time'])
    print("TYPE=", transfer['type'],"Mbytes= {0:.1f}".format(transfer['bytes_transferred']/1024),"Mbytes/s= {0:.1f}".format(transfer['effective_bytes_per_second']/1024))
    


# In[ ]:



