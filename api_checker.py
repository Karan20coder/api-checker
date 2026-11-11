import os
import sys
import time
import json
import urllib.request
import urllib.error

def load_dotenv():
    """Simple built-in .env loader."""
    env_file = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key not in os.environ:
                        os.environ[key] = val

def mask_key(key: str) -> str:
    """Mask key for display, e.g. sk-ant-usr-1...TQAA"""
    clean = key.strip()
    if len(clean) <= 12:
        return "****"
    return f"{clean[:12]}...{clean[-4:]}"

def detect_provider(key: str) -> str:
    """Detect AI provider by API key format."""
    clean = key.strip()
    if clean.startswith("sk-ant-"):
        return "Anthropic"
    elif clean.startswith("gsk_"):
        return "Groq"
    elif clean.startswith("sk-or-"):
        return "OpenRouter"
    elif clean.startswith("AIzaSy"):
        return "Google Gemini"
    elif clean.startswith("sk-") or clean.startswith("sk-proj-"):
        return "OpenAI"
    return "Unknown"

# ==================== ANTHROPIC CHECKER ====================
def check_anthropic(api_key: str, model: str = None):
    print("\n" + "=" * 60)
    print(f" Checking Anthropic Claude API Key: {mask_key(api_key)}")
    print("=" * 60)

    headers = {
        "x-api-key": api_key.strip(),
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }

    # Step 1: List models
    print("\n[1/2] Verifying credentials & fetching accessible models...")
    t0 = time.time()
    req = urllib.request.Request("https://api.anthropic.com/v1/models", headers=headers)
    available_models = []
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            latency = (time.time() - t0) * 1000
            data = json.loads(resp.read().decode("utf-8"))
            available_models = [m.get("id") for m in data.get("data", [])]
            print(f"  [SUCCESS] Authenticated in {latency:.1f}ms")
            print(f"  Found {len(available_models)} accessible models:")
            for m in available_models[:8]:
                print(f"    * {m}")
            if len(available_models) > 8:
                print(f"    * ... and {len(available_models) - 8} more")
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8")
        print(f"  [FAILED] HTTP {e.code}: {err}")
        return False
    except Exception as e:
        print(f"  [ERROR] Connection error: {e}")
        return False

    # Auto-select the first available model if none specified
    if not model or model not in available_models:
        model = available_models[0] if available_models else "claude-3-5-sonnet-20241022"

    # Step 2: Generation test
    print(f"\n[2/2] Testing message generation with '{model}'...")
    t0 = time.time()
    payload = {
        "model": model,
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": "Respond in one short sentence: 'API key is verified and ready.'"}]
    }
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        data=json.dumps(payload).encode("utf-8")
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            latency = (time.time() - t0) * 1000
            data = json.loads(resp.read().decode("utf-8"))
            content_blocks = data.get("content", [])
            text_blocks = [b.get("text", "") for b in content_blocks if b.get("type") == "text"]
            text = "\n".join(text_blocks).strip()
            usage = data.get("usage", {})
            print(f"  [SUCCESS] Generation completed in {latency:.1f}ms")
            print(f"  Model reply: \"{text}\"")
            print(f"  Token Usage: {usage.get('input_tokens', 0)} in / {usage.get('output_tokens', 0)} out")
            print("\n" + "=" * 60)
            print(" STATUS: ANTHROPIC KEY IS ACTIVE AND 100% OPERATIONAL")
            print("=" * 60 + "\n")
            return True
    except Exception as e:
        print(f"  [FAILED] Generation test failed: {e}")
        return False

# ==================== OPENAI CHECKER ====================
def check_openai(api_key: str):
    print("\n" + "=" * 60)
    print(f" Checking OpenAI API Key: {mask_key(api_key)}")
    print("=" * 60)
    headers = {
        "Authorization": f"Bearer {api_key.strip()}",
        "Content-Type": "application/json",
    }
    t0 = time.time()
    req = urllib.request.Request("https://api.openai.com/v1/models", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            latency = (time.time() - t0) * 1000
            data = json.loads(resp.read().decode("utf-8"))
            models = [m.get("id") for m in data.get("data", [])]
            print(f"  [SUCCESS] Authenticated in {latency:.1f}ms")
            print(f"  Available models ({len(models)} accessible)")
            print("\n" + "=" * 60)
            print(" STATUS: OPENAI KEY IS VALID AND ACTIVE")
            print("=" * 60 + "\n")
            return True
    except urllib.error.HTTPError as e:
        print(f"  [FAILED] HTTP {e.code}: {e.read().decode('utf-8')}")
        return False
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False

# ==================== GEMINI CHECKER ====================
def check_gemini(api_key: str):
    print("\n" + "=" * 60)
    print(f" Checking Google Gemini API Key: {mask_key(api_key)}")
    print("=" * 60)
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key.strip()}"
    t0 = time.time()
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            latency = (time.time() - t0) * 1000
            data = json.loads(resp.read().decode("utf-8"))
            models = [m.get("name") for m in data.get("models", [])]
            print(f"  [SUCCESS] Authenticated in {latency:.1f}ms")
            print(f"  Found {len(models)} accessible models")
            print("\n" + "=" * 60)
            print(" STATUS: GEMINI KEY IS VALID AND ACTIVE")
            print("=" * 60 + "\n")
            return True
    except urllib.error.HTTPError as e:
        print(f"  [FAILED] HTTP {e.code}: {e.read().decode('utf-8')}")
        return False
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False

