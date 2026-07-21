# Local PII Guardrail Detection Demo

A local Python implementation demonstrating how to build an isolated, offline privacy guardrail that intercepts and flags Personal Identifiable Information (PII) using **Guardrails AI** and **Microsoft Presidio**.

---

## 📋 Features & Implementation Updates
*   **Offline Mode:** Configured for standalone local execution (`use_local=True`) to avoid network requests and 401 authentication errors.
*   **Direct Architecture Imports:** Upgraded to the modern explicit `guardrails_ai` package namespace format.
*   **Noisy Warning Suppression:** Internal filters silence system event loop warnings and multi-language dictionary mismatched logs (`presidio-analyzer`).

---

## 🛠️ Requirements & System Setup

### 1. Python Version Compatibility
This project utilizes modern Guardrails plugins that strictly require **Python 3.10, 3.11, or 3.12** (`Requires-Python <4, >=3.10`). 

If your machine defaults to an older version (e.g., Python 3.9), upgrade using Homebrew before creating the environment:

```bash
#mac
brew install python@3.13
```

### 2. Isolated Virtual Environment
Initialize a fresh environment tied explicitly to a compatible Python runtime:

```bash
# Remove an older environment if necessary
rm -rf .venv

# Build and activate using a compatible binary
python3.11 -m venv .venv
source .venv/bin/activate
```

### 3. Dependencies Installation
Upgrade your installation tools and pull down the explicit standalone PII detector distribution:

```bash
python -m pip install --upgrade pip
pip install guardrails-ai-detect-pii
```

---

## 🚀 Running the Project

Create a file named `demo_pii.py` and populate it with the optimized solution code below.

and run the application inside your terminal:

```bash
python demo_pii.py
```

---

## 🔍 Troubleshooting Log (Lessons Learned)

During the creation of this project, several configuration boundaries were identified and corrected:

1.  **`command not found: pip`**  
    *   *Cause:* Your machine's PATH environmental paths were disconnected from global executables.
    *   *Fix:* Switched to executing pip explicitly as a python core module: `python3 -m pip install <package>`.
2.  **`Could not find a version that satisfies the requirement`**  
    *   *Cause:* Attempting installation on an unsupported Python system version (e.g., Python < 3.10).
    *   *Fix:* Recreated the environment using a targeted `python3.11` or higher.
3.  **`TypeError: Guard.use() got an unexpected keyword argument`**  
    *   *Cause:* Config keys passed inside the wrapper rather than the child object.
    *   *Fix:* Instantiated the validator instance directly inside the method call: `Guard().use(DetectPII(args...))`.
4.  **`401: Remote Inference Unauthorized`**  
    *   *Cause:* Library defaulting to cloud hosting requiring cloud API keys.
    *   *Fix:* Passed `use_local=True` directly into the class initializer to keep text matching private on the local computer.
5.  **`WARNING:presidio-analyzer:Recognizer not added...`**  
    *   *Cause:* Internal parser trying to bind multilingual profiles (Spanish, Italian, Polish) to an English-only operating system footprint.
    *   *Fix:* Added runtime overrides using Python's `logging` system to filter tracking events lower than `ERROR`.

## 🤖 Continuous Integration (GitHub Actions)

This project includes an automated GitHub Actions CI workflow to verify your PII guardrails on every code push or pull request to the `main` branch. 

> Because it uses local inference, it runs completely free without needing cloud API keys.

### 1. Workflow Configuration

Create a file at `.github/workflows/ci.yml` like [ci.yml](./.github/workflows/ci.yml)


### 2. How it Works

1. When code is pushed, GitHub provisions a clean Linux runner.
2. It enforces the required **Python 3.11** environment.
3. It installs the exact standalone `guardrails-ai-detect-pii` package.
4. It executes `demo_pii.py` to ensure your privacy validators compile and run seamlessly without breaking the build pipeline.
