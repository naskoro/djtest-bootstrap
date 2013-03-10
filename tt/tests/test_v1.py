from django.contrib.auth.models import User
#from django.test import TestCase

from tt.cases import TestCase


class TestV1(TestCase):
    def go_to_admin(self, name='admin', password='password'):
        User.objects.create_superuser(name, None, password)
        self.client.login(username=name, password=password)
        res = self.client.get('/admin/')
        self.assertNotContains(res, 'this_is_the_login_form')

    def test_v0(self):
        res = self.client.get('/admin/')
        self.assertContains(res, 'this_is_the_login_form')

    #@_statprof
    def test_v1(self):
        self.go_to_admin()

    #@_statprof
    def test_v2(self):
        self.go_to_admin()
        self.go_to_admin('admin2')

    #@_statprof
    def test_v3(self):
        self.go_to_admin()
        self.go_to_admin('admin2')
        self.go_to_admin('admin3')

    #@_statprof
    def test_v4(self):
        self.go_to_admin()
        self.go_to_admin('admin2')
        self.go_to_admin('admin3')
        self.go_to_admin('admin4')


class TestV2(TestCase):
    def setUp(self):
        name, password = 'admin', 'password'
        User.objects.create_superuser(name, None, password)
        self.client.login(username=name, password=password)

    def go_to_admin(self, ):
        res = self.client.get('/admin/')
        self.assertNotContains(res, 'this_is_the_login_form')

    def test_v0(self):
        self.go_to_admin()

    def test_v1(self):
        self.go_to_admin()

    def test_v2(self):
        self.go_to_admin()
        self.go_to_admin()
        self.go_to_admin()

    def test_v3(self):
        self.go_to_admin()
        self.go_to_admin()
        self.go_to_admin()
        self.go_to_admin()

    def test_v4(self):
        self.go_to_admin()
        self.go_to_admin()
        self.go_to_admin()
        self.go_to_admin()
        self.go_to_admin()


class TestV3(TestCase):
    def create_superuser(self, name='admin', password='password'):
        User.objects.create_superuser(name, None, password)
        self.client.login(username=name, password=password)

    def test_v0(self):
        self.create_superuser()

    def test_v1(self):
        self.create_superuser()
        self.create_superuser('admin2')

    def test_v2(self):
        self.create_superuser()
        self.create_superuser('admin2')
        self.create_superuser('admin3')

    def test_v3(self):
        self.create_superuser()
        self.create_superuser('admin2')
        self.create_superuser('admin3')
        self.create_superuser('admin4')

    def test_v4(self):
        self.create_superuser()
        self.create_superuser('admin2')
        self.create_superuser('admin3')
        self.create_superuser('admin4')
        self.create_superuser('admin5')
