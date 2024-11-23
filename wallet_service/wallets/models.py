import uuid

from django.db import models

from .constants import (DEC_PLACES, DEF_BALANCE, MAX_DIGITS, NAME_LENGTH,
                        OPERATION_TYPES)


class Wallet(models.Model):
    wallet_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    balance = models.DecimalField(
        max_digits=MAX_DIGITS, decimal_places=DEC_PLACES, default=DEF_BALANCE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['wallet_id'])
        ]

    def __str__(self):
        return f'Кошелек: {self.wallet_id} - Баланс: {self.balance}'


class Operation(models.Model):
    operation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name='operations'
    )
    operation_type = models.CharField(
        max_length=NAME_LENGTH, choices=OPERATION_TYPES
    )
    amount = models.DecimalField(
        max_digits=MAX_DIGITS, decimal_places=DEC_PLACES
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f'Операция {self.operation_id} ({self.operation_type} '
                f'{self.amount})')
