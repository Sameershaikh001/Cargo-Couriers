"""
Rate calculation utilities for AWT Cargo & Couriers
"""

class RateCalculator:
    def __init__(self):
        self.base_rates = {
            'standard': {
                'base': 50.0,
                'per_km': 2.0,
                'per_kg': 8.0,
                'min_charge': 60.0
            },
            'express': {
                'base': 80.0,
                'per_km': 3.0,
                'per_kg': 10.0,
                'min_charge': 100.0
            },
            'same_day': {
                'base': 120.0,
                'per_km': 5.0,
                'per_kg': 12.0,
                'min_charge': 150.0
            }
        }
        
        # Additional charges
        self.additional_charges = {
            'cod_charge': 15.0,  # Cash on delivery charge
            'pickup_charge': 20.0,  # Remote area pickup
            'heavy_charge': 25.0,  # For parcels > 10kg
            'fragile_charge': 30.0  # For fragile items
        }
    
    def calculate_rate(self, weight, distance, service_type, options=None):
        """
        Calculate shipping rate based on weight, distance, and service type
        
        Args:
            weight (float): Parcel weight in kg
            distance (float): Distance in km
            service_type (str): Type of service ('standard', 'express', 'same_day')
            options (dict): Additional options like COD, fragile, etc.
        
        Returns:
            dict: Calculated rate breakdown
        """
        if service_type not in self.base_rates:
            service_type = 'standard'
        
        rates = self.base_rates[service_type]
        
        # Calculate base rate
        base_rate = rates['base']
        distance_charge = distance * rates['per_km']
        weight_charge = weight * rates['per_kg']
        
        # Calculate subtotal
        subtotal = base_rate + distance_charge + weight_charge
        
        # Apply minimum charge
        if subtotal < rates['min_charge']:
            subtotal = rates['min_charge']
        
        # Apply additional charges
        additional_charges = 0
        charge_breakdown = []
        
        if options:
            if options.get('cod'):
                additional_charges += self.additional_charges['cod_charge']
                charge_breakdown.append(('COD Charge', self.additional_charges['cod_charge']))
            
            if options.get('remote_pickup'):
                additional_charges += self.additional_charges['pickup_charge']
                charge_breakdown.append(('Remote Pickup', self.additional_charges['pickup_charge']))
            
            if weight > 10:  # Heavy parcel charge
                additional_charges += self.additional_charges['heavy_charge']
                charge_breakdown.append(('Heavy Parcel', self.additional_charges['heavy_charge']))
            
            if options.get('fragile'):
                additional_charges += self.additional_charges['fragile_charge']
                charge_breakdown.append(('Fragile Handling', self.additional_charges['fragile_charge']))
        
        # Calculate total
        total = subtotal + additional_charges
        
        # GST calculation (18%)
        gst = total * 0.18
        final_total = total + gst
        
        return {
            'base_rate': round(base_rate, 2),
            'distance_charge': round(distance_charge, 2),
            'weight_charge': round(weight_charge, 2),
            'subtotal': round(subtotal, 2),
            'additional_charges': round(additional_charges, 2),
            'charge_breakdown': charge_breakdown,
            'gst': round(gst, 2),
            'total': round(final_total, 2),
            'currency': 'INR'
        }
    
    def get_service_eta(self, service_type, distance):
        """
        Get estimated time of arrival for a service type
        
        Args:
            service_type (str): Type of service
            distance (float): Distance in km
        
        Returns:
            str: Estimated delivery time
        """
        eta_map = {
            'standard': '3-5 business days',
            'express': '1-2 business days', 
            'same_day': 'Same day delivery'
        }
        
        return eta_map.get(service_type, '3-5 business days')
    
    def validate_parameters(self, weight, distance, service_type):
        """
        Validate rate calculation parameters
        
        Args:
            weight (float): Parcel weight
            distance (float): Delivery distance
            service_type (str): Service type
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if weight <= 0:
            return False, "Weight must be greater than 0"
        
        if weight > 50:  # Maximum weight limit
            return False, "Maximum weight limit is 50kg"
        
        if distance <= 0:
            return False, "Distance must be greater than 0"
        
        if distance > 5000:  # Maximum distance limit
            return False, "Maximum distance limit is 5000km"
        
        if service_type not in self.base_rates:
            return False, "Invalid service type"
        
        return True, ""

# Global instance
rate_calculator = RateCalculator()