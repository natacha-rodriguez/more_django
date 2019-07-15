from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    """Form class for my Post objects"""

    class Meta:
        model = Post
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ('author', 'text')