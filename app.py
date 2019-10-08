from flask import Flask, jsonify, request, Response

from BookModel import *
from settings import *
import json

import jwt, datetime

app.config['SECRET_KEY'] = 'kungfupanda'

@app.route('/login')
def get_token():
  expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
  token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
  return token

#GET /store
@app.route('/books')
def get_books():
  token = request.args.get('token')
  try:
    jwt.decode(token, app.config['SECRET_KEY'])
  except:
    return jsonify({'error': 'Need a valid token to view this page'}), 401
    
  return jsonify({'books': Book.get_all_books()})

def validBookObject(bookObject):
  if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
    return True
  else:
    return False

def valid_put_request_data(bookObject):
  if ("name" in bookObject and "price" in bookObject):
    return True
  else:
    return False

@app.route('/books', methods=['POST'])
def add_book():
  request_data = request.get_json()
  if(validBookObject(request_data)):
    Book.add_book(request_data['name'],request_data['price'],request_data['isbn'])
    response = Response("",201,mimetype='application/json')
    response.headers['Location'] = "/books/" + str(request_data['isbn'])
    return response
  else:
    invalidBookObjectErrorMsg = {
      "error": "Invalid book object passed in request",
      "helpString": "Data passed in similar to this {'name': 'bookname', 'price': 7.34, 'isbn': 123456789123456}"
    }
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
    return response

@app.route ('/books/<int:isbn>')
def get_book_by_isbn(isbn):
  return_value = Book.get_book(isbn)
  return jsonify(return_value)

# PUT /books/123456789
# {
#   'name': 'book name',
#   'price': 1.99
# }

@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
  request_data = request.get_json()
  if(not valid_put_request_data(request_data)):
    invalidBookObjectErrorMsg = {
      "error": "Valid book object must be passed in the request",
      "help": "Data passed in similar to this {'name': 'bookname', 'price': 7.99}"
    }
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
    return response

  Book.replace_book(isbn, request_data['name'], request_data['price'])
  response = Response("", status=204)
  return response

# PATCH /books/9782371000193
# {
#   'name': 'The Cat In The Hat'
# }

# PATCH /books/9782371000193
# {
#   'price': 6.99
# }


@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
  request_data = request.get_json()

  if("name" in request_data):
    Book.update_book_name(isbn, request_data['name'])
  if("price" in request_data):
    Book.update_book_price(isbn, request_data['price'])
  response = Response("", status=204)
  response.headers['Location'] = "/books/" + str(isbn)
  return response

@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
  if(Book.delete_book(isbn)):
    response = Response("", status=204)
    return response
  invalidBookObjectErrorMsg = {
    "error": "Book with ISBN number that was provided was not found, so therefore unable to delete it"
  }
  response = Response(json.dumps(invalidBookObjectErrorMsg), status=404, mimetype='application/json')
  return response


app.run(port=5000)
 