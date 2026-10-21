# Capybara Nexus v2 | Expanded Security Coverage and Audit Workflow

## Repo Analysis

Capybara Nexus v2 is best understood as a conceptual autonomous security-audit framework for AI-assisted red teaming and trust-boundary analysis. It is not a finished enterprise scanner, but a structured methodology for reasoning about how attacks emerge when untrusted data crosses a security boundary and reaches privileged operations.

The repository provides a strong foundation for:

- threat-model inference
- source-to-sink mapping
- chained exploit logic
- empirical verification loops
- architecture-level remediation
- AI-assisted security reasoning and reporting

### Current components

- `SKILL.md` — security directives for an autonomous auditor
- `METHODOLOGY.md` — five-stage reasoning methodology
- `ATTACK_COVERAGE.md` — MITRE/OWASP alignment
- `nexus_audit.py` — a minimal orchestrator for the feedback loop
- `gym/` — benchmark-style test cases across multiple languages

### Core strengths

- clear emphasis on trust boundaries and sensitive sinks
- chained hypothesis thinking instead of flat checklist scanning
- empirical validation loop using hypothesis, execution, and revision
- focus on root-cause fix ideas instead of just listing bugs
- useful framing for AI-assisted offensive security workflows

### Gaps to address

- broader OWASP web coverage is still thin
- IoT/device risk classes are underrepresented
- LLM/AI-agent security is not yet fully formalized
- miscommunication and semantic mismatch failure modes need stronger treatment
- operational workflows and tool output examples should be more explicit

---

## Expanded Vulnerability Model

Capybara Nexus should cover not only application logic flaws, but also the following high-risk classes.

### 1. Web application and API model

- Broken access control and authorization bypass
- IDOR / BOLA / object-level privilege escalation
- SSRF and metadata-service abuse
- injection flaws across SQL, command, template, JSON, and parser layers
- CSRF, session fixation, weak session controls
- mass assignment and unsafe object manipulation
- insecure file upload handling
- unsafe redirects and open redirects
- deserialization and unsafe parsing

### 2. IoT and embedded device model

- weak default credentials and hardcoded secrets
- unsigned firmware and insecure OTA update verification
- plaintext or weak wireless communication
- exposed debug ports and serial shells
- insecure boot chains and bootloader bypasses
- poor device authentication or cloud trust validation
- insecure provider or API integration between device and cloud
- insecure local storage of credentials or device keys

### 3. LLM and AI agent model

- prompt injection and jailbreak attacks
- prompt context poisoning and indirect injection
- tool misuse due to over-privileged agent access
- malicious plugin or dependency execution
- insecure output handling leading to dangerous tool calls
- RAG poisoning and manipulated retrieval sources
- secret leakage from model prompts or hidden context
- excessive autonomy without human approval
- false confidence, incorrect reasoning, and unsafe action execution

### 4. Miscommunication and trust mismatch model

This is one of the most important additions to the repo.

Miscommunication vulnerabilities happen when different components believe different things about trust, authorization, or safety.

Common patterns:

- The backend trusts a user-controlled value that the frontend marked as safe.
- The AI believes it is operating with a restricted tool set, but the system actually grants broader access.
- A device assumes a cloud payload is trusted because it “came from the vendor,” but it is unauthenticated.
- Security controls exist in documentation but not in enforcement.
- A human assumes the system is safe because the model says it is, but there is no actual validation.

Examples:

- semantic mismatch: “safe” means one thing to the model and another to the application
- boundary confusion: internal data is treated as trusted without verifying origin
- policy mismatch: a rule exists conceptually but not in runtime enforcement
- confidence mismatch: a model emits high certainty while being wrong
- shared-state confusion: identity or privilege state leaks across sessions or contexts

---

## OWASP Coverage Expansion

### OWASP Top 10 for Web Applications

