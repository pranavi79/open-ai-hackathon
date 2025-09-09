# API Documentation

## Overview

The Emergency Accident Response System provides a RESTful API for processing accident reports and coordinating emergency responses using AI agents.

## Base URL

```
http://localhost:8000
```

## Endpoints

### GET /

**Description:** Get basic API information

**Response:**
```json
{
  "message": "Emergency Accident Response System API",
  "version": "1.0.0",
  "status": "operational"
}
```

### GET /v1/health

**Description:** Health check endpoint to verify system status

**Response (Healthy):**
```json
{
  "status": "healthy",
  "services": {
    "api": "operational",
    "openai": "configured",
    "google_maps": "configured",
    "twilio": "configured"
  }
}
```

**Response (Degraded):**
```json
{
  "status": "degraded",
  "services": {
    "api": "operational",
    "openai": "not configured",
    "google_maps": "configured",
    "twilio": "not configured"
  },
  "warnings": "Missing configuration for: openai, twilio"
}
```

### POST /v1/ask

**Description:** Process an accident report and coordinate emergency response

**Request Body:**
```json
{
  "request": "string",     // Accident description
  "longitude": "string",   // Longitude coordinate
  "latitude": "string"     // Latitude coordinate
}
```

**Example Request:**
```json
{
  "request": "I just witnessed a motor accident on the road near Ananta Tech Park in Bangalore. A bike collided with a car at the traffic signal. The rider fell down and has a deep cut on his leg, and he looks like he's bleeding heavily. He seems conscious but in a lot of pain.",
  "longitude": "77.6107",
  "latitude": "12.9345"
}
```

**Response:**
```json
{
  "accident_type": "string",      // "minor" or "major trauma"
  "first_aid_tips": "string",     // First aid instructions
  "location": "string",           // Processed location
  "details": "string"             // Accident summary
}
```

**Example Response:**
```json
{
  "accident_type": "major trauma",
  "first_aid_tips": "Apply direct pressure to the wound with a clean cloth, elevate the leg if possible, keep the person calm and still until medical help arrives.",
  "location": "Ananta Tech Park, Bangalore",
  "details": "Bike-car collision at traffic signal resulting in deep leg cut with heavy bleeding"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid input: Accident description cannot be empty"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error: Connection to external service failed"
}
```

### 503 Service Unavailable
```json
{
  "detail": "Service temporarily unavailable"
}
```

## Authentication

Currently, the API does not require authentication. In a production environment, you should implement proper authentication and rate limiting.

## Rate Limiting

No rate limiting is currently implemented. Consider implementing rate limiting for production use to prevent abuse of external APIs (Google Maps, Twilio, OpenAI).

## Testing

### Using curl

```bash
# Health check
curl -X GET "http://localhost:8000/v1/health"

# Process accident report
curl -X POST "http://localhost:8000/v1/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "request": "Minor car accident, driver has small cuts",
    "longitude": "77.6107",
    "latitude": "12.9345"
  }'
```

### Using Python requests

```python
import requests

# Health check
response = requests.get("http://localhost:8000/v1/health")
print(response.json())

# Process accident report
data = {
    "request": "Serious motorcycle accident, rider unconscious",
    "longitude": "77.6107",
    "latitude": "12.9345"
}
response = requests.post("http://localhost:8000/v1/ask", json=data)
print(response.json())
```

## Workflow

1. **Client sends accident report** with location coordinates to `/v1/ask`
2. **Accident Response Agent** analyzes description and classifies severity
3. **Hospital Finder Agent** finds nearby hospitals using Google Maps API
4. **Contact Agent** automatically calls hospitals for major trauma cases via Twilio
5. **System returns** structured accident report with first aid guidance

## Data Models

### UserRequest
- `request` (string): Accident description
- `longitude` (string): Longitude coordinate
- `latitude` (string): Latitude coordinate

### AccidentReport
- `accident_type` (string): "minor" or "major trauma"
- `first_aid_tips` (string): First aid instructions
- `location` (string): Processed location description
- `details` (string): Summarized accident details

### HospitalInfo
- `name` (string): Hospital name
- `address` (string): Hospital address
- `rating` (float, optional): Hospital rating
- `user_ratings_total` (int, optional): Number of reviews
- `phone_number` (string, optional): Contact number