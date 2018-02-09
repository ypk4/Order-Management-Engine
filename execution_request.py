# Driver program for Execution links (Group 2)

# USAGE
# python execution_request.py

# import the necessary packages
import requests
import json

# initialize the REST API endpoint URL
URL_FOR_EXECUTION = "http://localhost:5000/execution_endpoint"
headers = {'Content-Type' : 'application/json'}

fill_data = {'fill_ids': [75, 89], 'order_id': 124, 'qtydone': [10,20], 'prices': [45, 85], 'exchange_id':6766}

# submit the request
r = requests.post(URL_FOR_EXECUTION, data = json.dumps(fill_data), headers = headers).json()

# ensure the request was sucessful
if r["success"]:
	print ('Request succeeded')
	
# otherwise, the request failed
else:
	print ("Request failed")
