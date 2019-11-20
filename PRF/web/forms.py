
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
from web.models import RequestType, SHRINK_WRAP, PALLET_TYPE
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
    required_date = forms.DateField(label="Required Date",required=True, initial=datetime.date.today,widget=forms.DateInput(attrs={
                                     'type': 'date',
                                     'class': ''
                                 }))
    request_type = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple(attrs={
                                     'class': 'form-check form-check-inline request-type'
                                 }),queryset=RequestType.objects.all())
    customer_address_id = forms.CharField(max_length=10, required=True)
    shrink_wrap = forms.ChoiceField(label="Shrink Wrap",choices=SHRINK_WRAP, required=True)
    pallet_type = forms.ChoiceField(label="Pallet Type",choices=PALLET_TYPE, required=True)
    class Meta:
        model = ProductionJob
        fields = ('customer_name', 'request_type', 'required_date','prf_number','requested_by',
                  'special_instructions','pallet_type','address_label', 'shrink_wrap','customer_address_id')
        labels = {
            'customer_name': 'Customer Name',
            'address_label': 'Do you need an address label?',
        }


class CustomerForm(ModelForm):
    country = forms.ChoiceField(choices=COUNTRIES, initial='GB')
    # customer_name = forms.ModelMultipleChoiceField(label='Customer Name',queryset=Customer.objects.all())
    class Meta:
        model = Customer
        fields = ('customer_name','sage_customer_id',
        'country')
        labels = {
            'customer_name': 'Customer Name',
            'sage_customer_id': 'Sage Customer ID',
        }


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
