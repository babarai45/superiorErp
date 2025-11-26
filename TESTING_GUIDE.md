# CampusGPT Homepage - Testing & Running Guide

## Prerequisites
- Python 3.8+
- Django 5.2.8
- Project located at: `E:\Specialization\django_Sep\superiorErp`

---

## Step 1: Navigate to Project Directory

```powershell
cd E:\Specialization\django_Sep\superiorErp
```

---

## Step 2: Activate Virtual Environment (if using venv)

```powershell
# For Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Or if using uv (based on your uv.lock file)
uv sync
```

---

## Step 3: Run Migrations (First Time Only)

```powershell
python manage.py migrate
```

---

## Step 4: Start Development Server

```powershell
python manage.py runserver
```

**Expected Output:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

---

## Step 5: Access the Homepage

### Option A: Using Web Browser
- Open your browser and go to: **http://localhost:8000/**
- Or: **http://127.0.0.1:8000/**

### Option B: Using curl in PowerShell
```powershell
Invoke-WebRequest http://localhost:8000/ | Select-Object -ExpandProperty Content
```

---

## Testing the Homepage

### Visual Testing
1. **Responsive Design**: Resize your browser window to test mobile, tablet, and desktop views
2. **Dark/Light Mode**: Open DevTools (F12) and toggle dark mode in the HTML element:
   ```javascript
   // In browser console:
   document.documentElement.classList.toggle('dark');
   ```
3. **Navigation**: Click all navbar links to verify smooth scrolling
4. **Buttons**: Hover over and click buttons to verify interactivity

### Sections to Verify
- ✅ Navbar with logo and navigation
- ✅ Hero section with headline and CTAs
- ✅ Features grid (4 cards)
- ✅ AI Chatbot section
- ✅ Student Dashboard section
- ✅ Teacher Panel section
- ✅ University-Wide Features (6 cards)
- ✅ Testimonials (3 cards)
- ✅ Call-to-Action section
- ✅ Footer with links

---

## Project Files Structure

```
superiorErp/
├── manage.py                          # Django management script
├── views.py                           # Homepage view (NEW)
├── superiorErp/
│   ├── settings.py                    # Django settings (UPDATED)
│   ├── urls.py                        # URL routing (UPDATED)
│   ├── asgi.py
│   └── wsgi.py
├── templates/
│   └── home.html                      # Homepage template (NEW)
└── pyproject.toml
```

---

## File Changes Made

### 1. **templates/home.html** (NEW)
- Complete responsive homepage
- Tailwind CSS with dark mode support
- 10 major sections as specified
- No external image assets

### 2. **views.py** (NEW)
```python
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
```

### 3. **superiorErp/urls.py** (UPDATED)
```python
from django.contrib import admin
from django.urls import path
from views import home

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
]
```

---

## Troubleshooting

### Issue: "No module named 'views'"
**Solution**: Ensure you're in the correct project directory and the views.py file exists in the root.

### Issue: "TemplateDoesNotExist at /"
**Solution**: Verify the template path in settings.py:
```python
TEMPLATES = [
    {
        "DIRS": [BASE_DIR / 'templates'],  # Should include this
        ...
    }
]
```

### Issue: Tailwind CSS not loading
**Solution**: The template uses CDN from `https://cdn.tailwindcss.com`. Ensure you have internet access.

### Issue: Static files not loading
**Solution**: For development, Django serves static files automatically. For production, run:
```powershell
python manage.py collectstatic
```

---

## Performance Tips

1. **Fast Refresh**: Changes to `home.html` are auto-reloaded by Django
2. **Console Debugging**: Open browser DevTools (F12) to check for errors
3. **Network Tab**: Check if Tailwind CDN is loading properly

---

## Next Steps (Optional Enhancements)

1. **Create Django App**: `python manage.py startapp core`
2. **Move View to App**: Move views and URLs to the app
3. **Add CSS Locally**: Download Tailwind instead of using CDN
4. **Add Database**: Create models for features like user accounts, courses
5. **Authentication**: Add Django authentication for Login/Sign Up
6. **API Integration**: Connect backend API endpoints

---

## Admin Panel Access

To access Django admin:
1. Create superuser: `python manage.py createsuperuser`
2. Go to: `http://localhost:8000/admin/`
3. Login with credentials

---

## Server Management

### Stop Server
Press `CTRL + C` in the terminal

### Restart Server
Simply run the runserver command again

### Run on Different Port
```powershell
python manage.py runserver 8001
```

---

**Your CampusGPT homepage is now ready for testing!** 🚀

