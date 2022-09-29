import pytest

from rest_framework.test import APIClient
from django.urls import reverse_lazy


url = reverse_lazy('Bars')


@pytest.mark.django_db
def test_retrieve_bar_auth(api_client_user, bar):
    client = api_client_user
    response = client.get(url)
    assert response.status_code == 200
    assert '1er étage' == response.data['results'][0]['name']


@pytest.mark.django_db
def test_retreive_bar_no_auth(bar):
    client = APIClient()
    response = client.get(url)
    assert response.status_code == 401
    assert "Informations d'authentification non fournies." in response.data['detail']


@pytest.mark.django_db
def test_post_bar_is_staff(api_client_staff_user):
    client = api_client_staff_user
    response = client.post(url, data={'name': '3ème étage'})
    assert response.status_code == 201
    assert '3ème étage' in response.data['name']


@pytest.mark.django_db
def test_post_bar_user(api_client_user):
    client = api_client_user
    response = client.post(url, data={'name': '3ème étage'})
    assert response.status_code == 403
    assert "Vous n'avez pas la permission d'effectuer cette action." in response.data['detail']


@pytest.mark.django_db
def test_put_bar_is_staff(api_client_staff_user, bar):
    client = api_client_staff_user
    response = client.put(reverse_lazy('Bar Details', kwargs={'pk': 1}), data={'name': '4ème étage', 'id': '1'})
    assert response.status_code == 200
    assert '4ème étage' in response.data['name']


@pytest.mark.django_db
def test_put_bar_user(api_client_user, bar):
    client = api_client_user
    response = client.put(reverse_lazy('Bar Details', kwargs={'pk': 1}), data={'name': '4ème étage', 'id': '1'})
    assert response.status_code == 403
    assert "Vous n'avez pas la permission d'effectuer cette action." in response.data['detail']
