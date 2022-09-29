import pytest

from rest_framework.test import APIClient
from django.urls import reverse_lazy


url = reverse_lazy('Stock Details', kwargs={'pk': 1})


@pytest.mark.django_db
def test_retrieve_stock_auth(api_client_user, stock):
    client = api_client_user
    response = client.get(url)
    assert response.status_code == 200
    assert 'leffeblonde' == response.data[0]['ref']


@pytest.mark.django_db
def test_retreive_stock_no_auth():
    client = APIClient()
    response = client.get(url)
    assert response.status_code == 401
    assert "Informations d'authentification non fournies." in response.data['detail']
