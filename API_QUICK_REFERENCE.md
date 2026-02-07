# Upendo Charity API - Quick Reference

## Base URL
```
http://localhost:8000/api
```

## Authentication
All requests below marked with 🔒 require JWT access token in header:
```
Authorization: Bearer {access_token}
```

---

## Authentication Endpoints

### Register New Donor
```
POST /auth/register/
```
| Aspect | Details |
|--------|---------|
| **Auth** | Not required |
| **Body** | `{username, email, password, full_name}` |
| **Success** | 201 Created |
| **Error** | 400 (duplicate email/username), 422 (validation) |

---

### Login
```
POST /auth/login/
```
| Aspect | Details |
|--------|---------|
| **Auth** | Not required |
| **Body** | `{email, password}` |
| **Response** | `{access, refresh, user}` |
| **Success** | 200 OK |
| **Error** | 401 Unauthorized |

---

### Refresh Token 🔒
```
POST /auth/token/refresh/
```
| Aspect | Details |
|--------|---------|
| **Auth** | Not required (uses refresh token) |
| **Body** | `{refresh}` |
| **Response** | `{access}` (new access token) |
| **Success** | 200 OK |
| **Error** | 401 Unauthorized |

---

## Donation Endpoints

### Submit Donation 🔒
```
POST /donations/pay/
```
| Aspect | Details |
|--------|---------|
| **Auth** | Required |
| **Body** | `{amount: decimal, message?: string}` |
| **Response** | `{id, donor, amount, transaction_reference, timestamp, message}` |
| **Success** | 201 Created |
| **Error** | 400 (invalid amount), 401 (no token) |

**Validation:**
- Amount: 0.01 - 999,999.99
- Message: Optional, max 500 chars
- Transaction Reference: Auto-generated (TXN-YYYYMMDD-XXXXXX)

---

### Get Donation History 🔒
```
GET /donations/my-history/
```
| Aspect | Details |
|--------|---------|
| **Auth** | Required |
| **Query Params** | `?page=1&page_size=10` (optional) |
| **Response** | Paginated list `{count, next, previous, results}` |
| **Success** | 200 OK |
| **Error** | 401 (no token), 400 (invalid params) |

**Filters (Optional):**
```
?start_date=2026-01-01&end_date=2026-02-07
?ordering=-timestamp  # newest first (default)
```

---

### Get Fundraising Stats
```
GET /donations/stats/
```
| Aspect | Details |
|--------|---------|
| **Auth** | Not required (Public) |
| **Response** | `{total_amount_raised, total_donations, unique_donors, average_donation}` |
| **Success** | 200 OK |
| **Caching** | 5-minute TTL (optional) |

---

## Response Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Missing/invalid token |
| 403 | Forbidden - Authenticated but no permission |
| 404 | Not Found - Resource doesn't exist |
| 422 | Unprocessable Entity - Validation error |
| 500 | Server Error - Internal error |

---

## Error Response Format

### Validation Error
```json
{
  "amount": ["Ensure this value is greater than 0.00"],
  "message": ["Ensure this field has no more than 500 characters"]
}
```

### Authentication Error
```json
{
  "detail": "Invalid credentials",
  "status_code": 401
}
```

---

## Token Lifetimes

| Token | Lifetime | Usage |
|-------|----------|-------|
| Access | 5 minutes | API requests (Authorization header) |
| Refresh | 24 hours | Get new access token via /auth/token/refresh/ |

---

## Examples

### Register
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "full_name": "John Doe"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

### Submit Donation (with token)
```bash
curl -X POST http://localhost:8000/api/donations/pay/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "amount": 150.50,
    "message": "Supporting education"
  }'
```

### Get History (with token)
```bash
curl -X GET "http://localhost:8000/api/donations/my-history/?page=1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Get Stats (no token needed)
```bash
curl -X GET http://localhost:8000/api/donations/stats/
```

---

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Missing token | Add `Authorization: Bearer {token}` header |
| 400 Bad Request | Invalid amount | Use decimal format: 150.50 (not 150.5 or "150.50") |
| 422 Validation Error | Weak password | Password must include uppercase, lowercase, number, special char |
| Token expired | Access token > 5 min old | Use refresh endpoint with refresh token |
| CORS Error | Frontend not whitelisted | Add domain to `CORS_ALLOWED_ORIGINS` in settings |

---

## Development Testing

### Using Django Test Client
```python
from rest_framework.test import APIClient

client = APIClient()
response = client.post('/api/auth/register/', {
    'username': 'test_user',
    'email': 'test@example.com',
    'password': 'TestPass123!',
    'full_name': 'Test User'
})
```

### Using Swagger UI
Navigate to: `http://localhost:8000/api/schema/swagger-ui/`
- Try endpoints interactively
- View request/response schemas
- Test with real tokens

---

## Admin Interface

Access: `http://localhost:8000/admin/`
- Login with staff/admin credentials
- View/manage users
- View/search all donations
- Filter by date range
- Monitor statistics

