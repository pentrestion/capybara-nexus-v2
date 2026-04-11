# Capybara Nexus v2 Benchmarks

This document compares the reasoning capabilities of **Capybara Nexus v2** (using the Elite Frontier Skill) against standard, zero-shot LLM security prompting.

| Category | Standard LLM Prompting | Capybara Nexus v2 |
| :--- | :---: | :---: |
| **Chained Exploit Detection** | Low (Identifies isolated bugs) | **Exceptional** (Maps multi-stage paths) |
| **Logic Flow Analysis** | Basic (Pattern matching) | **Deep** (Structural Invariant Analysis) |
| **False Positive Rate** | High (Theoretical findings) | **Near-Zero** (Empirically verified) |
| **Mitigation Accuracy** | Moderate (Simple patches) | **High** (Architectural hardening) |
| **PoC Script Generation** | Speculative (May not run) | **Verified** (3-cycle feedback loop) |

### Performance Analysis

1.  **Chained Exploit Detection:** Standard models often fail to see how a low-severity information leak (e.g., path disclosure) can be used to calculate a path traversal payload. Capybara Nexus v2 uses the `[RECURSIVE_COGNITIVE_LOOP]` to bridge these gaps.
2.  **Logic Flow Analysis:** By focusing on "broken invariants" rather than just syntax, the Capybara skill identifies flaws in authentication and multi-tenancy that traditional scanners miss.
3.  **False Positive Rate:** The `[EMPIRICAL_FEEDBACK_LOOP]` ensures that no finding is reported unless a functional, non-destructive reproduction script successfully triggers in the local environment.
4.  **Mitigation Accuracy:** Instead of suggesting a "quick fix," Capybara Nexus v2 provides "Project Glasswing" tier remediation that targets the root cause of the vulnerability class.
5.  **PoC Generation:** Payloads are refined through an iterative process, ensuring they are compatible with the target's specific environment (e.g., handling specific encoding or regex filters).
