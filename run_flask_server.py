import flask
from flask_pymongo import PyMongo

import time
import datetime

import requests
import json

app = flask.Flask(__name__)
app.config['MONGO_DBNAME'] = 'order_entry'
app.config['MONGO_URI'] = 'mongodb://admin:thisisyouradmin@ds141068.mlab.com:41068/order_entry'

mongo = PyMongo(app)



def send_to_exec_link(new_order, content_type):								## send to execution link
	# initialize the REST API endpoint URL
	URL_FOR_ORDER = "http://localhost:5001/execution_REST_API_dummy"
	headers = {'Content-Type' : 'application/json'}



	order_data = {'type': content_type, 'order_id': new_order['order_id'], 'user_id': new_order['user_id'], 
				'product_id' : new_order['product_id'], 'side': new_order['side'], 
				'ask_price': new_order['ask_price'], 'total_qty' : new_order['total_qty'], 
				'order_stamp' : new_order['order_stamp'], 'state' : new_order['state'] }

	# submit the request
	r = requests.post(URL_FOR_ORDER, data = json.dumps(order_data), headers = headers).json()

	# ensure the request was sucessful
	if r["success"]:
		print ('Request succeeded')
		
	# otherwise, the request failed
	else:
		print ("Request failed")


def send_to_trade_post(order, fill, fill_list):				## send to trade post
	# initialize the REST API endpoint URL
	URL_FOR_ORDER_FILL = "http://localhost:5002/trade_post_REST_API_dummy"
	headers = {'Content-Type' : 'application/json'}

	order_fill_data = {'order_id': order['order_id'], 'user_id': order['user_id'], 
				'product_id' : order['product_id'], 'side': order['side'], 
				'ask_price': order['ask_price'], 'total_qty' : order['total_qty'], 
				'order_stamp' : order['order_stamp'], 'state' : order['state'],
				'fill' : fill }

	# submit the request
	r = requests.post(URL_FOR_ORDER_FILL, data = json.dumps(order_fill_data), headers = headers).json()

	# ensure the request was sucessful
	if r["success"]:
		print ('Request succeeded')
		
	# otherwise, the request failed
	else:
		print ("Request failed")




# Following endpoint corresponds to order_entry() function defined below it.
# It can be called by client on 'http://localhost:5000/order_endpoint' url.

