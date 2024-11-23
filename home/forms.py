from django import forms
from .models import input_save, Category, Userprofile, Income, Expense, Budget, EMI

# Form for input_save model
class InputSaveForm(forms.ModelForm):
    class Meta:
        model = input_save
        fields = ['name', 'number']

# Form for Category model
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

# Form for Userprofile model
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ['profession', 'savings', 'income', 'pro_pic']

# Form for Income model
class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['category', 'amount', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})  # Customize the date input widget
        }

# Form for Expense model
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})  # Customize the date input widget
        }

# Form for Budget model
class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'total_budget','limit', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),  # Customize the date input widget
            'end_date': forms.DateInput(attrs={'type': 'date'})  # Customize the date input widget
        }

# Form for EMI model
class EMIForm(forms.ModelForm):
    class Meta:
        model = EMI
        fields = ['amount', 'due_date', 'description']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})  # Customize the date input widget
        }
