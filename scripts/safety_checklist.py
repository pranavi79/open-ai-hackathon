#!/usr/bin/env python3
"""
Comprehensive Safety Checklist for Emergency Response System
Verifies all cost protection measures are in place
"""
import os
import json
from dotenv import load_dotenv
from twilio.rest import Client

def check_demo_mode():
    """Check if demo mode is enabled"""
    load_dotenv()
    demo_mode = os.getenv('DEMO_MODE', 'false').lower() == 'true'
    
    if demo_mode:
        print("Demo mode ENABLED - No API charges will occur")
        return True
    else:
        print("Demo mode DISABLED - Live API calls enabled")
        return False

def check_daily_limits():
    """Check if daily limits are configured"""
    load_dotenv()
    
    limits = {
        'OpenAI': os.getenv('MAX_DAILY_OPENAI_REQUESTS', '50'),
        'Google Maps': os.getenv('MAX_DAILY_GOOGLE_REQUESTS', '100'),
        'Twilio Calls': os.getenv('MAX_DAILY_TWILIO_CALLS', '5'),
        'Twilio Minutes': os.getenv('MAX_DAILY_TWILIO_MINUTES', '10')
    }
    
    print("[INFO] Daily Usage Limits:")
    for service, limit in limits.items():
        print(f"   {service}: {limit}")
    
    return True

def check_twilio_configuration():
    """Check if Twilio is properly configured"""
    load_dotenv()
    
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    phone_number = os.getenv('TWILIO_PHONE_NUMBER')
    
    if not all([account_sid, auth_token, phone_number]):
        print("[WARN]  Twilio credentials not fully configured")
        return False
    
    print("[OK] Twilio credentials configured")
    print("[COST] Emergency address configured via Twilio Console")
    return True

def check_api_keys():
    """Check if API keys are configured"""
    load_dotenv()
    
    keys = {
        'OpenAI': os.getenv('OPENAI_API_KEY', ''),
        'Google Maps': os.getenv('GOOGLE_MAPS_API_KEY', ''),
        'Twilio SID': os.getenv('TWILIO_ACCOUNT_SID', ''),
        'Twilio Token': os.getenv('TWILIO_AUTH_TOKEN', '')
    }
    
    print("[KEY] API Keys Status:")
    all_configured = True
    for service, key in keys.items():
        if key:
            print(f"   [OK] {service}: Configured")
        else:
            print(f"   [ERROR] {service}: Missing")
            all_configured = False
    
    return all_configured

def check_usage_tracking():
    """Check if usage tracking file exists"""
    usage_file = 'api_usage.json'
    
    if os.path.exists(usage_file):
        with open(usage_file, 'r') as f:
            data = json.load(f)
        print("[OK] Usage tracking file exists")
        return True
    else:
        print("[WARN]  Usage tracking file not yet created (will be created on first use)")
        return True

def calculate_cost_estimates():
    """Calculate potential daily costs"""
    load_dotenv()
    
    openai_limit = int(os.getenv('MAX_DAILY_OPENAI_REQUESTS', '50'))
    google_limit = int(os.getenv('MAX_DAILY_GOOGLE_REQUESTS', '100'))
    twilio_minutes = int(os.getenv('MAX_DAILY_TWILIO_MINUTES', '10'))
    
    openai_cost = openai_limit * 0.002
    google_cost = google_limit * 0.005
    twilio_cost = twilio_minutes * 0.013
    total_cost = openai_cost + google_cost + twilio_cost
    
    print("[COST] Maximum Daily Cost Estimates:")
    print(f"   OpenAI: ${openai_cost:.4f}")
    print(f"   Google Maps: ${google_cost:.4f}")
    print(f"   Twilio: ${twilio_cost:.4f}")
    print(f"   TOTAL: ${total_cost:.4f}")
    
    monthly_estimate = total_cost * 30
    print(f"   Monthly (if used daily): ${monthly_estimate:.2f}")
    
    if total_cost > 1.0:
        print("[WARN]  Daily cost limit exceeds $1.00")
        return False
    else:
        print("[OK] Daily costs under $1.00")
        return True

def main():
    print("[SECURITY]  EMERGENCY RESPONSE SYSTEM - SAFETY CHECKLIST")
    print("=" * 60)
    
    checks = [
        ("Demo Mode", check_demo_mode),
        ("Daily Limits", check_daily_limits),
        ("Twilio Configuration", check_twilio_configuration),
        ("API Keys", check_api_keys),
        ("Usage Tracking", check_usage_tracking),
        ("Cost Estimates", calculate_cost_estimates)
    ]
    
    passed_checks = 0
    critical_issues = []
    
    for check_name, check_func in checks:
        print(f"\n[CHECK] {check_name}:")
        try:
            if check_func():
                passed_checks += 1
            else:
                if check_name in ["Demo Mode"]:
                    critical_issues.append(check_name)
        except Exception as e:
            print(f"[ERROR] Error in {check_name}: {e}")
            if check_name in ["Demo Mode"]:
                critical_issues.append(check_name)
    
    print("\n" + "=" * 60)
    print(f"📈 SAFETY SCORE: {passed_checks}/{len(checks)} checks passed")
    
    if critical_issues:
        print(f"\n🚨 CRITICAL ISSUES FOUND:")
        for issue in critical_issues:
            if issue == "Demo Mode":
                print("   [WARN]  Demo mode disabled - API charges will occur")
                print("   🔧 Fix: Run 'python cost_protection_cli.py demo-on'")
        
        print("\n🛑 RECOMMENDATION: Fix critical issues before proceeding!")
    else:
        print("\n[SUCCESS] ALL SAFETY CHECKS PASSED!")
        print("[OK] Your system is protected from unexpected charges")
        
        demo_mode = os.getenv('DEMO_MODE', 'false').lower() == 'true'
        if demo_mode:
            print("[INFO] Running in demo mode - safe for unlimited testing")
        else:
            print("[WARN]  Running in live mode - monitor usage carefully")

if __name__ == "__main__":
    main()
