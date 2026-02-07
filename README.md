# Upendo Charity Donation Management System

## Project Overview

A streamlined backend system designed to manage direct financial contributions to the Upendo organization. The system provides RESTful API endpoints for donors to submit donations and view public fundraising statistics. No signup or login is required.

**Project Type:** Django REST API  
**Capstone Project:** Upendo Charity Organization  
**Status:** 🎯 Ready for Implementation  
**Target Duration:** 4 weeks

---

## Quick Start - Key Information

### 🔗 Base API URL
```
http://localhost:8000/api
```

### 📚 Project Files

- README.md
- requirements.txt

### ✨ Key Features

✅ **Donation Management**
- Submit donations with validation
- Auto-generated unique transaction references
- Optional donor name and email per donation

✅ **Transparency**
- Public endpoint showing total funds raised
- Includes donation count, average amount
- No authentication required

✅ **Admin Features**
- Django admin interface for monitoring
- View all donations across platform
- User account management
- Filtered donation reports

✅ **Security**
- Input validation on all endpoints
- HTTPS-ready configuration

---

## System Architecture

### Layered Design
```
┌─────────────────────────────────────────────┐
│         Client Layer (Frontend)              │
│    (React/Vue/Mobile Apps)                   │
└──────────────┬──────────────────────────────┘
               │ HTTP/REST/JSON
┌──────────────▼──────────────────────────────┐
│          API Layer (Django)                  │
│  ┌────────────────────────────────────────┐ │
│  │ URL Router (/api/donations/*)          │ │
│  └────────────────────────────────────────┘ │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│    Business Logic Layer (DRF)               │
│  ┌────────────────────────────────────────┐ │
│  │ Views (Donations, Stats)               │ │
│  │ Serializers (Validation, Transform)    │ │
│  │ Managers (Complex Queries)             │ │
│  └────────────────────────────────────────┘ │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│        Data Layer (Models)                   │
│  ┌────────────────────────────────────────┐ │
│  │ Donation (with auto-ref generation)    │ │
│  └────────────────────────────────────────┘ │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│      Database Layer (PostgreSQL)             │
│  donations_donation (Transactions)          │
│  Django admin interface                     │
│  Backup & Recovery system                   │
└──────────────────────────────────────────────┘
```

---

## API Endpoints at a Glance

### Donations
| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| POST | `/donations/pay/` | Submit a donation | ❌ |
| GET | `/donations/stats/` | View total funds raised | ❌ |

### Admin & Docs
| Endpoint | Purpose |
|----------|---------|
| `/admin/` | Django admin interface (staff only) |
| `/schema/swagger-ui/` | Interactive API documentation |
| `/schema/redoc/` | Alternative API documentation |

---

## Database Design

### Donation Model
```
id                          INT             PRIMARY KEY
donor_name                  VARCHAR(100)    OPTIONAL
donor_email                 VARCHAR(254)    OPTIONAL
amount                      DECIMAL(10,2)   Range: 0.01 - 999,999.99
transaction_reference       VARCHAR(50)     UNIQUE, Indexed
message                     TEXT            OPTIONAL, Max: 500 chars
timestamp                   TIMESTAMP       AUTO_NOW_ADD, Indexed
```

### Indexes (Performance)
```
donations(donor_id, -timestamp)
donations(transaction_reference)
donations(timestamp)
```

---

## Technology Stack

### Framework & Libraries
```
Django 4.2+                          # Web framework
Django REST Framework 3.14+          # REST API
django-cors-headers 4.0+             # CORS support
drf-spectacular 0.26+                # OpenAPI/Swagger docs
psycopg2-binary 2.9+                 # PostgreSQL driver
python-decouple 3.8                  # Environment variables
```

### Database
```
PostgreSQL 12+                       # Relational database (Production)
SQLite 3                             # Database (Development)
```

### Testing
```
pytest 7.3+                          # Test framework
pytest-django 4.5+                   # Django integration
factory-boy                          # Test fixtures
```

