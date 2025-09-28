from rest_framework import serializers
from .models import Author, Book
import datetime

# serializer for the book model
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title", "publication_year", "author"]

    def validate_publication_year(self, value):
        """
        Ensure the publication year is not in the future.
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

# serializer for the Author model
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ["id","name", "books"]


