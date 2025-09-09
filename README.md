# Emergency Accident Response System

A comprehensive AI-powered emergency response system built for the OpenAI Hackathon. This system uses multiple specialized AI agents to handle accident reports, find nearby hospitals, and coordinate emergency responses.

## 🚀 Features

- **Multi-Agent AI Architecture**: Specialized agents for different emergency response tasks
- **Accident Classification**: Automatically classifies accidents as minor or major trauma
- **First Aid Guidance**: Provides immediate first aid instructions
- **Hospital Location**: Finds and ranks nearby hospitals using Google Maps API
- **Emergency Calling**: Automatically contacts hospitals for major trauma cases using Twilio
- **RESTful API**: Easy-to-use REST endpoints for integration

## 🏗️ Architecture

### Core Agents

1. **Accident Response Agent**: Analyzes accident descriptions and provides structured reports with first aid guidance
2. **Hospital Finder Agent**: Locates the best nearby hospitals based on location and accident severity
3. **Contact Agent**: Makes emergency calls to hospitals for major trauma cases
4. **Triage Agent**: Routes cases between agents based on severity and coordinates the response workflow

### Technology Stack

- **Backend**: FastAPI with Python 3.12+
- **AI Framework**: OpenAI Agents library with LiteLLM
- **External APIs**: Google Maps API, Twilio Voice API
- **Data Models**: Pydantic for type safety and validation

## 📋 Prerequisites

- Python 3.12 or higher
- OpenAI API key
- Google Maps API key
- Twilio account (Account SID, Auth Token, Phone Number)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/pranavi79/open-ai-hackathon.git
   cd open-ai-hackathon
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your API keys and credentials
   ```

## ⚙️ Configuration

Create a `.env` file with the following variables:

```env
# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Google Maps API Key for hospital search
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here

# Twilio Configuration for emergency calling
ACCOUNT_SID=your_twilio_account_sid_here
AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_PHONE_NUMBER=your_twilio_phone_number_here

# Ollama Model Configuration
OLLAMA_MODEL=gpt-oss:20b
```

## 🚀 Running the Application

1. **Start the server**
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the API**
   - API Base URL: `http://localhost:8000`
   - Interactive API Documentation: `http://localhost:8000/docs`
   - Alternative API Documentation: `http://localhost:8000/redoc`

## 📡 API Endpoints

### GET `/`
Returns basic information about the API.

**Response:**
```json
{
  "message": "This is your entry into open ai hackathon project"
}
```

### POST `/v1/ask`
Processes an accident report and coordinates emergency response.

**Request Body:**
```json
{
  "request": "I just witnessed a motor accident on the road near Ananta Tech Park in Bangalore. A bike collided with a car at the traffic signal. The rider fell down and has a deep cut on his leg, and he looks like he's bleeding heavily.",
  "longitude": "77.6107",
  "latitude": "12.9345"
}
```

**Response:**
```json
{
  "accident_type": "major trauma",
  "first_aid_tips": "Apply direct pressure to the wound with a clean cloth, elevate the leg if possible, keep the person calm and still.",
  "location": "Ananta Tech Park, Bangalore",
  "details": "Bike-car collision at traffic signal resulting in deep leg cut with heavy bleeding"
}
```

## 🔄 Workflow

1. **User submits accident report** with location coordinates
2. **Accident Response Agent** analyzes the description and classifies severity
3. **Hospital Finder Agent** locates nearby hospitals using Google Maps
4. **Contact Agent** automatically calls hospitals for major trauma cases
5. **System returns** structured accident report with first aid guidance

## 🧪 Testing Individual Agents

Each agent can be tested independently:

```bash
# Test Accident Response Agent
python backend/app/agents/accident_response_agent.py

# Test Hospital Finder Agent  
python backend/app/agents/hospital_finder_agent.py

# Test Contact Agent
python backend/app/agents/contact_agent.py
```

## 📁 Project Structure

```
open-ai-hackathon/
├── backend/
│   └── app/
│       ├── agents/          # AI agents for different tasks
│       ├── core/            # Configuration and settings
│       ├── models/          # Pydantic data models
│       ├── service/         # Business logic services
│       ├── tools/           # External API integration tools
│       ├── guardrails/      # Safety and validation
│       ├── main.py          # FastAPI application entry point
│       └── routes.py        # API route definitions
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Emergency Use Disclaimer

This system is designed as a proof-of-concept for hackathon purposes. For real emergency situations, always contact your local emergency services immediately (911, 112, etc.).

## 🙏 Acknowledgments

- OpenAI for the AI capabilities
- Google Maps API for location services
- Twilio for voice communication services
- FastAPI for the robust web framework