#!/usr/bin/env python3
"""
Check available Groq models
"""

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("❌ GROQ_API_KEY not set")
    exit(1)

client = Groq(api_key=api_key)

try:
    models = client.models.list()
    print("\n✅ Available Groq Models:\n")
    print("ID".ljust(40), "Creator", "Active")
    print("-" * 70)
    for model in models.data:
        print(f"{model.id.ljust(40)} {model.owned_by.ljust(10)} {model.active}")
except Exception as e:
    print(f"❌ Error fetching models: {e}")
