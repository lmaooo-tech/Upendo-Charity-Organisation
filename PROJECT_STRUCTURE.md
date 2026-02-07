# Upendo Charity Project Structure & File Organization

## Complete Project Directory Layout

```
upendo-charity/
│
├── 📄 manage.py                    # Django management script
├── 📄 requirements.txt             # Python dependencies
├── 📄 .env.example                 # Environment variables template
├── 📄 .gitignore                   # Git ignore rules
├── 📄 README.md                    # Project documentation
│
├── 📁 upendo_project/              # Main project settings package
│   ├── __init__.py
│   ├── 📄 settings.py              # Core Django settings
│   ├── 📄 urls.py                  # Main URL router
│   ├── 📄 wsgi.py                  # WSGI entrypoint
│   └── 📄 asgi.py                  # ASGI entrypoint (optional)
│
├── 📁 accounts/                    # User authentication app
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── 📄 models.py                # Custom User model
│   ├── 📄 serializers.py           # User serializers (Register, Login)
│   ├── 📄 views.py                 # Authentication views (register, login, refresh)
│   ├── 📄 urls.py                  # Auth endpoints routing
│   ├── 📄 admin.py                 # User admin configuration
│   └── 📄 apps.py                  # App configuration
│
├── 📁 donations/                   # Donation management app
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── 📄 models.py                # Donation model
│   ├── 📄 serializers.py           # Donation serializers
│   ├── 📄 views.py                 # Donation views (pay, history, stats)
│   ├── 📄 urls.py                  # Donation endpoints routing
│   ├── 📄 admin.py                 # Donation admin configuration
│   ├── 📄 managers.py              # Custom model managers
│   ├── 📄 utils.py                 # Utility functions (ref generation)
│   ├── 📄 signals.py               # Signal handlers (auto-generate references)
│   ├── 📄 apps.py                  # App configuration
│   └── 📄 filters.py               # Django-filter configurations
│
├── 📁 api/                         # API configuration package
│   ├── __init__.py
│   ├── 📄 urls.py                  # Main API URL routing
│   ├── 📄 permissions.py           # Custom permission classes
│   ├── 📄 pagination.py            # Pagination configuration
│   ├── 📄 renderers.py             # Custom response renderers
│   └── 📄 exceptions.py            # Custom exception handlers
│
├── 📁 tests/                       # Test suite
│   ├── __init__.py
│   ├── 📄 test_auth.py             # Auth endpoint tests
│   ├── 📄 test_donations.py        # Donation endpoint tests
│   ├── 📄 test_permissions.py      # Permission tests
│   ├── 📄 test_models.py           # Model tests
│   ├── 📄 test_serializers.py      # Serializer tests
│   └── 📄 conftest.py              # pytest fixtures and configuration
│
├── 📁 docs/                        # Documentation
│   ├── 📄 API_SPECIFICATION.md     # Detailed API spec
│   ├── 📄 DEPLOYMENT_GUIDE.md      # Deployment instructions
│   ├── 📄 TROUBLESHOOTING.md       # Common issues
│   └── 📄 DEVELOPMENT_SETUP.md     # Local development setup
│
├── 📁 static/                      # Static files (CSS, JS, images)
│   └── (placeholder for production static files)
│
└── 📁 media/                       # User-uploaded files
    └── (placeholder for production uploads)
```

---

## File Responsibilities

### 📄 **accounts/models.py**
**Purpose:** Define the custom User model
```python
- CustomUser (extends AbstractUser)
  - username, email, password (inherited)
  - full_name (custom field)
  - is_staff, is_active, date_joined (inherited)
```

### 📄 **accounts/serializers.py**
**Purpose:** Handle user data serialization for API
```python
- UserSerializer (list user info)
- RegisterSerializer (validate registration input)
- LoginSerializer (validate login credentials)
```

### 📄 **accounts/views.py**
**Purpose:** Handle authentication business logic
```python
- RegisterView (POST /auth/register/)
- LoginView (POST /auth/login/)
- TokenRefreshView (POST /auth/token/refresh/)
```

### 📄 **donations/models.py**
**Purpose:** Define Donation model
```python
- Donation
  - id (PK)
  - donor (FK → User)
  - amount (DecimalField)
  - transaction_reference (Unique CharField)
  - message (TextField, optional)
  - timestamp (DateTimeField, auto_now_add)
```

### 📄 **donations/serializers.py**
**Purpose:** Handle donation data serialization
```python
- DonationSerializer (create donations, list donations)
- StatsSerializer (aggregate statistics)
- DonationHistorySerializer (list user's donations)
```

### 📄 **donations/views.py**
**Purpose:** Handle donation business logic
```python
- DonationPayView (POST /donations/pay/)
- DonationHistoryView (GET /donations/my-history/)
- StatsView (GET /donations/stats/)
```

### 📄 **donations/utils.py**
**Purpose:** Helper functions
```python
- generate_transaction_reference()
- validate_donation_amount()
- calculate_stats()
```

### 📄 **donations/signals.py**
**Purpose:** Auto-generate transaction references
```python
- pre_save signal handler to generate reference before saving
- post_save signal handler for logging/notifications (optional)
```

### 📄 **donations/managers.py**
**Purpose:** Custom model managers for queries
```python
- DonationManager
  - get_stats() → aggregate totals
  - get_user_history(user) → user's donations
```

### 📄 **donations/admin.py**
**Purpose:** Django Admin configuration
```python
- DonationAdmin (list display, filters, search)
- UserAdmin (list display, filters)
```

