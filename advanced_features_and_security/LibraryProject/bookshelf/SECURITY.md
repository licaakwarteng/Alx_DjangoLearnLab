# Security Measures in Bookshelf App

1. DEBUG = False in production, ALLOWED_HOSTS restricted.
2. Browser protections enabled:
   - SECURE_BROWSER_XSS_FILTER
   - SECURE_CONTENT_TYPE_NOSNIFF
   - X_FRAME_OPTIONS = "DENY"
3. Cookies are secure: CSRF_COOKIE_SECURE, SESSION_COOKIE_SECURE.
4. All forms include `{% csrf_token %}`.
5. Database access uses Django ORM to prevent SQL injection.
6. CSP middleware enforces Content Security Policy.
