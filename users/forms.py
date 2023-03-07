from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control register'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control register'}))

    class Meta:
        model = Profile
        fields = ('image', 'description')
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control register',
                'rows': 4,
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control register',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].initial = self.instance.user.email
        self.fields['username'].initial = self.instance.user.username
    
    def clean_username(self):
        username = self.cleaned_data['username']
        username_exists = User.objects.filter(username__iexact=username).exclude(pk=self.instance.user.pk).exists()
        if username_exists:
            raise ValidationError('Username already taken')
        return username.capitalize()

    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit=False)
        user = profile.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            profile.save()
            user.save()
        return profile
    






