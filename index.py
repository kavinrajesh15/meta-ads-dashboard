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

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>STL Business Intelligence · Login</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body, html {height:100%;font-family:'Inter',system-ui,sans-serif}
.hero {
  min-height:100vh; background-color:#0a0a0a;
  background-image:linear-gradient(rgba(0,0,0,.40), rgba(0,0,0,.50)), url("/static-asset/spn.jpg");
  background-position:center; background-size:cover;
  display:flex; align-items:center; justify-content:center; padding:20px;
}
.login-card {
  background:rgba(12,16,24,.78); backdrop-filter:blur(18px);
  border:1px solid rgba(255,255,255,.14); border-radius:18px;
  padding:32px 28px; width:100%; max-width:420px; color:#f1f5f9; text-align:center;
}
.brand {display:flex;align-items:center;gap:12px;margin-bottom:22px;justify-content:center}
.brand img {height:44px;width:auto;border-radius:8px;background:#fff;padding:3px}
.stl {font-size:11px;font-weight:800;letter-spacing:.4px;color:#94a3b8;text-transform:uppercase}
.brand-text h1 {font-size:18px;font-weight:800;margin:2px 0 0;color:#f1f5f9}
.brand-text p {font-size:12px;color:#94a3b8;margin-top:2px}
label {display:block;font-size:12px;font-weight:600;color:#cbd5e1;margin-bottom:6px;text-align:left}
.form-group {margin-bottom:14px;text-align:left}
.form-control {width:100%;background:rgba(255,255,255,.94);border:none;border-radius:8px;padding:10px 12px;color:#0f172a}
.pwd-wrap {position:relative}
.pwd-wrap .form-control {padding-right:44px}
.toggle-pwd {position:absolute;right:8px;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer}
.remember {display:flex;align-items:center;gap:8px;margin-bottom:14px;font-size:13px;color:#cbd5e1;justify-content:center}
.captcha-row {display:flex;align-items:center;gap:10px;justify-content:center}
#captchaImg {border-radius:6px;background:#f1f5f9;height:45px}
.refresh-btn {background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.2);border-radius:6px;color:#e2e8f0;width:40px;height:45px}
.submit-btn {width:100%;margin-top:6px;background:linear-gradient(135deg,#0668E1,#4B9BFF);border:none;border-radius:8px;padding:12px;color:#fff;font-weight:700}
.error-msg {background:rgba(239,68,68,.18);border:1px solid rgba(239,68,68,.4);color:#fecaca;border-radius:8px;padding:10px 14px;margin-bottom:14px}
.footer {margin-top:16px;font-size:11px;color:rgba(255,255,255,.45)}
</style>
</head>
<body>
<div class="hero">
  <div class="login-card">
    <div class="brand">
      <img src="/static-asset/solarlogo.png" alt="Solar Time Ltd" onerror="this.style.display='none'">
      <div class="brand-text">
        <div class="stl">Solar Time Limited</div>
        <h1>STL Business Intelligence</h1>
        <p>Secure Login</p>
      </div>
    </div>
    {% if error %}<div class="error-msg">{{ error }}</div>{% endif %}
    <form method="POST" action="/login">
      <div class="form-group">
        <label for="email">Username / Email</label>
        <input type="email" class="form-control" id="email" name="email" required placeholder="sales@solartimeltd.com">
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <div class="pwd-wrap">
          <input type="password" class="form-control" id="password" name="password" required>
          <button type="button" class="toggle-pwd" id="togglePwd">👁️</button>
        </div>
      </div>
      <div class="remember">
        <input type="checkbox" id="rememberMe" name="rememberMe">
        <label for="rememberMe" style="margin:0">Remember me</label>
      </div>
      <div class="form-group">
        <label>CAPTCHA</label>
        <div class="captcha-row">
          <img src="/captcha" id="captchaImg" alt="CAPTCHA">
          <button type="button" class="refresh-btn" onclick="document.getElementById('captchaImg').src='/captcha?'+Math.random();">🔄</button>
        </div>
        <input type="text" name="captchaInput" class="form-control" style="margin-top:8px;text-align:center" required placeholder="Type the text above">
      </div>
      <button type="submit" class="submit-btn">Sign In</button>
    </form>
    <div class="footer">© 2026 Solar Time Ltd · Internal Use Only</div>
  </div>
</div>
<script>
document.getElementById("togglePwd").addEventListener("click", function() {
  const inp = document.getElementById("password");
  inp.type = inp.type === "password" ? "text" : "password";
  this.textContent = inp.type === "password" ? "\uD83D\uDC41\uFE0F" : "\uD83D\uDE48";
});
</script>
</body>
</html>
"""

MENU_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>STL Business Intelligence</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Georgia,serif;background:#fff;color:#1e293b;min-height:100vh}
.wrap{display:grid;grid-template-columns:260px 1fr;min-height:100vh}
.sidebar{background:linear-gradient(180deg,#f0f9ff,#e0f2fe);border-right:1px solid #bae6fd;padding:30px 20px}
.brand h2{color:#0284c7;letter-spacing:2px;text-align:center;margin-bottom:24px}
.nav a{display:block;padding:12px 14px;margin-bottom:8px;border-radius:6px;color:#0369a1;text-decoration:none;font-weight:600}
.nav a:hover,.nav a.on{background:#0ea5e9;color:#fff}
.main{padding:32px 40px}
.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:28px;border-bottom:1px solid #e0f2fe;padding-bottom:16px}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
.card{display:block;padding:22px 24px;border:1px solid #e0f2fe;border-radius:8px;text-decoration:none;color:#1e293b;font-weight:700}
.card:hover{background:#0ea5e9;color:#fff}
.off{opacity:.45;pointer-events:none}
.out{color:#0284c7;font-weight:700;text-decoration:none}
</style>
</head>
<body>
<div class="wrap">
  <aside class="sidebar">
    <div class="brand"><h2>SOLAR TIME</h2></div>
    <nav class="nav">
      <a class="on" href="/menu">All Reports</a>
      {% for d in dashboards %}
        {% if d.ready %}<a href="/dash/{{ d.slug }}">{{ d.title }}</a>{% endif %}
      {% endfor %}
    </nav>
  </aside>
  <main class="main">
    <div class="top">
      <div>
        <h1>STL Business Intelligence Portal</h1>
        <div>Welcome Asok</div>
      </div>
      <div><a class="out" href="/logout">Sign out</a></div>
    </div>
    <div class="grid">
      {% for d in dashboards %}
        {% if d.ready %}
          <a class="card" href="/dash/{{ d.slug }}">{{ d.title }}<br><small>{{ d.note }}</small></a>
        {% else %}
          <div class="card off">{{ d.title }}<br><small>File not uploaded yet</small></div>
        {% endif %}
      {% endfor %}
    </div>
  </main>
</div>
</body>
</html>
"""


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("authenticated"):
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper


def dash_list():
    items = []
    for d in DASHBOARDS:
        item = dict(d)
        item["ready"] = os.path.isfile(os.path.join(ROOT, d["file"]))
        items.append(item)
    return items


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        captcha_entered = request.form.get("captchaInput", "").strip()
        if email != ALLOWED_EMAIL:
            error = "Access denied. Invalid username."
        elif password != ALLOWED_PASSWORD:
            error = "Incorrect password. Access denied."
        elif captcha_entered != session.get("captcha_text"):
            error = "Incorrect CAPTCHA. Please try again."
        else:
            session["authenticated"] = True
            return redirect(url_for("menu"))
    return render_template_string(LOGIN_TEMPLATE, error=error)


@app.route("/captcha")
def generate_captcha():
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    captcha_text = "".join(random.choices(chars, k=5))
    session["captcha_text"] = captcha_text
    image = Image.new("RGB", (160, 50), color=(241, 245, 249))
    draw = ImageDraw.Draw(image)
    for _ in range(5):
        draw.line([
            (random.randint(0, 160), random.randint(0, 50)),
            (random.randint(0, 160), random.randint(0, 50))
        ], fill=(random.randint(80, 180), random.randint(80, 180), random.randint(80, 180)), width=2)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
    except IOError:
        font = ImageFont.load_default()
    for i, char in enumerate(captcha_text):
        draw.text((18 + i * 28, 10), char, fill=(15, 23, 42), font=font)
    buf = io.BytesIO()
    image.save(buf, "PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


@app.route("/menu")
@login_required
def menu():
    return render_template_string(MENU_TEMPLATE, dashboards=dash_list())


@app.route("/dash/<slug>")
@login_required
def dash(slug):
    item = next((d for d in DASHBOARDS if d["slug"] == slug), None)
    if not item:
        abort(404)
    path = os.path.join(ROOT, item["file"])
    if not os.path.isfile(path):
        abort(404)
    return send_from_directory(ROOT, item["file"])


@app.route("/static-asset/<path:name>")
def static_asset(name):
    allowed = {"spn.jpg", "solarlogo.png", "spnn.jpeg"}
    if name not in allowed:
        abort(404)
    return send_from_directory(ROOT, name)


@app.route("/dashboard.html")
@login_required
def old_dashboard():
    return send_from_directory(ROOT, "dashboard.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/healthz")
def healthz():
    return {"ok": True}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