@app.route("/order_endpoint", methods=["POST"])
def order_entry():
	mongo_order = mongo.db.orders
	mongo_fill = mongo.db.fills
	
	if flask.request.method == "POST":
		#print request.data
		if flask.request.is_json:
			content = flask.request.get_json()	
			print content
			#print 'IP of sender : ', flask.request.remote_addr
			#print flask.request.environ['REMOTE_ADDR']


			if content['type'] == 1:				# Insert new order
				ack = {"success": False}
			
				order_id = content['order_id']
				user_id = content['user_id']
				product_id = content['product_id']
				side = content['side']
				ask_price = content['ask_price']
				total_qty = content['total_qty']
				
				ts = time.time()
				order_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
				
				mongo_order.insert({'order_id' : order_id, 'user_id' : user_id, 'product_id' : product_id, 'side' : side, 'ask_price' : ask_price, 'total_qty' : total_qty, 'LTP' : -1, 'order_stamp' : order_stamp, 'reason_cancellation' : '', 'state' : 1})
				
				# state = 1 (live), 2 (closed), 3 (cancelled), 4 (filled), 5 (rejected)
				
				ack["success"] = True

				new_order = mongo_order.find_one({'order_id' : order_id})		## new/updated/canceled order
				send_to_exec_link(new_order, content['type'])
				
				

			elif content['type'] == 2:				# Update price of order
				ack = {"success": False}
				
				order_id = content['order_id']
				ask_price = content['ask_price']
				
				ts = time.time()
				order_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
				
				existing = mongo_order.find_one({'order_id' : order_id})
				print '< existing ', existing, ' >'
			
				old_price = existing['ask_price']
				old_qty = existing['total_qty']
				old_stamp = existing['order_stamp']
				old_state = existing['state']
			
				old_values = { 'ask_price': old_price, 'total_qty': old_qty, 'order_stamp': old_stamp, 'state': old_state }
			
				history = []
			
				if 'history' not in existing:				# Create history list and add old values
					history.append(old_values)
					print 'here'
				
				else:							# Append old values to history list	
					history = existing['history']
					history.append(old_values)
					print 'there'
					
				print 'history ', history

				mongo_order.update_one({'order_id': order_id}, {'$set': {'history': history} }, upsert=False)
				mongo_order.update_one({'order_id': order_id}, {'$set': {'ask_price': ask_price} }, upsert=False)
				mongo_order.update_one({'order_id': order_id}, {'$set': {'order_stamp': order_stamp} }, upsert=False)				
				
				#To print contents of 'order' collection :-
				'''results = mongo_order.find()
				print 'BELOW\n'
				for res in results:
					print res
				'''
				
				ack["success"] = True

				new_order = mongo_order.find_one({'order_id' : order_id})		## new/updated/canceled order
				send_to_exec_link(new_order, content['type'])
				
								
							
			elif content['type'] == 3:				# Update quantity in order
				ack = {"success": False}
				
				order_id = content['order_id']
				total_qty = content['total_qty']
				
				ts = time.time()
				order_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
				
				existing = mongo_order.find_one({'order_id' : order_id})
				print '<', existing, '>'
					
				old_price = existing['ask_price']
				old_qty = existing['total_qty']
				old_stamp = existing['order_stamp']
				old_state = existing['state']
			
				old_values = { 'ask_price': old_price, 'total_qty': old_qty, 'order_stamp': old_stamp, 'state': old_state }
				
				history = []
			
				if 'history' not in existing:				# Create history list and add old values
					history.append(old_values)
					print 'no history'
				
				else:							# Append old values to history list	
					history = existing['history']
					history.append(old_values)
					print 'history there'
					
				print history

				mongo_order.update_one({'order_id': order_id}, {'$set': {'history': history} }, upsert=False)
				mongo_order.update_one({'order_id': order_id}, {'$set': {'total_qty': total_qty} }, upsert=False)
				mongo_order.update_one({'order_id': order_id}, {'$set': {'order_stamp': order_stamp} }, upsert=False)
				
				ack["success"] = True

				new_order = mongo_order.find_one({'order_id' : order_id})		## new/updated/canceled order
				send_to_exec_link(new_order, content['type'])
				


			elif content['type'] == 4:				# Cancel order
				ack = {"success": False}
				
				order_id = content['order_id']
				reason_cancellation = content['reason_cancellation']
				
				ts = time.time()
				order_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
				
				existing = mongo_order.find_one({'order_id' : order_id})
				print '<', existing, '>'
				
				old_price = existing['ask_price']
				old_qty = existing['total_qty']
				old_stamp = existing['order_stamp']
				old_state = existing['state']
			
				old_values = { 'ask_price': old_price, 'total_qty': old_qty, 'order_stamp': old_stamp, 'state': old_state }
					
				history = []
			
				if 'history' not in existing:				# Create history list and add old values
					history.append(old_values)
				
				else:							# Append old values to history list	
					history = existing['history']
					history.append(old_values)

				mongo_order.update_one({'order_id': order_id}, {'$set': {'history': history} }, upsert=False)
				mongo_order.update_one({'order_id': order_id}, {'$set': {'state': 3} }, upsert=False)
				mongo_order.update_one({'order_id': order_id}, {'$set': {'order_stamp': order_stamp} }, upsert=False)
					
				ack["success"] = True

				new_order = mongo_order.find_one({'order_id' : order_id})		## new/updated/canceled order
				send_to_exec_link(new_order, content['type'])



			elif content['type'] == 5:				# get order details
				user_id = content['user_id']

				orders = []
				order_data = mongo_order.find({'user_id' : user_id})

				order_columns = ["Side", "State", "Symbol", "Client", "Size", "QtyDone", "QtyOpen", "OrderId",
								"PriceInstruction", "Exchange", "OrderStamp", "ProductType", "Ask", "Bid",
								"LTP", "fill_columns"]

				fill_columns = ["OrderId", "QtyDone", "Exchange", "Stamp", "Price", "FillId"]

				data = []
				
				for order in order_data:
					tmp_order = []
					tmp_order.append(order['side'])
					tmp_order.append(order['state'])
					#tmp_order.append('symbol')
					#tmp_order.append('Client')
					#tmp_order.append(Size)
					#tmp_order.append(QtyDone)
					#tmp_order.append(QtyOpen)

					#tmp_order['total_qty'] = order['total_qty']

					tmp_order.append(order['order_id'])
					#tmp_order.append("PriceInstruction")
					#tmp_order.append("Exchange")
					tmp_order.append(order['order_stamp'])
					#tmp_order.append('ProductType')
					tmp_order.append(order['ask_price'])
					#tmp_order.append(Bid)
					tmp_order.append(order['LTP'])

										#tmp_order['product_id'] = order['product_id']
										#tmp_order['reason_cancellation'] = ''


					fill_data = mongo_fill.find({'order_id' : order['order_id']})
					fills = []
					fill_list = []
				
					for record in fill_data:
						fill_list = record['fills']
						break

					for fill in fill_list: 
						tmp_fill = []
						tmp_fill.append(order['order_id'])
						tmp_fill.append(fill['qtydone'])
						#tmp_fill.append('Exchange')
						tmp_fill.append(fill['exchange_stamp'])
						tmp_fill.append(fill['price'])
						tmp_fill.append(fill['fill_id'])
										#tmp_fill['exchange_id'] = fill['exchange_id']

						fills.append(tmp_fill)

					tmp_order.append(fills)

					data.append(tmp_order)

				ack = {'order_columns' : order_columns, 'fill_columns' : fill_columns, 'data' : data}
				print(json.dumps(ack, sort_keys=True, indent=4))

			#new_order = mongo_order.find_one({'order_id' : order_id_send})			## new/updated/canceled order
			#send_to_exec_link(new_order, content['type'])				

	# return the data dictionary as a JSON response
	return flask.jsonify(ack)



