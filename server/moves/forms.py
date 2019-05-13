from django import forms


class MoveUsersForm(forms.Form):
    user_id = forms.IntegerField()


class MoveVehicleForm(forms.Form):
    vehicle_id = forms.IntegerField()


class MoveDetailsForm(forms.Form):
    departure_from_office = forms.DateTimeField(
        input_formats=['%m/%d/%Y %I:%M %p', ],
        widget=forms.TextInput(attrs={'id': 'dep-at-office'}))
    arrival_at_office = forms.DateTimeField(
        input_formats=['%m/%d/%Y %I:%M %p', ],
        widget=forms.TextInput(attrs={'id': 'arr-at-office'}))
    speedometer_out = forms.FloatField()
    speedometer_in = forms.FloatField()
    fuel_intake = forms.FloatField()


class DelightForm(forms.Form):
    arrival_at_client = forms.DateTimeField(
        input_formats=['%m/%d/%Y %I:%M %p', ])
    departure_from_client = forms.DateTimeField(
        input_formats=['%m/%d/%Y %I:%M %p', ])
    smartness = forms.IntegerField()
    time = forms.IntegerField()
    courtesy = forms.IntegerField()
    creativity = forms.IntegerField()
    explanation = forms.IntegerField()
    willingness = forms.IntegerField()
    leader_competence = forms.IntegerField()
    team_competence = forms.IntegerField()
    care_attention = forms.IntegerField()
    satisfaction = forms.IntegerField()
    comments = forms.CharField(required=False)
    token = forms.CharField()


class MoveTeamLeadForm(forms.Form):
    member_id = forms.IntegerField()