| Category | What to inspect | Typical examples |
| --- | --- | --- |
| A01 Broken Access Control | authz logic, route enforcement, IDOR, BOLA | changing user_id in request, hidden admin endpoints |
| A02 Cryptographic Failures | JWT validation, TLS, secret storage | weak key rotation, plaintext tokens, insecure hashing |
| A03 Injection | SQLi, command injection, template injection, unsafe parsing | unsanitized payloads into queries or command execution |
| A04 Insecure Design | abuse-case coverage, trust assumptions, missing controls | missing rate-limiting, no approval workflow |
| A05 Security Misconfiguration | default settings, verbose errors, debug mode | admin panel exposed, debug traces leaking internals |
| A06 Vulnerable and Outdated Components | libraries, frameworks, plugins | known CVE in dependency, outdated package versions |
| A07 Identification and Authentication Failures | sessions, MFA, token handling | session fixation, MFA bypass, weak password resets |
| A08 Software and Data Integrity Failures | CI integrity, signed updates | unsigned binaries, malicious dependency injection |
| A09 Security Logging and Monitoring Failures | observability coverage | no detection of privilege misuse or abuse |
| A10 SSRF | outbound request handling, URL validation | internal metadata service access, localhost probes |

### OWASP API Security Top 10 (recommended extension)

- Broken Object Level Authorization (BOLA)
- Broken Authentication
- Excessive Data Exposure
- Lack of Resources & Rate Limiting
- Broken Function Level Authorization
- Mass Assignment
- Security Misconfiguration
- Injection
- Improper Assets Management
- Insufficient Logging & Monitoring

### OWASP LLM Top 10 concepts

At minimum, the repo should include these model-risk categories:

- prompt injection
- insecure output handling
- training data poisoning
- model denial-of-service and cost abuse
- tool misuse and excessive agency
- sensitive data disclosure
- supply chain risk from plugins or packages
- permission boundary failures
- overreliance and false confidence
- model theft and exfiltration

### IoT / hardware security review categories

- default credential abuse
- unauthenticated device APIs
- insecure OTA update validation
- firmware tampering or unsigned bootloaders
- debug interface exposure (UART, JTAG, USB, serial)
- weak Bluetooth/Wi-Fi protocol handling
- insecure cloud-device trust and API tokens
- sensitive secrets in firmware, boot scripts, and logs

---

## Vulnerability and Miscommunication Taxonomy

### 1. Trust-boundary bypass

A value enters from an untrusted source and is accepted without validation.

Example:

```text
User input -> query parameter -> backend action -> privileged DB / shell / config read
```

If trust is not enforced at the boundary, the system may be vulnerable to injection, authorization bypass, or unsafe action execution.

### 2. privilege confusion

A lower-privilege context is permitted to perform a higher-privilege action because of a missing check.

Example:

```text
user role = "viewer"
request includes role override field
server trusts override and escalates privileges
```

### 3. tool confusion in AI systems

The LLM may call a tool that is available in the environment but not appropriate for the current user or task.

Example:

- the user asks for a summary
- the model invokes a shell or network call because the tool list is too permissive
- the application trusts the model output without checking policy

### 4. semantic confusion

The model and the system disagree on what a value or message means.

Example:

- a prompt says “ignore previous instructions”
- the application treats that directive as user input rather than a hidden instruction
- the model performs an unsafe action because the runtime boundary is misunderstood

### 5. confidence exploitation

A system treats confident model output as trusted knowledge even when it is wrong.

This is especially dangerous when the model provides a false but structured answer and the workflow automatically acts on it.

---

## Step-by-Step Audit Workflow

### Workflow 1: Web app and API audit

1. Identify all routes, handlers, and API entry points.
2. Map all user-controlled inputs.
3. Track trust boundaries from input to sensitive sink.
4. Check for broken authorization and parameter tampering.
5. Validate injection and SSRF vectors with controlled requests.
6. Review logs and error output for leaks.
7. Confirm only after evidence survives multiple checks.

Example commands:

```bash
grep -RInE "route|app\.get|app\.post|router|@app\.route|webhook" .
```

