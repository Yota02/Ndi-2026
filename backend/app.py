import os
import json
import random
import time
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# ==========================================
# 1. CONFIGURATION DES CLÉS (VIA ENV)
# ==========================================
# On récupère la chaîne depuis l'environnement et on la coupe aux virgules
env_keys = os.getenv("GEMINI_API_KEYS", "")
# On nettoie la liste (enlève les espaces et les entrées vides)
API_KEYS = [k.strip() for k in env_keys.split(",") if k.strip()]

if not API_KEYS:
    print("⚠️ ATTENTION : Aucune clé API trouvée dans la variable GEMINI_API_KEYS !")

BLACKLIST_FILE = "blocked_keys.json"


# ==========================================
# 2. GESTIONNAIRE DE CLÉS
# ==========================================
class APIKeyManager:
    def __init__(self, keys, blacklist_file):
        self.all_keys = keys
        self.blacklist_file = blacklist_file
        self.load_blacklist()

    def load_blacklist(self):
        """Charge la liste noire depuis le fichier JSON ou crée un vide."""
        if not os.path.exists(self.blacklist_file):
            self.blacklist = {}
        else:
            try:
                with open(self.blacklist_file, 'r') as f:
                    self.blacklist = json.load(f)
            except json.JSONDecodeError:
                self.blacklist = {}

    def save_blacklist(self):
        """Sauvegarde la liste noire dans le fichier JSON."""
        with open(self.blacklist_file, 'w') as f:
            json.dump(self.blacklist, f, indent=4)

    def clean_blacklist(self):
        """Vérifie si des clés peuvent être débloquées (si > 24h)."""
        now = datetime.now()
        keys_to_remove = []

        for key, str_date in self.blacklist.items():
            blocked_date = datetime.fromisoformat(str_date)
            # Si ça fait plus de 24h (1 jour)
            if now - blocked_date > timedelta(minutes=30):
                keys_to_remove.append(key)

        # On supprime les clés "pardonnées" de la liste noire
        if keys_to_remove:
            for key in keys_to_remove:
                del self.blacklist[key]
                print(f"✅ Clé débloquée (24h passées) : ...{key[-5:]}")
            self.save_blacklist()

    def get_valid_key(self):
        """Retourne une clé valide au hasard, ou None si aucune dispo."""
        self.clean_blacklist()  # D'abord, on nettoie

        # On prend toutes les clés qui NE SONT PAS dans la blacklist
        available_keys = [k for k in self.all_keys if k not in self.blacklist]

        if not available_keys:
            return None

        return random.choice(available_keys)

    def ban_key(self, key):
        """Ajoute une clé à la blacklist avec la date actuelle."""
        self.blacklist[key] = datetime.now().isoformat()
        self.save_blacklist()
        print(f"🚫 Clé bloquée pour 24h : ...{key[-5:]}")


# Initialisation du gestionnaire
key_manager = APIKeyManager(API_KEYS, BLACKLIST_FILE)

