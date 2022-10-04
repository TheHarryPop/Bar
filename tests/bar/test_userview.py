import pytest
from rest_framework.test import APIClient
from django.urls import reverse_lazy


client = APIClient()


@pytest.mark.django_db
def test_registrer_user():
    url = reverse_lazy('signup')
    payload = {'username': 'Quentin', 'password': 'azert123456', 'password2': 'azert123456'}
    response = client.post(url, data=payload)
    data = response.data
    assert data['username'] == payload['username']
    assert response.status_code == 201


@pytest.mark.django_db
def test_login_user(user):
    url = reverse_lazy('login')
    payload = {'username': 'Quentin', 'password': 'azert12345'}
    response = client.post(url, data=payload)
    assert 'access' in response.data
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_user_wrong_password(user):
    url = reverse_lazy('login')
    payload = {'username': 'Quentin', 'password': 'azert'}
    response = client.post(url, data=payload)
    assert 'Aucun compte actif' in response.data['detail']
    assert response.status_code == 401

