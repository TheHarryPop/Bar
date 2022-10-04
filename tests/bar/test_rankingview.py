import pytest

from rest_framework.test import APIClient
from django.urls import reverse_lazy


url_1 = reverse_lazy('Ranking')
url_2 = reverse_lazy('Ranking Orders')


@pytest.mark.django_db
def test_get_ranking_auth(api_client_user, stock):
    client = api_client_user
    response = client.get(url_1)
    assert response.status_code == 200
    assert response.data[0]['name'] == 'all_stock'
    assert response.data[0]['bars'] == [1]


@pytest.mark.django_db
def test_get_ranking_no_auth():
    client = APIClient()
    response = client.get(url_1)
    assert response.status_code == 401
    assert "Informations d'authentification non fournies." in response.data['detail']


@pytest.mark.django_db
def test_get_ranking_orders_auth(api_client_user, order_items):
    client = api_client_user
    response = client.get(url_2)
    assert response.status_code == 200
    assert response.data[0]['name'] == 'most_pints'
    assert response.data[0]['bars'] == [1]


@pytest.mark.django_db
def test_get_ranking_orders_no_auth():
    client = APIClient()
    response = client.get(url_2)
    assert response.status_code == 401
    assert "Informations d'authentification non fournies." in response.data['detail']
