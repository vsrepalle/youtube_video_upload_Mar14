import json
import sys
import os
import re
from google import genai
from openai import OpenAI
from dotenv import load_dotenv

# ────────────────────────────────────────────────
#                  LOAD ENV VARIABLES
# ────────────────────────────────────────────────

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROK_API_KEY = os.getenv("GROK_API_KEY")

if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY not found in environment variables")
    sys.exit(1)

if not GROK_API_KEY:
    print("❌ GROK_API_KEY not found in environment variables")
    sys.exit(1)

# ────────────────────────────────────────────────
#                  CONFIGURATION
# ────────────────────────────────────────────────

# List of Gemini models to try (in order of preference)
GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-latest",
    "gemini-2.5-pro",
    "gemini-2.5-flash-lite",
]

# Grok models to try (in order)
GROK_MODELS = [
    "grok-4.20-beta-0309",
    "grok-4-0709",
    "grok-4.20-multi-agent-beta-0309",
    "grok-3-mini",
]

# ────────────────────────────────────────────────
#                  HELPERS
# ────────────────────────────────────────────────

def clean_json_text(text: str) -> str:
    """Extract JSON from common LLM response patterns"""
    if not text:
        return ""

    text = re.sub(r'^```(?:json)?\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s*```$', '', text)

    text = text.strip()

    match = re.search(r'(\{.*\})', text, re.DOTALL)
    if match:
        text = match.group(1)

    return text


def try_gemini(prompt: str) -> str | None:
    print("📡 Attempting Gemini (Primary)...")

    client = genai.Client(api_key=GEMINI_API_KEY)

    for model_name in GEMINI_MODELS:
        print(f"  → Trying model: {model_name}")
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            raw = response.text
            print(f"  ✓ {model_name} succeeded")
            return raw

        except Exception as e:
            print(f"  ✗ {model_name} failed: {str(e)[:120]}...")
            continue

    print("⚠️ All Gemini models failed.")
    return None


def try_grok(prompt: str) -> str | None:
    print("🚀 Attempting Grok (Fallback)...")

    client = OpenAI(
        api_key=GROK_API_KEY,
        base_url="https://api.x.ai/v1"
    )

    for model_name in GROK_MODELS:
        print(f"  → Trying model: {model_name}")

        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a JSON-only news generator. Respond with valid JSON only — no explanations, no markdown, no fences."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=4096
            )

            raw = response.choices[0].message.content
            print(f"  ✓ {model_name} succeeded")

            return raw

        except Exception as e:
            print(f"  ✗ {model_name} failed: {str(e)[:120]}...")
            continue

    print("⚠️ All Grok models failed.")
    return None


def generate_script(channel_type: str):

    prompt_path = f"prompts/prompt_{channel_type}.txt"

    if not os.path.exists(prompt_path):
        print(f"❌ Prompt file not found: {prompt_path}")
        return

    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt = f.read().strip()

    print(f"\n🔍 Generating script for channel: {channel_type}")
    print(f"  Prompt file: {prompt_path} ({len(prompt):,} chars)\n")

    raw_text = try_gemini(prompt)

    if not raw_text:
        raw_text = try_grok(prompt)

    if not raw_text:
        print("💀 Both AI providers failed. Cannot continue.")
        return

    cleaned = clean_json_text(raw_text)

    try:
        data = json.loads(cleaned)

        output_file = "data.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"\n✅ Success! Wrote clean JSON to: {output_file}")
        print(f"   → {len(data)} top-level keys found\n")

    except json.JSONDecodeError as e:

        print("\n❌ JSON parsing failed even after cleaning.")
        print(f"Error: {e}")

        print("\nRaw model output (first 800 chars):")
        print("─" * 60)

        print(raw_text[:800] + "..." if len(raw_text) > 800 else raw_text)

        print("─" * 60)

        with open("failed_response.txt", "w", encoding="utf-8") as f:
            f.write(raw_text)

        print("→ Saved full raw response to: failed_response.txt")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python generate_data_json.py [channel_type]")
        print("Example: python generate_data_json.py spacemind")
        sys.exit(1)

    channel = sys.argv[1].strip().lower()

    generate_script(channel)