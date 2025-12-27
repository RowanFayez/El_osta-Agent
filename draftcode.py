import json
import torch
import re
from typing import Dict
from transformers import AutoTokenizer, AutoModelForCausalLM


# =====================
# CONFIG
# =====================
LOCAL_MODEL_PATH = "/Users/tokamohamed/Downloads/langgraph_ai_agent/qwen_finetuned_model"


SYSTEM_PROMPT = """
You are a routing NLU system.

Extract routing information from Egyptian Arabic text.

Output ONLY valid JSON using this schema:
{
    "intent": "find_route | plan_multistop_trip | chitchat",
    "stops": [
        { "type": "origin | destination", "place": string }
    ]
}

Rules:
- Do NOT explain
- Do NOT translate names
- Do NOT add text outside JSON
"""


# =====================
# LOAD MODEL
# =====================
tokenizer = None
model = None


def load_local_model():
        global tokenizer, model

        if model is not None:
                return

        tokenizer = AutoTokenizer.from_pretrained(
                LOCAL_MODEL_PATH,
                trust_remote_code=True,
                fix_mistral_regex=True
        )

        model = AutoModelForCausalLM.from_pretrained(
                LOCAL_MODEL_PATH,
                device_map="auto",
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                trust_remote_code=True
        )

        model.eval()


# =====================
# JSON SAFE EXTRACTION
# =====================
def extract_json(text: str) -> Dict:
        # Try to find the last occurrence of JSON (after "Assistant JSON:")
        lines = text.split('\n')
        
        # Search backwards for valid JSON
        for i in range(len(lines) - 1, -1, -1):
                line = lines[i].strip()
                if line.startswith('{'):
                        # Try to extract JSON from this line onwards
                        remaining_text = '\n'.join(lines[i:])
                        match = re.search(r'\{[^}]*"intent"[^}]*"stops"[^}]*\}', remaining_text, re.DOTALL)
                        if match:
                                json_str = match.group()
                                # Remove any trailing ]
                                json_str = re.sub(r'\]\s*$', '', json_str)
                                try:
                                        return json.loads(json_str)
                                except json.JSONDecodeError:
                                        continue
        
        # Fallback: try to find any JSON object
        match = re.search(r'\{[\s\S]*?\}', text)
        if not match:
                raise ValueError("No JSON found in output")

        json_str = match.group()
        # Clean up common issues
        json_str = re.sub(r'\]\s*\]\s*$', ']', json_str)  # Remove duplicate closing brackets
        
        try:
                return json.loads(json_str)
        except json.JSONDecodeError as e:
                print(f"[DEBUG] Failed JSON string: {json_str}")
                raise ValueError(f"Invalid JSON format: {e}")


# =====================
# LOCAL LLM PARSER
# =====================
def parse_with_local_llm(user_input: str) -> Dict:
        load_local_model()

        if tokenizer is None or model is None:
                raise RuntimeError("Model failed to load")

        prompt = f"""
{SYSTEM_PROMPT}

User:
{user_input}

JSON:
"""

        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

        with torch.no_grad():
                outputs = model.generate(
                        **inputs,
                        max_new_tokens=256,
                        do_sample=False,
                        pad_token_id=tokenizer.eos_token_id
                )

        decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print("\n========== RAW MODEL OUTPUT ==========")
        print(decoded)
        print("=====================================\n")
        
        return extract_json(decoded)


# =====================
# HELPERS
# =====================
def extract_origin_destination(parsed: Dict) -> Dict:
        origin = None
        destination = None

        for stop in parsed.get("stops", []):
                if stop.get("type") == "origin":
                        origin = stop.get("place")
                elif stop.get("type") == "destination":
                        destination = stop.get("place")

        return {
                "origin": origin,
                "destination": destination,
                "intent": parsed.get("intent")
        }


# =====================
# PUBLIC API
# =====================
def llm_parse(user_input: str) -> Dict:
        try:
                parsed = parse_with_local_llm(user_input)
                print(f"[DEBUG] Extracted JSON: {parsed}")
                return extract_origin_destination(parsed)

        except Exception as e:
                print("[LLM PARSE ERROR]", e)
                import traceback
                traceback.print_exc()
                return {
                        "origin": None,
                        "destination": None
                }
