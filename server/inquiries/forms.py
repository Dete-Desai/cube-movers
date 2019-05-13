from django import forms
from core.models import MoveType, PropertyDetails


class NewCustomerInquiryForm(forms.Form):
    move_type = forms.ModelChoiceField(
        label='Move Type',
        widget=forms.Select,
        queryset=MoveType.objects.filter(is_active=True)
    )


class InquiryDetailsForm(forms.Form):
    primary_area_name = forms.CharField()
    secondary_area_name = forms.CharField()
    street_name = forms.CharField()
    secondary_street_name = forms.CharField()
    gate_color = forms.CharField()
    compound_name = forms.CharField()
    house_no = forms.CharField()
    floor = forms.CharField()
    land_marks = forms.CharField()
    side_of_road = forms.CharField()
    survey_time = forms.DateTimeField(input_formats=['%m/%d/%Y %I:%M %p', ])
    move_time = forms.DateTimeField(input_formats=['%m/%d/%Y %I:%M %p', ])


class PropertyDetailsForm(forms.ModelForm):

    class Meta:
        model = PropertyDetails
        fields = '__all__'
