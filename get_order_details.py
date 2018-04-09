# Driver program for Order entry gateway (Group 1)

# USAGE
# python order_request.py

# import the necessary packages
import requests
import json

# initialize the REST API endpoint URL
URL_FOR_ORDER = "http://localhost:5000/order_endpoint"
headers = {'Content-Type' : 'application/json'}


query = {'type': 5, 'user_id': 50}

# type: 1 - Add new order, 2 - Update price of order, 3 - Update quantity in order, 4 - Cancel order

# submit the request
r = requests.post(URL_FOR_ORDER, data = json.dumps(query), headers = headers).json()

# if r["success"]:
# 	print ('Request succeeded')
# else:
# 	print ("Request failed")

print(json.dumps(r, indent=4))