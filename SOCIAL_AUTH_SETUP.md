# Social Authentication Setup Guide

## Overview
The login page now supports **three social authentication methods**:
- ✅ **Google OAuth**
- ✅ **GitHub OAuth**  
- ✅ **Facebook OAuth**

All powered by **django-allauth** which is already installed and configured.

---

## Installation & Configuration

### 1. Social Providers Already Configured
In `django_travel_agency/settings.py`, the following are installed:
```python
INSTALLED_APPS = [
    ...
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.facebook',
    ...
]
```

### 2. Database Setup
Social apps are stored in Django's database. To add them:

1. **Start Django shell:**
   ```bash
   python manage.py shell
   ```

2. **Create social apps programmatically:**
   ```python
   from django.contrib.sites.models import Site
   from allauth.socialaccount.models import SocialApp
   
   # Get current site
   site = Site.objects.get_current()
   
   # GOOGLE OAUTH
   google_app = SocialApp.objects.create(
       name='Google',
       provider='google',
       client_id='YOUR_GOOGLE_CLIENT_ID',
       secret='YOUR_GOOGLE_CLIENT_SECRET'
   )
   google_app.sites.add(site)
   
   # GITHUB OAUTH
   github_app = SocialApp.objects.create(
       name='GitHub',
       provider='github',
       client_id='YOUR_GITHUB_CLIENT_ID',
       secret='YOUR_GITHUB_CLIENT_SECRET'
   )
   github_app.sites.add(site)
   
   # FACEBOOK OAUTH
   facebook_app = SocialApp.objects.create(
       name='Facebook',
       provider='facebook',
       client_id='YOUR_FACEBOOK_CLIENT_ID',
       secret='YOUR_FACEBOOK_CLIENT_SECRET'
   )
   facebook_app.sites.add(site)
   ```

3. **Or use Django Admin:**
   - Go to: `http://localhost:8000/admin/socialaccount/socialapp/`
   - Click "Add Social application"
   - Fill in the details for each provider

---

## Getting OAuth Credentials

### Google OAuth Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **Google+ API**
4. Create **OAuth 2.0 credentials** (Web Application)
5. Add redirect URI: `http://localhost:8000/accounts/google/login/callback/`
6. Copy **Client ID** and **Client Secret**

### GitHub OAuth Setup
1. Go to [GitHub Settings → Developer settings](https://github.com/settings/developers)
2. Click **New OAuth App**
3. Fill in:
   - Application name: `Pandurang Travels`
   - Homepage URL: `http://localhost:8000/`
   - Authorization callback URL: `http://localhost:8000/accounts/github/login/callback/`
4. Copy **Client ID** and **Client Secret**

### Facebook OAuth Setup
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app
3. Add **Facebook Login** product
4. Settings → Basic: Copy **App ID** and **App Secret**
5. Add redirect URLs in Settings → Basic:
   - `http://localhost:8000/accounts/facebook/login/callback/`

---

## Frontend Implementation

The login form includes three social login buttons with icons:
```html
<!-- SOCIAL LOGIN BUTTONS -->
<div class="social-buttons">
    <a href="{% provider_login_url 'google' %}" class="social-btn google">
        <i class="fab fa-google"></i>
    </a>
    <a href="{% provider_login_url 'github' %}" class="social-btn github">
        <i class="fab fa-github"></i>
    </a>
    <a href="{% provider_login_url 'facebook' %}" class="social-btn facebook">
        <i class="fab fa-facebook-f"></i>
    </a>
</div>
```

---

## Database Integration

### Social Account Model
When a user logs in with a social provider, `django-allauth` automatically:
1. Creates a new `SocialAccount` record linking the user to their social profile
2. Stores the social account ID, provider, and user data
3. Links to the existing `User` model

**Database Tables Used:**
- `socialaccount_socialapp` - OAuth app configurations
- `socialaccount_socialaccount` - User social accounts
- `socialaccount_socialtoken` - Access tokens (if needed)
- `auth_user` - User account information (reused from Django auth)

### Sample Query to Check Social Accounts:
```python
from allauth.socialaccount.models import SocialAccount

# Get all social accounts
SocialAccount.objects.all()

# Get a user's social accounts
user = User.objects.get(email='user@example.com')
user.socialaccount_set.all()
```

---

## Features Implemented

✅ **Secure OAuth 2.0 Authentication**
✅ **Automatic User Registration** (creates user on first social login)
✅ **Email Verification** (configured to not require)
✅ **Session Management** (handled by Django sessions)
✅ **Database Storage** of social profiles
✅ **Responsive Design** (works on mobile & desktop)
✅ **Icon-based Buttons** (Google, GitHub, Facebook)
✅ **Graceful Fallback** to email/password login

---

## Testing Social Login Locally

1. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

2. **Go to Django Admin:**
   ```
   http://localhost:8000/admin/
   ```

3. **Add Social Apps:**
   - Go to "Social applications"
   - For localhost testing, use:
     - Client ID: `test_client_id`
     - Secret: `test_secret`
   - Assign to your site

4. **Test the Login Page:**
   ```
   http://localhost:8000/en/packages/login/
   ```

---

## Production Checklist

Before deploying to production:
1. ✅ Update `ALLOWED_HOSTS` in settings
2. ✅ Use real OAuth credentials (not test ones)
3. ✅ Set `DEBUG = False`
4. ✅ Configure SSL/HTTPS
5. ✅ Update callback URLs to use production domain
6. ✅ Set up `CSRF_TRUSTED_ORIGINS` for cross-domain requests
7. ✅ Store secrets in environment variables (not hardcoded)
8. ✅ Enable database backups
9. ✅ Configure email for notifications
10. ✅ Set up proper logging

---

## Troubleshooting

### Error: "Provider not configured"
- Make sure the SocialApp is created in Django admin
- Check that the site is assigned to the app

### Error: "Redirect URI mismatch"
- Ensure callback URL matches exactly in both OAuth provider and Django

### Users not being created
- Check `ACCOUNT_EMAIL_VERIFICATION` setting
- Ensure `SOCIALACCOUNT_AUTO_SIGNUP = True` (default)

### Database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Files Modified

1. **templates/login.html** - Added social buttons and improved styling
2. **django_travel_agency/settings.py** - Already configured with allauth

## Efficient HTML Features

✅ **Grid Layout** for responsive social buttons
✅ **CSS Transitions** for smooth interactions
✅ **Semantic HTML** with aria-labels
✅ **Mobile-First Responsive Design**
✅ **Optimized CSS** (no bloated frameworks)
✅ **Accessibility Compliant**

---

For more info, see [django-allauth documentation](https://django-allauth.readthedocs.io/)