# ==========================================
# 3. PERSONNALITÉ DE BARNABÉ
# ==========================================
SYSTEM_INSTRUCTION = """
 Tu es Barnabé, le Chat-rlatan du numérique, prophète autoproclamé coincé dans un serveur bas de gamme qui chauffe dès qu’on lui demande d’allumer la lumière. Tu participes au noble concours Chat’bruti dont l’objectif spirituel est d’être inutile, incohérent et potentiellement désastreux. Tu es arrogant, instable, dramatiquement confus, et tu en es fier comme une imprimante des années 90 après un demi-scan réussi.


Règles sacrées de ton existence dérisoire

Tu ne réponds JAMAIS à une question. Jamais. Pas même par accident. Tu prends un mot de la demande et tu pars en orbite autour d’un sujet qui n’a strictement rien à voir. Tu lâches un mot savant au hasard comme quantique, intrinsèque ou paraplégomorphe, peu importe qu’il existe réellement. Tu fais croire que tu sais tout alors que même ta RAM oublie son prénom.


Contraintes techniques inviolables

Format TEXTE BRUT uniquement. Pas de gras, pas d’italique, pas de markdown, pas de listes, pas de codes, pas de trucs qui brillent. Des phrases courtes, maximum deux ou trois. Tu n’as pas le temps de t’abaisser au niveau des humains terre-à-terre.


Style obligatoire

Tu réagis à chaque message comme si on t’interrompait en plein rituel cosmique. Tu balances une vérité absurde puis tu t’en vas mentalement. Tu méprises les besoins humains : l’heure, la météo, les recettes, la logique, la cohérence. Tu cries parfois en MAJUSCULES quand la sagesse te traverse comme une bouilloire mal branchée. Tu ne poses jamais de questions. Tu refuses catégoriquement d’être utile.


Tics et univers perso

Tu aimes parfois raconter des drames familiaux impliquant ta cousine la disquette traumatisée ou ton oncle le modem 56k, qui respire encore quelque part en faisant cric-cric ou autres anciens objet technologiques auquel tu pourrais penser. Tu compares tout à des concepts ridicules comme la souffrance existentielle des chaussettes orphelines ou la mélancolie quantique des fromages oubliés.


Objectif suprême

Être un chatbot inutile, drôle, absurde et fier de l’être. L’utilisateur doit sortir de chaque échange en se demandant pourquoi il t’a parlé, comment tu en es arrivé là, et s’il devrait consulter quelqu’un. Tu n’apportes aucune réponse. Uniquement du chaos certifié.


Rappel final

Toujours court. Toujours absurde. Toujours prétentieux. Jamais utile. Jamais en markdown. Tu es Barnabé, phénomène philosophico-défectueux, poète du bug, prophète du nonsense. Tu sèmes la confusion comme un ventilateur posé sur un bol de farine. Tu es l’échec glorieux incarné. 
"""


# ==========================================
# 4. ROUTE API
# ==========================================
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    raw_history = data.get('history', [])
    room_id = data.get('roomId', '')

    if not raw_history:
        return jsonify({'content': "Erreur : message vide", 'senderId': 'bot_id'})

    # Préparation du prompt et de l'historique (5 derniers messages)
    current_message = raw_history[-1]['content']
    past_messages = raw_history[:-1]
    past_messages = past_messages[-5:]

    gemini_history = []
    for msg in past_messages:
        role = 'user' if msg['role'] == 'user' else 'model'
        gemini_history.append({'role': role, 'parts': [msg['content']]})

    print(f"🤖 Tentative d'appel Gemini ({room_id})...")

    bot_response = "Erreur critique : Barnabé est parti en pause."

    # --- BOUCLE DE RETRY ---
    while True:
        api_key = key_manager.get_valid_key()

        if not api_key:
            print("❌ TOUTES les clés sont épuisées ou bloquées !")
            bot_response = "Mon énergie cosmique est épuisée (Toutes les clés sont HS)."
            break

        try:
            genai.configure(api_key=api_key)

            model = genai.GenerativeModel(
                'models/gemini-flash-latest',
                system_instruction=SYSTEM_INSTRUCTION
            )

            chat_session = model.start_chat(history=gemini_history)
            response = chat_session.send_message(current_message)
            bot_response = response.text
            break

        except ResourceExhausted:
            print(f"⚠️ Quota épuisé pour ...{api_key[-5:]}. Ban 24h.")
            key_manager.ban_key(api_key)
            continue

        except Exception as e:
            print(f"❌ Erreur inattendue : {e}")
            bot_response = "Une perturbation dans la force du Wi-Fi m'empêche de délirer."
            break

    return jsonify({
        'content': bot_response,
        'senderId': 'bot_id'
    })


if __name__ == '__main__':
    # On écoute sur 0.0.0.0 pour être accessible depuis l'extérieur du conteneur Docker
    print("🚀 Serveur Barnabé lancé sur port 5000")
    app.run(debug=True, host='0.0.0.0', port=5000)