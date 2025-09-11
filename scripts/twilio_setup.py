#!/usr/bin/env python3
"""
Twilio Emergency Setup - Complete Twilio Configuration Tool
Handles emergency address registration, debugging, and fixes
"""
import os
import sys
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import json
import argparse

class TwilioEmergencySetup:
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.phone_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        if not all([self.account_sid, self.auth_token]):
            print("ERROR: Twilio credentials not found in environment variables")
            print("Please set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN in your .env file")
            sys.exit(1)
        
        self.client = Client(self.account_sid, self.auth_token)
    
    def register_emergency_address(self):
        """Register an emergency address for calling services"""
        print("Twilio Emergency Address Registration")
        print("=" * 50)
        print("For legal compliance, you must register an emergency address")
        print("before making emergency calls.\n")
        
        # Get address information
        customer_name = input("Enter customer name: ")
        street = input("Enter street address: ")
        city = input("Enter city: ")
        region = input("Enter state/region: ")
        postal_code = input("Enter ZIP/postal code: ")
        iso_country = input("Enter country code (e.g., US): ").upper()
        
        try:
            # Create emergency address
            address = self.client.addresses.create(
                customer_name=customer_name,
                street=street,
                city=city,
                region=region,
                postal_code=postal_code,
                iso_country=iso_country,
                emergency_enabled=True
            )
            
            print(f"\nSUCCESS: Emergency address registered!")
            print(f"Address SID: {address.sid}")
            print(f"Address: {address.street}, {address.city}, {address.region} {address.postal_code}")
            
            # Save address info
            self._save_address_info(address)
            
            return address
            
        except TwilioRestException as e:
            print(f"ERROR: Failed to register emergency address")
            print(f"Error code: {e.code}")
            print(f"Error message: {e.msg}")
            return None
    
    def list_emergency_addresses(self):
        """List all registered emergency addresses"""
        try:
            addresses = self.client.addresses.list(limit=20)
            
            if not addresses:
                print("No emergency addresses found")
                return
            
            print("Registered Emergency Addresses:")
            print("=" * 50)
            
            for address in addresses:
                print(f"SID: {address.sid}")
                print(f"Name: {address.customer_name}")
                print(f"Address: {address.street}, {address.city}, {address.region} {address.postal_code}")
                print(f"Emergency Enabled: {address.emergency_enabled}")
                print("-" * 30)
                
        except TwilioRestException as e:
            print(f"ERROR: Failed to list addresses")
            print(f"Error: {e.msg}")
    
    def debug_twilio_setup(self):
        """Debug Twilio configuration and test connectivity"""
        print("Twilio Configuration Debug")
        print("=" * 50)
        
        # Check credentials
        print("1. Checking credentials...")
        if self.account_sid and self.auth_token:
            print("   Credentials found in environment")
        else:
            print("   ERROR: Missing credentials")
            return
        
        # Test connection
        print("2. Testing Twilio connection...")
        try:
            account = self.client.api.accounts(self.account_sid).fetch()
            print(f"   Connected to account: {account.friendly_name}")
            print(f"   Account status: {account.status}")
        except Exception as e:
            print(f"   ERROR: Connection failed - {e}")
            return
        
        # Check phone numbers
        print("3. Checking phone numbers...")
        try:
            phone_numbers = self.client.incoming_phone_numbers.list(limit=10)
            if phone_numbers:
                print(f"   Found {len(phone_numbers)} phone number(s):")
                for number in phone_numbers:
                    print(f"     {number.phone_number} - {number.friendly_name}")
            else:
                print("   No phone numbers found")
        except Exception as e:
            print(f"   ERROR: Failed to get phone numbers - {e}")
        
        # Check emergency addresses
        print("4. Checking emergency addresses...")
        try:
            addresses = self.client.addresses.list(limit=5)
            if addresses:
                print(f"   Found {len(addresses)} emergency address(es):")
                for addr in addresses:
                    print(f"     {addr.customer_name} - {addr.city}, {addr.region}")
            else:
                print("   No emergency addresses found")
                print("   WARNING: You need to register an emergency address for calling")
        except Exception as e:
            print(f"   ERROR: Failed to get addresses - {e}")
        
        # Check account balance
        print("5. Checking account balance...")
        try:
            balance = self.client.api.accounts(self.account_sid).balance.fetch()
            print(f"   Account balance: {balance.balance} {balance.currency}")
        except Exception as e:
            print(f"   ERROR: Failed to get balance - {e}")
        
        print("\nDebug complete!")
    
    def fix_emergency_address(self):
        """Fix or update emergency address configuration"""
        print("Emergency Address Fix Tool")
        print("=" * 50)
        
        # List current addresses
        self.list_emergency_addresses()
        
        print("\nWhat would you like to do?")
        print("1. Update existing address")
        print("2. Delete address")
        print("3. Add new address")
        
        choice = input("Enter choice (1-3): ")
        
        if choice == "1":
            self._update_address()
        elif choice == "2":
            self._delete_address()
        elif choice == "3":
            self.register_emergency_address()
        else:
            print("Invalid choice")
    
    def _update_address(self):
        """Update an existing emergency address"""
        address_sid = input("Enter Address SID to update: ")
        
        try:
            # Get current address
            address = self.client.addresses(address_sid).fetch()
            print(f"Current address: {address.street}, {address.city}, {address.region}")
            
            # Get new information (press enter to keep current)
            street = input(f"New street ({address.street}): ") or address.street
            city = input(f"New city ({address.city}): ") or address.city
            region = input(f"New region ({address.region}): ") or address.region
            postal_code = input(f"New postal code ({address.postal_code}): ") or address.postal_code
            
            # Update address
            updated_address = self.client.addresses(address_sid).update(
                street=street,
                city=city,
                region=region,
                postal_code=postal_code
            )
            
            print("Address updated successfully!")
            
        except TwilioRestException as e:
            print(f"ERROR: Failed to update address - {e.msg}")
    
    def _delete_address(self):
        """Delete an emergency address"""
        address_sid = input("Enter Address SID to delete: ")
        
        try:
            self.client.addresses(address_sid).delete()
            print("Address deleted successfully!")
            
        except TwilioRestException as e:
            print(f"ERROR: Failed to delete address - {e.msg}")
    
    def _save_address_info(self, address):
        """Save address information to backup file"""
        try:
            address_data = {
                "sid": address.sid,
                "customer_name": address.customer_name,
                "street": address.street,
                "city": address.city,
                "region": address.region,
                "postal_code": address.postal_code,
                "iso_country": address.iso_country,
                "created": str(address.date_created)
            }
            
            # Save to backup file
            os.makedirs("emergency_address_backup", exist_ok=True)
            with open("emergency_address_backup/address_backup.json", "w") as f:
                json.dump(address_data, f, indent=2)
            
            print(f"Address information saved to emergency_address_backup/address_backup.json")
            
        except Exception as e:
            print(f"Warning: Could not save address backup - {e}")

def main():
    parser = argparse.ArgumentParser(description="Twilio Emergency Setup Tool")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Register command
    subparsers.add_parser('register', help='Register new emergency address')
    
    # List command
    subparsers.add_parser('list', help='List all emergency addresses')
    
    # Debug command
    subparsers.add_parser('debug', help='Debug Twilio configuration')
    
    # Fix command
    subparsers.add_parser('fix', help='Fix or update emergency addresses')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    setup = TwilioEmergencySetup()
    
    if args.command == 'register':
        setup.register_emergency_address()
    elif args.command == 'list':
        setup.list_emergency_addresses()
    elif args.command == 'debug':
        setup.debug_twilio_setup()
    elif args.command == 'fix':
        setup.fix_emergency_address()

if __name__ == "__main__":
    main()
