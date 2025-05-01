# start_all.py
import subprocess
import time

print("🔄 Starting FastAPI server...")
uvicorn_process = subprocess.Popen(["uvicorn", "main:app", "--reload"])

time.sleep(5)

print("🌐 Starting ngrok tunnel...")
ngrok_process = subprocess.Popen(["ngrok", "http", "8000"])

try:
    uvicorn_process.wait()
except KeyboardInterrupt:
    print("🛑 Shutting down...")
    ngrok_process.terminate()
    uvicorn_process.terminate()