### Optional Enhancements
```
Redis                                # Caching (stats endpoint)
Gunicorn                             # Production WSGI server
Nginx                                # Reverse proxy
```

---

## Security Features

### Data Protection
✅ SQL injection prevention via Django ORM  
✅ DECIMAL fields prevent floating-point errors  

### API Security
✅ CORS configuration (whitelist allowed origins)  
✅ Input validation at serializer level  
✅ No sensitive data in error messages  

### Infrastructure Security
✅ HTTPS/TLS enforcement in production  
✅ Security headers (HSTS, CSP, X-Frame-Options)  
✅ Environment variables for secrets  
✅ Admin interface behind staff-only permission  

---

## Request/Response Examples

### Submit Donation
```bash
POST /api/donations/pay/
Content-Type: application/json

{
  "amount": "150.50",
  "donor_name": "John Doe",
  "donor_email": "john@example.com",
  "message": "Supporting education programs"
}

Response (201 Created):
{
  "id": 1,
  "donor_name": "John Doe",
  "donor_email": "john@example.com",
  "amount": "150.50",
  "transaction_reference": "TXN-20260207-ABC123",
  "message": "Supporting education programs",
  "timestamp": "2026-02-07T14:30:45.123456Z"
}
```

### View Stats
```bash
GET /api/donations/stats/

Response (200 OK):
{
  "total_amount_raised": "5250.75",
  "total_donations": 25,
  "unique_donors": 18,
  "average_donation": "210.03"
}
```

---

## Project Timeline

### Week 1: Foundation
**Deliverable:** Working donation submission + stats
- Django project setup
- Donation model
- Donation submission endpoint
- Stats endpoint

### Week 2: Core Donation Logic
**Deliverable:** Ability to save donations with unique references
- Donation model
- Transaction reference generation (signal-based)
- POST endpoint for donations
- Amount validation

### Week 3: Reporting
**Deliverable:** Public statistics and admin monitoring
- Stats aggregation and public endpoint
- Optional caching on stats
- Django admin for monitoring

### Week 4: Testing & Deployment
**Deliverable:** Submission-ready API with full documentation
- Comprehensive unit tests
- Integration tests
- API documentation (Swagger)
- Security hardening
- Deployment guide

---

## Getting Started (Installation)

### Prerequisites
```bash
Python 3.9+
PostgreSQL 12+ (or SQLite for development)
pip (Python package manager)
git (version control)
```

### Setup Steps (Coming After Design Approval)
```bash
# 1. Clone repository
git clone <repo-url>
cd upendo-charity

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your database and secret configurations

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create superuser (admin)
python manage.py createsuperuser

# 7. Run development server
python manage.py runserver

# 8. Run tests
pytest

# 9. View API documentation
# Navigate to http://localhost:8000/api/schema/swagger-ui/
```

---

## File Structure

```
upendo-charity/
│
├── 📋 Design Documents (Created)
│   ├── DESIGN_DOCUMENTATION.md      # Complete specification
│   ├── API_QUICK_REFERENCE.md       # Quick lookup guide
│   ├── PROJECT_STRUCTURE.md         # File organization
│   ├── TESTING_STRATEGY.md          # Test planning
│   ├── SECURITY_DEPLOYMENT.md       # Security & ops
│   ├── DESIGN_SUMMARY.md            # Overview & index
│   └── README.md                    # This file
│
├── 📁 upendo_project/               # Django settings (To be created)
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── 📁 accounts/                     # User management (To be created)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── 📁 donations/                    # Donation management (To be created)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── managers.py
│   ├── signals.py
│   └── urls.py
│
├── 📁 api/                          # API configuration (To be created)
│   ├── urls.py
│   ├── permissions.py
│   └── pagination.py
│
├── 📁 tests/                        # Test suite (To be created)
│   ├── test_auth.py
│   ├── test_donations.py
│   ├── test_permissions.py
│   └── conftest.py
│
├── 📄 manage.py                     # Django CLI
├── 📄 requirements.txt              # Dependencies
├── 📄 .env.example                  # Environment template
└── 📄 .gitignore                    # Git ignore rules
```