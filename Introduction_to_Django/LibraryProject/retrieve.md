imported Book from bookshelf.models
Retrieved and displayed all attributes of the book created



`Command line execution`
'from bookshelf.models import Book'

book = Book.objects.get(title="1984")
print(book.title)
print(book.author)
print(book.publication_year)

