import pytest
import factory

from allauth.account.views import SignupView, LoginView, LogoutView
from django.urls import reverse
from .factories import UserFactory


class TestAllAuthViews:
    @pytest.mark.django_db
    def test_allauth_account_signup_view(self, rf):
        user          = UserFactory()
        request       = rf.post(
                             path  = reverse(
                                       viewname  = 'account_signup'
                                     ),
                             data  = {
                                       'email':      user.email,
                                       'password1':  user.password,
                                       'password2':  user.password,
                                       'name':       user.name,
                                       'username':   user.username,
                                     }
                           )
        request.user  = user
        response      = SignupView.as_view()(request)

        assert response.status_code == 302
        assert response.url == '/users/~redirect/'

        request       = rf.get(
                             path  = reverse(
                                       viewname  = 'account_logout'
                                     )
                           )
        request.user  = user
        response      = LogoutView.as_view()(request)

        assert response.status_code == 200

        request       = rf.post(
                             path  = reverse(
                                       viewname  = 'account_login'
                                     ),
                             data  = {
                                       'username':   user.username,
                                       'password':   user.password,
                                     }
                           )
        request.user  = user
        response      = LoginView.as_view()(request)

        assert response.status_code == 302
        assert response.url == '/users/~redirect/'

    @pytest.mark.django_db
    def test_allauth_account_signup_url(self, client):
        user          = UserFactory()

        client.session['account_verified_email']  = user.email

        response      = client.post(
                                 path  = reverse(
                                           viewname  = 'account_signup'
                                         ),
                                 data  = {
                                           'email':      user.email,
                                           'password1':  user.password,
                                           'password2':  user.password,
                                           'name':       user.name,
                                           'username':   user.username,
                                         }
                               )

        assert response.status_code == 200

        response      = client.get(
                                 path  = reverse(
                                           viewname  = 'account_logout'
                                         )
                               )

        assert response.status_code == 302
        assert response.url == '/'

        response      = client.post(
                                 path  = reverse(
                                           viewname  = 'account_login'
                                         ),
                                 data  = {
                                           'username':   user.username,
                                           'password':   user.password,
                                         }
                               )

        assert response.status_code == 200
