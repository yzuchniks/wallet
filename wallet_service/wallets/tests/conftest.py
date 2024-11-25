import pytest
from django.urls import reverse

from wallets.models import Wallet
from .constants import INITIAL_AMOUNT, INVALID_UUID, NON_EXISTENT_UUID


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture()
def wallet():
    wallet = Wallet.objects.create(balance=INITIAL_AMOUNT)
    return wallet


@pytest.fixture
def balance_url(wallet):
    return reverse('wallet-detail',
                   kwargs={'wallet_id': wallet.wallet_id})


@pytest.fixture
def operatoin_url(wallet):
    return reverse('wallet-operation',
                   kwargs={'wallet_id': wallet.wallet_id})


@pytest.fixture
def balance_invalid_url():
    """Возвращает URL с некорректным UUID."""
    return f'/api/v1/wallets/{INVALID_UUID}/'


@pytest.fixture
def balance_nonexist_url():
    """Возвращает URL с валидным, но несуществующим UUID."""
    return f'/api/v1/wallets/{NON_EXISTENT_UUID}/'


@pytest.fixture
def operation_invalid_url():
    """Возвращает URL с некорректным UUID."""
    return f'/api/v1/wallets/{INVALID_UUID}/operation/'


@pytest.fixture
def operation_nonexist_url():
    """Возвращает URL с валидным, но несуществующим UUID."""
    return f'/api/v1/wallets/{NON_EXISTENT_UUID}/operation/'
