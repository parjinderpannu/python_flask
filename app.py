from flask import Flask, jsonify, request, Response
import json
app = Flask(__name__)

books = [
  {
    'name': 'Green Eggs and Ham',
    'price': 7.99,
    'isbn': 9780394800165
  },
  {
    'name': 'The Cat In The Hat',
    'price': 6.99,
    'isbn': 9782371000193
  }
]

#GET /store
@app.route('/books')
def get_books():
  return jsonify({'books': books})

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
    new_book = {
      "name": request_data['name'],
      "price": request_data['price'],
      "isbn": request_data['isbn']
    }
    books.insert(0, new_book)
    response = Response("",201,mimetype='application/json')
    response.headers['Location'] = "/books/" + str(new_book['isbn'])
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
  return_value = {}
  for book in books:
    if book["isbn"] == isbn:
      return_value = {
        'name': book["name"],
        'price': book["price"]
      }
  return jsonify(return_value)

# PUT /books/123456789
# {
#   'name': 'book name',
#   'price': 1.99
# }

# (1) no valid book object from our client
#   --> not add the book to the store

# valid book object has name and price field

# (2) no valid book object

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

  new_book = {
    'name': request_data['name'],
    'price': request_data['price'],
    'isbn': isbn
  }
  i = 0;
  for book in books:
    currentIsbn = book["isbn"]
    if currentIsbn == isbn:
      books[i] = new_book
    i += 1
  response = Response("", status=204)
  return response

app.run(port=5000)
