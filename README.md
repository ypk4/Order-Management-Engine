# Order-Management-Engine
Order Management Engine in Trade Life Cycle


## A Simple REST API

The API currently accepts JSON from client. On receiving true JSON, it prints the content of JSON at server side and then sends a JSON acknowledgement 'ack' to client with {'success':'true'}.

You need to install [Flask](http://flask.pocoo.org/) and [requests](http://docs.python-requests.org/en/master/):
```
$ pip install flask gevent requests
```

## Starting the Flask server
```
$ python run_keras_server.py 
...
 * Running on http://127.0.0.1:5000
```

You can now access the REST API via `http://127.0.0.1:5000`.


## Submitting requests to the server

Requests can be submitted via cURL from another terminal instance:
```
$ curl  -X POST  -H "Content-Type: application/json"  -d '{"key1":"value1", "key2":"value2"}' 'http://localhost:5000/order_endpoint'  
{
  "success": false
}
```

OR programmatically using python/PHP/any other language:
```
$ python simple_request.py
```
