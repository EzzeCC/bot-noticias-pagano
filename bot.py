import feedparser
import time
from datetime import datetime, timedelta
import requests

# --- TUS URLS DE SLACK (Tu webhook + El webhook correcto de Gabriel) ---
SLACK_WEBHOOK_URLS = [
    "https://hooks.slack.com/services/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",
    "https://hooks.slack.com/services/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"
]

def enviar_mensaje_slack(mensaje):
    payload = {"text": mensaje}
    for webhook_url in SLACK_WEBHOOK_URLS:
        try:
            response = requests.post(webhook_url, json=payload)
            if response.status_code == 200:
                print("    -> ¡Mensaje enviado con éxito a Slack!")
            else:
                print(f"    -> Error al enviar a Slack: {response.text}")
        except Exception as e:
            print(f"    -> Error de conexión con Slack: {e}")

def enviar_alerta_slack(titulo, link):
    mensaje = f"🚨 *Noticia de HOY detectada*\n• *Título:* {titulo}\n• *Link:* {link}"
    enviar_mensaje_slack(mensaje)

KEYWORDS = [
    "MARCELA PAGANO", "PAGANO", "DIPUTADA", "ESPOSO", "CONGRESO",
    "CÁMARA DE DIPUTADOS", "COMISIÓN", "INTERNA", "MONO BLOQUE",
    "LIBERTAD AVANZA", "PERIODISTA", "POLÉMICA", "DENUNCIA", "FRANCO BINDI", "BINDI"
]

FEEDS = [
    "https://news.google.com/rss/search?q=Marcela+Pagano&hl=es-419&gl=AR&ceid=AR:es-419",
    "https://news.google.com/rss/search?q=Marcela+Pagano+Franco+Bindi&hl=es-419&gl=AR&ceid=AR:es-419"
]

DOMINIOS_EXCLUIDOS = ["medium.com", "reddit.com", "twitter.com", "facebook.com"]

def escanear():
    hora_actual = datetime.now().strftime("%H:%M:%S")
    print(f"[{hora_actual}] 🔍 Escaneando noticias exclusivas de HOY...")

    encontrados = 0
    limite_tiempo = datetime.now() - timedelta(hours=24)

    for url in FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    fecha_publicacion = datetime.fromtimestamp(time.mktime(entry.published_parsed))
                    if fecha_publicacion < limite_tiempo:
                        continue
                else:
                    continue

                titulo = entry.title
                link = entry.link

                if any(dominio in link.lower() for dominio in DOMINIOS_EXCLUIDOS):
                    continue

                if any(kw in titulo.upper() for kw in KEYWORDS):
                    print(f"\n[MATCH HOY] {titulo}")
                    enviar_alerta_slack(titulo, link)
                    encontrados += 1
        except Exception as e:
            print(f"Error procesando feed: {e}")

    print(f"\nEscaneo finalizado. Se detectaron {encontrados} noticias de hoy.")

    if encontrados == 0:
        aviso_vacio = f"ℹ️ *Reporte de escaneo ({hora_actual})*: Por el momento no tenemos novedades nuevas de Marcela Pagano."
        enviar_mensaje_slack(aviso_vacio)

if __name__ == "__main__":
    escanear()
