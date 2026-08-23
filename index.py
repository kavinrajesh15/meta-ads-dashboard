import io
import random
from flask import Flask, request, session, render_template_string, redirect, url_for, send_file
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
app.secret_key = "solar_time_secret_key_change_in_production"

# Credentials (as used on live Meta Ads login)
ALLOWED_EMAIL = "sales@solartimeltd.com"
ALLOWED_PASSWORD = "Solar123$"

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Solar Time Ltd - Login</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body, html {
  height: 100%;
  font-family: 'Inter', system-ui, sans-serif;
  -webkit-font-smoothing: antialiased;
}
.hero {
  min-height: 100vh;
  background-color: #0a0a0a;
  background-image: linear-gradient(rgba(0,0,0,0.40), rgba(0,0,0,0.50)), url("spn.jpg");
  background-position: center center;
  background-repeat: no-repeat;
  background-size: cover;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.login-card {
  background: rgba(12, 16, 24, 0.78);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border: 1px solid rgba(255,255,255,0.14);
  border-radius: 18px;
  padding: 32px 28px;
  box-shadow: 0 25px 60px rgba(0,0,0,0.6);
  width: 100%;
  max-width: 420px;
  color: #f1f5f9;
  text-align: center;
}
.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 22px;
  justify-content: center;
}
.brand img {
  height: 44px;
  width: auto;
  border-radius: 8px;
  background: #fff;
  padding: 3px;
}
.brand-text .stl {
  font-size: 11px;
  font-weight: 800;
  letter-spacing: .4px;
  color: #94a3b8;
  text-transform: uppercase;
}
.brand-text h1 {
  font-size: 18px;
  font-weight: 800;
  margin: 2px 0 0;
  color: #f1f5f9;
}
.brand-text p {
  font-size: 12px;
  color: #94a3b8;
  margin-top: 2px;
}
label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #cbd5e1;
  margin-bottom: 6px;
  text-align: left;
}
.form-group { margin-bottom: 14px; text-align: left; }
.form-control, .form-select {
  width: 100%;
  background: rgba(255,255,255,0.94);
  border: none;
  border-radius: 8px;
  padding: 10px 12px;
  color: #0f172a;
  font-size: 14px;
}
.form-control:focus, .form-select:focus {
  box-shadow: 0 0 0 3px rgba(6,104,225,0.35);
  outline: none;
}
.pwd-wrap { position: relative; }
.pwd-wrap .form-control { padding-right: 44px; }
.toggle-pwd {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  font-size: 16px;
  padding: 4px;
}
.remember {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 14px;
  font-size: 13px;
  color: #cbd5e1;
  justify-content: center;
}
.remember input { width: 16px; height: 16px; accent-color: #0668E1; }
.captcha-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
  justify-content: center;
}
#captchaImg {
  border-radius: 6px;
  background: #f1f5f9;
  height: 45px;
}
.refresh-btn {
  background: rgba(255,255,255,0.15);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 6px;
  color: #e2e8f0;
  width: 40px;
  height: 45px;
  cursor: pointer;
  font-size: 16px;
}
.submit-btn {
  width: 100%;
  margin-top: 6px;
  background: linear-gradient(135deg, #0668E1 0%, #4B9BFF 100%);
  border: none;
  border-radius: 8px;
  padding: 12px;
  color: #fff;
  font-weight: 700;
  font-size: 14px;
  cursor: pointer;
}
.submit-btn:hover {
  filter: brightness(1.08);
  box-shadow: 0 4px 20px rgba(6,104,225,0.4);
}
.error-msg {
  background: rgba(239,68,68,0.18);
  border: 1px solid rgba(239,68,68,0.4);
  color: #fecaca;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 13px;
  margin-bottom: 14px;
}
.footer {
  text-align: center;
  margin-top: 16px;
  font-size: 11px;
  color: rgba(255,255,255,0.45);
}
</style>
</head>
<body>
<div class="hero">
  <div class="login-card">
    <div class="brand">
      <img src="solarlogo.png" alt="Solar Time Ltd" onerror="this.style.display='none'">
      <div class="brand-text">
        <div class="stl">Solar Time Ltd</div>
        <h1>Meta Ads Manager</h1>
        <p>Secure Login</p>
      </div>
    </div>

    {% if error %}
    <div class="error-msg">{{ error }}</div>
    {% endif %}

    <form method="POST" action="/login">
      <div class="form-group">
        <label for="email">Username / Email</label>
        <input type="email" class="form-control" id="email" name="email" required
               placeholder="sales@solartimeltd.com" autocomplete="username">
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <div class="pwd-wrap">
          <input type="password" class="form-control" id="password" name="password" required
                 placeholder="Enter password" autocomplete="current-password">
          <button type="button" class="toggle-pwd" id="togglePwd" title="Show/Hide">👁️</button>
        </div>
      </div>

      <div class="remember">
        <input type="checkbox" id="rememberMe" name="rememberMe">
        <label for="rememberMe" style="margin:0;cursor:pointer">Remember me</label>
      </div>

      <div class="form-group">
        <label>CAPTCHA</label>
        <div class="captcha-row">
          <img src="/captcha" id="captchaImg" alt="CAPTCHA">
          <button type="button" class="refresh-btn"
                  onclick="document.getElementById('captchaImg').src='/captcha?'+Math.random();">🔄</button>
        </div>
        <input type="text" id="captchaInput" name="captchaInput" class="form-control"
               style="margin-top:8px;text-align:center" required placeholder="Type the text above" autocomplete="off">
      </div>

      <button type="submit" class="submit-btn">Sign In</button>
    </form>

    <div class="footer">© 2026 Solar Time Ltd · Internal Use Only</div>
  </div>
</div>

<script>
document.getElementById("togglePwd").addEventListener("click", function() {
  const inp = document.getElementById("password");
  if (inp.type === "password") {
    inp.type = "text";
    this.textContent = "🙈";
  } else {
    inp.type = "password";
    this.textContent = "👁️";
  }
});
</script>
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

        if email.lower() != ALLOWED_EMAIL:
            error = "Access denied. Invalid username."
        elif password != ALLOWED_PASSWORD:
            error = "Incorrect password. Access denied."
        elif captcha_entered != session.get("captcha_text"):
            error = "Incorrect CAPTCHA. Please try again."
        else:
            session["authenticated"] = True
            # After successful login redirect to the static Meta Ads dashboard
            return redirect("/dashboard.html")

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
        try:
            font = ImageFont.truetype("arialbd.ttf", 24)
        except IOError:
            font = ImageFont.load_default()

    for i, char in enumerate(captcha_text):
        draw.text((18 + i * 28, 10), char, fill=(15, 23, 42), font=font)

    buf = io.BytesIO()
    image.save(buf, "PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")

@app.route("/logout")
def logout():
    session.pop("authenticated", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
