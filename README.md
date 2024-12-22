# HTTP Server Python

## Overview
This project is a simple HTTP server implemented in Python with a weather service microservice architecture. It handles user management and weather information requests.

## Requirements
- Docker and Docker Compose
- Python 3.9+ (for local development)

## Quick Start with Docker
Start the services:
```bash
docker-compose up --build
```

## Available Endpoints

### Main Web Service (http://localhost/)
- `GET /` - API documentation
- `GET /users` - List all users
- `POST /user` - Create new user
- `GET /user/{id}` - Get user by ID
- `PUT /user/{id}` - Update user
- `DELETE /user/{id}` - Delete user
- `GET /weather?city={city}` - Get weather for city (via web service)

### Weather Service (http://localhost/api/weather)
- `GET /api/weather?city={city}` - Get weather for city (direct microservice access)

## Local Development
To install dependencies and run locally:
```bash
pip install -r requirements.txt
python server.py
```

## Architecture
- Nginx: Reverse proxy (Port 80)
- Web Service: User management and routing (Port 5000)
- Weather Service: Weather data microservice (Port 5001)

```plantuml
@startuml System Boundaries

skinparam backgroundColor #FFFFFF
skinparam ComponentStyle uml2

!define CLIENT_ZONE #LightBlue
!define SERVER_ZONE #LightGreen 
!define EXTERNAL_ZONE #LightGray

rectangle "Client Boundary" as ClientZone CLIENT_ZONE {
    actor "User" as user 
    component "Web Browser" as browser
    component "HTTP Client" as client
}

rectangle "External System Boundary" as ExternalZone EXTERNAL_ZONE {
    [Weather API Service] as weatherAPI
}

rectangle "Server Boundary" as ServerZone SERVER_ZONE {
    node "Infrastructure Layer" {
        component "Nginx Reverse Proxy" as nginx
        database "PostgreSQL DB" as db
    }
    
    package "Main Service" {
        [User Management Service] as userMgmt
        [Authentication Service] as auth
        [API Gateway] as gateway
    }
    
    package "Weather Service" {
        [Weather Data Provider] as weatherProvider
        [Weather Statistics] as weatherStats
    }
}

user --> browser
browser --> client 
client --> nginx : HTTP/HTTPS

nginx --> gateway
gateway --> userMgmt
gateway --> weatherProvider

userMgmt --> db
auth --> db
weatherStats --> db

weatherProvider --> weatherAPI : REST API

userMgmt ..> auth : uses
gateway ..> auth : uses
weatherProvider ..> weatherStats : uses

left to right direction

@enduml
```