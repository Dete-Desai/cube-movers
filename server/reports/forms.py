from django import forms


class MovesReportForm(forms.Form):
    move_status = forms.CharField()
    frequency = forms.CharField()
    from_time = forms.DateTimeField(input_formats=['%d/%m/%Y', ])
    to_time = forms.DateTimeField(input_formats=['%d/%m/%Y', ])
    source = forms.IntegerField()
    move_type = forms.IntegerField()
    move_rep = forms.IntegerField(required=False)
    move_sup = forms.IntegerField(required=False)


class MovesReportComparisonForm(forms.Form):
    move_status_1 = forms.CharField()
    move_status_2 = forms.CharField()
    # frequency = forms.CharField()
    from_time = forms.DateTimeField(input_formats=['%d/%m/%Y', ])
    to_time = forms.DateTimeField(input_formats=['%d/%m/%Y', ])
    # source = forms.IntegerField()
    move_rep = forms.IntegerField(required=False)
    # move_sup = forms.IntegerField(required=False)


class ReportQuotationsPendingForm(forms.Form):
    status = forms.CharField()
    from_time = forms.DateTimeField(input_formats=['%d/%m/%Y', ])
    to_time = forms.DateTimeField(input_formats=['%d/%m/%Y', ])
    move_rep = forms.IntegerField(required=False)


class ReportQuotationsTurnaroundTimeForm(forms.Form):
    from_time = forms.DateTimeField(input_formats=['%d/%m/%Y', ])
    to_time = forms.DateTimeField(input_formats=['%d/%m/%Y', ])
    move_rep = forms.IntegerField(required=False)


class ReportBookingOrdersForm(forms.Form):
    from_time = forms.DateTimeField(input_formats=['%d/%m/%Y', ])
    to_time = forms.DateTimeField(input_formats=['%d/%m/%Y', ])
    move_rep = forms.IntegerField(required=False)


class ReportPersonnelTransportForm(forms.Form):
    from_time = forms.DateTimeField(input_formats=['%d/%m/%Y', ])
    to_time = forms.DateTimeField(input_formats=['%d/%m/%Y', ])
    move_rep = forms.IntegerField(required=False)


class ReportRemovalForm(forms.Form):
    from_time = forms.DateTimeField(input_formats=['%d/%m/%Y', ])
    to_time = forms.DateTimeField(input_formats=['%d/%m/%Y', ])
    move_rep = forms.IntegerField(required=False)


class ReportDelightForm(forms.Form):
    from_time = forms.DateTimeField(input_formats=['%d/%m/%Y', ])
    to_time = forms.DateTimeField(input_formats=['%d/%m/%Y', ])
    move_rep = forms.IntegerField(required=False)
