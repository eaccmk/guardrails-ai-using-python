import sys
import logging
import warnings

from guardrails import Guard
from guardrails_ai.detect_pii import DetectPII

# Silence the underlying Microsoft Presidio analyzer warnings like:
# WARNING:presidio-analyzer:Recognizer not added to registry because language is not supported by registry - CreditCardRecognizer supported languages: es, registry supported languages: en
logging.getLogger("presidio-analyzer").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=UserWarning, module="guardrails")

def run_demo():
    print("--- Initializing PII Guardrail ---")
    
    # 1. Local execution setup : Initialize the guardrail with the entities you want to scan for.
    guard = Guard().use(
        DetectPII(
            pii_entities=["EMAIL_ADDRESS", "PHONE_NUMBER"], 
            on_fail="exception",
            use_local=True
    )
    )

    # 2. Test Case A: Safe input text
    safe_text = "Hello! I am reviewing the documentation for our upcoming API rollout."
    print(f"\n[Test 1] Validating safe text: '{safe_text}'")
    
    try:
        guard.validate(safe_text)
        print("✅ Success: No sensitive data detected. Text is safe to process.")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

    # 3. Test Case B: Input text containing PII
    unsafe_text = "Please reach out to me directly at dev_support@example.com or call 555-0199."
    print(f"\n[Test 2] Validating unsafe text: '{unsafe_text}'")
    
    try:
        guard.validate(unsafe_text)
        print("✅ Success: Text passed validation.")
    except Exception as e:
        print("❌ Guardrail Blocked Prompt! Sensitive PII data was found.")
        print(f"Detailed Error: {e}")
        # Add this line if you want GitHub Actions to intentionally report a failure when PII leaks
        sys.exit(1)

if __name__ == "__main__":
    run_demo()
