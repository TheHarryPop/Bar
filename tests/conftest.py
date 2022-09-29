from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

import pytest

from bar.models import User, Bar, Reference, Stock, Order, OrderItems


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
def stock(db, bar, ref):
    stock_1 = Stock.objects.create(stock=5, comptoir=bar[0], reference=ref[0])
    stock_2 = Stock.objects.create(stock=8, comptoir=bar[0], reference=ref[1])
    stock_3 = Stock.objects.create(stock=4, comptoir=bar[0], reference=ref[2])
    stock_4 = Stock.objects.create(stock=5, comptoir=bar[1], reference=ref[0])
    stock_5 = Stock.objects.create(stock=8, comptoir=bar[1], reference=ref[1])
    stock_6 = Stock.objects.create(stock=0, comptoir=bar[1], reference=ref[2])
    return stock_1, stock_2, stock_3, stock_4, stock_5, stock_6


@pytest.fixture
def order(db, bar):
    order_1 = Order.objects.create(comptoir=bar[0])
    order_2 = Order.objects.create(comptoir=bar[1])
    return order_1, order_2


@pytest.fixture
def order_items(db, order, ref):
    order_items_1 = OrderItems.objects.create(item=ref[0], order=order[0])
    order_items_2 = OrderItems.objects.create(item=ref[0], order=order[0])
    order_items_3 = OrderItems.objects.create(item=ref[1], order=order[0])
    order_items_4 = OrderItems.objects.create(item=ref[2], order=order[1])
    order_items_5 = OrderItems.objects.create(item=ref[2], order=order[1])
    return order_items_1, order_items_2, order_items_3, order_items_4, order_items_5
