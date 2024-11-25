import logging

from celery import shared_task
from django.db import IntegrityError, transaction
from django.db.utils import OperationalError

from .models import Operation, Wallet

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def process_wallet_operation(self, wallet_id, operation_type, amount):
    try:
        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(
                wallet_id=wallet_id
            )

            if operation_type == 'DEPOSIT':
                wallet.balance += amount
            elif operation_type == 'WITHDRAW':
                wallet.balance -= amount

            wallet.save()
            logger.info(f'Баланс после операции для кошелька '
                        F'{wallet_id}: {wallet.balance}')

            Operation.objects.create(
                wallet=wallet, operation_type=operation_type, amount=amount
            )
            return (
                f'Операция {operation_type} выполнена для кошелька '
                f'{wallet_id}. Баланс: {wallet.balance}'
            )

    except Wallet.DoesNotExist:
        return f'Ошибка: Кошелек с UUID {wallet_id} не найден.'
    except IntegrityError as e:
        return (
            f'Ошибка целостности данных при выполнении операции для '
            f'кошелька {wallet_id}: {str(e)}'
        )
    except OperationalError as e:
        return (
            f'Ошибка подключения к базе данных при обработке '
            f'кошелька {wallet_id}: {str(e)}'
        )
    except Exception as e:
        return (
            f'Неизвестная ошибка при обработке кошелька '
            f'{wallet_id}: {str(e)}'
        )
