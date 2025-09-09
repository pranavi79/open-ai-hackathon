# Architecture Overview

## System Architecture

The Emergency Accident Response System uses a **multi-agent AI architecture** to process accident reports and coordinate emergency responses. The system is built with modularity and scalability in mind.

## High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client App    │    │   Web Browser   │    │  Mobile App     │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   FastAPI       │
                    │   REST API      │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │  Agent Runner   │
                    │   Framework     │
                    └─────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Accident Agent  │    │ Hospital Agent  │    │ Contact Agent   │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐               │
         │              │ Google Maps API │               │
         │              └─────────────────┘               │
         │                                                │
┌─────────────────┐                              ┌─────────────────┐
│   OpenAI API    │                              │   Twilio API    │
└─────────────────┘                              └─────────────────┘
```

## Core Components

### 1. FastAPI Application Layer

**Location:** `backend/app/main.py`, `backend/app/routes.py`

- **Purpose:** HTTP API interface for the emergency response system
- **Features:**
  - RESTful endpoints for accident reporting
  - Health check and monitoring endpoints
  - Error handling and validation
  - CORS support for web applications

### 2. Agent Framework Layer

**Location:** `backend/app/agents/`

The system uses specialized AI agents that communicate and coordinate to handle different aspects of emergency response:

#### a) Accident Response Agent
- **File:** `accident_response_agent.py`
- **Purpose:** Analyzes accident descriptions and provides initial assessment
- **Capabilities:**
  - Classifies accidents as "minor" or "major trauma"
  - Generates appropriate first aid instructions
  - Extracts key details from unstructured descriptions
  - Outputs structured JSON responses

#### b) Hospital Finder Agent
- **File:** `hospital_finder_agent.py`
- **Purpose:** Locates and ranks nearby medical facilities
- **Capabilities:**
  - Integrates with Google Maps API
  - Finds hospitals within 5km radius
  - Ranks hospitals by rating and reviews
  - Returns best hospital recommendation

#### c) Contact Agent
- **File:** `contact_agent.py`
- **Purpose:** Handles emergency communication
- **Capabilities:**
  - Makes automated calls to hospitals via Twilio
  - Crafts professional emergency messages
  - Provides hospital staff with accident details
  - Only activated for major trauma cases

#### d) Triage Agent
- **File:** `triage_agent.py`
- **Purpose:** Orchestrates the overall response workflow
- **Capabilities:**
  - Routes cases between agents based on severity
  - Coordinates handoffs between different response phases
  - Manages the overall decision tree

### 3. Service Layer

**Location:** `backend/app/service/`

Business logic that coordinates between agents:

- **`run_accident_response_agent.py`:** Main orchestration service
- **`hospital_search_service.py`:** Hospital location and selection logic
- **`contact_agent_service.py`:** Emergency calling coordination

### 4. Tools Layer

**Location:** `backend/app/tools/`

External integrations and utilities:

- **`fetch_nearest_hospital.py`:** Google Maps API integration
- **`calling_tool.py`:** Twilio voice API integration

### 5. Data Models

**Location:** `backend/app/models/`

Pydantic models for type safety and validation:

- **`user_request.py`:** Input data structure
- **`accident_report.py`:** Output data structure
- **`hospital_info.py`:** Hospital data structure
- **`location_context.py`:** Geographic data structure

## Data Flow

### 1. Request Processing
```
User Request → Input Validation → Agent Orchestration
```

### 2. Accident Analysis
```
Raw Description → Accident Agent → Structured Report
                               → Severity Classification
                               → First Aid Instructions
```

### 3. Hospital Location
```
Location Coordinates → Google Maps API → Hospital List
                                      → Rating Analysis
                                      → Best Hospital Selection
```

### 4. Emergency Response
```
Major Trauma Detection → Contact Agent → Twilio API → Hospital Call
```

## External Dependencies

### AI and ML
- **OpenAI API:** Powers the intelligent agents
- **LiteLLM:** Model provider abstraction layer
- **Agents Framework:** Multi-agent orchestration

### Location Services
- **Google Maps API:** Hospital search and location services

### Communication
- **Twilio:** Voice calling for emergency notifications

## Scalability Considerations

### Horizontal Scaling
- Stateless API design allows for multiple server instances
- Agent framework supports distributed processing
- External APIs handle their own scaling

### Performance Optimization
- Async/await patterns for non-blocking operations
- Efficient agent handoffs minimize processing time
- Caching can be added for hospital data

### Reliability
- Health check endpoints for monitoring
- Error handling and fallback mechanisms
- External API timeout and retry logic

## Security Considerations

### API Security
- Input validation and sanitization
- Rate limiting recommendations
- Environment variable management for secrets

### Data Privacy
- No persistent storage of sensitive information
- Minimal data retention
- Secure API key management

## Configuration Management

**Location:** `backend/app/core/config.py`

Centralized configuration using Pydantic settings:
- Environment variable management
- API key configuration
- Model and service settings
- Development vs production modes

## Monitoring and Health Checks

### Health Endpoints
- Service availability checks
- External API connectivity verification
- Configuration validation

### Logging
- Structured logging for debugging
- Error tracking and alerting
- Performance monitoring capabilities

This architecture provides a robust, scalable foundation for emergency response automation while maintaining clear separation of concerns and extensibility for future enhancements.