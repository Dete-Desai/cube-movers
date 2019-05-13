from django import forms
from tinymce.widgets import TinyMCE


class QuoteApprovalForm(forms.Form):
    quote_id = forms.IntegerField()
    hash = forms.CharField()


class QuoteRejectForm(forms.Form):
    move_id = forms.IntegerField()
    reason = forms.CharField()


class QuoteDateForm(forms.Form):
    move_id = forms.IntegerField()
    date = forms.DateTimeField(input_formats=['%m/%d/%Y %I:%M %p', ])


class QuoteItemEditForm(forms.Form):
    quote_id = forms.IntegerField()
    units = forms.IntegerField()
    cost = forms.FloatField()


class QuoteItemDeleteForm(forms.Form):
    quote_id = forms.IntegerField()


class QuoteParametersForm(forms.Form):
    profit_margin = forms.FloatField()
    commission = forms.FloatField()
    vat = forms.FloatField()
    discount = forms.FloatField()


class EditQuoteForm(forms.Form):
    """
    Provides a field that allows for editing a quote
    """
    quote_content = forms.CharField(
        widget=TinyMCE(
            attrs={'cols': 120, 'rows': 30}))
    move = forms.CharField()
