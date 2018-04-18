# Driver program for Order entry gateway (Group 1)

# USAGE
# python order_request.py

# import the necessary packages
import requests
import json

# initialize the REST API endpoint URL
URL_FOR_ORDER = "http://localhost:5000/order_endpoint"
headers = {'Content-Type' : 'application/json'}


order_data = {'type': 1, 'user_id': 3820, 'product_id' : 'TCS', 'side': 1, 'price_instruction':'LIMIT', 'ask_price': 70, 'total_qty' : 40, 'client': 1, 'exchange_id': 'NSE'}
# type: 1 - Add new order, 2 - Update price/qty of order, 3 - Cancel order, 4 - Get user's order details

# submit the request
ack = requests.post(URL_FOR_ORDER, data = json.dumps(order_data), headers = headers).json()

# ensure the request was sucessful
if ack["success"]:
	print ('Request succeeded')
	print ack
	
# otherwise, the request failed
else:
	print ("Request failed")
