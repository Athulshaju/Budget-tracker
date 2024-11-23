# filters.py
import django_filters
from .models import Income, Expense, Category
from django import forms

class TransactionFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        label='Category',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    start_date = django_filters.DateFilter(field_name='date', lookup_expr='gte', label='From',
                                           widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    end_date = django_filters.DateFilter(field_name='date', lookup_expr='lte', label='To',
                                         widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = Income  # Use Income as a base model
        fields = ['category', 'start_date', 'end_date']
