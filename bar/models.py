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

    def __str__(self):
        return f"User: {self.username} | Role: {self.role}"


class Bar(models.Model):
    name = models.CharField(max_length=150, null=False)


class Reference(models.Model):
    ref = models.CharField(max_length=150, null=False)
    name = models.CharField(max_length=150, null=False)
    description = models.CharField(max_length=150, null=False)


class OrderItems(models.Model):
    reference = models.ManyToManyField(to=Reference, blank=True, related_name='reference')


class Order(models.Model):
    order_items = models.ForeignKey(to=OrderItems, on_delete=models.CASCADE, null=False, related_name='order_items')



