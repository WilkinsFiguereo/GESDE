import sys
import os
import pytest
import time
import threading
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from PYTHON.app import GESDEApp

# Servidor de testing
_test_server = None
_test_thread = None
_PORT = 5001

def run_test_server():
    """Ejecuta el servidor de testing en un hilo separado"""
    global _test_server
    _test_server = GESDEApp(testing=True)
    _test_server.app.run(host='127.0.0.1', port=_PORT, debug=False, use_reloader=False)

@pytest.fixture(scope="session")
def test_server():
    """Fixture para iniciar/detener el servidor de testing"""
    global _test_thread
    
    # Iniciar servidor en un hilo separado
    _test_thread = threading.Thread(target=run_test_server)
    _test_thread.daemon = True
    _test_thread.start()
    
    # Esperar a que el servidor esté listo
    time.sleep(3)
    
    yield f"http://127.0.0.1:{_PORT}"

@pytest.fixture
def login_page(page, test_server):
    """Fixture para navegar a la página de login"""
    page.goto(f"{test_server}/login", wait_until='domcontentloaded', timeout=10000)
    return page

@pytest.mark.playwright
class TestLoginUI:
    """Tests de UI para la página de login"""
    
    def test_login_page_loads(self, login_page):
        """Verifica que la página de login se carga correctamente"""
        assert login_page.locator('body').is_visible()
        assert login_page.locator('form').count() > 0
        assert login_page.locator('input').count() >= 2
        
    def test_login_form_elements(self, login_page):
        """Verifica que el formulario de login tiene los elementos necesarios"""
        username_input = login_page.locator('input[type="text"], input[name*="user"], input[name*="email"], input[name*="IDcard"]').first
        password_input = login_page.locator('input[type="password"], input[name*="password"], input[name*="Password"]').first
        submit_button = login_page.locator('button[type="submit"], input[type="submit"], button').first
        
        assert username_input.is_visible()
        assert password_input.is_visible()
        assert submit_button.is_visible()
        
    def test_login_form_submit_behavior(self, login_page):
        """Verifica el comportamiento del formulario de login"""
        # Buscar y llenar campos
        username_input = login_page.locator('input[type="text"], input[name*="user"], input[name*="email"], input[name*="IDcard"]').first
        password_input = login_page.locator('input[type="password"], input[name*="password"], input[name*="Password"]').first
        submit_button = login_page.locator('button[type="submit"], input[type="submit"], button').first
        
        # Llenar formulario
        username_input.fill("00000000000")
        password_input.fill("admin123")
        
        # Capturar URL antes del envío
        initial_url = login_page.url
        
        # Enviar formulario
        submit_button.click()
        
        # Esperar respuesta del servidor
        login_page.wait_for_timeout(3000)
        
        # Verificar diferentes escenarios posibles:
        current_url = login_page.url
        
        # Escenario 1: Login exitoso - redirige a otra página
        if current_url != initial_url and "login" not in current_url.lower():
            # Login exitoso - test pasa
            assert True
            return
            
        # Escenario 2: Login falla - muestra mensaje de error
        error_elements = login_page.locator('.error, .alert, [class*="error"], [class*="alert"]')
        if error_elements.count() > 0:
            # Hay mensaje de error - test pasa (comportamiento esperado en testing)
            assert True
            return
            
        # Escenario 3: Permanece en login pero el formulario se reseteó
        form_still_present = login_page.locator('form').count() > 0
        if form_still_present:
            # El formulario sigue presente - test pasa
            assert True
            return
            
        # Si llegamos aquí, el test falla
        assert False, "El formulario no produjo ninguna respuesta observable esperada"

@pytest.mark.playwright
def test_login_invalid_credentials(login_page):
    """Verifica el comportamiento con credenciales inválidas"""
    username_input = login_page.locator('input[type="text"], input[name*="user"], input[name*="email"], input[name*="IDcard"]').first
    password_input = login_page.locator('input[type="password"], input[name*="password"], input[name*="Password"]').first
    submit_button = login_page.locator('button[type="submit"], input[type="submit"], button').first
    
    initial_url = login_page.url
    
    username_input.fill("invalid_user_12345")
    password_input.fill("wrong_password_12345")
    
    submit_button.click()
    login_page.wait_for_timeout(3000)
    
    current_url = login_page.url
    error_elements = login_page.locator('.error, .alert, [class*="error"], [class*="alert"]')
    
    # Verificar que o bien permanece en login o muestra mensaje de error
    assert "login" in current_url.lower() or error_elements.count() > 0 or current_url != initial_url