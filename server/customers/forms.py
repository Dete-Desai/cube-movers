from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from core.models import (
    Source, MoveType, Branch, MoveTypeDetails, Customer)


class CustomerForm(forms.Form):
    source = forms.ModelChoiceField(
        label='Source of Inquiry',
        widget=forms.Select,
        queryset=Source.objects.all(),
        required=True,
        empty_label=None,
        help_text='The source of inquiry is required')
    move_type = forms.ModelChoiceField(
        label='Move Type',
        widget=forms.Select,
        queryset=MoveType.objects.filter(is_active=True),
        required=True,
        empty_label=None,
        help_text='The move type is required')
    move_type_details = forms.ModelChoiceField(
        label='Move Type Details',
        widget=forms.Select,
        queryset=MoveTypeDetails.objects.all(),
        required=True,
        empty_label=None,
        help_text='The move type details is required')
    branch = forms.ModelChoiceField(
        label='Branch',
        widget=forms.Select,
        queryset=Branch.objects.all(),
        required=True,
        empty_label=None,
        help_text='Branch details is required')
    full_name = forms.CharField(
        help_text='Full Name is required',
        widget=forms.TextInput(attrs={'placeholder': 'E.g John Doe'}))
    secondary_name = forms.CharField(required=False)
    phone_number = PhoneNumberField(
        help_text='Phone Number is required',
        widget=forms.TextInput(attrs={'placeholder': 'E.g +25X7XXXXXXXX'}))
    secondary_phone_number = PhoneNumberField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'E.g +25X7XXXXXXXX'}))
    email = forms.EmailField(
        help_text='Email is required',
        widget=forms.TextInput(attrs={'placeholder': 'E.g johndoe@gmail.com'}))
    secondary_email = forms.EmailField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'E.g johndoe2@gmail.com'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        # check if user already has an account
        if User.objects.filter(username=email).exists():
            raise ValidationError('A customer with that email already exists')
        return email


class CustomerEditForm(forms.ModelForm):
    source = forms.ModelChoiceField(
        label='Source of Inquiry',
        widget=forms.Select,
        queryset=Source.objects.all(),
        required=True,
        empty_label=None,
        help_text='The source of inquiry is required')

    class Meta:
        model = Customer
        fields = [
            'full_name', 'secondary_name', 'phone_number', 'secondary_phone_number',
            'source', 'secondary_email']
