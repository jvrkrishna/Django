from django import forms
from decimal import Decimal
from django.core.exceptions import ValidationError
import datetime

class DepositForm(forms.Form):
    amount = forms.DecimalField(min_value=Decimal('0.01'), max_digits=12, decimal_places=2)
    description = forms.CharField(max_length=255, required=False)

    def clean_amount(self):
        amt = self.cleaned_data['amount']
        if amt <= 0:
            raise ValidationError("Amount must be greater than zero.")
        return amt


class WithdrawForm(forms.Form):
    amount = forms.DecimalField(min_value=Decimal('0.01'), max_digits=12, decimal_places=2)
    description = forms.CharField(max_length=255, required=False)

    def clean_amount(self):
        amt = self.cleaned_data['amount']
        if amt <= 0:
            raise ValidationError("Amount must be greater than zero.")
        return amt


class StatementFilterForm(forms.Form):
    choice = forms.ChoiceField(choices=(
        ('month', 'Month'),
        ('year', 'Year'),
        ('range', 'Date range'),
        ('all', 'All'),
    ), required=False, initial='month')
    month = forms.IntegerField(min_value=1, max_value=12, required=False)
    year = forms.IntegerField(min_value=1900, max_value=2100, required=False)
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def clean(self):
        cleaned = super().clean()
        choice = cleaned.get('choice')
        date_from = cleaned.get('date_from')
        date_to = cleaned.get('date_to')

        if choice == 'range' and date_from and date_to and date_from > date_to:
            raise forms.ValidationError("Start date cannot be after end date.")
        return cleaned
