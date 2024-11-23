import pytest
from rest_framework import status

from .constants import (AMOUNT, BIG_AMOUNT, DEPOSIT, INITIAL_AMOUNT,
                        NEGATIVE_AMOUNT, WITHDRAW, ZERO_AMOUNT)


@pytest.mark.parametrize(
    'operation_type, amount, expected_balance_change',
    (
        (DEPOSIT, AMOUNT, INITIAL_AMOUNT + AMOUNT),
        (WITHDRAW, AMOUNT, INITIAL_AMOUNT - AMOUNT)
    )
)
def test_wallet_operation(operatoin_url, client, wallet, operation_type,
                          amount, expected_balance_change):
    """Проверка операций DEPOSIT и WITHDRAW с кошельком."""
    response = client.post(operatoin_url, {
        'operation_type': operation_type,
        'amount': amount
    }, content_type='application/json')

    assert response.status_code == status.HTTP_202_ACCEPTED
    wallet.refresh_from_db()
    assert wallet.balance == expected_balance_change


@pytest.mark.parametrize(
    'amount, expected_error_message',
    (
        (NEGATIVE_AMOUNT, 'Сумма должна быть больше нуля.'),
        (ZERO_AMOUNT, 'Сумма должна быть больше нуля.')
    )
)
def test_negative_or_zero_amount(operatoin_url, client, amount,
                                 expected_error_message):
    """
    Проверка, что запрос с отрицательной или нулевой суммой
    возвращает ошибку 400 с правильным сообщением.
    """
    response = client.post(operatoin_url, {
        'operation_type': 'DEPOSIT',
        'amount': amount
    }, content_type='application/json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert expected_error_message in response.json()['amount']


def test_withdraw_balance_insufficient_funds(operatoin_url, client, wallet):
    """
    Проверка, что запрос с суммой, превышающей текущий баланс кошелька
    при операции WITHDRAW, возвращает ошибку 400.
    """
    response = client.post(operatoin_url, {
        'operation_type': 'WITHDRAW',
        'amount': BIG_AMOUNT
    }, content_type='application/json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert ('Недостаточно средств для '
            'выполнения операции.' in response.json()['non_field_errors'])


def test_invalid_operation_type(operatoin_url, client):
    """
    Проверка, что запрос с неверным типом операции
    (например, "TRANSFER") возвращает ошибку 400.
    """
    response = client.post(operatoin_url, {
        'operation_type': 'TRANSFER',
        'amount': AMOUNT
    }, content_type='application/json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert ('Тип операции должен быть '
            'DEPOSIT или WITHDRAW.' in response.json()['operation_type'])


@pytest.mark.parametrize(
    'url, expected_status_code',
    (
        (pytest.lazy_fixture('operation_invalid_url'),
         status.HTTP_400_BAD_REQUEST),
        (pytest.lazy_fixture('operation_nonexist_url'),
         status.HTTP_400_BAD_REQUEST)
    )
)
def test_invalid_uuid_format(url, expected_status_code, client):
    """
    Проверка, что запрос с некорректным UUID или с несуществующим UUID
    возвращает ошибку.
    """
    response = client.post(url)

    assert response.status_code == expected_status_code


def test_invalid_json_format(operatoin_url, client):
    """Проверка, что запрос с невалидным JSON возвращает ошибку 400."""
    response = client.post(
        operatoin_url,
        '{"operation_type": "DEPOSIT", "amount": 500',
        content_type='application/json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
