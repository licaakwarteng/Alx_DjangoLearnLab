from django import forms
from .models import Post, Comment, Tag
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from taggit.forms import TagWidget

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PostForm(forms.ModelForm):
    # Comma-separated tags input
    tags = forms.CharField(
        required=False,
        help_text="Enter comma-separated tags (e.g. django,python,tutorial).",
        widget=forms.TextInput(attrs={'placeholder': 'tag1, tag2, tag3'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'tags': TagWidget(),
        }

    def __init__(self, *args, **kwargs):
        # If editing existing instance, populate tags initial value from instance
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial['tags'] = ', '.join([t.name for t in self.instance.tags.all()])

    def clean_tags(self):
        raw = self.cleaned_data.get('tags', '')
        # Split, strip, remove empties and duplicates, and lower-case (optional)
        tag_names = [t.strip() for t in raw.split(',') if t.strip()]
        # To keep tags case-insensitive but display as typed, we will store them as given
        # but ensure uniqueness
        unique = []
        for t in tag_names:
            if t not in unique:
                unique.append(t)
        return unique

    def save(self, commit=True):
        # Save Post first, then update tags
        post = super().save(commit=commit)
        # cleaned tags is a list of names
        tag_names = self.cleaned_data.get('tags', [])
        if commit:
            # create or get tags, then set on post
            tags = []
            for name in tag_names:
                tag_obj, _ = Tag.objects.get_or_create(name=name)
                tags.append(tag_obj)
            post.tags.set(tags)
        else:
            # If not committing, we still want to attach tags on later save
            # So store them to be handled by caller if needed
            self._pending_tags = tag_names
        return post

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'}),
        max_length=2000,
        label=''
    )

    class Meta:
        model = Comment
        fields = ['content']

    def clean_content(self):
        c = self.cleaned_data.get('content', '').strip()
        if not c:
            raise forms.ValidationError("Comment can't be empty.")
        return c