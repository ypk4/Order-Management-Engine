# Driver program for Execution links (Group 2)

# USAGE
# python execution_request.py

# import the necessary packages
import requests
import json

# initialize the REST API endpoint URL
URL_FOR_EXECUTION = "http://localhost:5000/execution_endpoint"
headers = {'Content-Type' : 'application/json'}

fill_data = {'fill_id': 75, 'data_2': -1, 'data_3': 47, 'data_4': 'SBY'}

# submit the request
r = requests.post(URL_FOR_EXECUTION, data = json.dumps(fill_data), headers = headers).json()

# ensure the request was sucessful
if r["success"]:
	print ('Request succeeded')
	
# otherwise, the request failed
else:
	print ("Request failed")
