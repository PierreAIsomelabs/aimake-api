import json, anthropic
from flask import Blueprint, request, jsonify
from utils.claude_prompts import SYSTEM_CADQUERY, build_generate_prompt, build_vision_prompt
from utils.cadquery_runner import run_cadquery
from utils.file_manager import build_file_response

generate_bp = Blueprint("generate", __name__)
client = anthropic.Anthropic()

def analyze_images(images_b64, description):
    try:
        content = []
        for img in images_b64[:4]:
            content.append({"type":"image","source":{"type":"base64","media_type":"image/jpeg","data":img}})
        content.append({"type":"text","text":build_vision_prompt(description)})
        r = client.messages.create(model="claude-opus-4-5",max_tokens=512,messages=[{"role":"user","content":content}])
        p = json.loads(r.content[0].text.strip())
        return "Type:{piece_type} Géom:{geometry} Procédé:{process} Matière:{material_guess} Dommage:{damage}-{damage_description}".format(**p)
    except Exception as e:
        return "Analyse échouée: {}".format(e)

def call_claude_code(prompt):
    r = client.messages.create(model="claude-opus-4-5",max_tokens=2048,system=SYSTEM_CADQUERY,messages=[{"role":"user","content":prompt}])
    code = r.content[0].text.strip()
    if code.startswith("```"):
        lines = code.split("\n")
        code = "\n".join(lines[1:-1] if lines[-1].strip()=="```" else lines[1:])
    return code

@generate_bp.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json()
    dimensions = data.get("dimensions", {})
    description = data.get("description", "pièce mécanique")
    images_b64 = data.get("images", [])
    photos_analysis = analyze_images(images_b64, description) if images_b64 else "Pas d'images."
    prompt = build_generate_prompt(dimensions, description, photos_analysis)
    code = call_claude_code(prompt)
    result = run_cadquery(code)
    if not result["success"]:
        return jsonify({"success":False,"error":result["error"],"cadquery_code":code}), 500
    return jsonify({"success":True,"job_id":result["job_id"],"cadquery_code":code,"files":build_file_response(result["step_path"],result["stl_path"],result["job_id"])})
