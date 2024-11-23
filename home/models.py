from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class input_save(models.Model):
    name=models.CharField(max_length=50)
    number=models.CharField(max_length=50)


class Category(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class Userprofile(models.Model):
    user=models.OneToOneField(User ,on_delete=models.CASCADE)
    profession=models.CharField(max_length=100,blank=True)
    savings=models.IntegerField(null=True,blank=True)
    income=models.BigIntegerField(null=True,blank=True)
    pro_pic=models.ImageField(default='default.jpg',upload_to="pro_image",blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    



class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(null=True, blank=True)
    



class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    total_budget = models.DecimalField(max_digits=10, decimal_places=2)
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField() 
    def __str__(self):
        return f"{self.user.username}'s budget: {self.total_budget} from {self.start_date} to {self.end_date}"



class EMI(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'EMI of {self.amount} due on {self.due_date}'