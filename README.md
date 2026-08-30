# STL Business Intelligence Portal

Repo name is still `meta-ads-dashboard` (GitHub URL cannot be renamed from here).
App title inside is **STL Business Intelligence**.

This is a Python Flask app. Deploy on Render, not GitHub Pages.

## Login
- Email: sales@solartimeltd.com
- Password: set APP_PASSWORD on Render (default Solar123$)

After login you see the business menu. Only uploaded HTML files become clickable.

## Render
Build: `pip install -r requirements.txt`
Start: `gunicorn index:app --bind 0.0.0.0:$PORT --timeout 120`

Env:
- SECRET_KEY
- APP_USER=sales@solartimeltd.com
- APP_PASSWORD=Solar123$
