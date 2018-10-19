from .models import Blog
from django import forms
from ckeditor.widgets import CKEditorWidget

class BlogCreateForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = (
            'title',
            'short_description',
            'picture',
            'body',
            'slug'
        )
