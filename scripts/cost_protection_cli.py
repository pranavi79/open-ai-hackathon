#!/usr/bin/env python3
"""
Cost Protection CLI for Emergency Response System
Helps monitor and control API usage to prevent unexpected charges
"""
import json
import os
import sys
from datetime import datetime
import argparse

class CostProtectionCLI:
    def __init__(self):
        self.usage_file = "api_usage.json"
        self.env_file = ".env"
    
    def show_usage(self):
        """Show current API usage statistics"""
        try:
            if os.path.exists(self.usage_file):
                with open(self.usage_file, 'r') as f:
                    data = json.load(f)
                
                today = datetime.now().strftime("%Y-%m-%d")
                month = datetime.now().strftime("%Y-%m")
                
                today_usage = data.get("usage", {}).get(today, {})
                daily_limits = data.get("daily_limits", {})
                
                print("API USAGE REPORT")
                print("=" * 50)
                print(f"Date: {today}")
                print()
                
                # OpenAI Usage
                openai_used = today_usage.get("openai_requests", 0)
                openai_limit = daily_limits.get("openai_requests", 50)
                openai_cost = openai_used * 0.002
                print(f"OpenAI API:")
                print(f"   Used: {openai_used}/{openai_limit} requests")
                print(f"   Cost: ${openai_cost:.4f}")
                print(f"   Status: {'NEAR LIMIT' if openai_used > openai_limit * 0.8 else 'Safe'}")
                print()
                
                # Google Maps Usage
                google_used = today_usage.get("google_maps_requests", 0)
                google_limit = daily_limits.get("google_maps_requests", 100)
                google_cost = google_used * 0.005
                print(f"Google Maps API:")
                print(f"   Used: {google_used}/{google_limit} requests")
                print(f"   Cost: ${google_cost:.4f}")
                print(f"   Status: {'NEAR LIMIT' if google_used > google_limit * 0.8 else 'Safe'}")
                print()
                
                # Twilio Usage
                twilio_calls = today_usage.get("twilio_calls", 0)
                twilio_minutes = today_usage.get("twilio_minutes", 0)
                twilio_call_limit = daily_limits.get("twilio_calls", 5)
                twilio_minute_limit = daily_limits.get("twilio_minutes", 10)
                twilio_cost = twilio_minutes * 0.013
                print(f"Twilio API:")
                print(f"   Calls: {twilio_calls}/{twilio_call_limit}")
                print(f"   Minutes: {twilio_minutes}/{twilio_minute_limit}")
                print(f"   Cost: ${twilio_cost:.4f}")
                print(f"   Status: {'NEAR LIMIT' if twilio_calls > twilio_call_limit * 0.8 else 'Safe'}")
                print()
                
                total_cost = openai_cost + google_cost + twilio_cost
                print(f"TOTAL TODAY'S COST: ${total_cost:.4f}")
                
            else:
                print("No usage data found. System not yet used today.")
                
        except Exception as e:
            print(f"Error reading usage data: {e}")
    
    def enable_demo_mode(self):
        """Enable demo mode to prevent API charges"""
        try:
            self._update_env_var("DEMO_MODE", "true")
            print("Demo mode ENABLED")
            print("No API charges will occur in demo mode")
            print("Restart the server to apply changes")
        except Exception as e:
            print(f"Error enabling demo mode: {e}")
    
    def disable_demo_mode(self):
        """Disable demo mode to enable live API calls"""
        try:
            self._update_env_var("DEMO_MODE", "false")
            print("Demo mode DISABLED")
            print("Live API calls enabled - charges may apply")
            print("Restart the server to apply changes")
        except Exception as e:
            print(f"Error disabling demo mode: {e}")
    
    def set_daily_limits(self, openai=None, google=None, twilio_calls=None, twilio_minutes=None):
        """Set custom daily usage limits"""
        try:
            updates = {}
            if openai is not None:
                updates["MAX_DAILY_OPENAI_REQUESTS"] = str(openai)
            if google is not None:
                updates["MAX_DAILY_GOOGLE_REQUESTS"] = str(google)
            if twilio_calls is not None:
                updates["MAX_DAILY_TWILIO_CALLS"] = str(twilio_calls)
            if twilio_minutes is not None:
                updates["MAX_DAILY_TWILIO_MINUTES"] = str(twilio_minutes)
            
            for key, value in updates.items():
                self._update_env_var(key, value)
            
            print("Daily limits updated:")
            for key, value in updates.items():
                print(f"   {key}: {value}")
            print("Restart the server to apply changes")
            
        except Exception as e:
            print(f"Error setting limits: {e}")
    
    def reset_usage(self):
        """Reset today's usage counters"""
        try:
            if os.path.exists(self.usage_file):
                with open(self.usage_file, 'r') as f:
                    data = json.load(f)
                
                today = datetime.now().strftime("%Y-%m-%d")
                if today in data.get("usage", {}):
                    del data["usage"][today]
                    
                    with open(self.usage_file, 'w') as f:
                        json.dump(data, f, indent=2)
                    
                    print("Today's usage counters reset")
                else:
                    print("No usage data for today to reset")
            else:
                print("No usage file found")
                
        except Exception as e:
            print(f"Error resetting usage: {e}")
    
    def _update_env_var(self, key, value):
        """Update environment variable in .env file"""
        if not os.path.exists(self.env_file):
            print(f".env file not found at {self.env_file}")
            return
        
        # Read current .env content
        with open(self.env_file, 'r') as f:
            lines = f.readlines()
        
        # Update or add the variable
        updated = False
        for i, line in enumerate(lines):
            if line.strip().startswith(f"{key}="):
                lines[i] = f"{key}={value}\n"
                updated = True
                break
        
        if not updated:
            lines.append(f"{key}={value}\n")
        
        # Write back to .env
        with open(self.env_file, 'w') as f:
            f.writelines(lines)

def main():
    parser = argparse.ArgumentParser(description="Cost Protection CLI for Emergency Response System")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Usage command
    subparsers.add_parser('usage', help='Show current API usage and costs')
    
    # Demo mode commands
    subparsers.add_parser('demo-on', help='Enable demo mode (no API charges)')
    subparsers.add_parser('demo-off', help='Disable demo mode (enable live API calls)')
    
    # Limits command
    limits_parser = subparsers.add_parser('limits', help='Set daily usage limits')
    limits_parser.add_argument('--openai', type=int, help='OpenAI daily request limit')
    limits_parser.add_argument('--google', type=int, help='Google Maps daily request limit')
    limits_parser.add_argument('--twilio-calls', type=int, help='Twilio daily call limit')
    limits_parser.add_argument('--twilio-minutes', type=int, help='Twilio daily minute limit')
    
    # Reset command
    subparsers.add_parser('reset', help='Reset today\'s usage counters')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = CostProtectionCLI()
    
    if args.command == 'usage':
        cli.show_usage()
    elif args.command == 'demo-on':
        cli.enable_demo_mode()
    elif args.command == 'demo-off':
        cli.disable_demo_mode()
    elif args.command == 'limits':
        cli.set_daily_limits(
            openai=args.openai,
            google=args.google,
            twilio_calls=args.twilio_calls,
            twilio_minutes=args.twilio_minutes
        )
    elif args.command == 'reset':
        cli.reset_usage()

if __name__ == "__main__":
    main()
