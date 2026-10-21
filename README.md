# Capybara Nexus v2 | Expanded Security Coverage and Audit Workflow

## Repository Analysis

This repository is not a full exploit framework or scanner. It is a security reasoning package and skill definition for an autonomous auditor, intended to be used with Gemini CLI or similar agentic tooling. The project combines:

- threat-model reasoning
- vulnerability classification
- attack-surface mapping
- empirical validation loops
- remediation-focused reporting

The main conceptual assets are:

- `SKILL.md` — elite directives and audit mandates
- `METHODOLOGY.md` — five-stage reasoning model
- `ATTACK_COVERAGE.md` — MITRE/OWASP alignment
- `nexus_audit.py` — an orchestration script that simulates the feedback loop
- `gym/` — multi-language example benchmarks and ablations

## Key Findings

### Strengths

- Good framing around trust boundaries and source-to-sink analysis.
- Reasonable emphasis on proving findings through iterative validation.
- Clear mapping to MITRE ATT&CK and OWASP categories.
- Strong concept of architecture-level remediation rather than just one-off bug reports.

### Gaps to address

- The current coverage is oriented more toward general web/infrastructure logic than toward modern AI and IoT-specific attack surfaces.
- The repo does not yet explicitly classify LLM application risks, device firmware risks, or miscommunication failure modes as first-class items.
- The workflow would benefit from explicit examples of tool outputs and structured step-by-step execution across different domains.

---

## Expanded Coverage to Add

### 1) Web application and API attack models

- Broken access control
- IDOR / BOLA
- SSRF
- injection and unsafe parsing
- CSRF and session issues
- insecure deserialization
- mass assignment and object property abuse
- unsafe file uploads

### 2) IoT and embedded device risks

- weak/default credentials
- OTA and firmware verification failure
- insecure Bluetooth or wireless protocols
- exposed debug interfaces
- device root / privilege escalation paths
- credential reuse and local secrets leakage
- unverified device-to-cloud trust

### 3) LLM / AI agent attack models

- prompt injection
- tool poisoning
- malicious plugin execution
- prompt and context leakage
- RAG poisoning
- output-to-action translation risks
- over-privileged autonomy
- false confidence and misinformation loops

### 4) Miscommunication / trust mismatch models

- user/system semantic mismatch
- unclear trust boundaries between components
- AI confident but wrong conclusions
- undefined policy assumptions
- hidden authorization differences across layers

---

## OWASP Coverage Additions

### OWASP Web Top 10 mapping

| Category | What to inspect |
| --- | --- |
| A01 Broken Access Control | role checks, object-level auth, route-level enforcement |
| A02 Cryptographic Failures | token validation, secret storage, TLS use |
| A03 Injection | SQL, command, SSRF, template, LDAP, unsafe parsing |
| A04 Insecure Design | missing abuse cases, weak design assumptions |
| A05 Security Misconfiguration | default config, open admin surfaces, debug info |
| A06 Vulnerable Components | known lib issues, old runtime packages |
| A07 Authentication Failures | session management, MFA bypass, credential reuse |
| A08 Software Integrity | unsigned updates, insecure CI, dependency tampering |
| A09 Monitoring Failures | no audit trail, poor detection |
| A10 SSRF | metadata service abuse, blind internal requests |

### OWASP LLM Top 10 concepts

- prompt injection
- insecure output handling
- training data poisoning
- model theft and exfiltration
- over-privileged tool access
- prompt leakage
- insecure supply chain around plugins or packages
- abuse of low-friction automation

### IoT-focused controls to check

- signed firmware and update verification
- secure boot and key protection
- lock down debug ports
- remove default secrets
- validate wireless pairing flows
- enforce least privilege for device APIs and services

---

## Step-by-Step Security Workflow

### Workflow 1: Web/API audit

1. Discover routes, handlers, and exposed endpoints.
2. Identify auth and authorization boundaries.
3. Trace user-controlled inputs to sensitive sinks.
4. Check for injection, SSRF, IDOR, and logic flaws.
5. Validate using controlled request tests.
6. Report misconfigurations and recommend design fixes.

Example commands:

```bash
grep -RInE "route|app\.get|app\.post|router|@app\.route" .
curl -I http://localhost:8080/
curl -s -D - http://localhost:8080/api/admin
```

Sample output:

```text
./app.py:14: @app.route("/api/admin")
HTTP/1.1 200 OK
Server: Werkzeug/2.3.3
```

### Workflow 2: IoT / device review

1. Enumerate exposed services and interfaces.
2. Review startup scripts and boot process.
3. Look for secrets, default credentials, or update logic.
4. Check for unsigned firmware, plaintext services, and debug access.
5. Validate whether device trust decisions rely on unverified local inputs.

Example commands:

```bash
grep -RInE "(password|secret|token|admin|firmware|ota|upgrade)" .
strings firmware.bin | grep -Ei "admin|password|token|ota"
```

### Workflow 3: LLM / AI agent review

1. Identify model system prompts and tool interfaces.
2. Map user input into tool invocation paths.
3. Examine whether the model can execute sensitive actions without policy enforcement.
4. Test prompt injection and output-to-action translation.
5. Review privilege boundaries for each tool call.

Example checks:

- tool policies
- user-role restrictions
- context trust boundaries
- confirmation gating
- output sanitization

---

## Tool Output Examples

### Static discovery example

```bash
grep -RInE "(SECRET|TOKEN|PASSWORD|API_KEY|JWT)" .
```

Output:

```text
./config/settings.py:12:SECRET_KEY = "dev-secret-key"
./server.py:23: auth_header = request.headers.get("Authorization")
./firmware/boot.sh:11: OTA_TOKEN="hardcoded-token"
```

### Network or route validation example

```bash
curl -s -D - http://localhost:8080/api/config
```

Output:

```text
HTTP/1.1 200 OK
Content-Type: application/json
{"role":"admin","config":"..."}
```

This kind of tool output helps identify whether endpoints expose privileged state without consistent authorization gating.

---

## Reference List

- OWASP Top 10: https://owasp.org/Top10/
- OWASP API Security: https://owasp.org/www-project-api-security/
- OWASP LLM Security Top 10: https://owasp.org/www-project-llm-security-top-10/
- HackTricks: https://book.hacktricks.xyz
- MITRE ATT&CK: https://attack.mitre.org/
- CWE: https://cwe.mitre.org/

---

## Recommended Repo Updates

The repo should include explicit sections for:

- Web OWASP Top 10
- API OWASP Top 10
- LLM OWASP risk models
- IoT/embedded device security
- Miscommunication and trust boundary failure analysis
- Step-by-step workflow with sample tool outputs
- Reference links to HackTricks and major standards

This will make the framework more comprehensive and more aligned with how real-world security reviews are performed.
