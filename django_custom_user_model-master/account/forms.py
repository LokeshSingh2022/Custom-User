from dataclasses import fields
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *
from django.forms import ModelForm

class BookDetails(ModelForm):
    title = forms.CharField(max_length=200)
    Author = forms.CharField(max_length=200)
    Price = forms.IntegerField()
    Edition = forms.IntegerField()
    class Meta:
        model = Book
        fields = ['title','Author','Price','Edition']
class CustomerDetails(ModelForm):
    name=forms.CharField(max_length=200)
    phone=forms.CharField(max_length=200)
    email=forms.CharField(max_length=100)
    class Meta:
        model = Customer
        fields = ['name','phone','email']

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'date_of_birth')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'date_of_birth',
                  'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


