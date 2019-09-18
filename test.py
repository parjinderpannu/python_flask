def validBookObject(bookObject):
  if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
    return True
  else:
    return False

valid_object = {
    'name': 'Green Eggs and Ham',
    'price': 7.99,
    'isbn': 9780394800165
  }

missing_name = {
    'price': 7.99,
    'isbn': 9780394800165
  }

missing_price = {
    'name': 'Green Eggs and Ham',
    'isbn': 9780394800165
  }

missing_isbn = {
    'name': 'Green Eggs and Ham',
    'price': 7.99
  }

empty_dictionary = {}