# Following endpoint corresponds to execution_links() function defined below it.
# It can be called by client on 'http://localhost:5000/execution_endpoint' url.

@app.route("/execution_endpoint", methods=["POST"])
def execution_links():
	# initialize the ack dictionary that will be returned from the view
	ack = {"success": False}
	mongo_fill = mongo.db.fills
	mongo_order = mongo.db.orders 								##
	
	if flask.request.method == "POST":
		#print request.data
		if flask.request.is_json:
			content = flask.request.get_json()	
			print content
			#print flask.request.environ['REMOTE_ADDR']
			#print 'IP of sender : ', flask.request.remote_addr
			
			order_id = content['order_id']
			fill = content['fill']			
			print fill
			
			ts = time.time()
			exchange_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
			fill['exchange_stamp'] = exchange_stamp
			print fill
			
			LTP = fill['price']		# Latest traded price	

			'''qtydone = content['qtydone']
			prices = content['prices']
			exchange_id = content['exchange_id']
			
			fill.insert({'fill_ids' : fill_ids, 'order_id' : order_id, 'qtydone' : qtydone, 'prices' : prices, 'exchange_id' : exchange_id})'''
			
			existing = mongo_fill.find_one({'order_id' : order_id})
			print '<', existing, '>'
			
			if existing == None:		# If fills for this order_id do not exist, create new json with list of fills
				mongo_fill.insert({ 'order_id' : order_id, 'fills' : [fill] })
				
			else:				# If fills for this order_id already exist, then append the new fill to list
				existing_fills = existing['fills']
				existing_fills.append(fill)
				mongo_fill.update_one( {'order_id': order_id}, {'$set': {'fills': existing_fills} }, upsert=False)
			
			mongo_order.update_one( {'order_id': order_id}, {'$set': {'LTP': LTP} }, upsert=False)
			
			# indicate that the request was a success
			ack["success"] = True


			order_send = mongo_order.find_one({'order_id' : order_id})    ##
			fill_list_send = mongo_fill.find_one({'order_id' : order_id})		##		
			send_to_trade_post(order_send, fill, fill_list_send)				## send to trade post

	return flask.jsonify(ack)


# if this is the main thread of execution first load the model and then start the server
if __name__ == "__main__":
	print(("* Flask starting server..."
		"Please wait until server has fully started"))
	app.run(debug=True)


