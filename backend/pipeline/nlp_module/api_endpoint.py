# bridge contact from celery wrorker/ app backend
import subprocess 
from api_endpoint_temp_vals import temp_values
# sensitive url routes stored in above file reference but follow this shape:
# temp_values={
#     'pdf':'qwen-student-experience.pdf',
#     'chunk_out':'qwen-student-experience.txt',
#     'doc-id':'[pick a number]',
#     'title':'student-experience',
#     'pages':'[enter range '0-inf']',
#     # below are parameters for extr_command
#     'profile':'per-chunk-profile.YAML',
#     'input': 'qwen-student-experience.txt',
#     'output': 'data_repo/'
# }









chunk_command = [
    "python3","chunking.py","--pdf",
    temp_values["pdf"],
    "--output",temp_values["chunk_out"],
    "--document-id",temp_values["doc-id"],
    "--title", temp_values["title"],
    "--pages", temp_values["pages"]]

print('chunking running')
result = subprocess.run(chunk_command, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)




extr_command = ["python3","engine.py","extract",
    "--profile", temp_values["profile"],
    "--input", temp_values["input"],
    "--output-dir", temp_values["output"]]

print('extraction running')
result = subprocess.run(extr_command, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)