#  COST PROTECTION GUIDE
## Preventing Unexpected API Charges

###  IMPORTANT: API COSTS OVERVIEW

Your emergency response system uses three paid APIs:

1. **OpenAI GPT-3.5-turbo**: ~$0.002 per request
2. **Google Maps API**: ~$0.005 per request (but $200/month free credit)
3. **Twilio Calling**: ~$0.013 per minute (most expensive!)

 **CRITICAL TWILIO WARNING**: Without an emergency address, Twilio charges **$75 per emergency call**! 

 **Emergency Address Protection**: Emergency address has been configured via Twilio Console to prevent these charges.

###  BUILT-IN PROTECTION FEATURES

 **Daily Usage Limits**:
- OpenAI: 50 requests/day max
- Google Maps: 100 requests/day max  
- Twilio: 5 calls/day max, 10 minutes total

 **Demo Mode**: Set `DEMO_MODE=true` to disable all API calls

 **Usage Tracking**: Automatic monitoring in `api_usage.json`

 **Cost Estimation**: Real-time cost calculation

### 🎮 DEMO MODE (RECOMMENDED FOR TESTING)

**Enable Demo Mode** to test without any charges:
```bash
# Update .env file
DEMO_MODE=true

# Or use CLI
python cost_protection_cli.py demo-on
```

In demo mode:
-  No OpenAI API calls (uses fallback responses)
-  No Google Maps API calls (uses mock data)  
-  No Twilio calls (simulates calling)
-  All functionality works for testing

###  MONITORING USAGE

**Check current usage**:
```bash
# CLI method
python cost_protection_cli.py usage

# API method  
curl http://localhost:8000/api-usage
```

**Reset daily counters**:
```bash
python cost_protection_cli.py reset
```

### ⚙️ CUSTOMIZING LIMITS

**Set stricter limits**:
```bash
# Very conservative limits
python cost_protection_cli.py limits --openai 10 --google 20 --twilio-calls 2

# Emergency-only limits
python cost_protection_cli.py limits --openai 5 --google 10 --twilio-calls 1
```

**Update .env file directly**:
```properties
MAX_DAILY_OPENAI_REQUESTS=10
MAX_DAILY_GOOGLE_REQUESTS=20
MAX_DAILY_TWILIO_CALLS=2
MAX_DAILY_TWILIO_MINUTES=5
```

###  COST-SAVING STRATEGIES

1. **Use Demo Mode** for all development and testing
2. **Set conservative daily limits** (start with 5-10 requests)
3. **Monitor usage regularly** with the CLI tool
4. **Only use live mode** for actual demonstrations
5. **Reset counters** if you hit limits accidentally

###  EMERGENCY COST CONTROLS

**If you're worried about charges**:

1. **Immediately enable demo mode**:
   ```bash
   python cost_protection_cli.py demo-on
   ```

2. **Check current usage**:
   ```bash
   python cost_protection_cli.py usage
   ```

3. **Remove API keys temporarily**:
   ```bash
   # Edit .env and comment out keys
   # OPENAI_API_KEY=...
   # GOOGLE_MAPS_API_KEY=...
   # TWILIO_ACCOUNT_SID=...
   ```

### 📱 REAL-TIME MONITORING

**API endpoints for monitoring**:
- `GET /api-usage` - Current usage stats
- `GET /` - System status with cost info
- `POST /enable-demo-mode` - Enable demo mode
- `POST /disable-demo-mode` - Disable demo mode

###  ESTIMATED COSTS

**Conservative daily usage**:
- 10 OpenAI requests: $0.02
- 20 Google Maps requests: $0.10 
- 2 Twilio calls (2 min): $0.05
- **Total per day: ~$0.17**

**Monthly estimate**: ~$5.10 (well within free tiers)

### 🔒 SAFETY GUARDRAILS

The system has multiple safety layers:
1.  Usage tracking before each API call
2.  Daily/monthly limit enforcement  
3.  Demo mode for safe testing
4.  Automatic fallback responses
5.  Real-time cost monitoring

###  QUICK START FOR SAFE TESTING

```bash
# 1. Enable demo mode
python cost_protection_cli.py demo-on

# 2. Start the server  
cd backend && python -m uvicorn app.main:app --reload

# 3. Test everything safely (no charges!)
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "request": "I cut my finger, need help",
    "latitude": "40.7128",
    "longitude": "-74.0060"
  }'

# 4. Monitor usage
python cost_protection_cli.py usage

# 5. Only disable demo mode for real demos
python cost_protection_cli.py demo-off
```

### ❓ FAQ

**Q: How do I know if I'm in demo mode?**
A: Check the API response - it will show `"demo_mode": true`

**Q: What happens if I hit a limit?**
A: API calls are blocked and you get fallback responses

**Q: Can I increase limits temporarily?**
A: Yes, use the CLI or update .env file

**Q: How to completely disable Twilio?**
A: Remove Twilio credentials from .env file

**Q: Is the Google Maps free tier enough?**
A: Yes! You get $200/month credit = 40,000 requests free

###  RECOMMENDED SETTINGS FOR HACKATHON

```properties
# Conservative settings for presentation
DEMO_MODE=false
MAX_DAILY_OPENAI_REQUESTS=20
MAX_DAILY_GOOGLE_REQUESTS=50
MAX_DAILY_TWILIO_CALLS=3
MAX_DAILY_TWILIO_MINUTES=5
```

This gives you enough for demonstrations while preventing runaway costs!

### 🏠 EMERGENCY ADDRESS MANAGEMENT

**Critical**: Twilio charges $75 per call without a registered emergency address!

 **Emergency address configured**: You've successfully added the emergency address through Twilio Console.

**Emergency address details configured**:
- Customer name: Emergency Response System
- Address: 123 Main Street, Boston, MA 02101
- Status:  Active and protecting from $75/call charges

**Backup scripts available** (if needed in future):
```bash
# Emergency address management scripts moved to backup folder
ls emergency_address_backup/
```

 **Your phone number (+17817761348) is protected from $75/call charges!**
