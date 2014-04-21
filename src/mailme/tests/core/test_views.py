import pytest

from mailme.tests.factories.core import UserFactory


@pytest.mark.django_db
class TestLogoutView:
    def test_logout_not_logged_in(self, client):
        response = client.get('/logout/')
        assert response.status_code == 302
        assert response['Location'] == 'http://testserver/'
        assert '_auth_user_id' not in client.session

    def test_logout_logged_in(self, client):
        user = UserFactory.create()
        client.login(username=user.username, password='secret')
        assert '_auth_user_id' in client.session  # ensure login was successful

        response = client.get('/logout/')
        assert response.status_code == 302
        assert response['Location'] == 'http://testserver/'
        assert '_auth_user_id' not in client.session
