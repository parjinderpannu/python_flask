from flask import Flask, jsonify, request
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

app.run(port=5000)