### 📄 **api/permissions.py**
**Purpose:** Custom permission classes
```python
- IsAuthenticatedOrPublic (allow public or authenticated)
- IsAuthenticated (only logged-in users)
- IsAdminUser (only staff users)
```

### 📄 **api/pagination.py**
**Purpose:** Pagination configuration
```python
- CustomPagination (page number pagination)
- PAGE_SIZE = 10 (default)
```

### 📄 **upendo_project/settings.py**
**Purpose:** Main Django configuration
```python
- INSTALLED_APPS configuration
- JWT settings
- CORS configuration
- Database configuration
- Authentication backend setup
- Logging configuration
```

### 📄 **upendo_project/urls.py**
**Purpose:** Main URL router
```python
- Include /api/ endpoints
- Include Django Admin
- Include Swagger/ReDoc docs
```

### 📄 **tests/test_auth.py**
**Purpose:** Test authentication endpoints
```python
- test_user_registration_success
- test_user_registration_duplicate_email
- test_login_success
- test_login_invalid_credentials
- test_token_refresh
```

### 📄 **tests/test_donations.py**
**Purpose:** Test donation endpoints
```python
- test_submit_donation_authenticated
- test_submit_donation_unauthenticated
- test_submit_invalid_amount
- test_get_donation_history
- test_get_stats_public
```

### 📄 **tests/test_permissions.py**
**Purpose:** Test permission enforcement
```python
- test_unauthenticated_cannot_donate
- test_cannot_view_others_history
- test_public_can_view_stats
```

---

## Database Schema Summary

### Users Table (accounts_customuser)
```
Column              | Type          | Constraints
--------------------|---------------|------------------
id                  | INT            | PRIMARY KEY
username            | VARCHAR(150)   | UNIQUE
email               | VARCHAR(254)   | UNIQUE
password            | VARCHAR(128)   | 
full_name           | VARCHAR(100)   | 
is_staff            | BOOLEAN        | DEFAULT FALSE
is_active           | BOOLEAN        | DEFAULT TRUE
date_joined         | TIMESTAMP      | AUTO NOW_ADD
last_login          | TIMESTAMP      | NULLABLE
```

### Donations Table (donations_donation)
```
Column                  | Type          | Constraints
------------------------|---|------------------
id                      | INT            | PRIMARY KEY
donor_id                | INT            | FK → users(id) ON DELETE CASCADE
amount                  | DECIMAL(10,2)  | POSITIVE
transaction_reference   | VARCHAR(50)    | UNIQUE
message                 | TEXT           | NULLABLE
timestamp               | TIMESTAMP      | AUTO NOW_ADD
```

### Indexes (for performance)
```
- donations(donor_id, timestamp DESC)
- donations(transaction_reference)
- users(email)
- donations(timestamp)
```

---

## Configuration Files

### **requirements.txt**
```
Django==4.2.0
djangorestframework==3.14.0
djangorestframework-simplejwt==5.2.2
django-cors-headers==4.0.0
psycopg2-binary==2.9.6
python-decouple==3.8
pytest==7.3.1
pytest-django==4.5.2
drf-spectacular==0.26.1
django-filter==23.1
```

### **.env.example**
```
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=upendo_db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_LIFETIME=5
JWT_REFRESH_TOKEN_LIFETIME=24

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Email Settings (optional, for notifications)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Redis (optional, for caching)
REDIS_URL=redis://localhost:6379/0
```

### **.gitignore**
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# Django
*.log
db.sqlite3
/media/
/static/

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

---

## Key Design Patterns Used

### 1. **Model-View-Serializer (MVS) Pattern**
- Models define database schema
- Serializers handle data validation and transformation
- Views orchestrate business logic

### 2. **Signal-Driven Reference Generation**
- Pre-save signal auto-generates transaction references
- Ensures unique references without manual intervention

### 3. **Permission-Based Access Control**
- Custom permission classes for fine-grained access
- Public vs. authenticated vs. admin endpoints

### 4. **Custom Managers**
- DonationManager simplifies complex queries
- Aggregation logic centralized in managers

### 5. **JWT-Based Stateless Authentication**
- No session storage needed
- Scalable across multiple servers
- Suitable for mobile apps and SPAs

---

## URL Routing Structure

```
/admin/                                 → Django Admin
/api/schema/swagger-ui/                → Swagger docs
/api/schema/redoc/                     → ReDoc docs
/api/schema/                           → OpenAPI schema

/api/auth/register/                    → POST (create user)
/api/auth/login/                       → POST (get tokens)
/api/auth/token/refresh/               → POST (refresh access token)

/api/donations/pay/                    → POST (submit donation)
/api/donations/my-history/             → GET (user's donations)
/api/donations/stats/                  → GET (public statistics)
```

---

## Development Workflow

1. **Create a feature branch:** `git checkout -b feature/new-feature`
2. **Write tests first** (TDD approach)
3. **Implement the feature**
4. **Run tests:** `pytest`
5. **Run linting:** `flake8`
6. **Commit:** `git commit -m "Add new feature"`
7. **Push:** `git push origin feature/new-feature`
8. **Create Pull Request**

---

## Important Notes

- **Custom User Model** is essential before any migrations
- **Transaction References** are immutable (generated at creation)
- **Donation Amount** uses DECIMAL field to avoid floating-point errors
- **JWT Tokens** are stateless (no database lookup for validation)
- **Admin Interface** is built-in Django feature, no custom UI needed
- **Permissions** are enforced at view level, not model level
