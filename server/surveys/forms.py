from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from core.models import Survey, Vehicle


def get_surveyors():
    surveyors = []
    for user in User.objects.filter(groups__name__in=['move_reps']):
        temp = (user.id, user.get_full_name())
        surveyors.append(temp)
    return surveyors


class SurveyForm(forms.ModelForm):
    surveyor = forms.ChoiceField(
        label='Assigned Move Rep',
        widget=forms.Select,
        choices=get_surveyors(),
        required=True)
    vehicle = forms.ModelChoiceField(
        label='Assigned Vehicle',
        widget=forms.Select,
        queryset=Vehicle.objects.all(),
        required=True,
        empty_label='Select Vehicle')
    # survey_time = forms.DateTimeField(
    #     input_formats=['%m/%d/%Y %I:%M %p', ],
    #     widget=forms.TextInput(attrs={'id': 'survey-time'}))

    def clean_surveyor(self):
        surveyor = self.cleaned_data['surveyor']
        user = None
        try:
            user = User.objects.get(pk=surveyor)
        except User.DoesNotExist:
            raise ValidationError('The surveyor selected does not exist')
        if not user:
            raise ValidationError('No surveyor selected')
        return user

    class Meta:
        model = Survey
        fields = '__all__'
        exclude = ('move_time',)


class ChecklistAddNewForm(forms.Form):
    name = forms.CharField()
    office = forms.IntegerField(required=False)
    room_id = forms.IntegerField()
    vol = forms.FloatField()
    qty = forms.IntegerField()


class ChecklistDeleteForm(forms.Form):
    item_id = forms.IntegerField()


class ChecklistEditForm(forms.Form):
    item_id = forms.IntegerField()
    vol = forms.FloatField()
    qty = forms.IntegerField()


class SurveyInstructionsForm(forms.Form):
    special_instructions = forms.CharField()
    access_instructions = forms.CharField()
