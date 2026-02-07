# Upendo Charity Donation Management System - Design Documentation

## 1. System Architecture Overview

### Technology Stack
- **Backend Framework:** Django 4.2+
- **REST API:** Django REST Framework (DRF)
- **Authentication:** JWT (djangorestframework-simplejwt)
- **Database:** PostgreSQL (recommended) / SQLite (development)
- **Documentation:** drf-spectacular (OpenAPI/Swagger)
- **Testing:** pytest-django
- **Additional Libraries:** 
  - django-cors-headers (CORS support)
  - python-decouple (environment variables)
  - django-filter (filtering, searching)

---

## 2. Database Design

### Entity Relationship Diagram (ERD)

**Entities:**
- **User (Custom User Model)**
  - Extends Django's AbstractUser
  - Fields: id, username, email, password, full_name, is_staff, is_active, date_joined, last_login
  - Relationships: One-to-Many with Donation

- **Donation**
  - Fields: id, donor_id (FK → User), amount, transaction_reference, message, timestamp
  - Constraints: 
    - donor_id: Foreign Key (CASCADE delete)
    - amount: Positive DecimalField(max_digits=10, decimal_places=2)
    - transaction_reference: Unique CharField (max_length=50)
    - timestamp: auto_now_add (immutable)

### Database Indexes
```sql
-- Improve query performance
CREATE INDEX idx_donation_donor_id ON donations(donor_id);
CREATE INDEX idx_donation_timestamp ON donations(timestamp);
CREATE INDEX idx_donation_transaction_reference ON donations(transaction_reference);
CREATE INDEX idx_user_email ON users(email);
```

---

## 3. API Endpoints Specification

### Base URL
```
http://localhost:8000/api/
```

### Authentication Endpoints

#### 1. Register New Donor
```
POST /auth/register/
```
**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePassword123!",
  "full_name": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "message": "User registered successfully"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid input, duplicate email/username
- `422 Unprocessable Entity` - Validation errors (weak password, etc.)

**Validation Rules:**
- Username: 3-150 chars, alphanumeric + underscore
- Email: Valid format, unique
- Password: Min 8 chars, includes uppercase, lowercase, number, special char
- Full Name: 2-100 chars, non-empty

---

#### 2. Login (Generate Tokens)
```
POST /auth/login/
```
**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe"
  }
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid credentials
- `400 Bad Request` - Missing email or password

**Token Details:**
- Access Token: 5-minute expiration
- Refresh Token: 24-hour expiration
- Refresh endpoint: `POST /auth/token/refresh/` (using refresh token, returns new access token)

---

#### 3. Refresh Access Token
```
POST /auth/token/refresh/
```
**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or expired refresh token

---

### Donation Endpoints

#### 4. Submit a Donation
```
POST /donations/pay/
```
**Authentication:** Required (Bearer Token)

