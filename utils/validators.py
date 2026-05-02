"""
Validation utilities for AWT Cargo & Couriers
"""

import re
from datetime import datetime

class Validators:
    @staticmethod
    def validate_email(email):
        """
        Validate email address format
        
        Args:
            email (str): Email address to validate
        
        Returns:
            bool: True if valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone):
        """
        Validate Indian phone number format
        
        Args:
            phone (str): Phone number to validate
        
        Returns:
            bool: True if valid, False otherwise
        """
        # Indian phone number pattern (10 digits, optional country code)
        pattern = r'^(\+91[\-\s]?)?[0]?(91)?[6789]\d{9}$'
        return bool(re.match(pattern, phone))
    
    @staticmethod
    def validate_tracking_number(tracking_number):
        """
        Validate tracking number format
        
        Args:
            tracking_number (str): Tracking number to validate
        
        Returns:
            bool: True if valid, False otherwise
        """
        # AWT followed by 8-12 alphanumeric characters
        pattern = r'^AWT[A-Z0-9]{8,12}$'
        return bool(re.match(pattern, tracking_number.upper()))
    
    @staticmethod
    def validate_weight(weight):
        """
        Validate parcel weight
        
        Args:
            weight (float): Weight in kg
        
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            weight_float = float(weight)
            if weight_float <= 0:
                return False, "Weight must be greater than 0"
            if weight_float > 50:  # Maximum weight limit
                return False, "Maximum weight limit is 50kg"
            return True, ""
        except (ValueError, TypeError):
            return False, "Weight must be a valid number"
    
    @staticmethod
    def validate_distance(distance):
        """
        Validate delivery distance
        
        Args:
            distance (float): Distance in km
        
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            distance_float = float(distance)
            if distance_float <= 0:
                return False, "Distance must be greater than 0"
            if distance_float > 5000:  # Maximum distance limit
                return False, "Maximum distance limit is 5000km"
            return True, ""
        except (ValueError, TypeError):
            return False, "Distance must be a valid number"
    
    @staticmethod
    def validate_name(name):
        """
        Validate person name
        
        Args:
            name (str): Name to validate
        
        Returns:
            bool: True if valid, False otherwise
        """
        if not name or len(name.strip()) < 2:
            return False
        # Name should contain only letters, spaces, and common punctuation
        pattern = r'^[a-zA-Z\s\.\-\']+$'
        return bool(re.match(pattern, name.strip()))
    
    @staticmethod
    def validate_address(address):
        """
        Validate address
        
        Args:
            address (str): Address to validate
        
        Returns:
            bool: True if valid, False otherwise
        """
        if not address or len(address.strip()) < 10:
            return False
        return True
    
    @staticmethod
    def validate_pincode(pincode):
        """
        Validate Indian pincode format
        
        Args:
            pincode (str): Pincode to validate
        
        Returns:
            bool: True if valid, False otherwise
        """
        pattern = r'^[1-9][0-9]{5}$'
        return bool(re.match(pattern, str(pincode)))
    
    @staticmethod
    def validate_service_type(service_type):
        """
        Validate service type
        
        Args:
            service_type (str): Service type to validate
        
        Returns:
            bool: True if valid, False otherwise
        """
        valid_types = ['standard', 'express', 'same_day']
        return service_type in valid_types
    
    @staticmethod
    def validate_booking_data(booking_data):
        """
        Validate complete booking data
        
        Args:
            booking_data (dict): Booking form data
        
        Returns:
            tuple: (is_valid, errors)
        """
        errors = {}
        
        # Validate sender details
        if not Validators.validate_name(booking_data.get('sender_name', '')):
            errors['sender_name'] = 'Please enter a valid sender name'
        
        if not Validators.validate_phone(booking_data.get('sender_phone', '')):
            errors['sender_phone'] = 'Please enter a valid phone number'
        
        if not Validators.validate_address(booking_data.get('sender_address', '')):
            errors['sender_address'] = 'Please enter a complete pickup address'
        
        # Validate receiver details
        if not Validators.validate_name(booking_data.get('receiver_name', '')):
            errors['receiver_name'] = 'Please enter a valid receiver name'
        
        if not Validators.validate_phone(booking_data.get('receiver_phone', '')):
            errors['receiver_phone'] = 'Please enter a valid phone number'
        
        if not Validators.validate_address(booking_data.get('receiver_address', '')):
            errors['receiver_address'] = 'Please enter a complete delivery address'
        
        # Validate parcel details
        weight_valid, weight_error = Validators.validate_weight(booking_data.get('weight'))
        if not weight_valid:
            errors['weight'] = weight_error
        
        if not Validators.validate_service_type(booking_data.get('service_type')):
            errors['service_type'] = 'Please select a valid service type'
        
        return len(errors) == 0, errors

# Global instance
validators = Validators()