from django import forms

class PaymentForm(forms.Form):
    amount = forms.DecimalField(label="Amount", min_value=1.00, decimal_places=2)