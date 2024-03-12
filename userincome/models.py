from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class UserIncome(models.Model):
    amount = models.FloatField()  # DECIMAL
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.ForeignKey('Source', on_delete=models.CASCADE)  # ForeignKey to Source model

    def __str__(self):
        return self.source

    class Meta:
        ordering = ['-date']  # Fixing the ordering attribute


class Source(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