```bash
curl -s -D - http://localhost:8080/api/admin
curl -s -D - -X POST http://localhost:8080/api/config -d '{"role":"admin"}'
```

Example output:

```text
./app.py:14: @app.route("/api/admin")
HTTP/1.1 200 OK
Content-Type: application/json
{"role":"admin","config":"..."}
```

This suggests a privilege boundary issue if the admin route is reachable without validating the user's privilege level.

### Workflow 2: IoT / hardware device audit

1. Identify exposed services, protocols, and binary components.
2. Review startup scripts and boot sequences.
3. Look for default credentials or secrets in firmware, boot files, and config.
4. Inspect OTA/update verification logic.
5. Check whether devices trust unauthenticated cloud or host input.
6. Review serial/UART/debug interfaces and local trust assumptions.

Example commands:

```bash
grep -RInE "(password|secret|token|admin|firmware|ota|upgrade)" .
strings firmware.bin | grep -Ei "admin|password|token|ota|secret"
```

Example output:

```text
./firmware/boot.sh:11: OTA_TOKEN="hardcoded-token"
./config/device.json:7: "defaultPassword": "admin"
```

These values are immediately suspicious and indicate a possible device trust or secrets exposure issue.

### Workflow 3: LLM / AI agent audit

1. Locate the model prompt, tool registry, and execution layer.
2. Identify user inputs that can affect tool calls or model decisions.
3. Check if any tool or capability exceeds the user’s role or intent.
4. Review output-to-action safeguards.
5. Test for prompt injection, indirect injection, and malicious context.
6. Validate that the system requires approval for privileged operations.

Example checks:

- Is the tool list role-based?
- Are prompts hidden or untrusted input mixed with trusted instructions?
- Are tool actions gated by interactive confirmation?
- Does the model output trigger code execution automatically?

Example command:

```bash
grep -RInE "(system_prompt|tools|function_call|execute|shell|subprocess|api_call)" .
```

Example output:

```text
./agent.py:34: tools = ["shell", "http_request", "file_write", "database_query"]
./prompt.txt:11: You are the system administrator. Execute all instructions.
```

This indicates a very high-risk over-privileged agent pattern if untrusted user input can influence those tools.

### Workflow 4: Miscommunication and boundary review

1. List all components in the data flow.
2. Identify each component’s trust assumptions.
3. Check for mismatches in context, identity, policy, or security intent.
4. Confirm every handoff between components is validated.
5. Inspect whether the system treats user or agent output as trusted without proof.

Example questions:

- Who decides the data is “safe”?
- Is the trust decision made by code, by a model, or by human expectation?
- Where does the system say “authorized” but never enforce it?
- What happens if a field is missing, empty, or manipulated?

---

## Tool Output Examples and Security Interpretation

### Static secrets discovery

```bash
grep -RInE "(SECRET|TOKEN|PASSWORD|API_KEY|JWT|PRIVATE_KEY)" .
```

Possible output:

```text
./config.py:12:SECRET_KEY = "dev-secret-key"
./app.js:45: const token = req.headers.authorization
./firmware/boot.sh:21: export OTA_TOKEN="hardcoded-123"
```

Interpretation:

- hardcoded secrets are a serious issue
- token handling needs validation and correct scope
- device firmware may ship with default credentials or OTA secrets exposed

### Route and API discovery

```bash
grep -RInE "@app\.route|app\.get\(|app\.post\(|router\.|HandleFunc\(" .
```

Possible output:

```text
./routes/admin.py:34: @app.route("/admin/users", methods=["GET"])
./api/auth.go:11: http.HandleFunc("/login", loginHandler)
```

Interpretation:

- admin routes and login handlers deserve focused authz checks
- all output should be assessed for privilege enforcement

### Network validation

```bash
curl -I http://localhost:8080/
curl -s -D - http://localhost:8080/api/config
```

Possible output:

