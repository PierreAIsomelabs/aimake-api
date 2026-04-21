import os, uuid
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

from routes.generate import generate_bp
from routes.repair import repair_bp
from routes.modify import modify_bp
from utils.cadquery_runner import cleanup_old_files

app = Flask(__name__)
CORS(app)

app.register_blueprint(generate_bp)
app.register_blueprint(repair_bp)
app.register_blueprint(modify_bp)

@app.route("/")
def index():
with open(os.path.join(os.path.dirname(__file__), "index.html"), encoding="utf-8") as f:
    return f.read(), 200, {"Content-Type": "text/html; charset=utf-8"}
      

@app.route("/health")
def health():
    return jsonify({"status":"ok","service":"AImake API","version":"1.0.0"})

@app.route("/api/download/<job_id>/<file_type>")
def download(job_id, file_type):
    tmp_dir = os.path.join(os.path.dirname(__file__), "tmp")
    ext = "step" if file_type == "step" else "stl"
    path = os.path.join(tmp_dir, "{}.{}".format(job_id, ext))
    if not os.path.exists(path):
        return jsonify({"error":"Fichier expiré"}), 404
    return send_file(path, as_attachment=True, download_name="aimake_{}.{}".format(job_id, ext))

@app.route("/api/arm2", methods=["POST"])
def arm2_escalation():
    data = request.get_json()
    dossier_id = "ARM2-{}".format(str(uuid.uuid4())[:6].upper())
    return jsonify({"success":True,"dossier_id":dossier_id,"message":"Dossier transmis à ARM2. Réponse sous 48h.","arm2_contact":"contact@arm2.fr"})

@app.route("/api/cleanup", methods=["POST"])
def cleanup():
    cleanup_old_files(int(os.getenv("MAX_FILE_AGE_MINUTES","60")))
    return jsonify({"success":True})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
