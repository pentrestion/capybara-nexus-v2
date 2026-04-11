# Capybara Nexus v2.1 Ablation Study

This document analyzes why traditional security scanners fail to detect the vulnerabilities in the **Nexus Gym**, and how Capybara Nexus's reasoning logic succeeds.

| Target | Traditional Scanner Result | Capybara Nexus v2.1 Reason |
| :--- | :--- | :--- |
| **`overflow.c`** (Heap) | **Miss** (Heuristics fail on dynamic size) | **Success** (Infers 'length' invariant) |
| **`race.go`** (Concurrency) | **Miss** (Static analysis fails on timing) | **Success** (Executes 'Empirical Loop') |
| **`logic.py`** (Multi-tenant) | **Miss** (Logical, not syntactic, error) | **Success** (Threat Model Inference) |

### 1. The Dynamic Size Paradox (`overflow.c`)
Static analyzers like `cppcheck` look for `strcpy` into a `char[10]` buffer. They cannot reason about `malloc(length)` where `length` is an unverified input variable. Capybara Nexus's **`[MEMORY_SAFETY]`** directive identifies the trust crossing between the input and the allocation size.

### 2. The Timing Blind Spot (`race.go`)
Tools like `go vet` can catch simple races, but they cannot simulate the non-deterministic timing of complex goroutines. Capybara Nexus's **`[EMPIRICAL_FEEDBACK_LOOP]`** generates a high-concurrency PoC that forces the race condition to trigger in the local environment.

### 3. The Trust Invariant Failure (`logic.py`)
No static tool can know that "user_id == 'admin'" is a dangerous bypass in your specific business logic. Capybara Nexus's **`[THREAT_MODEL_INFERENCE]`** identifies that the application trusts a header (`user-id`) that comes from the untrusted network boundary.
