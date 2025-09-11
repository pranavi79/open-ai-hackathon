# Emergency Response AI System - Frontend Demo

This is a simple web interface to test and demonstrate all the API endpoints of the Emergency Response AI System built for the hackathon.

## Features

- **Clean UI**: Modern, responsive design showcasing all 9 API endpoints
- **Live Testing**: Interactive forms to test each endpoint with real data
- **Real-time Status**: API health monitoring and system status display
- **Demo Mode**: Works with demo data when API keys are not configured
- **Cost Protection**: Shows current usage and billing protection status

## How to Use

1. **Start the Backend Server**:
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload
   ```

2. **Open the Frontend**:
   - Simply open `index.html` in your web browser
   - Or serve it with a simple HTTP server:
   ```bash
   cd frontend
   python -m http.server 8080
   # Then open http://localhost:8080
   ```

## Available Endpoints to Test

1. **Health Check** - Verify API is running
2. **Emergency Analysis** - AI-powered emergency assessment
3. **Hospital Search** - Find nearby hospitals by location
4. **Emergency Call** - Initiate emergency calls (demo mode)
5. **Voice to Text** - Convert voice to text (demo simulation)
6. **Cost Protection** - Check API usage and billing limits
7. **Demo Mode** - Toggle demo mode on/off
8. **System Status** - Comprehensive system information
9. **Test Endpoint** - Simple connectivity test

## Demo Data

The interface comes pre-loaded with sample data:
- Sample emergency description
- New York coordinates (40.7128, -74.0060)
- Demo phone number
- Various emergency types

## Perfect for Hackathon

This frontend demonstrates:
- All consolidated API endpoints working
- Professional UI suitable for presentation
- Real-time interaction with the backend
- Cost protection and safety features
- Demo mode for testing without API keys

## Technical Details

- **Pure HTML/CSS/JavaScript** - No build process required
- **Responsive Design** - Works on all devices
- **Real-time Updates** - API status monitoring
- **Error Handling** - Graceful error display
- **Modern UI** - Gradient backgrounds and animations
