"""
Email utility functions for AWT Cargo & Couriers
"""

import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import os

class EmailSender:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.sender_email = os.getenv('SMTP_EMAIL', 'noreply@awtcargo.com')
        self.sender_password = os.getenv('SMTP_PASSWORD', '')
    
    def send_booking_confirmation(self, recipient_email, tracking_number, booking_details):
        """
        Send booking confirmation email
        
        Args:
            recipient_email (str): Customer email address
            tracking_number (str): Generated tracking number
            booking_details (dict): Booking information
        """
        subject = f"Booking Confirmation - Tracking No: {tracking_number}"
        
        # HTML email template
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #0d6efd; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background: #f8f9fa; }}
                .tracking-number {{ font-size: 24px; font-weight: bold; color: #0d6efd; }}
                .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #6c757d; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>AWT Cargo & Couriers</h1>
                    <p>Booking Confirmation</p>
                </div>
                <div class="content">
                    <h2>Your Parcel is Booked!</h2>
                    <p>Dear {booking_details.get('sender_name', 'Customer')},</p>
                    <p>Your parcel has been successfully booked with us. Here are your booking details:</p>
                    
                    <div style="background: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
                        <p><strong>Tracking Number:</strong> <span class="tracking-number">{tracking_number}</span></p>
                        <p><strong>Service Type:</strong> {booking_details.get('service_type', 'Standard').title()}</p>
                        <p><strong>Pickup Address:</strong> {booking_details.get('sender_address', '')}</p>
                        <p><strong>Delivery Address:</strong> {booking_details.get('receiver_address', '')}</p>
                    </div>
                    
                    <p>You can track your parcel using the following link:</p>
                    <p><a href="https://awtcargo.com/tracking?number={tracking_number}" 
                          style="background: #0d6efd; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                        Track Your Parcel
                    </a></p>
                    
                    <p>Thank you for choosing AWT Cargo & Couriers!</p>
                </div>
                <div class="footer">
                    <p>&copy; 2024 AWT Cargo & Couriers Solution Pvt. Ltd. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(recipient_email, subject, html)
    
    def send_status_update(self, recipient_email, tracking_number, status_update):
        """
        Send parcel status update email
        
        Args:
            recipient_email (str): Customer email address
            tracking_number (str): Tracking number
            status_update (dict): Status update information
        """
        subject = f"Parcel Status Update - {tracking_number}"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #198754; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background: #f8f9fa; }}
                .status {{ font-size: 20px; font-weight: bold; color: #198754; }}
                .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #6c757d; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>AWT Cargo & Couriers</h1>
                    <p>Parcel Status Update</p>
                </div>
                <div class="content">
                    <h2>Your Parcel Status Has Been Updated</h2>
                    
                    <div style="background: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
                        <p><strong>Tracking Number:</strong> {tracking_number}</p>
                        <p><strong>Current Status:</strong> <span class="status">{status_update.get('status', '')}</span></p>
                        <p><strong>Location:</strong> {status_update.get('location', '')}</p>
                        <p><strong>Update Time:</strong> {status_update.get('timestamp', '')}</p>
                        <p><strong>Notes:</strong> {status_update.get('notes', '')}</p>
                    </div>
                    
                    <p>Track your parcel for real-time updates:</p>
                    <p><a href="https://awtcargo.com/tracking?number={tracking_number}" 
                          style="background: #198754; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                        View Detailed Tracking
                    </a></p>
                </div>
                <div class="footer">
                    <p>&copy; 2024 AWT Cargo & Couriers Solution Pvt. Ltd. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(recipient_email, subject, html)
    
    def send_partner_welcome(self, recipient_email, partner_details):
        """
        Send partner welcome email
        
        Args:
            recipient_email (str): Partner email address
            partner_details (dict): Partner information
        """
        subject = "Welcome to AWT Cargo Partner Network"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #6f42c1; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background: #f8f9fa; }}
                .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #6c757d; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>AWT Cargo & Couriers</h1>
                    <p>Partner Welcome</p>
                </div>
                <div class="content">
                    <h2>Welcome to Our Partner Network!</h2>
                    <p>Dear {partner_details.get('contact_person', 'Partner')},</p>
                    
                    <p>Thank you for joining the AWT Cargo & Couriers partner network. We're excited to have you on board!</p>
                    
                    <div style="background: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
                        <p><strong>Company:</strong> {partner_details.get('company_name', '')}</p>
                        <p><strong>Service Area:</strong> {partner_details.get('service_area', '')}</p>
                        <p><strong>Business Type:</strong> {partner_details.get('business_type', '').title()}</p>
                    </div>
                    
                    <p>Our team will review your application and contact you within 2 business days to complete the onboarding process.</p>
                    
                    <p>In the meantime, you can explore our partner portal and resources.</p>
                    
                    <p>Best regards,<br>
                    AWT Cargo Partner Team</p>
                </div>
                <div class="footer">
                    <p>&copy; 2024 AWT Cargo & Couriers Solution Pvt. Ltd. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(recipient_email, subject, html)
    
    def send_email(self, recipient_email, subject, html_content):
        """
        Send email using SMTP
        
        Args:
            recipient_email (str): Recipient email address
            subject (str): Email subject
            html_content (str): HTML email content
        
        Returns:
            bool: Success status
        """
        try:
            # Create message
            message = MimeMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = recipient_email
            
            # Create HTML part
            html_part = MimeText(html_content, "html")
            message.attach(html_part)
            
            # Send email (commented out for safety - uncomment in production)
            """
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            """
            
            # For demo purposes, just print the email details
            print(f"Email sent to: {recipient_email}")
            print(f"Subject: {subject}")
            print("Email content generated successfully")
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

# Global instance
email_sender = EmailSender()