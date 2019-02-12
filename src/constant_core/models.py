from django.db import models


class ConstantManager(models.Manager):
    def get_queryset(self):
        return models.QuerySet(self.model, using='constant')


class User(models.Model):
    class Meta:
        db_table = 'users'
        managed = False

    id = models.PositiveIntegerField(primary_key=True)
    updated_at = models.DateTimeField(auto_now=True)
    constant_balance = models.BigIntegerField()

    objects = ConstantManager()


class Reserves(models.Model):
    class Meta:
        db_table = 'reserves'
        managed = False

    id = models.AutoField(primary_key=True)
    user_id = models.PositiveIntegerField()
    status = models.PositiveSmallIntegerField(default=7)
    payment_status = models.PositiveSmallIntegerField(default=0)
    reserve_type = models.PositiveSmallIntegerField(default=2)
    amount = models.BigIntegerField()
    fee = models.BigIntegerField(default=0)
    tx_hash = models.CharField(max_length=10, blank=True)
    wallet_address = models.CharField(max_length=10, blank=True)
    to_user_id = models.PositiveIntegerField()
    ext_request = models.CharField(max_length=10, blank=True)
    ext_response = models.CharField(max_length=10, blank=True)
    ext_error = models.CharField(max_length=10, blank=True)
    ext_id = models.CharField(max_length=10, blank=True)
    ext_status = models.CharField(max_length=10, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ConstantManager()
