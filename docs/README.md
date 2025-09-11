# Emergency Response AI System

A comprehensive AI-powered emergency response system that provides instant emergency analysis, hospital location services, and emergency calling capabilities.

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Start in Demo Mode (Recommended)**
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Test the System**
   ```bash
   python tests/test_suite.py
   ```

## 📁 Project Structure

```
emergency-response-ai/
├── backend/
│   └── app/
│       ├── main.py           # FastAPI application
│       ├── routes.py         # All API endpoints
│       ├── services.py       # Business logic
│       ├── models.py         # Data models
│       ├── config.py         # Configuration
│       └── cost_protection.py # Usage tracking
├── scripts/
│   ├── cost_protection_cli.py # Usage monitoring CLI
│   ├── safety_checklist.py   # System validation
│   ├── twilio_setup.py       # Twilio configuration
│   └── start_demo.sh         # Quick start script
├── tests/
│   ├── test_suite.py         # Complete test suite
│   └── test_cost_protection.py # Cost protection tests
├── docs/
│   ├── README.md             # This file
│   ├── SETUP_GUIDE.md        # Detailed setup
│   └── API_DOCUMENTATION.md  # API reference
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
└── .gitignore              # Git ignore rules
```

## 🔧 Configuration

### Required Environment Variables

Create a `.env` file in the root directory:

```env
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here

# Cost Protection (Default: Demo Mode)
DEMO_MODE=true
MAX_DAILY_OPENAI_REQUESTS=50
MAX_DAILY_GOOGLE_REQUESTS=100
MAX_DAILY_TWILIO_CALLS=5
MAX_DAILY_TWILIO_MINUTES=10

# Application Settings
DEBUG=true
```

## 🛡️ Safety Features

- **Demo Mode**: Prevents API charges during development
- **Cost Protection**: Daily usage limits for all APIs
- **Usage Tracking**: Real-time monitoring of API costs
- **Professional Code**: Clean, emoji-free codebase

## 📚 API Endpoints

- `GET /health` - Health check
- `POST /analyze-emergency` - Emergency analysis
- `POST /find-hospitals` - Hospital search
- `POST /contact-emergency` - Emergency calling
- `POST /call-hospital` - Hospital calling
- `GET /api-usage` - Usage statistics
- `POST /demo-mode/enable` - Enable demo mode
- `POST /demo-mode/disable` - Disable demo mode

## 🔧 Management Tools

### Cost Protection CLI
```bash
python scripts/cost_protection_cli.py usage    # Check usage
python scripts/cost_protection_cli.py demo-on  # Enable demo mode
python scripts/cost_protection_cli.py demo-off # Disable demo mode
```

### Safety Checklist
```bash
python scripts/safety_checklist.py  # Validate system
```

### Twilio Setup
```bash
python scripts/twilio_setup.py register  # Register emergency address
python scripts/twilio_setup.py debug     # Debug configuration
```

## 🧪 Testing

Run the complete test suite:
```bash
python tests/test_suite.py
```

Test cost protection:
```bash
python tests/test_cost_protection.py
```

## 🚀 Deployment

For production deployment:

1. Set `DEMO_MODE=false` in .env
2. Register Twilio emergency address
3. Use production ASGI server:
   ```bash
   pip install gunicorn
   gunicorn backend.app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

## 📖 Documentation

- [Setup Guide](docs/SETUP_GUIDE.md) - Detailed setup instructions
- [API Documentation](docs/API_DOCUMENTATION.md) - Complete API reference
- [Cost Protection Guide](docs/COST_PROTECTION.md) - Cost management details

## 🆘 Emergency Services Compliance

⚠️ **Important**: Before using emergency calling features:
1. Register emergency address with Twilio
2. Comply with local emergency services regulations
3. Test in demo mode first

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the documentation in `docs/`
- Run `python scripts/safety_checklist.py` for system validation
- Review logs in the terminal output