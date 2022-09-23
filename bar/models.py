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


class Order(models.Model):
    comptoir = models.ForeignKey(to=Bar, on_delete=models.CASCADE, null=True, related_name='order_comptoir')


class OrderItems(models.Model):
    item = models.ForeignKey(to=Reference, on_delete=models.CASCADE, null=True, related_name='orderitems_reference')
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, null=True, related_name='orderitems_order')





# class Order(models.Model):
#     comptoir = models.ForeignKey(to=Bar, on_delete=models.CASCADE, null=True, related_name='order_comptoir')
#     order_items = models.ManyToManyField(to=Reference, blank=True, related_name='order_items')