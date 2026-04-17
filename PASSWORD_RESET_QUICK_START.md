# ⚡ Password Reset - Quick Setup (5 Minutes)

## Step 1: Update Email Settings (2 min)

Choose your email provider:

### **Gmail Setup (Easiest for Testing)**

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable "2-Step Verification"
3. Generate App Password:
   - Click "App passwords"
   - Select "Mail" and "Windows Computer"
   - Copy the 16-character password

4. Update `smartquiz_config/settings.py` (already partially configured):

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your-email@gmail.com'              # ← Your Gmail
EMAIL_HOST_PASSWORD = 'xxxx xxxx xxxx xxxx'           # ← 16-char app password
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

### **Or Use Console Backend (No Email Setup Needed - Great for Testing)**

```python
# In settings.py - emails will print to terminal
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## Step 2: Verify Templates Exist ✅

All files already created in `templates/accounts/`:
- `password_reset.html`
- `password_reset_done.html`
- `password_reset_confirm.html`
- `password_reset_complete.html`
- `password_reset_email.html`
- `password_reset_subject.txt`

## Step 3: Verify URLs Configured ✅

Already added to `accounts/urls.py`:
- `/accounts/password-reset/`
- `/accounts/password-reset/done/`
- `/accounts/password-reset/<uidb64>/<token>/`
- `/accounts/password-reset/complete/`

## Step 4: Test It! 🧪

```bash
# Start server
python manage.py runserver

# Visit
http://127.0.0.1:8000/accounts/login/
```

Click **"Forgot Password?"** link on login page!

## Step 5: Test Email Sending (1 min)

### **Option A: Console Output (Easiest)**

```bash
python manage.py runserver
```

Go to `http://127.0.0.1:8000/accounts/password-reset/`  
Enter any email and submit → Check terminal for email output

### **Option B: Gmail**

Configure Gmail as above, then:
1. Go to `http://127.0.0.1:8000/accounts/password-reset/`
2. Enter your actual Gmail address
3. Check Gmail inbox for reset link
4. Click link and set new password

### **Option C: Django Shell Test**

```bash
python manage.py shell
```

```python
from django.core.mail import send_mail

send_mail(
    subject='SmartQuiz Test',
    message='Password reset test',
    from_email='your-email@gmail.com',
    recipient_list=['your-email@gmail.com'],
)
# If using console backend, check terminal
# If using Gmail, check inbox
```

---

## That's It! 🎉

Your password reset system is fully functional!

**What Users See:**
```
Login Page → Click "Forgot Password?" → Enter Email → Check Email → Click Link → New Password → Login
```

**Behind the Scenes:**
- Django generates secure token
- Token expires in 1 hour
- Email includes reset link with token
- Password securely hashed with PBKDF2

For detailed guide, see [PASSWORD_RESET_GUIDE.md](PASSWORD_RESET_GUIDE.md)
