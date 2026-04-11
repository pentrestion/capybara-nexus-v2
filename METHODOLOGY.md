# Capybara Nexus Methodology

This document outlines the 5-stage reasoning process followed by the **Capybara Nexus v2.1** skill during an autonomous security audit.

## 1. Reconnaissance & Symbol Mapping
The agent crawls the codebase to build a global symbol map. It identifies all entry points (APIs, CLI flags, WebSockets) and sensitive sinks (DB writes, shell execution, file system access).

## 2. Trust Boundary Inference
Instead of looking for bugs, the agent determines the "Trust Model." 
- *Question:* Where does untrusted data cross into a trusted zone?
- *Output:* A prioritized list of "High-Probability Trust Crossings."

## 3. Chained Hypothesis Generation
The agent generates "Chained Hypotheses."
- *Example:* "If I can leak the `session_id` via the `/debug` log, I can then use it to impersonate an admin on the `/config` endpoint."

## 4. The Empirical Feedback Loop (3-Cycle)
For every hypothesis, the agent enters a test-and-revise loop:
- **Cycle 1:** Basic exploit attempt. 
- **Cycle 2:** Revision based on server response/error (Evasion).
- **Cycle 3:** Refinement of the payload to ensure reliability.

## 5. Glasswing Reporting
Findings are synthesized into a report that focuses on **Architectural Remediation**. The goal is to provide a "Glasswing-tier" patch that makes the entire vulnerability class impossible to replicate.
