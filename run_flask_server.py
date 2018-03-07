import flask
from flask_pymongo import PyMongo

import time
import datetime

app = flask.Flask(__name__)
app.config['MONGO_DBNAME'] = 'order_entry'
app.config['MONGO_URI'] = 'mongodb://admin:thisisyouradmin@ds141068.mlab.com:41068/order_entry'

mongo = PyMongo(app)

# Following endpoint corresponds to order_entry() function defined below it.
# It can be called by client on 'http://localhost:5000/order_endpoint' url.

@app.route("/order_endpoint", methods=["POST"])
def order_entry():
	mongo_order = mongo.db.orders
	# initialize the ack dictionary that will be returned from the view
	ack = {"success": False}
	if flask.request.method == "POST":
		#print request.data
		if flask.request.is_json:
			content = flask.request.get_json()	
			print content
			#print 'IP of sender : ', flask.request.remote_addr
			#print flask.request.environ['REMOTE_ADDR']
			
			if content['type'] == 1:				# Add new order
				# code for inserting order
				order_id = content['order_id']
				user_id = content['user_id']
				product_id = content['product_id']
				side = content['side']
				ask_price = content['ask_price']
				total_qty = content['total_qty']
				
				ts = time.time()
				order_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
				
				mongo_order.insert({'order_id' : order_id, 'user_id' : user_id, 'product_id' : product_id, 'side' : side, 'ask_price' : ask_price, 'total_qty' : total_qty, 'order_stamp' : order_stamp, 'state' : 'live'})
				
				ack["success"] = True
				

			elif content['type'] == 2:				# Update price of order
				# code for updating price
				pass
				
			
			elif content['type'] == 3:				# Update quantity in order
				# code for updating quantity
				pass

	# return the data dictionary as a JSON response
	return flask.jsonify(ack)



# Following endpoint corresponds to execution_links() function defined below it.
# It can be called by client on 'http://localhost:5000/execution_endpoint' url.

@app.route("/execution_endpoint", methods=["POST"])
def execution_links():
	# initialize the ack dictionary that will be returned from the view
	ack = {"success": False}
	mongo_fill = mongo.db.fills
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
			
			'''qtydone = content['qtydone']
			prices = content['prices']
			exchange_id = content['exchange_id']
			
			fill.insert({'fill_ids' : fill_ids, 'order_id' : order_id, 'qtydone' : qtydone, 'prices' : prices, 'exchange_id' : exchange_id})'''
			
			existing = mongo_fill.find_one({'order_id' : order_id})
			print '<', existing, '>'
			
			if existing == None:		# If fills for this order_id do not exist, create list of fills
				mongo_fill.insert({ 'order_id' : order_id, 'fills' : [fill] })
				
			else:				# If fills for this order_id already exist, then append the new fill to list
				existing_fills = existing['fills']
				existing_fills.append(fill)
				mongo_fill.update_one( {'order_id': order_id}, {'$set': {'fills': existing_fills} }, upsert=False)
			
			# indicate that the request was a success
			ack["success"] = True
	return flask.jsonify(ack)


# if this is the main thread of execution first load the model and then start the server
if __name__ == "__main__":
	print(("* Flask starting server..."
		"Please wait until server has fully started"))
	app.run(debug=True)
