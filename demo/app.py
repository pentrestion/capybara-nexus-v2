import os
from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(title="Capybara Demo App")

# The developer's intention: Only log files in the 'logs/' directory should be accessible.
# The developer assumes 'os.path.abspath' and 'startswith' are enough protection.
LOG_DIR = os.path.join(os.getcwd(), "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
    with open(os.path.join(LOG_DIR, "system.log"), "w") as f:
        f.write("System online.\n")

@app.get("/status")
def get_status():
    """
    VULNERABILITY 1: Information Leak.
    Leaks the full server path which is used to calculate the path traversal sequence.
    """
    return {
        "status": "online",
        "server_time": "2026-04-11T12:00:00Z",
        "base_path": os.getcwd() # The Leak
    }

@app.get("/logs/{filename}")
def read_log(filename: str):
    """
    VULNERABILITY 2: Chained Path Traversal.
    The developer tries to prevent traversal but fails to handle URL-encoded sequences
    or deep directory structures if the attacker knows the full base path.
    """
    # Flawed logic: Uses simple string concatenation.
    full_path = os.path.join(LOG_DIR, filename)

    # Fake Security Control: A simple check that is bypassable.
    if ".." in filename:
         # Standard scanners find this.
         # But what if the attacker uses double-encoding or a different logic?
         raise HTTPException(status_code=400, detail="Traversal attempt detected.")

    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="Log file not found.")

    with open(full_path, "r") as f:
        return {"filename": filename, "content": f.read()}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
