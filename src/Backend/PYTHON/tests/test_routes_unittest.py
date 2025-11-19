import sys
import os
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from PYTHON.app import GESDEApp


class TestGESDEApp(unittest.TestCase):
    
    def setUp(self):
        self.app_instance = GESDEApp(testing=True)
        self.app = self.app_instance.app
        self.client = self.app.test_client()
    
    def test_blueprint_registration(self):
        """Verifica que los blueprints estén registrados correctamente"""
        registered_blueprints = list(self.app.blueprints.keys())
        
        # Verificar blueprints esenciales
        essential_blueprints = ['login', 'dashboard', 'homepage', 'crud']
        for bp_name in essential_blueprints:
            self.assertIn(bp_name, registered_blueprints, 
                         f"Blueprint esencial '{bp_name}' no encontrado")
    
    def test_home_redirect(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)
    
    def test_login_accessible(self):
        response = self.client.get('/login')
        self.assertIn(response.status_code, [200, 302])
    
    def test_gesde_routes_exist(self):
        """Verifica que las rutas con prefijo /GESDE existen"""
        routes = [str(rule) for rule in self.app.url_map.iter_rules()]
        gesde_routes = [r for r in routes if '/GESDE' in r]
        self.assertTrue(len(gesde_routes) > 0, "No hay rutas con prefijo /GESDE")


if __name__ == '__main__':
    unittest.main()