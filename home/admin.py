from django.contrib import admin

# Register your models here.
from .models import Category, Expense, Income, EMI, Budget, input_save, Userprofile

admin.site.register(Userprofile)
admin.site.register(Category)
admin.site.register(Expense)
admin.site.register(Income)
admin.site.register(EMI)
admin.site.register(Budget)
admin.site.register(input_save)
