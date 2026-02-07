# Upendo Charity Donation Management System

## Project Overview

A streamlined backend system designed to manage direct financial contributions to the Upendo organization. The system provides RESTful API endpoints for donors to register, submit secure donations, and track their personal contribution history. It also features a public-facing statistics endpoint to promote organizational transparency by displaying total funds raised.

**Project Type:** Django REST API  
**Capstone Project:** Upendo Charity Organization  
**Status:** 🎯 Ready for Implementation (Design Phase Complete)  
**Target Duration:** 4 weeks

---

## Quick Start - Key Information

### 🔗 Base API URL
```
http://localhost:8000/api
```

### 📚 Documentation Files (Design Phase)

| Document | Purpose | Link |
|----------|---------|------|
| **DESIGN_SUMMARY.md** | Start here - Overview of all design | Index & key decisions |
| **DESIGN_DOCUMENTATION.md** | Comprehensive specification | Database, endpoints, validation |
| **API_QUICK_REFERENCE.md** | Quick API lookup | Endpoints, examples, errors |
| **PROJECT_STRUCTURE.md** | Directory organization | File layout & responsibilities |
| **TESTING_STRATEGY.md** | Test planning | Test types, fixtures, coverage |
| **SECURITY_DEPLOYMENT.md** | Security & operations | Security checklist, deployment |

### ✨ Key Features

✅ **User Authentication**
- Register with secure password requirements
- Login with JWT tokens (access + refresh)
- Stateless authentication for scalability

