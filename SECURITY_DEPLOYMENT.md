# Upendo Charity - Security & Deployment Guide

## Security Checklist

### Authentication Security

✅ **Password Requirements**
- Minimum 8 characters
- Must contain: uppercase, lowercase, number, special character
- Hashed using Django's PBKDF2 algorithm
- Never transmitted in plain text

✅ **JWT Token Security**
- Access tokens: 5-minute expiration
- Refresh tokens: 24-hour expiration
- Tokens are cryptographically signed (HS256 algorithm)
- Invalid tokens are rejected by middleware
- Tokens contain immutable claims (user_id, exp, iat)

✅ **Password Reset** (Future Enhancement)
- Generate secure reset tokens
- Expire tokens after 24 hours
- Send via email only
- Require password change confirmation

---

### Data Protection

✅ **Database Security**
- Foreign key constraints prevent orphaned records
- Cascading deletes remove user data on account deletion
- Transaction references are immutable (no updates allowed)
- Amounts use DECIMAL type (no floating-point errors)

✅ **Sensitive Data Handling**
- Passwords never logged or exposed in responses
- Email addresses validated but not exposed unnecessarily
- Donation messages treated as user content (sanitized on display)
- Database credentials stored in environment variables only

✅ **SQL Injection Prevention**
- Django ORM parameterizes all queries
- No raw SQL execution
- Input validated at serializer level before DB interaction

---

### API Security

✅ **CORS Configuration**
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Dev
    "https://upendo-frontend.com",  # Production
]
# Prevent requests from unauthorized origins
```

✅ **CSRF Protection**
- CSRF middleware enabled for state-changing requests
- CSRF tokens required for POST/PUT/DELETE if using sessions
- API uses JWT (stateless), so CSRF tokens aren't needed for JSON POST

✅ **Rate Limiting**
- Implement rate limiting on:
  - `/auth/register/` — 5 requests per hour per IP
  - `/auth/login/` — 5 failed attempts per 15 minutes
  - `/donations/pay/` — 100 requests per hour per user
- Use `djangorestframework-extensions` for implementation

✅ **Input Validation**
- Amount: Must be 0.01 - 999,999.99
- Message: Max 500 characters, plain text only
- Username: 3-150 alphanumeric + underscore
- Email: RFC 5322 compliant

✅ **Response Security**
- No stack traces in production (DEBUG=False)
- Generic error messages for failed auth
- No server information in response headers
- UUID or random IDs (never sequential) for resources

---

### Infrastructure Security

✅ **HTTPS/TLS**
- All production traffic must use HTTPS
- Force HTTPS redirect in Django:
  ```python
  SECURE_SSL_REDIRECT = True
  SESSION_COOKIE_SECURE = True
  CSRF_COOKIE_SECURE = True
  ```

✅ **Security Headers**
```python
# settings.py
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
}
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = "DENY"
```

✅ **Environment Variables**
- All secrets stored in `.env` file
- `.env` not committed to version control
- Required variables:
  - `SECRET_KEY` — Django secret (50+ chars, random)
  - `DEBUG` — Always False in production
  - `DB_PASSWORD` — Database password
  - `JWT_SECRET_KEY` — JWT signing key
  - `ALLOWED_HOSTS` — Domain whitelist

✅ **Dependency Security**
- Regular updates to Django and dependencies
- Use `pip audit` to check for vulnerabilities
- Pin versions in requirements.txt
- Use software composition analysis tools (Snyk, dependabot)

---

### Admin Interface Security

✅ **Admin Access Control**
- Admin panel behind `/admin/` path
- Only accessible by staff users (is_staff=True)
- Require strong passwords for admin accounts
- Consider 2FA (Two-Factor Authentication) for admins

✅ **Admin Audit Trail**
- Log all admin actions (Django supports this)
- Track: who changed what, when, why
- Implement admin action logging:
  ```python
  class DonationAdmin(admin.ModelAdmin):
      change_list_template = "admin/change_list.html"
      list_display = ('id', 'donor', 'amount', 'timestamp')
      readonly_fields = ('transaction_reference', 'timestamp')
      search_fields = ('transaction_reference', 'donor__email')
  ```

---

### Logging & Monitoring

✅ **Security Logging**
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'security.log',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
```

✅ **Events to Monitor**
- Failed login attempts (3+ per user per hour = alert)
- Register attempts with duplicate email (potential abuse)
- Large donation amounts (fraud detection)
- Invalid JWT tokens (attack attempts)
- Admin account changes

---

## Deployment Guide

### Pre-Deployment Checklist

- [ ] All tests passing (pytest)
- [ ] Code coverage > 80%
- [ ] No sensitive data in code
- [ ] Environment variables configured
- [ ] Database migrations reviewed
- [ ] Security headers configured
- [ ] CORS origins verified
- [ ] API documentation updated
- [ ] Load testing completed

---

### Deployment Steps

#### 1. Environment Setup
```bash
# Create .env from template
cp .env.example .env

# Update .env with production values
DATABASE_URL=postgresql://user:pass@host:5432/upendo_db
SECRET_KEY=<generate-50-char-random-string>
JWT_SECRET_KEY=<generate-50-char-random-string>
DEBUG=False
ALLOWED_HOSTS=upendo.org,www.upendo.org
```

#### 2. Database Setup (Production)
```bash
# Create database (in PostgreSQL)
CREATE DATABASE upendo_db;
CREATE USER upendo_user WITH PASSWORD 'secure_password';
ALTER ROLE upendo_user SET client_encoding TO 'utf8';
ALTER ROLE upendo_user SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE upendo_db TO upendo_user;
```

