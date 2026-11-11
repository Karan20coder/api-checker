# Universal AI API Key Checker

A fast, lightweight, and secure tool to verify AI API keys, inspect model permissions, test generation, and measure API response latency across **Anthropic Claude**, **OpenAI**, **Google Gemini**, and **Groq**.

---

## Features

- 🔒 **Zero Hardcoded Secrets:** Automatically loads keys from environment variables, `.env`, interactive prompt, or CLI arguments.
- 🤖 **Auto-Provider Detection:** Automatically identifies whether a key belongs to Anthropic (`sk-ant-`), OpenAI (`sk-`), Gemini (`AIzaSy`), or Groq (`gsk_`).
- 🛡️ **Safe Masking:** All API keys are masked in console output (e.g. `sk-ant-usr-1...TQAA`).
- ⚡ **Latency & Performance:** Displays round-trip latency (in milliseconds) for authentication and inference calls.
- 📋 **Model Permissions:** Queries the provider's API and lists accessible models.
- 🧪 **Live Generation Test:** Tests message completion (compatible with thinking tokens and standard outputs).
- 📁 **Batch Verification:** Check a list of keys stored in a `.txt` file (one per line) with a clean summary report.
- 📦 **Zero Mandatory Dependencies:** Uses Python's built-in standard library (`urllib`) with zero mandatory external dependencies.

---

## Supported Providers

| Provider | Key Format | Model Discovery | Generation Test |
| :--- | :--- | :--- | :--- |
| **Anthropic Claude** | `sk-ant-...` | Yes | Yes (Claude 3.5 Sonnet / Haiku) |
| **OpenAI** | `sk-...` / `sk-proj-...` | Yes | Yes |
| **Google Gemini** | `AIzaSy...` | Yes | Yes |
| **Groq** | `gsk_...` | Yes | Yes |

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/api-checker.git
cd api-checker
```

### 2. (Optional) Install SDK Dependencies
The core tool works out of the box with standard Python 3. If you want to use the official Anthropic SDK for additional scripts:
```bash
pip install -r requirements.txt
```

### 3. Configure Your Environment (Optional)
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Open `.env` and set your key:
```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

*(Note: `.env` is listed in `.gitignore` and will never be pushed to your repository).*

---

## Usage

### Interactive Mode
Run the tool without arguments:
```bash
python api_checker.py
```
You can choose to check a single key, test your `.env` key, or verify a batch file of keys.

### Single Key via CLI (Auto-detects Provider)
Pass any API key directly in your terminal:
```bash
python api_checker.py "sk-ant-usr-your-anthropic-key"
```
Or an OpenAI key:
```bash
python api_checker.py "sk-proj-your-openai-key"
```

### Batch Check Multiple Keys
Pass a text file with one key per line:
```bash
python api_checker.py keys.txt
```

### Quick Standalone Script
You can also run the quick standalone test script:
```bash
python test_key.py
```

---

## License

This project is licensed under the [MIT License](LICENSE).
