from django.db import models

# Create your models here.


class Coins(models.Model):
    name = models.TextField(null=True, blank=True)
    item = models.TextField(max_length=40, null=True, blank=True)
    deposit = models.TextField(blank=True, null=True)
    borrow = models.TextField(blank=True, null=True)
    staking = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "coins"