#### 3. Django Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Run tests
pytest --cov=.

# Start gunicorn server
gunicorn upendo_project.wsgi:application --workers 4 --bind 0.0.0.0:8000
```

#### 4. Web Server Configuration (Nginx)
```nginx
upstream django {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name upendo.org www.upendo.org;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name upendo.org www.upendo.org;
    
    # SSL certificates
    ssl_certificate /etc/ssl/certs/upendo_cert.pem;
    ssl_certificate_key /etc/ssl/private/upendo_key.pem;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    client_max_body_size 10M;
    
    location /api/ {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /admin/ {
        proxy_pass http://django;
        proxy_set_header Host $host;
    }
    
    location /static/ {
        alias /var/www/upendo/static/;
        expires 30d;
    }
    
    location / {
        root /var/www/upendo-frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
```

#### 5. Systemd Service File
```ini
[Unit]
Description=Upendo Charity Django Application
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/upendo
Environment="PATH=/var/www/upendo/venv/bin"
EnvironmentFile=/var/www/upendo/.env
ExecStart=/var/www/upendo/venv/bin/gunicorn \
    --workers 4 \
    --bind 127.0.0.1:8000 \
    --error-logfile /var/log/upendo/gunicorn_error.log \
    --access-logfile /var/log/upendo/gunicorn_access.log \
    upendo_project.wsgi:application

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 6. Enable and Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable upendo
sudo systemctl start upendo
sudo systemctl status upendo
```

---

### Database Backup Strategy

#### Automated Daily Backups
```bash
#!/bin/bash
# backup_db.sh
BACKUP_DIR="/backups/upendo"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

pg_dump upendo_db | gzip > "$BACKUP_DIR/upendo_$TIMESTAMP.sql.gz"

# Keep only last 30 days of backups
find $BACKUP_DIR -type f -mtime +30 -delete

# Upload to cloud storage (AWS S3, Google Cloud, etc.)
aws s3 cp "$BACKUP_DIR/upendo_$TIMESTAMP.sql.gz" s3://upendo-backups/
```

#### Restore from Backup
```bash
# Restore from backup
gunzip < upendo_20260207_143000.sql.gz | psql upendo_db
```

---

### Monitoring & Alerts

#### Health Check Endpoint (Optional Enhancement)
```python
# views.py
def health_check(request):
    """Simple health check for load balancers"""
    try:
        connection.ensure_connection()
        return JsonResponse({'status': 'healthy'})
    except:
        return JsonResponse({'status': 'unhealthy'}, status=500)
```

#### Uptime Monitoring
- Use services like Uptime Robot, DataDog, or New Relic
- Monitor:
  - API response times (target < 200ms)
  - Error rates (target < 1%)
  - Database query performance
  - Server CPU/Memory usage
  - Disk space

#### Log Aggregation
- Collect logs from:
  - Django application
  - Nginx
  - PostgreSQL
  - Systemd/journalctl
- Tools: ELK Stack, Splunk, Datadog, CloudWatch

---

### Rollback Procedure

If deployment has critical issues:

```bash
# 1. Stop current service
sudo systemctl stop upendo

# 2. Revert code to previous tag
git checkout <previous-tag>

# 3. Revert database if needed
psql upendo_db < backup_20260206.sql.gz

# 4. Restart service
sudo systemctl start upendo

# 5. Verify health
curl https://upendo.org/api/donations/stats/
```

---

### Performance Optimization

#### Caching Strategy
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Cache stats for 5 minutes
@cache_page(60 * 5)
def stats_view(request):
    ...
```

#### Database Optimization
- Use select_related() for foreign keys
- Use prefetch_related() for reverse relations
- Add database indexes on frequently queried fields
- Monitor slow queries with Django Debug Toolbar (dev only)

#### Load Balancing
```
Frontend
   ↓
Load Balancer (Nginx, HAProxy)
   ↓
[Server 1] [Server 2] [Server 3]
   ↓
Shared Database (PostgreSQL)
   ↓
Redis Cache
```

---

### Disaster Recovery Plan

| Scenario | Recovery Time |Response |
|----------|---------------|---------|
| Single server failure | 5 min | Failover to backup server |
| Database corruption | 15 min | Restore from latest backup |
| Security breach | 30 min | Rotate secrets, scan logs |
| Data loss | 1 hour | Restore from daily backup |
| Total outage | 2 hours | Full infrastructure rebuild |

---

### Version Control

#### Tagging for Deployment
```bash
# Tag release versions
git tag -a v1.0.0 -m "Production release v1.0.0"
git push origin v1.0.0

# Deploy specific version
git checkout v1.0.0
```

#### Semantic Versioning
- **v1.0.0** — Major.Minor.Patch
- Major: Breaking changes
- Minor: New features
- Patch: Bug fixes

---

## Post-Deployment

1. **Smoke Testing**
   - Test register endpoint
   - Test login endpoint
   - Test donation submission
   - Test stats endpoint

2. **Monitoring**
   - Check error logs
   - Monitor response times
   - Verify all endpoints accessible
   - Check database connectivity

3. **Documentation Update**
   - Update API docs with new domain
   - Document deployment time
   - Record any issues encountered
   - Update runbooks

4. **Team Notification**
   - Notify stakeholders of successful deployment
   - Share release notes
   - Gather feedback
