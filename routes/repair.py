from flask import Blueprint, request, jsonify
from utils.claude_prompts import build_repair_prompt
from utils.cadquery_runner import run_cadquery
from utils.file_manager import build_file_response
from routes.generate import analyze_images, call_claude_code

repair_bp = Blueprint("repair", __name__)

@repair_bp.route("/api/repair", methods=["POST"])
def repair():
    data = request.get_json()
    dimensions = data.get("dimensions", {})
    description = data.get("description", "pièce mécanique")
    damage = data.get("damage_description", "pièce cassée")
    images_b64 = data.get("images", [])
    photos_analysis = analyze_images(images_b64, description) if images_b64 else "Pas d'images."
    prompt = build_repair_prompt(dimensions, description, damage, photos_analysis)
    code = call_claude_code(prompt)
    result = run_cadquery(code)
    if not result["success"]:
        return jsonify({"success":False,"error":result["error"],"cadquery_code":code,"arm2_escalation":True}), 422
    return jsonify({"success":True,"job_id":result["job_id"],"mode":"repair","cadquery_code":code,"files":build_file_response(result["step_path"],result["stl_path"],result["job_id"])})
