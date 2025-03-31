# Testes de admin
from django.contrib.admin.sites import site
from django.contrib import admin
from django.test import TestCase
from ..models import Usuario
from ..admin import UsuarioAdmin


class UsuarioAdminTest(TestCase):
    def setUp(self):
        self.admin = UsuarioAdmin(Usuario, admin.site)

    def test_usuario_admin_registered(self):
        """Testa se o modelo Usuario está registrado no admin"""
        self.assertIn(Usuario, site._registry)
        self.assertIsInstance(site._registry[Usuario], UsuarioAdmin)

    def test_usuario_admin_class(self):
        """Testa se o modelo Usuario está usando a classe UsuarioAdmin"""
        self.assertIsInstance(site._registry[Usuario], UsuarioAdmin)

    def test_list_display(self):
        """Testa se a configuração list_display está correta"""
        self.assertEqual(self.admin.list_display, ('nome', 'email', 'ativo'))

    def test_list_editable(self):
        """Testa se a configuração list_editable está correta"""
        self.assertEqual(self.admin.list_editable, ('email',))

    def test_readonly_fields(self):
        """Testa se a configuração readonly_fields está correta"""
        self.assertEqual(self.admin.readonly_fields, ('senha',))

    def test_search_fields(self):
        """Testa se a configuração search_fields está correta"""
        self.assertEqual(self.admin.search_fields, ('nome', 'email'))

    def test_list_filter(self):
        """Testa se a configuração list_filter está correta"""
        self.assertEqual(self.admin.list_filter, ('ativo',))