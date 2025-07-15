import requests
from bs4 import BeautifulSoup
import os

# Configuración
url = "https://www.educa.jcyl.es/profesorado/es/oposiciones/oposiciones-cuerpo-maestros/oposiciones-2025-cuerpo-maestros"
bot_token = os.getenv("7993611113:AAH4tdw0dvziFeDZvpM4RB0RfJ1cP33mzJ8")  # Cargado desde variable en Railway
chat_id = os.getenv("8433465")      # Cargado desde variable en Railway
registro_url = "registro_urls.txt"

def obtener_noticias():
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        articulos = soup.find_all('article')
        noticias = []
        for a in articulos:
            h2 = a.find('h2')
            link = a.find('a', href=True)
            if h2 and link:
                titulo = h2.get_text(strip=True)
                enlace = link['href']
                if not enlace.startswith("http"):
                    enlace = "https://www.educa.jcyl.es" + enlace
                noticias.append((titulo, enlace))
        return noticias
    except Exception as e:
        print("⚠️ Error:", e)
        return []

def enviar_telegram(msg):
    if not bot_token or not chat_id:
        print("❌ BOT_TOKEN o CHAT_ID no definido.")
        return
    try:
        requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage", params={
            "chat_id": chat_id,
            "text": msg
        })
    except Exception as e:
        print("❌ Error enviando Telegram:", e)

def cargar_urls_previas():
    try:
        with open(registro_url, "r") as f:
            return set(l.strip() for l in f.readlines())
    except FileNotFoundError:
        return set()

def guardar_urls(urls):
    with open(registro_url, "w") as f:
        for u in urls:
            f.write(u + "\\n")

# === EJECUCIÓN UNA SOLA VEZ ===
vistos = cargar_urls_previas()
nuevas = obtener_noticias()

for titulo, enlace in nuevas:
    if enlace not in vistos:
        msg = f"📰 ¡Nueva publicación detectada!\\n📌 {titulo}\\n🔗 {enlace}"
        enviar_telegram(msg)
        print(f"✅ Notificada: {titulo}")
        vistos.add(enlace)

guardar_urls(vistos)
