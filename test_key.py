import os
import sys

# Read API key from environment variable, CLI arg, or input prompt
API_KEY = os.environ.get("ANTHROPIC_API_KEY")

if not API_KEY and len(sys.argv) > 1:
    API_KEY = sys.argv[1].strip()

# Check for .env file if available
if not API_KEY and os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("ANTHROPIC_API_KEY="):
                API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
                break

if not API_KEY:
    API_KEY = input("Enter your Anthropic API Key: ").strip()

if not API_KEY:
    print("Error: No API key provided.")
    print("Set the ANTHROPIC_API_KEY environment variable or create a .env file.")
    sys.exit(1)

# Model can be passed as 2nd argument or environment variable, defaults to standard model
model_name = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest")

try:
    import anthropic

    client = anthropic.Anthropic(api_key=API_KEY)
    message = client.messages.create(
        model=model_name,
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello, world"}],
    )
    print("Response from Claude:")
    # Extract text from content blocks (handling thinking blocks if present)
    text_parts = [block.text for block in message.content if hasattr(block, "text")]
    print("\n".join(text_parts) if text_parts else str(message.content))

except ModuleNotFoundError:
    print("anthropic library not installed. Using standard library (urllib) to test...")
    import json
    import urllib.request

    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": model_name,
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": "Hello, world"}],
    }

    req = urllib.request.Request(url, headers=headers, data=json.dumps(payload).encode("utf-8"))
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print("Response from Claude:")
        content_blocks = data.get("content", [])
        text_blocks = [b.get("text", "") for b in content_blocks if b.get("type") == "text"]
        print("\n".join(text_blocks))
