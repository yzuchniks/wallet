import pytest
from rest_framework import status

from .constants import INITIAL_AMOUNT


@pytest.mark.parametrize(
    'url, expected_status_code, expected_error_message',
    (
        (pytest.lazy_fixture('balance_url'),
         status.HTTP_200_OK, None),
        (pytest.lazy_fixture('balance_invalid_url'),
         status.HTTP_400_BAD_REQUEST, 'Неверный формат UUID'),
        (pytest.lazy_fixture('balance_nonexist_url'),
         status.HTTP_404_NOT_FOUND, 'Кошелек с таким UUID не найден.')
    )
)
def test_get_wallet_balance(
    client,
    url,
    expected_status_code,
    expected_error_message
):
    """Тесты на получение баланса кошелька с различными условиями."""

    response = client.get(url)

    assert response.status_code == expected_status_code

    if expected_error_message:
        assert response.json()['error'] == expected_error_message
    else:
        wallet_id = url.split('/')[-2]
        assert response.data['wallet_id'] == wallet_id
        assert response.data['balance'] == str(INITIAL_AMOUNT)
