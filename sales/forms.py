from django import forms

CHART_CHOICES = (
    ('#1', 'Bar Chart'),
    ('#2', 'Pie Chart'),
    ('#3', 'Line Chart'),
)
GROUP_CHOICES = (
    ('#1', 'Sale Date'),
    ('#2', 'Transaction'),
)

class SaleSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    chart_type =forms.ChoiceField(choices=CHART_CHOICES)
    group_by =forms.ChoiceField(choices=GROUP_CHOICES)