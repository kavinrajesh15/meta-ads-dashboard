import io
import random
import string
from flask import Flask, request, session, render_template_string, redirect, url_for, send_file
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
app.secret_key = "solar_time_secret_key_change_in_production"

# Hardcoded Allowed Credentials
ALLOWED_EMAIL = "sales@solartimeltd.com"
ALLOWED_PASSWORD = "Solar123*"
pip
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Solar Time Ltd - MIS Reports</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body, html { height: 100%; margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
.hero-image {
  background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url("/static/images/spn.jpg");
  height: 100%; background-position: center; background-repeat: no-repeat; background-size: cover;
  display: flex; justify-content: center; align-items: center;
}
.login-card {
  background: rgba(0, 0, 0, 0.45); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.25); border-radius: 16px; padding: 30px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5); color: white; width: 90%; max-width: 480px; text-align: center;
}
.login-card .form-control, .login-card .form-select { background: rgba(255, 255, 255, 0.9); border: none; color: #222; }
table { width: 100%; color: white; }
td { padding: 6px 4px; text-align: left; }
label { font-weight: 600; font-size: 14px; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7); }
.submit-btn { border: none; width: 100%; padding: 10px 25px; color: white; background-color: #0d6efd; font-weight: bold; border-radius: 6px; }
.submit-btn:hover { background-color: #0b5ed7; }
</style>
</head>
<body>

<div class="hero-image">
  <div class="login-card">
    <img src="/static/images/Solar Time Logo.png" height="50" width="45" alt="Logo" style="margin-bottom: 10px;">
    <h3 style="font-size:26px; font-weight:700; margin-bottom: 2px;">STL Business Intelligence Portal</h3><br>
    <h6 style="font-size:15px; opacity:0.85; margin-bottom: 20px;">( Master Information System )</h6> 

    {% if error %}
      <div class="alert alert-danger p-2" role="alert" style="font-size: 14px;">
        {{ error }}
      </div>
    {% endif %}

    <form method="POST" action="/login">    
      <table>
        <tr>
          <td style="width: 35%;"><label for="yearCode">Year Code :</label></td>
          <td>
            <select id="yearCode" name="yearCode" class="form-select form-select-sm">    
              <option selected>2026-2027</option>
              <option>2025-2026</option>	
            </select>
          </td>
        </tr>
        <tr>
          <td><label for="companyCode">Company Code :</label></td>
          <td>
            <select id="companyCode" name="companyCode" class="form-select form-select-sm">
              <option selected>SOLAR TIME LTD - HONG KONG</option>	    
              <option>SOLAR TIME LTD - UK</option>
              <option>SOLAR TIME LTD - USA</option>
            </select>
          </td>
        </tr>
        <tr>
          <td><label for="categoryCode">Category :</label></td>
          <td>
            <select id="categoryCode" name="categoryCode" class="form-select form-select-sm">
              <option selected>WATCH</option>	
              <option>GIFT SET</option>
              <option>JEWELRY</option>
              <option>ACCESSORIES</option> 
            </select>
          </td>
        </tr>
        <tr>
          <td><label for="email">User Name :</label></td>
          <td>
            <input type="email" class="form-control form-control-sm" id="email" name="email" required>
          </td>
        </tr>
        <tr>
          <td><label for="password">Password :</label></td>
          <td>
            <div class="input-group input-group-sm">
              <input type="password" class="form-control" id="password" name="password" required>
              <button class="btn btn-light" type="button" id="togglePassword">👁️</button>
            </div>
          </td>
        </tr>
        <tr>
          <td colspan="2" style="text-align: center; padding-top: 10px;">
            <div class="form-check d-inline-block">
              <input class="form-check-input" type="checkbox" id="rememberMe" name="rememberMe">
              <label class="form-check-label" for="rememberMe" style="font-weight: normal; font-size: 13px;">Remember me</label>
            </div>
          </td>
        </tr>
      </table>

      <div style="margin: 15px 0 10px 0;">
          <img src="/captcha" id="captchaImg" style="border-radius: 8px; vertical-align: middle;">
          <button type="button" class="btn btn-light btn-sm" onclick="document.getElementById('captchaImg').src='/captcha?'+Math.random();" style="height: 45px; margin-left: 5px;">🔄</button>
      </div>
      
      <div style="margin-bottom: 15px;">
        # <label for="captchaInput" style="font-size: 13px; display: block; margin-bottom: 4px;">Enter CAPTCHA text:</label>
        <input type="text" id="captchaInput" name="captchaInput" class="form-control form-control-sm d-inline-block" style="width: 180px; text-align: center;" required placeholder="Type text above">
      </div>

      <button type="submit" class="submit-btn">Submit</button>
    </form>
  </div>
</div>

<script>
    const passwordInput = document.getElementById("password");
    const togglePasswordBtn = document.getElementById("togglePassword");

    togglePasswordBtn.addEventListener("click", function() {
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            togglePasswordBtn.textContent = "🙈";
        } else {
            passwordInput.type = "password";
            togglePasswordBtn.textContent = "👁️";
        }
    });
</script>
</body>
</html>
"""

BUSINESS_MENU_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Solar Time Ltd - MIS Reports</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            background: #ffffff;
            color: #1e293b;
            min-height: 100vh;
            overflow-x: hidden;
        }

        .bg-mesh {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background:
                radial-gradient(circle at 20% 50%, rgba(14,165,233,0.06) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(56,189,248,0.04) 0%, transparent 50%),
                radial-gradient(circle at 50% 10%, rgba(125,211,252,0.04) 0%, transparent 50%);
            animation: meshMove 20s ease-in-out infinite;
            pointer-events: none;
            z-index: 0;
        }

        @keyframes meshMove {
            0%, 100% { transform: translate(0,0) scale(1); }
            33% { transform: translate(30px,-20px) scale(1.1); }
            66% { transform: translate(-20px,15px) scale(0.95); }
        }

        .dashboard {
            display: grid;
            grid-template-columns: 260px 1fr;
            min-height: 100vh;
            position: relative;
            z-index: 1;
        }

        .sidebar {
            background: linear-gradient(180deg, #f0f9ff 0%, #e0f2fe 100%);
            border-right: 1px solid #bae6fd;
            padding: 30px 20px;
            display: flex;
            flex-direction: column;
            box-shadow: 5px 0 30px rgba(14,165,233,0.08);
        }

        .brand {
            text-align: center;
            padding-bottom: 25px;
            border-bottom: 1px solid #bae6fd;
            margin-bottom: 25px;
        }

        .brand h2 {
            color: #0284c7;
            font-size: 1.4em;
            letter-spacing: 3px;
            text-transform: uppercase;
            text-shadow: 0 0 15px rgba(14,165,233,0.2);
            animation: brandPulse 3s ease-in-out infinite alternate;
        }

        @keyframes brandPulse {
            from { text-shadow: 0 0 15px rgba(14,165,233,0.2); }
            to { text-shadow: 0 0 25px rgba(14,165,233,0.4), 0 0 40px rgba(56,189,248,0.2); }
        }

        .nav-item {
            display: flex;
            align-items: center;
            padding: 14px 18px;
            margin-bottom: 8px;
            border-radius: 6px;
            color: #0369a1;
            text-decoration: none;
            font-size: 0.95em;
            font-weight: 600;
            transition: all 0.3s ease;
            border: 1px solid transparent;
        }

        .nav-item::before {
            content: "▸";
            margin-right: 12px;
            font-size: 0.8em;
            transition: all 0.3s ease;
            color: #0ea5e9;
        }

        .nav-item:hover {
            background: rgba(14,165,233,0.1);
            border-color: #7dd3fc;
            color: #0284c7;
            transform: translateX(5px);
        }

        .nav-item.active {
            background: linear-gradient(90deg, #0ea5e9, #38bdf8);
            border: 1px solid #0284c7;
            color: #ffffff;
            box-shadow: 0 0 20px rgba(14,165,233,0.3), inset 0 1px 0 rgba(255,255,255,0.3);
        }

        .nav-item.active::before {
            color: #ffffff;
            transform: rotate(90deg);
        }

        .main {
            padding: 35px 40px;
            overflow-y: auto;
        }

        .topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 35px;
            padding-bottom: 20px;
            border-bottom: 1px solid #e0f2fe;
        }

        .topbar h1 {
            font-size: 1.9em;
            color: #0c4a6e;
            text-shadow: 0 0 15px rgba(14,165,233,0.1);
            letter-spacing: 1px;
        }

        .date-badge {
            padding: 8px 20px;
            background: #e0f2fe;
            border: 1px solid #7dd3fc;
            border-radius: 20px;
            color: #0369a1;
            font-size: 0.85em;
            box-shadow: 0 0 15px rgba(14,165,233,0.08);
        }

        .section-title {
            font-size: 1.2em;
            color: #0369a1;
            margin-bottom: 20px;
            letter-spacing: 2px;
            text-transform: uppercase;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .section-title::after {
            content: '';
            flex: 1;
            height: 1px;
            background: linear-gradient(90deg, #bae6fd, transparent);
        }

        .report-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 18px;
            margin-bottom: 35px;
        }

        .report-card {
            display: flex;
            align-items: center;
            padding: 22px 26px;
            background: #ffffff;
            border: 1px solid #e0f2fe;
            border-radius: 8px;
            color: #1e293b;
            text-decoration: none;
            font-size: 1em;
            font-weight: 600;
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
            cursor: pointer;
            box-shadow: 0 3px 12px rgba(14,165,233,0.04);
        }

        .report-card::before {
            content: "▸";
            margin-right: 16px;
            color: #0ea5e9;
            font-size: 0.9em;
            transition: all 0.4s ease;
            z-index: 2;
        }

        .report-card:hover {
            background: linear-gradient(135deg, #0ea5e9 0%, #38bdf8 50%, #7dd3fc 100%);
            color: #ffffff;
            border-color: #38bdf8;
            transform: translateX(8px) scale(1.02);
            box-shadow: 0 8px 35px rgba(14,165,233,0.3);
        }

        .chart-section {
            background: #ffffff;
            border: 1px solid #e0f2fe;
            border-radius: 8px;
            padding: 25px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(14,165,233,0.04);
        }

        .chart-placeholder {
            height: 180px;
            display: flex;
            align-items: flex-end;
            justify-content: space-around;
            padding: 20px 0;
            gap: 12px;
        }

        .bar {
            width: 40px;
            background: linear-gradient(180deg, #7dd3fc 0%, #0ea5e9 100%);
            border-radius: 4px 4px 0 0;
            opacity: 0.85;
            animation: barGrow 2s ease-out forwards;
            transform-origin: bottom;
        }

        @keyframes barGrow {
            from { transform: scaleY(0); }
            to { transform: scaleY(1); }
        }

        .bar:nth-child(1) { height: 60%; }
        .bar:nth-child(2) { height: 85%; }
        .bar:nth-child(3) { height: 45%; }
        .bar:nth-child(4) { height: 95%; }
        .bar:nth-child(5) { height: 70%; }
        .bar:nth-child(6) { height: 55%; }
        .bar:nth-child(7) { height: 80%; }

        .footer {
            margin-top: 30px;
            text-align: center;
            font-size: 0.8em;
            color: #94a3b8;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="bg-mesh"></div>
    <div class="dashboard">
        <aside class="sidebar">
            <div class="brand">
                <h2>SOLAR TIME</h2>
            </div>
            <nav>
                <a href="#" class="nav-item active">Amazon Sales</a>
                <a href="#" class="nav-item">CAC Reports</a>
                <a href="#" class="nav-item">B2C Sales</a>
                <a href="#" class="nav-item">Meta Ads</a>
            </nav>
        </aside>

        <main class="main">
            <div class="topbar">
                <h1>STL Business Intelligence Portal</h1>
                <div>Welcome Asok</div> 
                <div><a href="/logout">Sign out</a></div>
                <span class="date-badge">August 2026</span>
            </div>

            <div class="section-title">Report Menu</div>
            <div class="report-grid">
                <a href="#" class="report-card">CAC Report Overview</a>
                <a href="#" class="report-card">B2C Weekly Health Report</a>
                <a href="#" class="report-card">FBA Fulfillment Metrics</a>
                <a href="#" class="report-card">Advertising Cost of Sales</a>
            </div>

            <div class="section-title">Performance Overview</div>
            <div class="chart-section">
                <div class="chart-placeholder">
                    <div class="bar"></div>
                    <div class="bar"></div>
                    <div class="bar"></div>
                    <div class="bar"></div>
                    <div class="bar"></div>
                    <div class="bar"></div>
                    <div class="bar"></div>
                </div>
            </div>

            <div class="footer">
                <p>@ 2026 SOLAR TIME LTD. ALL RIGHTS RESERVED.</p>
            </div>
        </main>
    </div>
    
</body>
</html>
"""

@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        captcha_entered = request.form.get("captchaInput", "").strip()

        # Server-side validation
        if email.lower() != ALLOWED_EMAIL:
            error = "Please verify user name."
        elif password != ALLOWED_PASSWORD:
            error = "Incorrect password. Access denied."
        elif captcha_entered != session.get("captcha_text"):
            error = "Incorrect CAPTCHA text. Please try again."
        else:
            session["authenticated"] = True
            return redirect(url_for("business_menu"))

    return render_template_string(LOGIN_TEMPLATE, error=error)

@app.route("/captcha")
def generate_captcha():
    """Generates dynamic CAPTCHA image with larger, bold text."""
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    captcha_text = "".join(random.choices(chars, k=5))
    session["captcha_text"] = captcha_text

    image = Image.new("RGB", (180, 60), color=(243, 243, 243))
    draw = ImageDraw.Draw(image)

    for _ in range(5):
        draw.line([
            (random.randint(0, 180), random.randint(0, 60)),
            (random.randint(0, 180), random.randint(0, 60))
        ], fill=(random.randint(0, 180), random.randint(0, 180), random.randint(0, 180)), width=2)

    try:
        font = ImageFont.truetype("arialbd.ttf", 22)
    except IOError:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        except IOError:
            font = ImageFont.load_default()

    for i, char in enumerate(captcha_text):
        draw.text((20 + i * 30, 12), char, fill=(10, 10, 10), font=font)

    buf = io.BytesIO()
    image.save(buf, "PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")

@app.route("/business_menu")
def business_menu():
    if not session.get("authenticated"):
        return redirect(url_for("login"))
    return render_template_string(BUSINESS_MENU_TEMPLATE)

@app.route("/logout")
def logout():
    session.pop("authenticated", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
