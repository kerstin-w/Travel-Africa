from django.forms import ModelForm, CheckboxInput
from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Post, Comment
from django.core.exceptions import ValidationError


class PostForm(ModelForm):
    """
    Form to create a Blog Post
    """

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "country",
            "featured_image",
            "featured",
            "regions",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Add title here...",
                }
            ),
            "content": SummernoteWidget(),
            "country": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Add the country here...",
                }
            ),
            "featured_image": forms.FileInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "featured": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "region": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }


class CommentForm(forms.ModelForm):
    """
    Form to create a comment
    """

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields["body"].label = False
        self.fields["body"].widget.attrs.update(
            {
                "class": "input-comment form-control light-shadow",
                "placeholder": "Add your comment (maximum of 255 characters)",
                "rows": 3,
            }
        )

    class Meta:
        model = Comment
        fields = ["body"]
