from flask import Flask, redirect, request, session, render_template_string, send_from_directory
import requests
import os
import time

app = Flask(__name__)
app.secret_key = "MAX_OPTIMIZER_SUPER_SECRET_KEY"

CLIENT_ID = "1555303680180232223"
CLIENT_SECRET = "bbhiXj-ZpLhPXSp0JRDnPm00rdwd7Gfo"
REDIRECT_URI = "http://localhost:5000/callback"
GUILD_ID = "1458377017375326337"
BOT_TOKEN = "MTU1NTMwMzY4MDE4MDIzMjIyMw.GDfp8q.9NZ7ZpF0p2lQ7jPwKzh38DOQTqsJ6XBeSjkZaU"

DISCORD_INVITE_LINK = "https://discord.gg/nXua98Shh"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="{{ lang }}" dir="{{ 'rtl' if lang == 'ar' else 'ltr' }}">
<head>
    <meta charset="UTF-8">
    <title>Max Optimizer - Video Suite</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body, html {
            margin: 0; padding: 0; height: 100vh; overflow: hidden;
            font-family: 'Tahoma', sans-serif; color: #fff;
            background: linear-gradient(-45deg, #050507, #0b0b12, #141421, #08080c);
            background-size: 400% 400%;
            animation: liquidBackground 12s ease infinite;
        }
        @keyframes liquidBackground {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .wrapper {
            height: 100vh; display: flex; justify-content: center; align-items: center;
        }
        .card-glass {
            background: rgba(12, 12, 18, 0.85); backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 20px;
            padding: 40px; box-shadow: 0 25px 50px rgba(0,0,0,0.9); text-align: center; max-width: 480px; width: 100%;
        }
        .btn-discord {
            background-color: #5865F2; color: white; font-weight: bold; padding: 12px 20px;
            border-radius: 10px; border: none; transition: 0.3s; text-decoration: none; display: inline-block; width: 100%;
        }
        .btn-discord:hover { background-color: #4752C4; color: white; transform: translateY(-2px); }
        .lang-switch {
            position: absolute; top: 20px; {{ 'left' if lang == 'ar' else 'right' }}: 20px;
            background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12);
            color: #fff; padding: 6px 15px; border-radius: 8px; text-decoration: none; font-size: 14px; transition: 0.3s;
        }
        .lang-switch:hover { background: rgba(255,255,255,0.15); color: #00ff88; }
    </style>
</head>
<body>
    <a href="/set_lang?lang={{ 'en' if lang == 'ar' else 'ar' }}" class="lang-switch">
        {{ 'English 🌐' if lang == 'ar' else 'العربية 🌐' }}
    </a>

    <div class="wrapper">
        <div class="card-glass">
            <h1 class="fw-bold mb-3" style="color: #00ff88;">MAX OPTIMIZER ⚡</h1>
            <p class="text-secondary mb-4">{{ 'منصة ذكية لتحسين ومعالجة الفيديوهات بأعلى أداء.' if lang == 'ar' else 'Smart platform for high-performance video optimization.' }}</p>
            <a href="/login" class="btn btn-discord">{{ 'تسجيل الدخول عبر ديسكورد 🎮' if lang == 'ar' else 'Login with Discord 🎮' }}</a>
        </div>
    </div>
</body>
</html>
"""

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="{{ lang }}" dir="{{ 'rtl' if lang == 'ar' else 'ltr' }}">
<head>
    <meta charset="UTF-8">
    <title>Dashboard - Max Optimizer</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body, html {
            margin: 0; padding: 0; min-height: 100vh; overflow-x: hidden;
            font-family: 'Tahoma', sans-serif; color: #fff;
            background: linear-gradient(-45deg, #050507, #0b0b12, #141421, #08080c);
            background-size: 400% 400%;
            animation: liquidBackground 12s ease infinite;
        }
        @keyframes liquidBackground {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .wrapper {
            min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px;
        }
        .card-glass {
            background: rgba(12, 12, 18, 0.88); backdrop-filter: blur(18px);
            border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 20px;
            padding: 35px; box-shadow: 0 25px 50px rgba(0,0,0,0.95); max-width: 600px; width: 100%;
        }
        .form-control, .form-select, .form-control:focus, .form-select:focus {
            background: rgba(20, 20, 30, 0.9); border: 1px solid rgba(255,255,255,0.12); color: #fff; border-radius: 8px;
        }
        .form-control::file-selector-button {
            background-color: #5865F2; color: white; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer; {{ 'margin-left' if lang == 'ar' else 'margin-right' }}: 10px;
        }
        .btn-custom {
            background-color: #00ff88; color: #0b0b0f; font-weight: bold; padding: 12px;
            border-radius: 8px; border: none; transition: 0.3s; width: 100%;
        }
        .btn-custom:hover { background-color: #00cc6a; transform: translateY(-2px); }
        .lang-switch {
            position: absolute; top: 20px; {{ 'left' if lang == 'ar' else 'right' }}: 20px;
            background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12);
            color: #fff; padding: 6px 15px; border-radius: 8px; text-decoration: none; font-size: 14px; transition: 0.3s;
        }
        .lang-switch:hover { background: rgba(255,255,255,0.15); color: #00ff88; }
    </style>
</head>
<body>
    <a href="/set_lang?lang={{ 'en' if lang == 'ar' else 'ar' }}" class="lang-switch">
        {{ 'English 🌐' if lang == 'ar' else 'العربية 🌐' }}
    </a>

    <div class="wrapper">
        <div class="card-glass text-center">
            <h3 class="fw-bold mb-2" style="color: #00ff88;">Max Optimizer Studio 🛠️</h3>
            <p class="text-secondary mb-4">{{ 'اختر الفيديو وقم بتخصيص خيارات المعالجة الاحترافية.' if lang == 'ar' else 'Select your video and customize advanced processing options.' }}</p>
            
            <form action="/upload" method="POST" enctype="multipart/form-data" onsubmit="showLoading()">
                <div class="mb-3 text-start">
                    <label class="form-label text-light">{{ 'ملف الفيديو:' if lang == 'ar' else 'Video File:' }}</label>
                    <input type="file" name="video" class="form-control" accept="video/*" required>
                </div>
                
                <div class="row">
                    <div class="col-md-6 mb-3 text-start">
                        <label class="form-label text-light">{{ 'دقة الإخراج:' if lang == 'ar' else 'Resolution:' }}</label>
                        <select name="resolution" class="form-select">
                            <option value="original">{{ 'نفس الدقة الأصلية' if lang == 'ar' else 'Original Resolution' }}</option>
                            <option value="1080p">Full HD (1080p)</option>
                            <option value="4k" selected>Ultra HD (4K)</option>
                        </select>
                    </div>

                    <div class="col-md-6 mb-3 text-start">
                        <label class="form-label text-light">{{ 'معدل الإطارات:' if lang == 'ar' else 'Frame Rate:' }}</label>
                        <select name="framerate" class="form-select">
                            <option value="normal">{{ 'عادي (بدون تغيير)' if lang == 'ar' else 'Normal (Unchanged)' }}</option>
                            <option value="60fps" selected>60 FPS (سلس وثابت)</option>
                        </select>
                    </div>
                </div>

                <div class="row">
                    <div class="col-md-6 mb-3 text-start">
                        <label class="form-label text-light">{{ 'فلتر تحسين الحِدة:' if lang == 'ar' else 'Sharpness Filter:' }}</label>
                        <select name="enhancement" class="form-select">
                            <option value="none">{{ 'بدون فلاتر' if lang == 'ar' else 'None' }}</option>
                            <option value="sharp" selected>{{ 'تفعيل Ultra Sharp (وضوح عالي)' if lang == 'ar' else 'Ultra Sharp' }}</option>
                        </select>
                    </div>

                    <div class="col-md-6 mb-4 text-start">
                        <label class="form-label text-light">{{ 'سرعة المعالجة (Preset):' if lang == 'ar' else 'Encoding Speed:' }}</label>
                        <select name="speed_preset" class="form-select">
                            <option value="fast" selected>{{ 'سريع جداً (Ultrafast)' if lang == 'ar' else 'Ultrafast' }}</option>
                            <option value="balanced">{{ 'متوازن (Balanced)' if lang == 'ar' else 'Balanced' }}</option>
                        </select>
                    </div>
                </div>

                <button type="submit" id="submitBtn" class="btn btn-custom">{{ 'بدء المعالجة والتحسين 🚀' if lang == 'ar' else 'Start Optimization 🚀' }}</button>
            </form>

            <div id="loadingBox" class="mt-4" style="display: none;">
                <div class="spinner-border text-success" role="status"></div>
                <p class="mt-2 text-warning fw-bold">{{ 'جاري معالجة الفيديو، يرجى الانتظار...' if lang == 'ar' else 'Processing video, please wait...' }}</p>
            </div>
        </div>
    </div>

    <script>
        function showLoading() {
            document.getElementById('submitBtn').style.display = 'none';
            document.getElementById('loadingBox').style.display = 'block';
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    lang = session.get('lang', 'ar')
    return render_template_string(HOME_TEMPLATE, lang=lang)

@app.route("/set_lang")
def set_lang():
    lang = request.args.get('lang', 'ar')
    session['lang'] = lang
    return redirect(request.referrer or "/")

@app.route("/login")
def login():
    discord_login_url = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify%20guilds.members.read"
    return redirect(discord_login_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "فشل تسجيل الدخول", 400

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    token_json = r.json()
    
    access_token = token_json.get("access_token")
    if not access_token:
        return f"فشل المصادقة: {token_json}", 400

    session['access_token'] = access_token
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    try:
        access_token = session.get('access_token')
        if not access_token:
            return redirect("/")
        
        user_headers = {"Authorization": f"Bearer {access_token}"}
        user_res = requests.get("https://discord.com/api/users/@me", headers=user_headers)
        user_info = user_res.json()
        
        user_id = user_info.get("id")
        if not user_id:
            return redirect("/")
        
        bot_headers = {"Authorization": f"Bot {BOT_TOKEN}"}
        member_check = requests.get(f"https://discord.com/api/guilds/{GUILD_ID}/members/{user_id}", headers=bot_headers)
        
        if member_check.status_code != 200:
            lang = session.get('lang', 'ar')
            msg = "عذراً، يجب عليك الانضمام إلى سيرفر الديسكورد أولاً! ❌" if lang == 'ar' else "Sorry, you must join the Discord server first! ❌"
            btn = "انضم لسيرفرنا الآن" if lang == 'ar' else "Join Our Server Now"
            return f"""
            <html dir="{ 'rtl' if lang == 'ar' else 'ltr' }"><body style="background:#050507; color:#fff; text-align:center; padding-top:100px; font-family:Tahoma;">
                <h2>{msg}</h2><br>
                <a href="{DISCORD_INVITE_LINK}" target="_blank" style="background:#5865F2; color:#fff; padding:10px 20px; text-decoration:none; border-radius:5px;">{btn}</a>
            </body></html>
            """
        
        lang = session.get('lang', 'ar')
        return render_template_string(DASHBOARD_TEMPLATE, lang=lang)
    except Exception as e:
        return redirect("/")

@app.route("/upload", methods=["POST"])
def upload_video():
    if 'access_token' not in session:
        return redirect("/")
    
    if 'video' not in request.files:
        return "لم يتم اختيار أي ملف", 400
    
    file = request.files['video']
    if file.filename == '':
        return "اسم الملف فارغ", 400
    
    resolution = request.form.get('resolution', '4k')
    framerate = request.form.get('framerate', '60fps')
    enhancement = request.form.get('enhancement', 'sharp')
    speed_preset = request.form.get('speed_preset', 'fast')
    
    safe_name = f"video_{int(time.time())}.mp4"
    input_path = os.path.join(UPLOAD_FOLDER, safe_name)
    output_filename = f"optimized_{safe_name}"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    
    file.save(input_path)
    
    filters = []
    if framerate == '60fps':
        filters.append("fps=60")
    if resolution == '4k':
        filters.append("scale=3840:2160:flags=lanczos")
    elif resolution == '1080p':
        filters.append("scale=1920:1080:flags=lanczos")
    if enhancement == 'sharp':
        filters.append("unsharp=5:5:1.0:5:5:0.0")
        
    filter_string = ",".join(filters) if filters else "scale=iw:ih"
    
    print(f"--- بدء المعالجة بـ Max Optimizer: {safe_name} ---")
    ffmpeg_cmd = f'ffmpeg -y -i "{input_path}" -vf "{filter_string}" -c:v libx264 -crf 16 -preset {speed_preset} -c:a copy "{output_path}"'
    os.system(ffmpeg_cmd)
    print("--- انتهت المعالجة بنجاح ---")
    
    lang = session.get('lang', 'ar')
    title_text = "تمت المعالجة بنجاح! 🎉" if lang == 'ar' else "Processing Successful! 🎉"
    desc_text = "الملف جاهز للتحميل بالإعدادات التي اخترتها." if lang == 'ar' else "Your file is ready with the selected settings."
    btn_text = "تحميل الفيديو 📥" if lang == 'ar' else "Download Video 📥"
    back_text = "← تحويل فيديو آخر" if lang == 'ar' else "← Optimize Another Video"

    return f"""
    <!DOCTYPE html>
    <html lang="{lang}" dir="{ 'rtl' if lang == 'ar' else 'ltr' }">
    <head>
        <meta charset="UTF-8">
        <title>Result - Max Optimizer</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body, html {{ margin: 0; padding: 0; height: 100vh; overflow: hidden; font-family: 'Tahoma', sans-serif; color: #fff; background: linear-gradient(-45deg, #050507, #0b0b12, #141421, #08080c); background-size: 400% 400%; animation: liquidBackground 12s ease infinite; }}
            @keyframes liquidBackground {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}
            .wrapper {{ height: 100vh; display: flex; justify-content: center; align-items: center; }}
            .card-glass {{ background: rgba(12, 12, 18, 0.88); backdrop-filter: blur(18px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 20px; padding: 40px; box-shadow: 0 25px 50px rgba(0,0,0,0.95); max-width: 500px; width: 100%; text-align: center; }}
            .btn-download {{ background-color: #00ff88; color: #0b0b0f; font-weight: bold; padding: 12px 24px; border-radius: 8px; text-decoration: none; display: inline-block; transition: 0.3s; }}
            .btn-download:hover {{ background-color: #00cc6a; }}
        </style>
    </head>
    <body>
        <div class="wrapper">
            <div class="card-glass">
                <h2 class="fw-bold mb-3" style="color: #00ff88;">{title_text}</h2>
                <p class="text-secondary mb-4">{desc_text}</p>
                <a href="/download/{output_filename}" class="btn btn-download">{btn_text}</a>
                <br><br>
                <a href="/dashboard" class="text-decoration-none text-secondary small">{back_text}</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=5000)