# USAGE
# Start the server :
# 	python run_keras_server.py
# Submit a request via cURL from different terminal :
# 	curl  -X POST  -H "Content-Type: application/json"  -d '{"key1":"value1", "key2":"value2"}' 'http://localhost:5000/order_endpoint'   OR
# Submit a request via separate Python / PHP / other language code from different terminal :
#	python simple_request.py


# import the necessary packages
import flask


# initialize our Flask application and the Keras model
app = flask.Flask(__name__)


# Following endpoint corresponds to order_entry() function defined below it. It can be called by client on 'http://localhost:5000/order_endpoint' url.

@app.route("/order_endpoint", methods=["POST"])
def order_entry():
	# initialize the ack dictionary that will be returned from the view
	ack = {"success": False}

	if flask.request.method == "POST":
		#print request.data
		if flask.request.is_json:
			content = flask.request.get_json()	
			print content
		
			print 'IP of sender : ', flask.request.remote_addr
			#print flask.request.environ['REMOTE_ADDR']
						
			# Our logic/code for the received JSON :-
			
			# e.g.- Adding order received from order entry
			
			#
			#

			# indicate that the request was a success
			ack["success"] = True

	# return the data dictionary as a JSON response
	return flask.jsonify(ack)


# Following endpoint corresponds to execution_links() function defined below it. It can be called by client on 'http://localhost:5000/execution_endpoint' url.

@app.route("/execution_endpoint", methods=["POST"])
def execution_links():
	# initialize the ack dictionary that will be returned from the view
	ack = {"success": False}

	if flask.request.method == "POST":
		#print request.data
		if flask.request.is_json:
			content = flask.request.get_json()	
			print content

			#print flask.request.environ['REMOTE_ADDR']
			print 'IP of sender : ', flask.request.remote_addr
			
			# Our logic/code for the received JSON :-
			
			# e.g.- Storing fill coming from execution links, etc
			
			#
			#

			# indicate that the request was a success
			ack["success"] = True

	# return the data dictionary as a JSON response
	return flask.jsonify(ack)


# if this is the main thread of execution first load the model and then start the server
if __name__ == "__main__":
	print(("* Flask starting server..."
		"Please wait until server has fully started"))

	# Any code that we want to run only once at the start at server side :-
	# e.g. - Loading trained classification model should be done only once at start of server and not for each POST request


	app.run()