✅ **Donation Management**
- Submit donations with validation
- Auto-generated unique transaction references
- View personal donation history

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
- Password validation (8+ chars, mixed case, numbers, symbols)
- JWT token-based authentication
- Role-based permissions (user, admin)
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
│  │ URL Router (/api/auth/*, /api/donations/*) │
│  │ JWT Middleware (Token Validation)      │ │
│  │ Permissions (IsAuth, IsPublic)         │ │
│  └────────────────────────────────────────┘ │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│    Business Logic Layer (DRF)               │
│  ┌────────────────────────────────────────┐ │
│  │ Views (Auth, Donations, Stats)         │ │
│  │ Serializers (Validation, Transform)    │ │
│  │ Managers (Complex Queries)             │ │
│  └────────────────────────────────────────┘ │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│        Data Layer (Models)                   │
│  ┌────────────────────────────────────────┐ │
│  │ User (Custom AbstractUser)             │ │
│  │ Donation (with auto-ref generation)    │ │
│  │ Signals (auto-generation)              │ │
│  └────────────────────────────────────────┘ │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│      Database Layer (PostgreSQL)             │
│  users_customuser (Donors)                  │
│  donations_donation (Transactions)          │
│  Django admin interface                     │
│  Backup & Recovery system                   │
└──────────────────────────────────────────────┘
```

---

## API Endpoints at a Glance

### Authentication
| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| POST | `/auth/register/` | Create new donor account | ❌ |
| POST | `/auth/login/` | Generate access & refresh tokens | ❌ |
| POST | `/auth/token/refresh/` | Get new access token | ❌ |

### Donations
| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| POST | `/donations/pay/` | Submit a donation | ✅ |
| GET | `/donations/my-history/` | View your donations | ✅ |
| GET | `/donations/stats/` | View total funds raised | ❌ |

### Admin & Docs
| Endpoint | Purpose |
|----------|---------|
| `/admin/` | Django admin interface (staff only) |
| `/schema/swagger-ui/` | Interactive API documentation |
| `/schema/redoc/` | Alternative API documentation |

---

## Database Design

### User Model (Custom User)
```
id                INT             PRIMARY KEY
username          VARCHAR(150)    UNIQUE
email             VARCHAR(254)    UNIQUE, Indexed
password          VARCHAR(128)    Hashed
full_name         VARCHAR(100)    
is_staff          BOOLEAN         DEFAULT: False
is_active         BOOLEAN         DEFAULT: True
date_joined       TIMESTAMP       AUTO_NOW_ADD
last_login        TIMESTAMP       NULLABLE
```

### Donation Model
```
id                          INT             PRIMARY KEY
donor_id                    INT             FK → User (CASCADE)
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
users(email)
users(username)
```

---

## Technology Stack

### Framework & Libraries
```
Django 4.2+                          # Web framework
Django REST Framework 3.14+          # REST API
djangorestframework-simplejwt 5.2+   # JWT authentication
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

### Authentication Security
✅ Password validation: 8+ chars, uppercase, lowercase, number, special char  
✅ Passwords hashed with PBKDF2 (bcrypt alternative compatible)  
✅ JWT tokens with 5-min access and 24-hour refresh lifetimes  
✅ Token payload signed and verified (HS256 algorithm)  

### Data Protection
✅ SQL injection prevention via Django ORM  
✅ Foreign key constraints enforce referential integrity  
✅ Cascading deletes respect data ownership  
✅ DECIMAL fields prevent floating-point errors  

### API Security
✅ CORS configuration (whitelist allowed origins)  
✅ Rate limiting on auth endpoints  
✅ Input validation at serializer level  
✅ No sensitive data in error messages  

### Infrastructure Security
✅ HTTPS/TLS enforcement in production  
✅ Security headers (HSTS, CSP, X-Frame-Options)  
✅ Environment variables for secrets  
✅ Admin interface behind staff-only permission  

---

## Request/Response Examples

### Register
```bash
POST /api/auth/register/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}

Response (201 Created):
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe"
}
```

### Login
```bash
POST /api/auth/login/
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "SecurePass123!"
}

Response (200 OK):
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

### Submit Donation
```bash
POST /api/donations/pay/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "amount": "150.50",
  "message": "Supporting education programs"
}

Response (201 Created):
{
  "id": 1,
  "donor": 1,
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

### Week 1: Foundation & Authentication
**Deliverable:** Working authentication system
- Django project setup
- Custom User model
- JWT authentication endpoints
- Database migrations

### Week 2: Core Donation Logic
**Deliverable:** Ability to save donations with unique references
- Donation model
- Transaction reference generation (signal-based)
- POST endpoint for donations
- Amount validation

### Week 3: Reporting & History
**Deliverable:** Donor tracking and public statistics
- Donation history endpoint with filtering
- Stats aggregation and public endpoint
- Pagination on history
- Optional caching on stats

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

---

## Key Design Decisions

### 1. Custom User Model
**Why:** Flexibility for future extensions (donor profiles, preferences)  
**Implementation:** Done before any migrations (critical)

### 2. JWT Authentication
**Why:** Stateless, scalable, suitable for mobile and SPAs  
**Benefit:** No session storage needed, horizontal scaling possible

### 3. Signal-Driven Reference Generation
**Why:** Automatic, consistent, reduces manual code  
**Implementation:** Django signal handler on model pre_save

### 4. DECIMAL Field for Amounts
**Why:** Avoids floating-point precision errors  
**Benefit:** Accurate financial calculations

### 5. Cascading Deletes
**Why:** Ensures data integrity and GDPR compliance  
**Benefit:** Deleting user removes all their associated data

### 6. Role-Based Permissions
**Why:** Fine-grained access control  
**Benefit:** Extensible for future roles

### 7. Pagination on History
**Why:** Scales to thousands of donations per user  
**Benefit:** Limited database queries and response size

---

## Testing Strategy

### Test Coverage Goals
- **Overall:** 80% minimum code coverage
- **Models:** 100% coverage
- **Views:** 85% coverage
- **Serializers:** 90% coverage

### Test Types
✅ Unit Tests (model validation, utilities)  
✅ Integration Tests (API endpoints, database)  
✅ Permission Tests (access control)  
✅ Edge Case Tests (concurrent operations, boundary conditions)

### Running Tests
```bash
pytest                                 # Run all tests
pytest tests/test_auth.py             # Run specific file
pytest --cov=. --cov-report=html      # Coverage report
pytest -v                             # Verbose output
```

---

## API Documentation

### Interactive Documentation
After deployment, access:
- **Swagger UI:** `http://localhost:8000/api/schema/swagger-ui/`
- **ReDoc:** `http://localhost:8000/api/schema/redoc/`
- **OpenAPI Schema:** `http://localhost:8000/api/schema/`

### Features
- Try endpoints directly from browser
- See request/response schemas
- Understand required parameters
- Test with real tokens

---

## Deployment

### Production Checklist
✅ Environment variables configured  
✅ Database migrations applied  
✅ Static files collected  
✅ Secret key generated  
✅ CORS origins configured  
✅ HTTPS certificates installed  
✅ Backup system active  
✅ Monitoring configured  

### Supported Environments
- **Development:** SQLite, DEBUG=True, localhost
- **Production:** PostgreSQL, DEBUG=False, example.com
- **Testing:** Separate test database, fast mode

### Deployment Platforms
- Heroku (with Procfile)
- AWS (EC2, RDS, S3)
- DigitalOcean (App Platform or Droplets)
- Linode
- Self-hosted Linux servers

**For detailed deployment guide:** See SECURITY_DEPLOYMENT.md

---

## Monitoring & Support

### Monitoring Points
- API response times (target < 200ms)
- Error rates (target < 1%)
- Database query performance
- Server CPU/Memory usage
- Disk space

### Logging
- Application logs (Django)
- Access logs (Nginx)
- Database logs (PostgreSQL)
- Security events

### Support Channels
- GitHub Issues for bug reports
- Email for security vulnerabilities
- Team Slack for questions

---

## Future Enhancements (v2+)

- Email verification for registration
- Password reset functionality
- Donation receipts (PDF generation)
- Monthly funding goals & progress
- Impact tracking (where funds are used)
- Notification system (donation confirmations)
- Two-factor authentication
- Donor profiles & preferences
- Advanced analytics & reporting
- Mobile app (iOS/Android)
- SMS notifications

---

## Compliance & Standards

### Code Standards
- PEP 8 (Python style guide)
- DRF conventions for API design
- Django best practices
- Clean code principles

### Security Standards
- OWASP top 10 prevention
- GDPR compliance (data protection)
- PCI DSS (if accepting payments)
- SOC 2 readiness

### API Standards
- RESTful design principles
- Semantic versioning
- OpenAPI 3.0 specification
- JSON request/response format

---

## Performance Targets

| Metric | Target | Note |
|--------|--------|------|
| API Response Time | < 200ms | 95th percentile |
| Database Query Time | < 100ms | Indexed queries |
| Error Rate | < 1% | 500 errors |
| Uptime | 99.9% | 4-5 hours downtime/year |
| Concurrent Users | 1000+ | Horizontally scalable |
| Requests/Second | 100+ | With 4 app servers |

---

## Contact & Questions

### Design Documentation
Start with **DESIGN_SUMMARY.md** for an overview, then refer to specific documents:
- Architecture: **PROJECT_STRUCTURE.md**
- Endpoints: **API_QUICK_REFERENCE.md** or **DESIGN_DOCUMENTATION.md**
- Testing: **TESTING_STRATEGY.md**
- Deployment: **SECURITY_DEPLOYMENT.md**

### Implementation Status
📍 **Current Phase:** Design Complete  
✅ **Design Phase:** Finished (Feb 7, 2026)  
⏳ **Next Phase:** Implementation (pending approval)

---

## License & Contribution

### Open Source
This project is open source and can be modified/extended.

### Contributing
1. Create a feature branch
2. Make changes
3. Write tests
4. Submit pull request
5. Code review before merge

---

**Project Status:** 🎯 Ready for Implementation  
**Last Updated:** February 7, 2026  
**Design Approval:** [Awaiting]

---

## Quick Links to Design Documents

1. [📋 DESIGN_DOCUMENTATION.md](DESIGN_DOCUMENTATION.md) – Complete specification
2. [🔗 API_QUICK_REFERENCE.md](API_QUICK_REFERENCE.md) – Quick API lookup
3. [📁 PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) – Directory layout
4. [🧪 TESTING_STRATEGY.md](TESTING_STRATEGY.md) – Test planning
5. [🔒 SECURITY_DEPLOYMENT.md](SECURITY_DEPLOYMENT.md) – Security & deployment
6. [📊 DESIGN_SUMMARY.md](DESIGN_SUMMARY.md) – Overview & index

---

**All design documents are complete and ready for implementation review.**