**Request Body:**
```json
{
  "amount": 150.50,
  "message": "Supporting education programs"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "donor": 1,
  "donor_name": "John Doe",
  "amount": "150.50",
  "transaction_reference": "TXN-20260207-ABC123",
  "message": "Supporting education programs",
  "timestamp": "2026-02-07T14:30:45.123456Z"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid amount (negative, zero, non-numeric)
- `401 Unauthorized` - Missing or invalid token
- `422 Unprocessable Entity` - Amount exceeds max decimal places

**Validation Rules:**
- Amount: Positive number, 0.01 - 999,999.99
- Message: Optional, max 500 chars
- Transaction Reference: Auto-generated (format: TXN-YYYYMMDD-RANDOM6CHARS)

---

#### 5. Get Donor Contribution History
```
GET /donations/my-history/
```
**Authentication:** Required (Bearer Token)

**Query Parameters (Optional):**
```
?page=1&page_size=10
?start_date=2026-01-01&end_date=2026-02-07
?ordering=-timestamp  # or +timestamp for ascending
```

**Response (200 OK):**
```json
{
  "count": 5,
  "next": "http://localhost:8000/api/donations/my-history/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "amount": "150.50",
      "transaction_reference": "TXN-20260207-ABC123",
      "message": "Supporting education programs",
      "timestamp": "2026-02-07T14:30:45.123456Z"
    },
    {
      "id": 2,
      "amount": "250.00",
      "transaction_reference": "TXN-20260206-XYZ789",
      "message": "Healthcare initiative",
      "timestamp": "2026-02-06T10:15:30.000000Z"
    }
  ]
}
```

**Error Responses:**
- `401 Unauthorized` - Missing or invalid token
- `400 Bad Request` - Invalid query parameters (wrong date format, page number)

**Features:**
- Pagination: Default 10 items per page
- Ordering: By timestamp (newest first by default)
- Date Filtering: Optional for custom ranges
- Serializer excludes donor_id for security (shows donor_name if needed)

---

### Public Endpoints

#### 6. Get Fundraising Statistics
```
GET /donations/stats/
```
**Authentication:** Not Required (Public Endpoint)

**Response (200 OK):**
```json
{
  "total_amount_raised": "5250.75",
  "total_donations": 25,
  "unique_donors": 18,
  "average_donation": "210.03",
  "latest_donation_timestamp": "2026-02-07T14:30:45.123456Z"
}
```

**Error Responses:**
- None typical (always returns 200, with 0 values if no donations)

**Features:**
- Cached response (optional Redis caching, 5-minute TTL)
- Aggregate calculations using Django ORM
- Suitable for homepage display or transparency dashboard

---

## 4. Authentication & Security Details

### JWT Token Structure

**Access Token Payload:**
```json
{
  "token_type": "access",
  "exp": 1234567890,
  "iat": 1234567200,
  "jti": "abc123def456",
  "user_id": 1,
  "username": "john_doe",
  "email": "john@example.com"
}
```

**Authorization Header Format:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Permission Rules

| Endpoint | Public | Authenticated | Staff Only |
|----------|--------|---------------|-----------|
| POST /auth/register/ | ✓ | ✗ | ✗ |
| POST /auth/login/ | ✓ | ✗ | ✗ |
| POST /auth/token/refresh/ | ✓ | ✗ | ✗ |
| GET /donations/stats/ | ✓ | ✓ | ✓ |
| POST /donations/pay/ | ✗ | ✓ | ✓ |
| GET /donations/my-history/ | ✗ | ✓ | ✓ |
| GET /admin/donations/ (Django Admin) | ✗ | ✗ | ✓ |

### CORS Configuration
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React dev server
    "http://localhost:5173",  # Vite dev server
    "https://yourdomain.com",  # Production frontend
]
```

---

## 5. Error Handling & Status Codes

### HTTP Status Codes Used

| Code | Scenario |
|------|----------|
| 200 OK | Successful GET request |
| 201 Created | Successful resource creation (POST) |
| 400 Bad Request | Invalid input, malformed request body |
| 401 Unauthorized | Missing or invalid authentication token |
| 403 Forbidden | Authenticated but lacks permission |
| 404 Not Found | Resource not found |
| 422 Unprocessable Entity | Validation error in request data |
| 500 Internal Server Error | Server-side error |

### Standard Error Response Format
```json
{
  "error": "Invalid credentials",
  "detail": "Email and password do not match any user",
  "status_code": 401
}
```

### Validation Error Response
```json
{
  "amount": ["Ensure this value is greater than 0.00"],
  "message": ["Ensure this field has no more than 500 characters"]
}
```

---

## 6. Transaction Reference Generation

### Format Architecture
```
TXN-[YYYYMMDD]-[6-CHAR-RANDOM]

Example: TXN-20260207-A7K2M9
```

### Generation Logic
1. Date Component: Current date in YYYYMMDD format
2. Random Component: 6 alphanumeric characters (uppercase)
3. Uniqueness: Guaranteed via database UNIQUE constraint + validation in serializer
4. Implementation: Signal handler on Donation model pre_save

### Collision Handling
- Check for existing reference before saving
- Retry generation (max 5 attempts) if collision occurs
- Log warnings for monitoring

---

## 7. API Response Pagination

### Pagination Configuration
```python
DEFAULT_PAGINATION_CLASS = 'rest_framework.pagination.PageNumberPagination'
PAGE_SIZE = 10
```

