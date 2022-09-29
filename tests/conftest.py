from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

import pytest

from bar.models import User, Bar, Reference, Stock


@pytest.fixture
def user(db):
    user = User.objects.create_user(username='Quentin', password='azert12345')
    return user


@pytest.fixture
def staff_user(db):
    staff_user = User.objects.create_user(username='admin', password='password', is_staff=True)
    return staff_user


@pytest.fixture
def api_client_user(user):
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    return client


@pytest.fixture
def api_client_staff_user(staff_user):
    client = APIClient()
    refresh = RefreshToken.for_user(staff_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    return client


@pytest.fixture
def bar(db):
    bar_1 = Bar.objects.create(name='1er étage')
    bar_2 = Bar.objects.create(name='2ème étage')
    return bar_1, bar_2


@pytest.fixture
def ref(db):
    ref_1 = Reference.objects.create(ref='leffeblonde',
                                     name='Leffe blonde',
                                     description="Une bière blonde d'abbaye brassée depuis 1240 et que l'on ne "
                                                 "présente plus !")

    ref_2 = Reference.objects.create(ref='brewdogipa',
                                     name='Brewdog Punk IPA',
                                     description="La Punk IPA est une bière écossaise s'inspirant des tendances "
                                                 "américaines en matière de brassage et du choix des houblons")

    ref_3 = Reference.objects.create(ref='fullerindiapale',
                                     name="Fuller's India Pale Ale",
                                     description="Brassée pour l'export, la Fuller's India Pale Ale est la vitrine "
                                                 "du savoir faire bien 'british' de cette brasserie historique")
    return ref_1, ref_2, ref_3


@pytest.fixture
def stock(db):
    bar_1 = Bar.objects.create(name='1er étage')
    ref_1 = Reference.objects.create(ref='leffeblonde',
                                     name='Leffe blonde',
                                     description="Une bière blonde d'abbaye brassée depuis 1240 et que l'on ne "
                                                 "présente plus !")
    stock_1 = Stock.objects.create(stock=5, comptoir=bar_1, reference=ref_1)
    return stock_1
