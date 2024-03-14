from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)

class Items(models.Model):
    ITEM_TYPE = [
        ("expense", "Expense"),
        ("income", "Income"),
        ("deposit", "Deposit")
    ]
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    amount = models.IntegerField()
    date = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    itemType = models.CharField(max_length=10, choices=ITEM_TYPE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Goals(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    amount = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title


class ProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)    
    income = models.IntegerField(default=0)
    expenses = models.IntegerField(default=0)
    last_transaction_amount = models.IntegerField(default=0)
    last_transaction_type = models.CharField(max_length=10, default="")
    def __str__(self):
        return self.user.username
    
    