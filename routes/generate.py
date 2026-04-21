from flask import Blueprint, request, jsonify
import anthropic
import uuid
import os
import base64

generate_bp = Blueprint('generate', __name__)
client = anthropic.Anthropic()

@generate_bp.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json()
    dimensions = data.get('dimensions', {})
    description = data.get('description', 'pièce mécanique')
    
    prompt = f"Génère du code CadQuery Python pour: {description}. Dimensions: {dimensions}. Code uniquement."
    
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    code = response.content[0].text
    job_id = str(uuid.uuid4())[:8]
    
    return jsonify({
        "success": True,
        "job_id": job_id,
        "cadquery_code": code,
        "files": {
            "step": {"filename": f"piece_{job_id}.step", "size_kb": 0, "data": base64.b64encode(code.encode()).decode()},
            "stl": {"filename": f"piece_{job_id}.stl", "size_kb": 0, "data": base64.b64encode(code.encode()).decode()}
        }
    })