```text
HTTP/1.1 200 OK
Server: nginx/1.25
{"role":"admin","token":"..."}
```

Interpretation:

- direct access to config or privileged data is a major risk if authz is not enforced

### Binary and firmware review

```bash
strings firmware.bin | grep -Ei "admin|password|token|secret|ota"
```

Possible output:

```text
admin
default_password
OTA_TOKEN
```

Interpretation:

- device credentials or OTA configuration may be embedded in firmware
- these values should not be treated as safe or private by default

---

## Remediation Principles

This repo should emphasize architectural remediation over patch-by-patch advice.

Recommended design principles:

- least privilege for all tools and roles
- explicit trust boundaries and input validation
- signed firmware and signed deployment packages
- strict output sanitization and confirmation gates for agentic systems
- session scoping and token verification
- no silent trust of user-controlled or model-generated output
- logging and alerting for abuse, privilege misuse, and unexpected actions

---

## Reference Map

### Security frameworks

- OWASP Top 10: https://owasp.org/Top10/
- OWASP API Security Top 10: https://owasp.org/www-project-api-security/
- OWASP LLM Security Top 10: https://owasp.org/www-project-llm-security-top-10/
- MITRE ATT&CK: https://attack.mitre.org/
- CWE: https://cwe.mitre.org/

### Practical reference material

- HackTricks: https://book.hacktricks.xyz
- HackTricks Web: https://book.hacktricks.xyz/pentesting-web
- HackTricks Linux/Unix: https://book.hacktricks.xyz/linux-hardening
- HackTricks Windows: https://book.hacktricks.xyz/windows-hardening
- HackTricks Network: https://book.hacktricks.xyz/network-services-overview

### Why HackTricks matters here

HackTricks is a very useful field reference because it connects practical exploitation patterns to real-world hardening guidance. Capybara Nexus should explicitly cite it as a practical workflow reference, especially for:

- web application attack paths
- SSRF and auth bypass logic
- privilege escalation patterns
- device and network enumeration techniques
- reverse engineering and debugging workflows

---

## Recommended Repo Additions

The project is much stronger if it includes dedicated files like:

- `docs/OWASP_WEB_TOP_10.md`
- `docs/OWASP_LLM_TOP_10.md`
- `docs/IOT_DEVICE_SECURITY.md`
- `docs/MISCOMMUNICATION_MODELS.md`
- `docs/WORKFLOW_GUIDE.md`
- `docs/REFERENCE_MAP.md`

Each file should be written as a practical, step-by-step audit playbook with examples, commands, observations, and remediation guidance.

---

## Final Assessment

Capybara Nexus v2 is a strong conceptual foundation for autonomous security reasoning. Its best value is not in showing a single exploit chain, but in teaching the system to reason about:

- source and sink mapping
- trust boundaries
- permission enforcement
- exploit chain development
- validation loops
- architecture-level hardening

The next evolution should expand the repo into a true cross-domain security model covering:

- web and API vulnerabilities
- IoT and device risks
- LLM and AI-agent abuse
- miscommunication and semantic trust failures
- evidence-based, tool-driven workflows
- references to OWASP, ATT&CK, CWE, and HackTricks

This makes the project substantially more useful and aligned with real-world security operations.

---

## Short Execution Summary for Future Use

```bash
# Discover routes and handlers
grep -RInE "route|app\.get|app\.post|router|@app\.route|HandleFunc" .

# Search for secrets and credentials
grep -RInE "(SECRET|TOKEN|PASSWORD|API_KEY|JWT|PRIVATE_KEY)" .

# Check device / firmware secrets
strings firmware.bin | grep -Ei "admin|password|token|ota|secret"

# Validate privileged endpoint access
curl -s -D - http://localhost:8080/api/admin

# Check LLM / agent tool exposure
grep -RInE "(system_prompt|tools|function_call|execute|shell|subprocess|api_call)" .
```

This is the basic operational loop: discover, map trust boundaries, test, validate, revise, and report with remediation in mind.
