from rest_framework import serializers
from .models import Income,Expense,Category,Budget,EMI
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name']


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Income
        fields=['id','category','amount','date'] 

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Expense
        fields=['id','category','amount','date','description']
        
        
class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model=Budget
        fields=['id','category','total_budget','start_date','end_date','limit']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email','password']
        extra_kwargs={'password':{'write_only':True}}


def create(self,validated_data):
    user=User(**validated_data)
    user.set_password(validated_data['password'])
    user.save()
    return user

class EMISerializer(serializers.ModelSerializer):
    class Meta:
        model=EMI
        fields=['id','amount','due_date','description']
