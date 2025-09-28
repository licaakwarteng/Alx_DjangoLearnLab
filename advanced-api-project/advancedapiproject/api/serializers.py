from rest_framework import serializers
from .models import Author, Book

# serializer for the Author model
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "name"

# serializer for the book model
class BookSerializer(serializers.ModelSerializer):
    # author = AuthorSerializer()

    def validate(self, data):
        if data['publication_year'] > self['publication_year']:
            raise serializers.ValidationError("Publication date cannot be a future date")
        else:
            return data
