import pytest

from bar.models import User


@pytest.fixture()
def user(db):
    user = User.objects.create_user(username='Quentin', password='azert12345')
    return user
