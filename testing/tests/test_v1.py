from django.contrib.auth.models import User
from django.test import TestCase as DjTestCase

from testing.cases import TestCase


class _TestsMixin(object):
    def go_to_admin(self, name='admin', password='password'):
        User.objects.create_superuser(name, None, password)
        self.client.login(username=name, password=password)
        res = self.client.get('/admin/')
        self.assertNotContains(res, 'this_is_the_login_form')

    def test_v0(self):
        res = self.client.get('/admin/')
        self.assertContains(res, 'this_is_the_login_form')

    def test_v1(self):
        self.go_to_admin()

    def test_v2(self):
        self.go_to_admin()
        self.go_to_admin('admin2')

    def test_v3(self):
        self.go_to_admin()
        self.go_to_admin('admin2')
        self.go_to_admin('admin3')

    def test_v4(self):
        self.go_to_admin()
        self.go_to_admin('admin2')
        self.go_to_admin('admin3')
        self.go_to_admin('admin4')

    def test_v5(self):
        for n in range(10):
            self.go_to_admin('admin' + str(n))


class TestV1(TestCase, _TestsMixin):
    pass


class TestV2(TestCase, _TestsMixin):
    pass


class TestV3(DjTestCase, _TestsMixin):
    pass


class TestV4(DjTestCase, _TestsMixin):
    pass
