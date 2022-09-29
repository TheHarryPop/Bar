import pytest

from rest_framework.test import APIClient
from django.urls import reverse_lazy


url = reverse_lazy('References')


@pytest.mark.django_db
def test_retrieve_ref_auth(api_client_user, ref):
    client = api_client_user
    response = client.get(url)
    assert response.status_code == 200
    assert 'Leffe blonde' == response.data['results'][0]['name']


@pytest.mark.django_db
def test_retreive_ref_no_auth(ref):
    client = APIClient()
    response = client.get(url)
    assert response.status_code == 401
    assert "Informations d'authentification non fournies." in response.data['detail']


@pytest.mark.django_db
def test_post_ref_is_staff(api_client_staff_user):
    client = api_client_staff_user
    response = client.post(url, data={'ref': 'leffeblonde',
                                      'name': 'Leffe blonde',
                                      'description': "Une bière blonde d'abbaye brassée depuis 1240 et que l'on ne "
                                                     "présente plus !"})
    assert response.status_code == 201
    assert 'Leffe blonde' in response.data['name']


@pytest.mark.django_db
def test_post_ref_user(api_client_user):
    client = api_client_user
    response = client.post(url, data={'ref': 'leffeblonde',
                                      'name': 'Leffe blonde',
                                      'description': "Une bière blonde d'abbaye brassée depuis 1240 et que l'on ne "
                                                     "présente plus !"})
    assert response.status_code == 403
    assert "Vous n'avez pas la permission d'effectuer cette action." in response.data['detail']


@pytest.mark.django_db
def test_put_ref_is_staff(api_client_staff_user, ref):
    client = api_client_staff_user
    response = client.put(reverse_lazy('Reference Details', kwargs={'pk': 1}),
                          data={'ref': 'leffeblonde', 'name': 'Leffe de Noël',
                                'description': 'Nouvelle Leffe de Noël'})
    assert response.status_code == 200
    assert 'Noël' in response.data['name']


@pytest.mark.django_db
def test_put_ref_user(api_client_user, ref):
    client = api_client_user
    response = client.put(reverse_lazy('Reference Details', kwargs={'pk': 1}),
                          data={'ref': 'leffeblonde', 'name': 'Leffe de Noël',
                                'description': 'Nouvelle Leffe de Noël'})
    assert response.status_code == 403
    assert "Vous n'avez pas la permission d'effectuer cette action." in response.data['detail']


@pytest.mark.django_db
def test_delete_ref_in_stock(api_client_staff_user, ref, bar, stock):
    client = api_client_staff_user
    response_stock = client.get(reverse_lazy('St'))
    response = client.delete(reverse_lazy('Reference Details', kwargs={'pk': 1}))
    print(response)
    print(response.data)
    assert response.status_code == 200
    assert 'Noël' in response.data['name']
