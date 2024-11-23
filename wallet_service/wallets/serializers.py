from rest_framework import serializers

from .models import Operation, Wallet


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ('operation_type', 'amount')

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Сумма должна быть больше нуля.')
        return value

    def to_internal_value(self, data):
        try:
            validated_data = super().to_internal_value(data)
        except serializers.ValidationError as exc:
            if 'operation_type' in exc.detail:
                exc.detail['operation_type'] = [
                    'Тип операции должен быть DEPOSIT или WITHDRAW.'
                ]
            raise exc
        return validated_data

    def validate(self, data):
        operation_type = data.get('operation_type')
        amount = data.get('amount')
        wallet_id = self.initial_data.get('wallet_id')
        try:
            wallet = Wallet.objects.get(wallet_id=wallet_id)
        except Wallet.DoesNotExist:
            raise serializers.ValidationError(
                {'wallet_id': f'Кошелек с UUID {wallet_id} не найден.'}
            )

        if operation_type == 'WITHDRAW' and wallet.balance < amount:
            raise serializers.ValidationError(
                'Недостаточно средств для выполнения операции.'
            )
        return data


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('wallet_id', 'balance')
