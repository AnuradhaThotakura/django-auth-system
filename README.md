# Django Authentication API

## Project Overview
This project is a Django-based authentication system with cookie-based authentication. It includes user registration, login, logout, and a protected endpoint to retrieve user details. It also integrates Swagger for API documentation and CSRF protection.

## Features
- User registration with email verification (OTP-based)
- User login with secure, HTTP-only cookie-based authentication
- Protected user details API requiring authentication
- Secure logout functionality
- CSRF protection with automatic token generation
- Swagger API documentation

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- PostgreSQL or SQLite (default)
- pip (Python package manager)
- Git (for version control)

### Setup Instructions

1. **Clone the Repository**:
   ```sh
   git clone <YOUR_REPOSITORY_URL>
   cd auth_project
   ```

2. **Create and Activate a Virtual Environment**:
   ```sh
   python3 -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate    # On Windows
   ```

3. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:
   ```sh
   python manage.py migrate
   ```

5. **Run the Development Server**:
   ```sh
   python manage.py runserver
   ```

6. **Access API Documentation**:
   Open [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/) in your browser.

## API Endpoints

| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/api/register/` | Register a new user |
| POST | `/api/register/verify/` | Verify user registration via OTP |
| POST | `/api/login/` | Log in and receive authentication token (in a cookie) |
| GET | `/api/me/` | Get logged-in user details (requires authentication) |
| POST | `/api/logout/` | Log out and clear authentication token |

## Environment Variables
Create a `.env` file in the root directory and configure:
```
SECRET_KEY=your_secret_key_here
DEBUG=True
DATABASE_URL=your_database_url_here
EMAIL_HOST_USER=your_email_here
EMAIL_HOST_PASSWORD=your_email_password_here
```

## Deployment
To deploy using Gunicorn and Nginx:
```sh
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 auth_project.wsgi:application
```

## Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch`).
3. Commit changes (`git commit -m "Added a new feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.


✅ Security Measures Implemented

   OTP Verification for Registration

      A one-time password (OTP) is generated and sent to the user's email.

      The user must verify their email before logging in.

      This helps prevent unauthorized account creation. ✅

   Secure Cookie-Based Authentication

      The login API sets an auth_token in an HTTP-only, secure cookie. ✅

      This prevents JavaScript-based XSS attacks from accessing the token. ✅

   Logout Mechanism

      The logout API clears the auth_token from cookies. ✅

      This ensures that users are properly logged out and prevents session reuse. ✅

   CSRF Protection

      There is a dedicated API (CSRFTokenView) to generate CSRF tokens. ✅

      However, CSRF protection for login, logout, and other views should be explicitly enabled using Django’s middleware.