"""
Test cases for rate calculator
"""

import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.rate_calculator import RateCalculator

class TestRateCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = RateCalculator()
    
    def test_standard_service_calculation(self):
        """Test standard service rate calculation"""
        result = self.calculator.calculate_rate(2.5, 100, 'standard')
        self.assertIn('total', result)
        self.assertGreater(result['total'], 0)
    
    def test_express_service_calculation(self):
        """Test express service rate calculation"""
        result = self.calculator.calculate_rate(2.5, 100, 'express')
        self.assertIn('total', result)
        self.assertGreater(result['total'], 0)
    
    def test_same_day_service_calculation(self):
        """Test same day service rate calculation"""
        result = self.calculator.calculate_rate(2.5, 100, 'same_day')
        self.assertIn('total', result)
        self.assertGreater(result['total'], 0)
    
    def test_minimum_charge(self):
        """Test minimum charge application"""
        # Very small weight and distance to trigger minimum charge
        result = self.calculator.calculate_rate(0.1, 1, 'standard')
        self.assertEqual(result['subtotal'], 60.0)  # Minimum charge for standard
    
    def test_additional_charges(self):
        """Test additional charges calculation"""
        options = {
            'cod': True,
            'fragile': True,
            'remote_pickup': True
        }
        result = self.calculator.calculate_rate(2.5, 100, 'standard', options)
        self.assertGreater(result['additional_charges'], 0)
    
    def test_heavy_parcel_charge(self):
        """Test heavy parcel charge application"""
        result = self.calculator.calculate_rate(15, 100, 'standard')
        self.assertGreater(result['additional_charges'], 0)
    
    def test_gst_calculation(self):
        """Test GST calculation"""
        result = self.calculator.calculate_rate(2.5, 100, 'standard')
        self.assertAlmostEqual(result['gst'], result['subtotal'] * 0.18, places=2)
    
    def test_invalid_service_type(self):
        """Test invalid service type handling"""
        result = self.calculator.calculate_rate(2.5, 100, 'invalid_service')
        self.assertIn('total', result)  # Should default to standard
    
    def test_service_eta(self):
        """Test service ETA retrieval"""
        eta = self.calculator.get_service_eta('standard', 100)
        self.assertIsInstance(eta, str)
        self.assertIn('days', eta)
    
    def test_parameter_validation(self):
        """Test parameter validation"""
        # Valid parameters
        is_valid, message = self.calculator.validate_parameters(2.5, 100, 'standard')
        self.assertTrue(is_valid)
        self.assertEqual(message, "")
        
        # Invalid weight
        is_valid, message = self.calculator.validate_parameters(0, 100, 'standard')
        self.assertFalse(is_valid)
        
        # Invalid distance
        is_valid, message = self.calculator.validate_parameters(2.5, 0, 'standard')
        self.assertFalse(is_valid)
        
        # Invalid service type
        is_valid, message = self.calculator.validate_parameters(2.5, 100, 'invalid')
        self.assertFalse(is_valid)

if __name__ == '__main__':
    unittest.main()