import pytest

from rest_framework.test import APIClient
from django.urls import reverse_lazy
from bar.models import Stock


url_1 = reverse_lazy('References')
url_2 = reverse_lazy('Reference Details', kwargs={'pk': 1})


@pytest.mark.django_db
def test_retrieve_ref_auth(api_client_user, ref):
    client = api_client_user
    response = client.get(url_1)
    assert response.status_code == 200
    assert 'Leffe blonde' == response.data['results'][0]['name']


@pytest.mark.django_db
def test_retreive_ref_no_auth():
    client = APIClient()
    response = client.get(url_1)
    assert response.status_code == 401
    assert "Informations d'authentification non fournies." in response.data['detail']


@pytest.mark.django_db
def test_post_ref_is_staff(api_client_staff_user):
    client = api_client_staff_user
    response = client.post(url_1, data={'ref': 'leffeblonde',
                                        'name': 'Leffe blonde',
                                        'description': "Une bière blonde d'abbaye brassée depuis 1240 et que l'on ne "
                                                       "présente plus !"})
    assert response.status_code == 201
    assert 'Leffe blonde' in response.data['name']


@pytest.mark.django_db
def test_post_ref_user(api_client_user):
    client = api_client_user
    response = client.post(url_1, data={'ref': 'leffeblonde',
                                        'name': 'Leffe blonde',
                                        'description': "Une bière blonde d'abbaye brassée depuis 1240 et que l'on ne "
                                                       "présente plus !"})
    assert response.status_code == 403
    assert "Vous n'avez pas la permission d'effectuer cette action." in response.data['detail']


@pytest.mark.django_db
def test_put_ref_is_staff(api_client_staff_user, ref):
    client = api_client_staff_user
    response = client.put(url_2, data={'ref': 'leffeblonde', 'name': 'Leffe de Noël',
                                       'description': 'Nouvelle Leffe de Noël'})
    assert response.status_code == 200
    assert 'Noël' in response.data['name']


@pytest.mark.django_db
def test_put_ref_user(api_client_user, ref):
    client = api_client_user
    response = client.put(url_2, data={'ref': 'leffeblonde', 'name': 'Leffe de Noël',
                                       'description': 'Nouvelle Leffe de Noël'})
    assert response.status_code == 403
    assert "Vous n'avez pas la permission d'effectuer cette action." in response.data['detail']


@pytest.mark.django_db
def test_delete_ref_in_stock(api_client_staff_user, stock):
    client = api_client_staff_user
    nbr_stock_before_del = Stock.objects.count()
    response = client.delete(url_2)
    nbr_stock_after_del = Stock.objects.count()
    assert response.status_code == 204
    assert (nbr_stock_before_del == nbr_stock_after_del + 2)
