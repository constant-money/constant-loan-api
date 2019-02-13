from decimal import Decimal

from django.db import transaction
from django.db.models import F

from constant_core.exceptions import NotEnoughBalanceException
from constant_core.models import User, Reserves


class ConstantCoreBusiness(object):
    @staticmethod
    @transaction.atomic
    def transfer(from_user_id: int, to_user_id: int, amount: Decimal):
        from_user = User.objects.get(id=from_user_id)
        to_user = User.objects.get(id=to_user_id)

        # Convert to constant amount
        int_amount = int('{:.0f}'.format(amount * Decimal(100)))

        if from_user.constant_balance < amount:
            raise NotEnoughBalanceException

        from_user.constant_balance = F('constant_balance') - int_amount
        to_user.constant_balance = F('constant_balance') + int_amount

        from_user.save()
        to_user.save()

        Reserves.objects.create(
            user_id=from_user_id,
            to_user_id=to_user_id,
            amount=int_amount,
        )
