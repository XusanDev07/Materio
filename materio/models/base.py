from django.db import models

class Omborlar(models.Model):
    nomi = models.CharField(max_length=120)
    location = models.CharField(max_length=120)
    employee = models.CharField(max_length=120)
    product = models.CharField(max_length=120)

    def __str__(self):
        return self.nomi


class Products(models.Model):
    pr_name = models.CharField(max_length=120)
    pr_size = models.CharField(max_length=120)
    pr_num = models.IntegerField()
    pr_color = models.CharField(max_length=120)
    price = models.IntegerField()
    total_price = models.IntegerField()

    def __str__(self):
        return self.pr_name
