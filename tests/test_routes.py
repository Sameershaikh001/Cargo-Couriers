"""
Test cases for AWT Cargo website routes
"""

import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_home_page(self):
        """Test home page loads successfully"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AWT Cargo', response.data)
    
    def test_booking_page(self):
        """Test booking page loads successfully"""
        response = self.app.get('/booking')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Book Courier Service', response.data)
    
    def test_tracking_page(self):
        """Test tracking page loads successfully"""
        response = self.app.get('/tracking')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Track Your Parcel', response.data)
    
    def test_calculator_page(self):
        """Test calculator page loads successfully"""
        response = self.app.get('/calculator')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Rate Calculator', response.data)
    
    def test_services_page(self):
        """Test services page loads successfully"""
        response = self.app.get('/services')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Our Services', response.data)
    
    def test_about_page(self):
        """Test about page loads successfully"""
        response = self.app.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About Us', response.data)
    
    def test_contact_page(self):
        """Test contact page loads successfully"""
        response = self.app.get('/contact')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Contact Us', response.data)
    
    def test_partner_registration_page(self):
        """Test partner registration page loads successfully"""
        response = self.app.get('/partner-registration')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Partner With Us', response.data)

if __name__ == '__main__':
    unittest.main()