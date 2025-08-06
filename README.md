# Moondance Backend

A comprehensive backend API for the Moondance web application built with Flask and Rococo framework, featuring microservices architecture with PostgreSQL, RabbitMQ, and email services.

## 🏗️ Architecture

The backend consists of multiple containerized services:

- **API Service**: Flask-based REST API with authentication and business logic
- **PostgreSQL**: Primary database for application data
- **RabbitMQ**: Message broker for asynchronous task processing
- **Email Transmitter**: Dedicated service for email notifications

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Environment configuration files

### Setup

1. **Environment Configuration**
   ```bash
   # Create your environment files
   cp .env.secrets.example .env.secrets # Secret configuration
   ```

2. **Start the Application**
   ```bash
   # Start all services
   ./run.sh

   # Or rebuild and start (for first-time setup or updates)
   ./run.sh --rebuild true
   ```

3. **Access the API**
   - API endpoint: `http://localhost:5000`
   - PostgreSQL: `localhost:5432`
   - RabbitMQ: `localhost:5672`

## 📁 Project Structure

```
moondance-backend/
├── flask/                  # Flask API application
│   ├── app/               # Main application package
│   │   ├── views/         # API endpoints and routes
│   │   ├── migrations/    # Database migrations
│   │   └── helpers/       # Utility functions
│   ├── main.py           # Application entry point
│   └── pyproject.toml    # Python dependencies
├── common/               # Shared modules
│   ├── models/          # Data models
│   ├── repositories/    # Data access layer
│   ├── services/        # Business logic services
│   ├── tasks/           # Background tasks
│   ├── helpers/         # Utility functions
│   └── utils/           # Common utilities
├── services/            # External services
│   ├── postgres/        # PostgreSQL configuration
│   ├── rabbitmq/        # RabbitMQ configuration
│   └── email_transmitter/ # Email service
├── docker-compose.yml   # Docker services configuration
├── run.sh              # Application startup script
└── local.env           # Environment variables
```

## 🔧 Technology Stack

- **Framework**: Flask 3.1.1 with Flask-RESTX
- **ORM**: Rococo 1.1.4 (with PostgreSQL, MySQL, messaging, and emailing support)
- **Database**: PostgreSQL
- **Message Queue**: RabbitMQ with Pika
- **Authentication**: JWT tokens
- **Validation**: Pydantic 2.10.6
- **Monitoring**: Rollbar for error tracking
- **Language**: Python 3.11+

## 🌐 API Endpoints

The API provides endpoints for:

- **Authentication**: User login, registration, and JWT token management
- **User Management**: Person and organization management
- **Todo Management**: Task creation, updates, and organization
- **Organizations**: Multi-tenant organization support

## 🗄️ Database Models

Key data models include:

- **Person**: User accounts and profiles
- **Organization**: Multi-tenant organization structure
- **Todo**: Task management system
- **Login Method**: Authentication methods
- **Email**: Email communication tracking

## 🐳 Docker Services

The application runs as a multi-container Docker application:

- **moondance_api**: Main Flask application (port 5000)
- **moondance_postgres**: PostgreSQL database (port 5432)
- **moondance_rabbitmq**: RabbitMQ message broker (port 5672)
- **moondance_email_transmitter**: Email processing service