# ==================== GROQ CHECKER ====================
def check_groq(api_key: str):
    print("\n" + "=" * 60)
    print(f" Checking Groq API Key: {mask_key(api_key)}")
    print("=" * 60)
    headers = {"Authorization": f"Bearer {api_key.strip()}"}
    t0 = time.time()
    req = urllib.request.Request("https://api.groq.com/openai/v1/models", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            latency = (time.time() - t0) * 1000
            data = json.loads(resp.read().decode("utf-8"))
            models = [m.get("id") for m in data.get("data", [])]
            print(f"  [SUCCESS] Authenticated in {latency:.1f}ms")
            print(f"  Found {len(models)} accessible models")
            print("\n" + "=" * 60)
            print(" STATUS: GROQ KEY IS VALID AND ACTIVE")
            print("=" * 60 + "\n")
            return True
    except urllib.error.HTTPError as e:
        print(f"  [FAILED] HTTP {e.code}: {e.read().decode('utf-8')}")
        return False
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False

def route_key(key: str) -> bool:
    """Detect and route key to correct provider checker."""
    provider = detect_provider(key)
    if provider == "Anthropic":
        return check_anthropic(key)
    elif provider == "OpenAI":
        return check_openai(key)
    elif provider == "Google Gemini":
        return check_gemini(key)
    elif provider == "Groq":
        return check_groq(key)
    else:
        print(f"\nProvider could not be detected automatically for key: {mask_key(key)}")
        print("1. Anthropic\n2. OpenAI\n3. Google Gemini\n4. Groq")
        choice = input("Select provider (1-4): ").strip()
        if choice == "1":
            return check_anthropic(key)
        elif choice == "2":
            return check_openai(key)
        elif choice == "3":
            return check_gemini(key)
        elif choice == "4":
            return check_groq(key)
        else:
            print("Invalid choice.")
            return False

def interactive_mode():
    print("""
==================================================
        AI API KEY HEALTH CHECKER
==================================================
Supported Providers:
  - Anthropic Claude (sk-ant-...)
  - OpenAI (sk-...)
  - Google Gemini (AIzaSy...)
  - Groq (gsk_...)

Options:
  1. Check an API Key (auto-detects provider)
  2. Check keys from a file (one key per line)
  3. Exit
    """)
    choice = input("Select an option (1-3): ").strip()

    if choice == "1":
        key = input("\nEnter API Key: ").strip()
        if not key:
            print("No key entered.")
            return
        route_key(key)

    elif choice == "2":
        filepath = input("\nEnter path to file with API keys (e.g. keys.txt): ").strip()
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            return
        with open(filepath, "r", encoding="utf-8") as f:
            keys = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        
        print(f"\nFound {len(keys)} key(s) to verify.")
        results = []
        for i, k in enumerate(keys, 1):
            print(f"\n--- Checking key {i} of {len(keys)} ---")
            is_valid = route_key(k)
            provider = detect_provider(k)
            results.append((mask_key(k), provider, "VALID" if is_valid else "INVALID"))
        
        print("\n" + "=" * 50)
        print(" BATCH SUMMARY")
        print("=" * 50)
        for masked, prov, status in results:
            print(f"  {masked:<25} ({prov:<12}) : {status}")
        print("=" * 50)

    elif choice == "3":
        print("Goodbye!")
        sys.exit(0)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    load_dotenv()

    # CLI argument supplied
    if len(sys.argv) > 1:
        arg = sys.argv[1].strip()
        if os.path.isfile(arg):
            with open(arg, "r", encoding="utf-8") as f:
                keys = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            for k in keys:
                route_key(k)
        else:
            route_key(arg)
    else:
        # Check if environment key exists
        env_key = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("OPENAI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        if env_key:
            provider = detect_provider(env_key)
            print(f"Detected key from environment/.env ({provider}: {mask_key(env_key)}).")
            use_env = input("Check this key? [Y/n]: ").strip().lower()
            if use_env in ("", "y", "yes"):
                route_key(env_key)
                sys.exit(0)

        interactive_mode()
