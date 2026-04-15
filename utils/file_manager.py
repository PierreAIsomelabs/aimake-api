import os, base64

def file_to_base64(path):
    with open(path,"rb") as f: return base64.b64encode(f.read()).decode("utf-8")

def get_file_size_kb(path):
    return round(os.path.getsize(path)/1024)

def build_file_response(step_path, stl_path, job_id):
    return {
        "job_id": job_id,
        "step": {"filename":"{}.step".format(job_id),"data":file_to_base64(step_path),"size_kb":get_file_size_kb(step_path)},
        "stl":  {"filename":"{}.stl".format(job_id), "data":file_to_base64(stl_path), "size_kb":get_file_size_kb(stl_path)}
    }
