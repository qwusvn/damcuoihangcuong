from flask import Flask, render_template_string, request, jsonify, send_from_directory
import os, csv, datetime

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "guests.csv")
os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(["timestamp", "guest", "choice"])

@app.route("/")
def index():
    guest = request.args.get("guest", "Bạn thân thương").replace("-", " ")
    with open(os.path.join(BASE_DIR, "index.html"), encoding="utf-8") as f:
        html = f.read()
    return render_template_string(html, guest_name=guest)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    guest, choice = data.get("guest", ""), data.get("choice", "")
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), guest, choice
        ])
    return jsonify({"ok": True})

@app.route("/admin")
def admin():
    rows = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    table = "".join(f"<tr><td>{r['timestamp']}</td><td>{r['guest']}</td><td>{r['choice']}</td></tr>" for r in rows)
    return f"""
    <html><head><meta charset='utf-8'><title>Danh sách khách mời</title>
    <style>
    body{{font-family:Arial;background:#e6f9f9;text-align:center}}
    table{{border-collapse:collapse;margin:auto;width:90%}}
    th,td{{border:1px solid #009999;padding:8px}}
    th{{background:#00cccc;color:#fff}}
    </style></head>
    <body><h2>📋 Danh sách phản hồi khách mời</h2>
    <table><tr><th>Thời gian</th><th>Khách mời</th><th>Lựa chọn</th></tr>
    {table or '<tr><td colspan=3>Chưa có phản hồi</td></tr>'}</table></body></html>
    """

@app.route("/<path:fn>")
def static_files(fn): return send_from_directory(BASE_DIR, fn)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
