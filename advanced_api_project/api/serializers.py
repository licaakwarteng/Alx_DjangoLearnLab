from rest_framework import serializers
from .models import Author, Book

#creating serializers for models created.
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = 'name'

#Book serializer has a nested serializer for authors
class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author']

    #adding a custom validation to ensure publication date is not in the future.
    def validate(self, book):
        if book['publication_year'] > self['publication_year']:
            raise serializers.ValidationError ("Publication year cannot be in the future.")
        else:
            return book