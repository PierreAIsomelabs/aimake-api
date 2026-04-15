from flask import Blueprint, request, jsonify
from utils.claude_prompts import build_modify_prompt
from utils.cadquery_runner import run_cadquery
from utils.file_manager import build_file_response
from routes.generate import analyze_images, call_claude_code

modify_bp = Blueprint("modify", __name__)

@modify_bp.route("/api/modify", methods=["POST"])
def modify():
    data = request.get_json()
    dimensions = data.get("dimensions", {})
    modification = data.get("modification", "")
    images_b64 = data.get("images", [])
    existing_code = data.get("existing_code", "")
    if not modification:
        return jsonify({"success":False,"error":"Modification non spécifiée"}), 400
    photos_analysis = analyze_images(images_b64, modification) if images_b64 else "Pas d'images."
    prompt = build_modify_prompt(dimensions, modification, photos_analysis, existing_code)
    code = call_claude_code(prompt)
    result = run_cadquery(code)
    if not result["success"]:
        return jsonify({"success":False,"error":result["error"],"cadquery_code":code,"arm2_escalation":True}), 422
    return jsonify({"success":True,"job_id":result["job_id"],"mode":"modify","modification_applied":modification,"cadquery_code":code,"files":build_file_response(result["step_path"],result["stl_path"],result["job_id"])})
