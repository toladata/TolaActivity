from django.utils import timezone
from factory import DjangoModelFactory,  SubFactory

from oauth2_provider.models import (
    Application as ApplicationM,
    Grant as GrantM
)
from .django_models import User


class Application(DjangoModelFactory):
    class Meta:
        model = ApplicationM

    client_id = 'CXGVOGFnTAt5cQW6m5AxbGrRq1lzKNSrou31dWm9'
    user = SubFactory(User)
    client_type = 'confidential'
    authorization_grant_type = 'authorization-code'
    client_secret = 'TOkNUHXShMasJzmY6aLeTey49lFvqHOcIQAhZMrc9Ax1gkSo6MUxjdRnXzfEghCwSROlj2bG6I5ksZ2D6QrYipETOqIDcrZKSm7h0wNfurxqzbIxr1F1tFbeeipkHRVC'
    name = 'TolaActivity'
    skip_authorization = False
    redirect_uris = 'http://testserver'


class Grant(DjangoModelFactory):
    class Meta:
        model = GrantM

    user = SubFactory(User)
    code = 'stRZ5ctBN8BUlZUTmRGK1EqIgs242K'
    application = SubFactory(Application)
    scope = 'read write'
    expires = timezone.now() + timezone.timedelta(days=1)
    redirect_uri = 'http://testserver'

