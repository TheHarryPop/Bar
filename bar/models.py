from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    Manager = 'Manager'
    Barman = 'Barman'

    RoleChoices = (
        (Manager, 'Manager'),
        (Barman, 'Barman'),
    )

    role = models.CharField(max_length=64, choices=RoleChoices, null=False, verbose_name='role')

    # def __str__(self):
    #     return f"User: {self.username} | Role: {self.role}"


class Bar(models.Model):
    name = models.CharField(max_length=150, null=False)

    def __str__(self):
        return self.name


class Reference(models.Model):
    ref = models.CharField(max_length=150, null=False)
    name = models.CharField(max_length=150, null=False)
    description = models.CharField(max_length=150, null=False)
    availability = 'available'

    def __str__(self):
        return self.name


class Stock(models.Model):
    comptoir = models.ForeignKey(to=Bar, on_delete=models.CASCADE, null=True, related_name='stock_comptoir')
    reference = models.ForeignKey(to=Reference, on_delete=models.CASCADE, null=True, related_name='stock_reference')
    stock = models.IntegerField(null=True)

    # class Meta:
    #     unique_together = ('comptoir', 'reference')


class Order(models.Model):
    comptoir = models.ForeignKey(to=Bar, on_delete=models.CASCADE, null=True, related_name='order_comptoir')
    order_items = models.ManyToManyField(to=Reference, blank=True, related_name='order_items')


"""
class Reference(models.Model):
    ref = models.CharField(max_length=150, null=False)
    name = models.CharField(max_length=150, null=False)
    description = models.CharField(max_length=150, null=False)
    availability = 'available'


class StockItems(models.Model):
    reference = models.ManyToManyField(to=Reference, blank=True, related_name='stock_reference')
    quantity = models.IntegerField(null=True)


class Bar(models.Model):
    name = models.CharField(max_length=150, null=False)
    stock_items = models.ForeignKey(to=StockItems, on_delete=models.CASCADE, null=True, related_name='stock_items')


class OrderItems(models.Model):
    reference = models.ManyToManyField(to=Reference, blank=True, related_name='order_reference')


class Order(models.Model):
    order_items = models.ForeignKey(to=OrderItems, on_delete=models.CASCADE, null=False, related_name='order_items')
"""


