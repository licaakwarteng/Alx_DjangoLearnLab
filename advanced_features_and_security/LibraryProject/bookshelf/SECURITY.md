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

# Security Configuration for Bookshelf App

## Django Settings
- SECURE_SSL_REDIRECT = True → Forces HTTPS
- SECURE_HSTS_SECONDS = 31536000 → Enforces HTTPS for 1 year
- SECURE_HSTS_INCLUDE_SUBDOMAINS = True → Covers all subdomains
- SECURE_HSTS_PRELOAD = True → Allows inclusion in browser preload lists
- SESSION_COOKIE_SECURE = True → Session cookies only over HTTPS
- CSRF_COOKIE_SECURE = True → CSRF cookies only over HTTPS
- X_FRAME_OPTIONS = "DENY" → Prevents clickjacking
- SECURE_CONTENT_TYPE_NOSNIFF = True → Prevents MIME-sniffing
- SECURE_BROWSER_XSS_FILTER = True → Helps prevent XSS attacks

## Deployment
- Nginx configured to redirect HTTP → HTTPS
- Let’s Encrypt SSL certificates installed with Certbot
- TLS 1.2 and TLS 1.3 enforced for secure connections

## Review & Testing
- Verified that HTTP requests are redirected to HTTPS
- Checked that secure cookies are only sent over HTTPS
- Confirmed CSP, HSTS, and security headers in browser dev tools
- Areas for improvement: 
  - Add Content Security Policy (CSP) for stricter script/style loading
  - Enable logging for unauthorized access attempts
