from flask import Flask, render_template, request, redirect
from datetime import datetime
import csv, os, hashlib, json

app = Flask(__name__)
BASE = os.path.dirname(__file__)
CAPTURE_FILE = os.path.join(BASE, '..', 'captured_credentials_redacted.csv')
LOG_FILE = os.path.join(BASE, '..', 'app_logs.jsonl')

def redact_and_hash(username, password):
    user_shr = (username[:3] + '***') if username else ''
    pwd_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()[:16] if password else ''
    return user_shr, pwd_hash

def write_csv(timestamp, ip, username, password_hash):
    write_header = not os.path.exists(CAPTURE_FILE)
    with open(CAPTURE_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(['timestamp_utc','src_ip','username_redacted','password_hash'])
        writer.writerow([timestamp, ip, username, password_hash])

def write_log(entry: dict):
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(entry) + '\\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username','')
    password = request.form.get('password','')
    u_r, p_h = redact_and_hash(username, password)
    timestamp = datetime.utcnow().isoformat() + 'Z'
    src_ip = request.remote_addr or '127.0.0.1'
    write_csv(timestamp, src_ip, u_r, p_h)
    write_log({
        "ts": timestamp,
        "src": src_ip,
        "action": "credential_submission",
        "username_redacted": u_r,
        "password_hash": p_h
    })
    return redirect('/')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
