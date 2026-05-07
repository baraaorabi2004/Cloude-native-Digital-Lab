import google.generativeai as genai
import os

API_KEY = os.environ.get("GEMINI_KEY", "AIzaSyB4DqnmzAUdrsUNyeiXERKIEFG-LdbwEWA")
genai.configure(api_key=API_KEY)

print("--- Available Models ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model Name: {m.name}")
except Exception as e:
    print(f"Error: {e}")
