import os, uuid, subprocess, time

TMP_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tmp")
os.makedirs(TMP_DIR, exist_ok=True)

def run_cadquery(code):
    job_id = str(uuid.uuid4())[:8]
    step_path = os.path.join(TMP_DIR, "{}.step".format(job_id))
    stl_path  = os.path.join(TMP_DIR, "{}.stl".format(job_id))
    script    = os.path.join(TMP_DIR, "{}.py".format(job_id))
    injected  = "step_path = r'{}'\nstl_path = r'{}'\n\n{}".format(step_path, stl_path, code)
    with open(script, "w") as f:
        f.write(injected)
    try:
        r = subprocess.run(["python", script], capture_output=True, text=True, timeout=60)
        if r.returncode != 0:
            return {"success":False,"error":r.stderr[-500:],"step_path":None,"stl_path":None,"job_id":job_id}
        if not os.path.exists(step_path) or not os.path.exists(stl_path):
            return {"success":False,"error":"Fichiers non générés","step_path":None,"stl_path":None,"job_id":job_id}
        return {"success":True,"step_path":step_path,"stl_path":stl_path,"job_id":job_id,"error":None}
    except subprocess.TimeoutExpired:
        return {"success":False,"error":"Timeout 60s","step_path":None,"stl_path":None,"job_id":job_id}
    finally:
        if os.path.exists(script): os.remove(script)

def cleanup_old_files(max_age_minutes=60):
    now = time.time()
    for f in os.listdir(TMP_DIR):
        fp = os.path.join(TMP_DIR, f)
        if os.path.isfile(fp) and (now - os.path.getmtime(fp))/60 > max_age_minutes:
            os.remove(fp)
