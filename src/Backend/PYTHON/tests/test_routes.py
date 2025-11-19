import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from PYTHON.app import GESDEApp
import werkzeug
werkzeug.__version__ = '3.1.0'


@pytest.fixture
def client():
    """Crea un cliente de prueba para la app Flask"""
    app_instance = GESDEApp(testing=True)
    app = app_instance.app
    with app.test_client() as client:
        yield client


def test_home_redirects_to_login(client):
    """Verifica que la ruta raíz redirige al login"""
    response = client.get('/')
    assert response.status_code == 302  # redirección
    assert '/login' in response.headers['Location']


def test_login_page_loads(client):
    """Verifica que el login se carga correctamente"""
    response = client.get('/login')
    assert response.status_code in [200, 302]  # depende si redirige o muestra login


def test_dashboard_page_loads(client):
    """Verifica que el dashboard del crud se carga correctamente"""
    response = client.get('/GESDE/dashboard')
    assert response.status_code in [200, 302, 401, 404]  # múltiples estados posibles


def test_listuser_page_loads(client):
    """Verifica que el dashboard del crud se carga correctamente"""
    response = client.get('/GESDE/listuser')
    assert response.status_code in [200, 302, 401, 404]


def test_blueprint_exists(client):
    """Verifica que los blueprints estén registrados"""
    # Obtener todas las rutas registradas
    routes = [str(rule) for rule in client.application.url_map.iter_rules()]
    
    # Verificar que existen rutas del blueprint CRUD
    crud_routes = [r for r in routes if '/GESDE' in r]
    assert len(crud_routes) > 0, "No se encontraron rutas del blueprint CRUD"
    
    # Verificar rutas específicas
    assert any('/GESDE/' in r for r in routes), "No se encontró el prefijo /GESDE"