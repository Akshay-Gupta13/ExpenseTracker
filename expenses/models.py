from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)  # ForeignKey to Category model

    def __str__(self):
        return self.description  # Returning description instead of category

    class Meta:
        ordering = ['-date']  # Fixing the ordering attribute


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
