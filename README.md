# Capybara Nexus v2: Frontier-Class Security Analysis

A high-precision, autonomous security auditing skill for the Gemini CLI, inspired by the "Claude Mythos" model and its reported "Capybara-tier" capabilities.

## Features
- **Autonomous Exploit Chaining:** Discovers how minor info leaks can be used to escalate attacks.
- **Zero False Positives:** Every finding is empirically verified with a local reproduction script.
- **Structural Invariant Analysis:** Identifies deep logic flaws that standard scanners miss.
- **Glasswing Hardening:** Provides architectural patches instead of simple bug fixes.

## Repository Contents
- `SKILL.md`: The core skill definition for Gemini CLI.
- `demo/app.py`: A Python FastAPI application with a subtle, chained vulnerability.
- `demo/exploit_verify.py`: An autonomous verification script that demonstrates the "Capybara" reasoning loop.

## Installation
1.  Copy `SKILL.md` to your Gemini CLI skills directory.
2.  Activate with `activate_skill capybara-nexus-v2`.
