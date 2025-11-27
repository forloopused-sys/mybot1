import requests
import platform
import socket
import psutil
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8535356385:AAG4sieAh2JqbnSy93qqMbZUL_UtgTudqUY"

def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "Unable to fetch public IP."

def get_local_ip():
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except:
        return "Unable to fetch local IP."

def get_device_info():
    info = {
        "System": platform.system(),
        "Node Name": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "CPU Cores": psutil.cpu_count(logical=True),
        "Total RAM (GB)": round(psutil.virtual_memory().total / (1024**3), 2)
    }
    return info

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Send /info to get device details.")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    public_ip = get_public_ip()
    local_ip = get_local_ip()
    device = get_device_info()

    message = "📡 Device & Network Information\n\n"
    message += f"🌐 Public IP: {public_ip}\n"
    message += f"🏠 Local IP: {local_ip}\n\n"
    message += "💻 Device Details:\n"
    for k, v in device.items():
        message += f"- {k}: {v}\n"

    await update.message.reply_text(message)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))

    print("Bot is running…")
    app.run_polling()  # <-- No await, works on Windows

if __name__ == "__main__":
    main()
