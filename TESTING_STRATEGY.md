# Upendo Charity - Testing Strategy & Test Plan

## Testing Overview

The project will follow Test-Driven Development (TDD) with comprehensive coverage across all layers:
- **Unit Tests:** Model validation, utility functions
- **Integration Tests:** API endpoints, database operations
- **Permission Tests:** Authentication and authorization
- **Edge Case Tests:** Boundary conditions, concurrent operations

---

## Test Structure

```
tests/
├── __init__.py
├── conftest.py              # pytest fixtures and configuration
├── test_auth.py            # Authentication endpoint tests
├── test_donations.py       # Donation endpoint tests
├── test_permissions.py     # Permission and authorization tests
├── test_models.py          # Model validation tests
├── test_serializers.py     # Serializer validation tests
└── test_utils.py           # Utility function tests
```

---

## Testing Framework Setup

### Tools Used
```
pytest                      # Testing framework
pytest-django              # Django integration for pytest
pytest-cov                 # Code coverage reporting
factory-boy                # Test data factories
freezegun                  # Time/date mocking
```

### Configuration (conftest.py)
```python
# Fixtures for common test data
@pytest.fixture
def test_user():
    """Create a test user"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='TestPass123!',
        full_name='Test User'
    )

@pytest.fixture
def authenticated_client(test_user):
    """Return client with authenticated user"""
    client = APIClient()
    refresh = RefreshToken.for_user(test_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client

@pytest.fixture
def donation_data():
    """Sample donation data"""
    return {'amount': '150.50', 'message': 'Test donation'}
```

---

## Unit Tests

### Model Tests (test_models.py)

#### User Model Tests
```python
def test_custom_user_creation():
    """Test creating a custom user with all fields"""
    user = User.objects.create_user(
        username='john_doe',
        email='john@example.com',
        password='SecurePass123!',
        full_name='John Doe'
    )
    assert user.full_name == 'John Doe'
    assert user.is_active == True
    assert user.check_password('SecurePass123!')

def test_duplicate_email_raises_error():
    """Test that duplicate emails raise an error"""
    User.objects.create_user(
        email='john@example.com',
        username='user1',
        password='Pass123!'
    )
    with pytest.raises(IntegrityError):
        User.objects.create_user(
            email='john@example.com',
            username='user2',
            password='Pass123!'
        )

def test_duplicate_username_raises_error():
    """Test that duplicate usernames raise an error"""
    User.objects.create_user(
        username='john_doe',
        email='user1@example.com',
        password='Pass123!'
    )
    with pytest.raises(IntegrityError):
        User.objects.create_user(
            username='john_doe',
            email='user2@example.com',
            password='Pass123!'
        )
```

#### Donation Model Tests
```python
def test_donation_creation(test_user):
    """Test creating a donation"""
    donation = Donation.objects.create(
        donor=test_user,
        amount=Decimal('150.50'),
        transaction_reference='TXN-20260207-ABC123',
        message='Test donation'
    )
    assert donation.donor == test_user
    assert donation.amount == Decimal('150.50')

def test_transaction_reference_unique(test_user):
    """Test that transaction references must be unique"""
    Donation.objects.create(
        donor=test_user,
        amount=Decimal('100.00'),
        transaction_reference='TXN-20260207-ABC123'
    )
    with pytest.raises(IntegrityError):
        Donation.objects.create(
            donor=test_user,
            amount=Decimal('200.00'),
            transaction_reference='TXN-20260207-ABC123'
        )

def test_donation_cascade_delete(test_user):
    """Test that deleting a user deletes their donations"""
    donation = Donation.objects.create(
        donor=test_user,
        amount=Decimal('100.00'),
        transaction_reference='TXN-20260207-ABC123'
    )
    test_user.delete()
    assert Donation.objects.filter(id=donation.id).count() == 0

def test_negative_amount_validation():
    """Test that negative amounts are rejected"""
    # This is handled at serializer level
    serializer = DonationSerializer(data={
        'amount': '-50.00',
        'message': 'Invalid'
    })
    assert not serializer.is_valid()
    assert 'amount' in serializer.errors
```

---

## Integration Tests

### Authentication Endpoint Tests (test_auth.py)

#### Registration Tests
```python
class TestUserRegistration:
    """Test user registration endpoint"""
    
    def test_register_success(self, client):
        """Test successful user registration"""
        response = client.post('/api/auth/register/', {
            'username': 'john_doe',
            'email': 'john@example.com',
            'password': 'SecurePass123!',
            'full_name': 'John Doe'
        })
        assert response.status_code == 201
        assert response.data['username'] == 'john_doe'
        assert response.data['email'] == 'john@example.com'
        assert User.objects.filter(email='john@example.com').exists()

    def test_register_duplicate_email(self, client, test_user):
        """Test registration with duplicate email"""
        response = client.post('/api/auth/register/', {
            'username': 'another_user',
            'email': test_user.email,  # Duplicate
            'password': 'SecurePass123!',
            'full_name': 'Another User'
        })
        assert response.status_code == 400
        assert 'email' in response.data

    def test_register_weak_password(self, client):
        """Test registration with weak password"""
        response = client.post('/api/auth/register/', {
            'username': 'weak_user',
            'email': 'weak@example.com',
            'password': '123456',  # Weak password
            'full_name': 'Weak User'
        })
        assert response.status_code == 400
        assert 'password' in response.data

    def test_register_missing_fields(self, client):
        """Test registration with missing required fields"""
        response = client.post('/api/auth/register/', {
            'username': 'incomplete'
            # Missing email, password, full_name
        })
        assert response.status_code == 400
        assert 'email' in response.data
        assert 'password' in response.data
```

#### Login Tests
```python
class TestUserLogin:
    """Test user login endpoint"""
    
    def test_login_success(self, client, test_user):
        """Test successful login"""
        response = client.post('/api/auth/login/', {
            'email': test_user.email,
            'password': 'password123'  # Default test_user password
        })
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert response.data['user']['id'] == test_user.id

    def test_login_invalid_credentials(self, client, test_user):
        """Test login with wrong password"""
        response = client.post('/api/auth/login/', {
            'email': test_user.email,
            'password': 'wrongpassword'
        })
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent email"""
        response = client.post('/api/auth/login/', {
            'email': 'nonexistent@example.com',
            'password': 'anypassword'
        })
        assert response.status_code == 401

    def test_token_refresh(self, client, test_user):
        """Test token refresh"""
        # Get tokens
        login_response = client.post('/api/auth/login/', {
            'email': test_user.email,
            'password': 'password123'
        })
        refresh_token = login_response.data['refresh']
        
        # Refresh access token
        response = client.post('/api/auth/token/refresh/', {
            'refresh': refresh_token
        })
        assert response.status_code == 200
        assert 'access' in response.data
```

---

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_auth.py
```

### Run with Coverage Report
```bash
pytest --cov=. --cov-report=html
```

### Run with Verbose Output
```bash
pytest -v
```

---

## Coverage Goals

- **Overall:** Minimum 80% code coverage
- **Models:** 100% coverage
- **Views:** 85% coverage
- **Serializers:** 90% coverage
- **Utilities:** 90% coverage

---

## Continuous Integration

Tests will run automatically on:
- Every git push
- Every pull request
- Before deployment to production

Failing tests block merges and deployments.
