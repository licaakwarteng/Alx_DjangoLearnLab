imported Book from bookshelf.models
Update the title of “1984” to “Nineteen Eighty-Four” and save the changes.


`Command line execution`
'from bookshelf.models import Book'

book = Book.objects.get(title="1984")
book.title="Nineteen Eighty-Four"
book.save()

