imported Book from bookshelf.models
Created a Book instance called book1
output book1



`Command line execution`
'from bookshelf.models import Book'

book1 = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book1)

