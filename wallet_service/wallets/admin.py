from django.contrib import admin

from .models import Operation, Wallet


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = (
        'operation_id', 'wallet', 'operation_type', 'amount'
    )


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('wallet_id', 'balance')
