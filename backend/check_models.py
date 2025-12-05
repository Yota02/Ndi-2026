import google.generativeai as genai
import os

# Remettez votre clé ici
GOOGLE_API_KEY = "AIzaSyA8_k8sAg-kPDPcbdftfpRGHb_q6TV-zE8"
genai.configure(api_key=GOOGLE_API_KEY)

print("🔍 Recherche des modèles disponibles...")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"- {m.name}")