# Driver program for Order entry gateway (Group 1)

# USAGE
# python order_request.py

# import the necessary packages
import requests
import json

# initialize the REST API endpoint URL
URL_FOR_ORDER = "http://localhost:5000/order_endpoint"
headers = {'Content-Type' : 'application/json'}


order_data = {'type': 1, 'user_id': 3408, 'product_id' : 302, 'side': 1, 'ask_price': 70, 'total_qty' : 40}
# type: 1 - Add new order, 2 - Update price of order, 3 - Update quantity in order, 4 - Cancel order

# submit the request
ack = requests.post(URL_FOR_ORDER, data = json.dumps(order_data), headers = headers).json()

# ensure the request was sucessful
if ack["success"]:
	print ('Request succeeded')
	print ack
	
# otherwise, the request failed
else:
	print ("Request failed")
