from materio.models.auth import User
from django.db import models


class Omborlar(models.Model):
    nomi = models.CharField(max_length=120)
    location = models.CharField(max_length=120)
    xodim_soni = models.IntegerField()
    maxsulot = models.IntegerField()

    def __str__(self):
        return self.nomi


class Maxsulot(models.Model):
    product_name = models.CharField(max_length=128)
    size = models.CharField(max_length=128)
    color = models.CharField(max_length=128)
    joyi = models.CharField(max_length=128)
    product_price = models.IntegerField(default=0)
    product_price_type = models.CharField(max_length=128)
    entry_price = models.IntegerField(default=0)
    entry_price_type = models.CharField(max_length=128)

    def __str__(self):
        return self.product_name


class Basket(models.Model):
    product = models.ForeignKey(Maxsulot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quent = models.IntegerField(default=1)
    price = models.BigIntegerField(default=0)
    price_type = models.CharField(max_length=10)
    status = models.BooleanField(default=True)

    def format(self):
        return {
            "product": self.product.product_name,
            "quent": self.quent,
            "price": self.price,
            "price_type": self.price_type
        }

    def save(self, *args, **kwargs):
        self.price = int(self.product.product_price) * int(self.quent)
        self.price_type = f"{self.product.product_price_type}"

        return super(Basket, self).save(*args, **kwargs)
