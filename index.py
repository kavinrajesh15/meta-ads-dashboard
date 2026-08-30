import io
import os
import random
from functools import wraps
from flask import (
    Flask, request, session, render_template_string,
    redirect, url_for, send_file, send_from_directory, abort
)
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "solar_time_secret_key_change_in_production")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

ALLOWED_EMAIL = os.environ.get("APP_USER", "sales@solartimeltd.com").strip().lower()
ALLOWED_PASSWORD = os.environ.get("APP_PASSWORD", "Solar123$")
ROOT = os.path.dirname(os.path.abspath(__file__))

DASHBOARDS = [
    {"slug": "meta", "file": "dashboard.html", "title": "Meta Ads Dashboard", "note": "Google Sheets live data"},
    {"slug": "amazon", "file": "Amazon_Weekly_Sales_Week34_17-23Aug2026.html", "title": "Amazon FBA Weekly Sales", "note": "Week 34"},
    {"slug": "b2c", "file": "B2C_Weekly_Health_Week34_FINAL.html", "title": "B2C Weekly Health Check", "note": "Week 34"},
    {"slug": "cac", "file": "CAC_Final_Dashboard_Week33_10-16Aug2026.html", "title": "Price Management · CAC", "note": "Week 33"},
    {"slug": "po", "file": "Outstanding_PO_Dashboard_28Aug2026.html", "title": "Outstanding PO", "note": "28 Aug 2026"},
    {"slug": "sc", "file": "Outstanding_Pending_SC_Dashboard_28Aug2026.html", "title": "Outstanding Pending SC", "note": "28 Aug 2026"},
    {"slug": "tro", "file": "TRO_Dashboard_28Aug2026.html", "title": "TRO / Transfer Request", "note": "28 Aug 2026"},
    {"slug": "sales", "file": "STL_Detail_Sales_Dashboard_2026_YTD_Final.html", "title": "STL Detail Sales 2026", "note": "2026 YTD"},
]
