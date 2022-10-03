import pytest

from rest_framework.test import APIClient
from django.urls import reverse_lazy


url_1 = reverse_lazy('Orders')
url_2 = reverse_lazy('Order Details', kwargs={'pk': 1})


@pytest.mark.django_db
def test_retrieve_order_details_auth(api_client_user, order_items):
    client = api_client_user
    response = client.get(url_2)
    assert response.status_code == 200
    assert 'Leffe blonde' == response.data['items'][0]['name']


@pytest.mark.django_db
def test_retreive_order_details_no_auth(order_items):
    client = APIClient()
    response = client.get(url_2)
    assert response.status_code == 401
    assert "Informations d'authentification non fournies." in response.data['detail']


@pytest.mark.django_db
def test_post_order_details_auth(api_client_user, ref, bar, stock):
    client = api_client_user
    response = client.post(url_2, data={"items": [{"ref": "leffeblonde"},
                                                  {"ref": "leffeblonde"},
                                                  {"ref": "brewdogipa"}]}, format='json')
    assert response.status_code == 403
    assert "Vous n'avez pas la permission" in response.data['detail']


@pytest.mark.django_db
def test_post_order_details_no_auth(ref, bar, stock):
    client = APIClient()
    response = client.post(url_2, data={"items": [{"ref": "leffeblonde"},
                                                      {"ref": "leffeblonde"},
                                                      {"ref": "brewdogipa"}]}, format='json')
    assert response.status_code == 200
    assert 'Leffe blonde' == response.data['items'][0]['name']


@pytest.mark.django_db
def test_low_stock(ref, bar, stock):
    client = APIClient()
    response = client.post(url_2, data={"items": [{"ref": "leffeblonde"},
                                                  {"ref": "leffeblonde"},
                                                  {"ref": "leffeblonde"},
                                                  {"ref": "leffeblonde"},]}, format='json')
    assert response.status_code == 200
    assert 'Attention, stock Leffe blonde < 2' in response.data[1]
