# Driver program for Order entry gateway (Group 1)

# USAGE
# python order_request.py

# import the necessary packages
import requests
import json

# initialize the REST API endpoint URL
URL_FOR_ORDER = "http://localhost:5000/order_endpoint"
headers = {'Content-Type' : 'application/json'}



order_data = {'type': 1, 'order_id': 78, 'user_id': 122, 'product_id' : 312, 'side': 0, 'ask_price': 80, 'total_qty' : 30}
# type: 1 - Add new order, 2 - Update price of order, 3 - Update quantity in order, 4 - Cancel order

# submit the request
r = requests.post(URL_FOR_ORDER, data = json.dumps(order_data), headers = headers).json()

# ensure the request was sucessful
if r["success"]:
	print ('Request succeeded')
	
# otherwise, the request failed
else:
	print ("Request failed")
