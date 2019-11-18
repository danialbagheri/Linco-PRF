
from django import forms
import datetime
from django.forms import ValidationError, ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import (RequestType,
                     ProductionList,
                     ProductionJob)
from customer.models import Address, Customer
from customer.countries import *
from crispy_forms.helper import FormHelper
# SOME CUSTOM VALIDATORS


# def phone_validator(value):
#     if len(str(value)) != 11:
#         raise ValidationError(
#             _('%(value)s is not a valid phone number. Do not use international prefix.'),
#             params={'value': value},
#         )


def passwordMatching(password1, password2):
    if password1 != password2:
        raise ValidationError(
            "the passwords you have entered are not matching, Please try again.")


class AddressForm(ModelForm):
    address_line_1 = forms.CharField(
        label='Address',
        widget=forms.TextInput(attrs={'placeholder': '1234 Main St'})
    )
    address_line_2 = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Area name, office bulding name'}), required=False
    )
    city = forms.CharField()
    country = forms.ChoiceField(choices=COUNTRIES, initial='GB')
    post_code = forms.CharField(label='Post Code')

    class Meta:
        model = Address
        fields = '__all__'


class ProductRequestForm(ModelForm):
    required_date = forms.DateField(required=True, initial=datetime.date.today,widget=forms.DateInput(attrs={
                                     'type': 'date',
                                     'class': ''
                                 }))
    class Meta:
        model = ProductionJob
        fields = {'customer_name', 'request_type', 'required_date',
                  'special_instructions','pallet_type','address_label'}


class CustomerForm(ModelForm):

    class Meta:
        model = Customer
        fields = ('customer_name','sage_customer_id')


class ProductionListForm(ModelForm):
    product = forms.CharField( max_length=200, required=True)
    quantity = forms.IntegerField(required=True)
    mfg_date = forms.DateField(required=False, initial=datetime.date.today,widget=forms.DateInput(attrs={
        'type': 'date',
        'class': ''
    }))
    expiry_date = forms.DateField(required=False, initial=datetime.date.today,widget=forms.DateInput(attrs={
                                     'type': 'date',
                                     'class': ''
                                 }))
    notes = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Any extra information'}), required=False
    )
    class Meta:
        model = ProductionList
        fields = ('product',
        'quantity',
        'mfg_date',
        'expiry_date',
        'notes')
# class CustomSignUpForm(UserCreationForm):
#     first_name = forms.CharField(required=True)
#     last_name = forms.CharField(required=True)
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(
#         label='Password confirmation', widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name',
#                   'email', 'password1', 'password2', )

#     def clean_password2(self):
#         # Check that the two password entries match
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords don't match")
#         return password2


# class UserEditForm(ModelForm):
#     class Meta:
#         model = User
#         fields = (
#             'first_name',
#             'last_name',
#             'email',
#         )
