from django.db import models

class Registration(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    age = models.IntegerField()
    phone = models.CharField(max_length=10)
    amount = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100,blank=True)
    # razopay_payment_id = models.CharField(max_length=100,blank=True)
    paid = models.BooleanField(default=False)


class Query(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
