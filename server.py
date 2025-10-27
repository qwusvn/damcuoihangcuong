from flask import Flask, render_template_string, request, jsonify, send_from_directory
import datetime, os, gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# --- Google Sheets setup ---
SHEET_ID = "1Ng1nH6b6sTLSjeY4KGveKFhRBPMd54FuB7P_4Bvm6zQ"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
gc = gspread.authorize(CREDS)
sheet = gc.open_by_key(SHEET_ID).sheet1

@app.route("/")
def index():
    guest = request.args.get("guest", "Bạn thân thương").replace("-", " ")
    with open("index.html", encoding="utf-8") as f:
        html = f.read()
    return render_template_string(html, guest_name=guest)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    guest = data.get("guest", "Không rõ")
    choice = data.get("choice", "Không rõ")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        sheet.append_row([timestamp, guest, choice])
        print(f"✅ {guest} → {choice}")
        return jsonify({"status": "ok"})
    except Exception as e:
        print("❌ Lỗi ghi Google Sheet:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/admin")
def admin():
    try:
        data = sheet.get_all_values()
        headers = data[0]
        rows = data[1:]
        table = "".join(f"<tr>{''.join(f'<td>{c}</td>' for c in r)}</tr>" for r in rows)
    except Exception as e:
        return f"<h3>Lỗi đọc sheet: {e}</h3>"

    return f"""
    <html><head><meta charset='utf-8'><title>Danh sách khách mời</title>
    <style>
        body {{ font-family: Arial; background:#e6f9f9; color:#004d4d; text-align:center; }}
        table {{ margin:auto; border-collapse: collapse; width:90%; max-width:800px; }}
        th, td {{ border:1px solid #009999; padding:8px; }}
        th {{ background:#00cccc; color:white; }}
    </style></head>
    <body>
      <h2>📋 Danh sách phản hồi khách mời (Google Sheet)</h2>
      <table>
        <tr>{''.join(f'<th>{h}</th>' for h in headers)}</tr>
        {table or '<tr><td colspan=3>Chưa có phản hồi nào</td></tr>'}
      </table>
    </body></html>
    """

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(os.getcwd(), filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
