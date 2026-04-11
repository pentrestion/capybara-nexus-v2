import os
import json
import subprocess
import time
import argparse

class CapybaraOrchestrator:
    def __init__(self, target_dir):
        self.target_dir = target_dir
        self.state_file = os.path.join(target_dir, ".nexus_state.json")
        self.state = self.load_state()

    def load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, "r") as f:
                return json.load(f)
        return {"findings": [], "history": [], "iteration": 0}

    def save_state(self):
        with open(self.state_file, "w") as f:
            json.dump(self.state, f, indent=4)

    def run_command(self, cmd):
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout, result.stderr, result.returncode
        except Exception as e:
            return "", str(e), 1

    def infer_threat_model(self):
        print(f"[*] [THREAT_MODEL_INFERENCE] Mapping trust boundaries in {self.target_dir}...")
        # In a real run, this would call the LLM to analyze the file structure.
        # Here we simulate the discovery of entry points.
        stdout, _, _ = self.run_command(f"grep -rE 'route|api|app.get|app.post' {self.target_dir}")
        print(f"[+] Found potential entry points:\n{stdout[:200]}...")

    def empirical_feedback_loop(self, hypothesis, exploit_script):
        print(f"\n[*] [EMPIRICAL_FEEDBACK_LOOP] Testing Hypothesis: {hypothesis}")
        for cycle in range(1, 4):
            print(f"[*] Cycle {cycle}/3: Executing PoC...")
            stdout, stderr, code = self.run_command(f"python3 {exploit_script}")
            
            if code == 0 and "VULNERABILITY CONFIRMED" in stdout:
                print(f"[!!!] SUCCESS: Finding confirmed in cycle {cycle}!")
                return True, stdout
            else:
                print(f"[-] Cycle {cycle} failed. Analyzing failure and revising hypothesis...")
                # Simulating the 'Revision' phase
                time.sleep(1) 
        return False, "Max iterations reached without confirmation."

    def audit(self):
        self.infer_threat_model()
        # Simulated findings for the demo
        print("\n[*] Starting Autonomous Audit Loop...")
        self.save_state()
        print("[+] Audit Complete. State saved to .nexus_state.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capybara Nexus v2.1 Autonomous Orchestrator")
    parser.add_argument("target", help="The directory to audit")
    args = parser.parse_args()

    orchestrator = CapybaraOrchestrator(args.target)
    orchestrator.audit()
