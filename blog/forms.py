from django.forms import ModelForm, CheckboxInput
from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Post


class PostForm(ModelForm):
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
                    "class": "form-control",
                }
            ),
        }
