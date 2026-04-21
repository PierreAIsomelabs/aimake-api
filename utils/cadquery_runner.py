import anthropic
import os
import uuid
import base64

client = anthropic.Anthropic()

def generate_cadquery_code(description, dimensions):
    prompt = f"""Tu es un expert CadQuery. Génère du code Python CadQuery pour: {description}
Dimensions: {dimensions}
Retourne UNIQUEMENT le code Python, sans explication."""
    
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def cleanup_old_files():
    pass