### Paginated Response Format
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/donations/my-history/?page=2",
  "previous": null,
  "results": [...]
}
```

### Pagination Query Parameters
```
?page=2&page_size=20
```

---

## 8. Django Admin Interface Configuration

### Staff Dashboard Features

**User Management:**
- List all registered donors (username, email, join date, is_active)
- Search by username or email
- Filter by registration date, staff status
- View/edit user profiles
- Bulk deactivate inactive accounts

**Donation Monitoring:**
- List all donations (donor name, amount, transaction reference, timestamp)
- Search by transaction reference or donor name
- Filter by date range (date_hierarchy on timestamp)
- Display donation statistics (total, count, average)
- View donor details with donation history
- Export donation data (optional)

**Readonly Fields (Security):**
- transaction_reference (prevent reference tampering)
- timestamp (prevent fraud)
- donor (prevent reassignment)

---

## 9. Data Validation Rules

### User Registration
- Username: 3-150 chars, alphanumeric + underscore, unique
- Email: Valid RFC 5322 format, unique
- Password: Min 8 chars, must contain uppercase, lowercase, digit, special char
- Full Name: 2-100 chars, non-empty

### Donation
- Amount: Decimal(10, 2), min 0.01, max 999,999.99
- Message: Optional, max 500 chars, plain text
- Donor: Required, FK to authenticated user
- Transaction Reference: Auto-generated, unique, 50 chars max

### Login
- Email: Required, valid format
- Password: Required, 1-128 chars

---

## 10. Database Constraints & Indexes

### Primary Keys
- User.id: Auto-increment, PRIMARY KEY
- Donation.id: Auto-increment, PRIMARY KEY

### Unique Constraints
- User.email: UNIQUE
- User.username: UNIQUE
- Donation.transaction_reference: UNIQUE

### Foreign Keys
- Donation.donor_id → User.id (ON DELETE CASCADE)

### Indexes for Performance
```python
# models.py
class Donation(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['donor', '-timestamp']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['transaction_reference']),
        ]
```

---

## 11. API Request/Response Flow Diagrams

### Authentication Flow
```
User (Browser/App)
    ↓
[Register] → Django API → Database → Response (User Created)
    ↓
[Login with email/password] → JWT Token Generation → Response (Access + Refresh Token)
    ↓
Store tokens in localStorage/sessionStorage
```

### Donation Flow
```
Authenticated User
    ↓
[POST /donations/pay/ with JWT token] → Middleware (Verify Token) → View → Serializer Validation
    ↓
Generate Transaction Reference (Signal)
    ↓
Save to Database
    ↓
Response (Donation Created with Reference)
```

### History Retrieval Flow
```
Authenticated User
    ↓
[GET /donations/my-history/ with JWT token] → Middleware (Verify Token) → View (Filter by user_id)
    ↓
QuerySet.filter(donor=request.user) → Pagination → Serialization
    ↓
Response (User's donations with pagination metadata)
```

### Stats Retrieval Flow
```
Any User (Authenticated or Public)
    ↓
[GET /donations/stats/] → View (No permission check)
    ↓
Aggregate.Sum('amount') + .count() + other calculations
    ↓
Cache result for 5 minutes (optional)
    ↓
Response (Statistics)
```

---

## 12. Development vs. Production Settings

### Development Configuration
```python
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
JWT_EXPIRATION_DELTA_ACCESS = timedelta(minutes=5)
JWT_EXPIRATION_DELTA_REFRESH = timedelta(days=1)
```

### Production Configuration
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
```

---

## 13. Implementation Sequence

### Phase 1: Foundation (Week 1)
1. Django project setup with custom User model
2. JWT authentication endpoints (register, login, refresh)

### Phase 2: Core Features (Week 2)
1. Donation model and migrations
2. Transaction reference generation
3. Donation submission endpoint

### Phase 3: Reports & Tracking (Week 3)
1. Stats aggregation and endpoint
2. Donation history endpoint with filtering
3. Django Admin configuration

### Phase 4: Polish & Deployment (Week 4)
1. Unit and integration tests
2. API documentation (Swagger)
3. Security hardening
4. Deployment preparation

---

## 14. Testing Strategy

### Unit Tests
- Model validation (amounts, duplicates, cascades)
- Transaction reference uniqueness
- User model password hashing

### Integration Tests
- POST /auth/register/ with valid/invalid data
- POST /auth/login/ with correct/incorrect credentials
- POST /donations/pay/ with/without authentication
- GET /donations/my-history/ filtering and pagination
- GET /donations/stats/ aggregation accuracy

### Permission Tests
- Unauthenticated users cannot access private endpoints
- Users cannot view other users' donations
- Only donors can submit donations (not public)

### Edge Cases
- Concurrent donation submissions
- Large donation amounts (decimal precision)
- Expired/invalid JWT tokens
- Non-existent user queries

---

## 15. API Documentation Endpoint

### Swagger UI
```
GET /api/schema/swagger-ui/
```
Auto-generated interactive documentation with try-it-out feature.

### ReDoc
```
GET /api/schema/redoc/
```
Alternative API documentation interface.

### OpenAPI Schema
```
GET /api/schema/
```
Raw OpenAPI 3.0 schema (JSON).

---

This design document serves as the blueprint for implementation. All endpoints, models, validations, and workflows are defined before any code is written.
