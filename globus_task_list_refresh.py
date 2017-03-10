
# coding: utf-8

# In[1]:

# monitor your last 5 GO task_id's

import time
import globus_sdk

CLIENT_ID='2826c2c1-2bdf-4ea4-8f3a-d25487ad9c4c'
client = globus_sdk.NativeAppAuthClient(CLIENT_ID)
client.oauth2_start_flow_native_app(refresh_tokens=True)

authorize_url = client.oauth2_get_authorize_url()
print('Please go to this URL and login: {0}'.format(authorize_url))

# this is to work on Python2 and Python3 -- you can just use raw_input() or
# input() for your specific version
get_input = getattr(__builtins__, 'raw_input', input)
auth_code = get_input(
    'Please enter the code you get after login here: ').strip()
token_response = client.oauth2_exchange_code_for_tokens(auth_code)
globus_auth_data = token_response.by_resource_server['auth.globus.org']


# In[2]:

def my_task_list(token_response):
	globus_transfer_data = token_response.by_resource_server['transfer.api.globus.org']
	# the refresh token and access token, often abbr. as RT and AT
	transfer_rt = globus_transfer_data['refresh_token']
	transfer_at = globus_transfer_data['access_token']
	expires_at_s = globus_transfer_data['expires_at_seconds']

	# a GlobusAuthorizer is an auxiliary object we use to wrap the token. In
	# more advanced scenarios, other types of GlobusAuthorizers give us
	# expressive power

	authorizer = globus_sdk.RefreshTokenAuthorizer(
	transfer_rt, client, access_token=transfer_at, expires_at=expires_at_s)

	tc = globus_sdk.TransferClient(authorizer=authorizer)

	for transfer in tc.task_list(num_results=5):
    		print("task_id= ( %s ) %s -> %s" % 
                  (transfer['task_id'],
                   transfer['source_endpoint_display_name'],
                   transfer['destination_endpoint_display_name']))
    		print("request_time %s" % transfer['request_time'])
    		print("completed    %s" % transfer['completion_time'])
    		print("type=%s Mbytes=%.1f Mbytes/s=%.1f" % 
                  (transfer['type'],transfer['bytes_transferred']/1024,
                   transfer['effective_bytes_per_second']/1024))
	    	print("=====================================================")

	print("______________________________________________________________________________")
	time.sleep(30)
# end def my_task_list


# In[3]:

while (0<1):
    my_task_list(token_response)
# end while    


# In[ ]:



