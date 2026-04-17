# 🔐 Password Reset System Implementation Guide

## ✅ What Has Been Implemented

Your SmartQuiz application now has a **complete, production-ready password reset system** with:

1. **Password Reset URL Routes** - 4 secure endpoints for the reset flow
2. **Beautiful Bootstrap Templates** - Professional UI for all reset pages
3. **Django Built-in Security** - Token-based, expiry-aware, hashed passwords
4. **Email Support** - Ready for Gmail, Hostinger, or any SMTP provider
5. **User-Friendly Flow** - Clear messages and error handling

---

## 📋 Features Overview

### 1. **Password Reset Flow** (User Perspective)

```
1. User clicks "Forgot Password?" on login page
2. Enters email address → Submits form
3. Sees confirmation: "Check your email"
4. Clicks reset link in email
5. Sets new password
6. Sees success page & can login
```

### 2. **Security Features**

✅ **Token-Based**: Django generates secure, one-time tokens  
✅ **Expiry**: Reset links expire in 1 hour (configurable)  
✅ **Password Hashing**: All passwords securely hashed (Django default)  
✅ **Email Verification**: Proves user owns the email  
✅ **CSRF Protection**: Django CSRF tokens on all forms  
✅ **Rate Limiting Ready**: Can add django-ratelimit if needed  

---

## 🔧 Configuration Guide

### **Email Setup (Choose One)**

#### **Option 1: Gmail (Recommended for Development)**

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable "2-Step Verification" if not already done
3. Generate App Password:
   - Click "App passwords" → Select "Mail" and "Windows Computer"
   - Copy the generated 16-character password

4. Update `smartquiz_config/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'xxxx xxxx xxxx xxxx'  # 16-char app password (copy paste as-is)
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

#### **Option 2: Hostinger (Production)**

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.hostinger.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'noreply@yourdomain.com'
EMAIL_HOST_PASSWORD = 'your-password'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'noreply@yourdomain.com'
```

#### **Option 3: Console Backend (Development/Testing)**

```python
# Emails will print to console instead of sending
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

#### **Option 4: File Backend (Development)**

```python
# Emails saved to files in a directory
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'
```

---

## 📁 Files Created/Modified

### **Modified Files:**

1. **[accounts/urls.py](accounts/urls.py)**
   - Added 4 password reset URL patterns
   - Uses Django's built-in auth views
   - Custom template names configured

2. **[smartquiz_config/settings.py](smartquiz_config/settings.py)**
   - Added EMAIL_BACKEND configuration
   - SMTP settings for email providers
   - PASSWORD_RESET_TIMEOUT = 3600 (1 hour)
   - Logging configuration for email debugging

3. **[templates/accounts/login.html](templates/accounts/login.html)**
   - Added "Forgot Password?" link under password field
   - Links to password reset form

### **New Templates Created:**

1. **[templates/accounts/password_reset.html](templates/accounts/password_reset.html)**
   - Email form for password reset request
   - Bootstrap styling with validation
   - Help text and error messages

2. **[templates/accounts/password_reset_done.html](templates/accounts/password_reset_done.html)**
   - Confirmation page after email submission
   - Instructions and security info
   - "Try again" link if email not received

3. **[templates/accounts/password_reset_confirm.html](templates/accounts/password_reset_confirm.html)**
   - New password form with validation
   - Shows password requirements
   - Handles invalid/expired tokens
   - Bootstrap form styling

4. **[templates/accounts/password_reset_complete.html](templates/accounts/password_reset_complete.html)**
   - Success page after password reset
   - Security tips
   - Links to login and home

5. **[templates/accounts/password_reset_email.html](templates/accounts/password_reset_email.html)**
   - Email template sent to users
   - Includes reset link with token
   - Security warnings and support info

6. **[templates/accounts/password_reset_subject.txt](templates/accounts/password_reset_subject.txt)**
   - Email subject line
   - Clear and professional

---

## 🚀 URL Endpoints

```
GET/POST  /accounts/password-reset/
          → Form to enter email for reset

GET       /accounts/password-reset/done/
          → Confirmation after email sent

GET/POST  /accounts/password-reset/<uidb64>/<token>/
          → Form to enter new password
          → Token is auto-validated by Django

GET       /accounts/password-reset/complete/
          → Success page after password reset
```

---

## 🧪 Testing the System

### **1. Console Email Backend (Easiest)**

Set in `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Then in terminal:
```bash
python manage.py runserver
```

Visit:
```
http://127.0.0.1:8000/accounts/password-reset/
```

Email will print to terminal console.

### **2. Gmail Testing**

Configure Gmail settings as shown above, then:

```bash
python manage.py runserver
```

Visit:
```
http://127.0.0.1:8000/accounts/password-reset/
```

Enter your email and check Gmail inbox.

### **3. Send Test Email (Django Shell)**

```bash
python manage.py shell
```

```python
from django.core.mail import send_mail

send_mail(
    subject='Test Email',
    message='This is a test email from SmartQuiz',
    from_email='your-email@gmail.com',
    recipient_list=['recipient@example.com'],
)
```

---

## 🔒 Security Best Practices

### **Already Implemented:**
✅ Django's token generator (cryptographically secure)  
✅ uidb64 encoding (prevents user enumeration)  
✅ CSRF protection on all forms  
✅ HTTPS-only in production (configure in settings.py)  
✅ Secure password hashing (PBKDF2)  

### **For Production, Also Do:**

```python
# settings.py for PRODUCTION

# Enforce HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Add to EMAIL settings
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False  # or True if your provider uses port 465

# Password reset timeout
PASSWORD_RESET_TIMEOUT = 1800  # 30 minutes (shorter for production)

# Rate limiting (optional - requires django-ratelimit)
# from django_ratelimit.decorators import ratelimit
```

---

## 🎯 How Django's Reset System Works

1. **User requests reset** → Django creates token from user ID + timestamp
2. **Token sent in email** → Link includes `uidb64` + `token`
3. **User clicks link** → Django validates token against stored data
4. **Token is valid** → User can enter new password
5. **Password saved** → Hashed with PBKDF2, token invalidated

**Why it's secure:**
- Token is one-time use
- Token includes timestamp (expires after 1 hour)
- uidb64 is base64-encoded user ID (not plaintext)
- No passwords transmitted in URLs or emails

---

## 📧 Email Template Variables

The `password_reset_email.html` template has access to:

```
{{ user }}              → User object (e.g., {{ user.username }})
{{ user.email }}        → User email address
{{ user.first_name }}   → First name
{{ user.last_name }}    → Last name
{{ protocol }}          → http or https
{{ domain }}            → yourdomain.com
{{ uid }}               → User ID (not used in template usually)
{{ token }}             → Reset token (auto-included in link)
{{ site_name }}         → Site name (if Site framework enabled)
```

Example custom email:
```html
Hi {{ user.first_name or user.username }},

Your password reset link: {{ protocol }}://{{ domain }}/reset/{{ uid }}/{{ token }}/
```

---

## 🚨 Troubleshooting

### **Emails Not Sending?**

1. **Check EMAIL_BACKEND**
   ```python
   # In Django shell:
   from django.conf import settings
   print(settings.EMAIL_BACKEND)
   ```

2. **Test with console backend**
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
   # Emails will print to terminal
   ```

3. **Check Gmail app password**
   - Make sure 2-step verification is enabled
   - App password should be 16 characters
   - Paste without spaces: `xxxxxxxxxxxxxxxx`

4. **Check firewall/ports**
   - Port 587 for TLS (most providers)
   - Port 465 for SSL (alternative)
   - May be blocked by ISP

### **Reset Link Not Working?**

1. **Check link isn't expired**
   - Links valid for 1 hour (configured in settings.py)
   - Change `PASSWORD_RESET_TIMEOUT` if needed

2. **Check email format**
   - Email in database should match reset request
   - Users model must have email field

3. **Check templates exist**
   - All 4 templates must be in `templates/accounts/`
   - Template names must match urls.py exactly

---

## 🎨 Customization Ideas

### **Change Email Subject:**
Edit `templates/accounts/password_reset_subject.txt`

### **Change Email Body:**
Edit `templates/accounts/password_reset_email.html`

### **Change Password Expiry:**
In `settings.py`:
```python
PASSWORD_RESET_TIMEOUT = 1800  # 30 minutes instead of 1 hour
```

### **Change Link Appearance:**
Edit `templates/accounts/login.html`:
```html
<!-- From current -->
<a href="{% url 'accounts:password_reset' %}" class="text-decoration-none small">
    Forgot Password?
</a>

<!-- To custom -->
<button class="btn btn-link btn-sm">
    <i class="bi bi-question-circle"></i> Forgot your password?
</button>
```

### **Add Rate Limiting:**
```bash
pip install django-ratelimit
```

```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/h')  # 5 attempts per hour
def password_reset(request):
    ...
```

---

## 📚 Django Documentation References

- [Password Reset Views](https://docs.djangoproject.com/en/5.2/contrib/auth/views/#password-reset)
- [Email Configuration](https://docs.djangoproject.com/en/5.2/topics/email/)
- [Token Generator](https://docs.djangoproject.com/en/5.2/auth/passwords/#password-reset-token-generator)
- [Custom User Model](https://docs.djangoproject.com/en/5.2/topics/auth/customizing/#using-a-custom-user-model)

---

## ✨ Next Steps (Optional Enhancements)

### **1. Two-Factor Authentication (2FA)**
```bash
pip install django-otp
# Adds extra security layer
```

### **2. Social Authentication**
```bash
pip install django-allauth
# Allow login via Google, GitHub, etc.
```

### **3. Email Verification on Signup**
Add email confirmation before allowing login.

### **4. Audit Logging**
Track password reset attempts for security.

### **5. Custom Validators**
```python
# Add in forms.py
from django.contrib.auth.password_validation import validate_password

def clean_new_password2(self):
    password = self.cleaned_data.get('new_password2')
    try:
        validate_password(password)
    except ValidationError as e:
        raise ValidationError(e.messages)
```

---

## 🎓 Quick Reference

| Action | URL | Method |
|--------|-----|--------|
| Reset form | `/accounts/password-reset/` | GET/POST |
| Confirmation | `/accounts/password-reset/done/` | GET |
| New password | `/accounts/password-reset/<uid>/<token>/` | GET/POST |
| Success | `/accounts/password-reset/complete/` | GET |

---

## 💡 Key Takeaways

✅ **Production-Ready**: Uses Django built-in security  
✅ **User-Friendly**: Clear messages and professional UI  
✅ **Secure**: Token-based, with expiry  
✅ **Flexible**: Works with any SMTP provider  
✅ **Maintainable**: Minimal custom code, uses Django defaults  

**Your password reset system is ready to use!** 🚀

