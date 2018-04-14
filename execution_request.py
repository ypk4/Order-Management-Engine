# Driver program for Execution links (Group 2)

# USAGE
# python execution_request.py

# import the necessary packages
import requests
import json

# initialize the REST API endpoint URL
URL_FOR_EXECUTION = "http://localhost:5000/execution_endpoint"
headers = {'Content-Type' : 'application/json'}

#fill_data = {'order_id': 124, 'fill_ids': [75, 89], 'qtydone': [10, 20], 'prices': [45, 85], 'exchange_id' : 6766}
#fill_data = { 'order_id': 125,  'fills': [ { 'fill_id': 75, 'qtydone': 10, 'price': 45, 'exchange_id': 6766 }, { 'fill_id': 89, 'qtydone': 20, 'price': 85, 'exchange_id': 6766 } ] }
fill_data = { 'order_id': '5ad1bb9e381adc1db17276f5',  'fill': { 'fill_id': 3, 'qtydone': 15, 'price': 60, 'exchange_id': 1 } }

# submit the request
r = requests.post(URL_FOR_EXECUTION, data = json.dumps(fill_data), headers = headers).json()

# ensure the request was sucessful
if r["success"]:
	print ('Request succeeded')
	
# otherwise, the request failed
else:
	print ("Request failed")
