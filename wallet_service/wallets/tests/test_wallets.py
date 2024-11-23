from rest_framework import status


def test_get_wallet_balance(balance_url, client):
    """Тест на получение баланса кошелька."""
    wallet_id = balance_url.split('/')[-2]
    response = client.get(balance_url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['wallet_id'] == wallet_id


def test_get_wallet_balance_invalid_uuid(balance_invalid_url, client):
    """Тест на некорректный формат UUID кошелька."""
    response = client.get(balance_invalid_url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['error'] == 'Неверный формат UUID'


def test_get_wallet_balance_non_existent_wallet(balance_nonexist_url, client):
    """Тест на несуществующий UUID кошелька."""
    response = client.get(balance_nonexist_url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['error'] == 'Кошелек с таким UUID не найден.'
