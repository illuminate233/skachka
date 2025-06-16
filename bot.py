import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔗 Надішли мені посилання, і я знайду всі зображення на сторінці у найкращій якості.")

def extract_high_quality_images(url):
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        img_urls = set()

        for img in img_tags:
            for attr in ['data-srcset', 'srcset', 'data-src', 'src']:
                src = img.get(attr)
                if src:
                    if " " in src and "," in src:
                        parts = [s.strip() for s in src.split(',')]
                        biggest = sorted(parts, key=lambda x: int(x.split()[-1].replace('w', '').replace('x', '')), reverse=True)[0]
                        src = biggest.split()[0]
                    img_urls.add(requests.compat.urljoin(url, src))
                    break
        return list(img_urls)
    except Exception as e:
        print(f"Error extracting images: {e}")
        return []

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    await update.message.reply_text("🔍 Шукаю зображення...")
    images = extract_high_quality_images(url)
    if not images:
        await update.message.reply_text("❌ Зображення не знайдені або сторінка захищена.")
        return
    for img_url in images[:10]:
        try:
            await update.message.reply_photo(photo=img_url)
        except Exception:
            continue

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

if __name__ == '__main__':
    app.run_polling()
