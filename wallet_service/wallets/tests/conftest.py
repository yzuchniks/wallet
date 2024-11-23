import pytest
from django.urls import reverse
from wallets.models import Wallet


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture()
def wallet():
    wallet = Wallet.objects.create(balance=1000)
    return wallet


@pytest.fixture
def balance_url(wallet):
    return reverse('wallet-detail',
                   kwargs={'wallet_id': wallet.wallet_id})


@pytest.fixture
def balance_invalid_url():
    """Возвращает URL с некорректным UUID."""
    invalid_uuid = '1234-invalid-uuid-5678'
    return f'/api/v1/wallets/{invalid_uuid}/'


@pytest.fixture
def balance_nonexist_url():
    """Возвращает URL с валидным, но несуществующим UUID."""
    non_existent_uuid = '11111111-1111-1111-1111-111111111111'
    return f'/api/v1/wallets/{non_existent_uuid}/'
