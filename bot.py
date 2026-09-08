import os
import time
from rubka import Robot, Message

# ===== تنظیمات =====
TOKEN = "CDIBFG0LOWKACQPCLOMUZYMXHATMXOPJXNOZEJVDBLAGQYTOWBOQRTZWGHZPQTLS"  # ← توکن رو اینجا عوض کن

# پوشه دانلود (اگه وجود نداشته باشه خودش ساخته میشه)
DOWNLOAD_FOLDER = "./downloads"
# ===================

# مطمئن میشیم پوشه وجود داره
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)
    print(f"📁 پوشه {DOWNLOAD_FOLDER} ساخته شد")

bot = Robot(token=TOKEN)

def get_file_type(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    
    # تصاویر
    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff']:
        return "Image"
    
    # ویدیوها
    if ext in ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.3gp', '.m4v', '.webm']:
        return "Video"
    
    # موسیقی
    if ext in ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.opus']:
        return "Audio"
    
    # سایر
    return "Document"

@bot.on_message(commands=["#"])
async def handle_hash(bot: Robot, message: Message):
    # گرفتن لیست همه فایل‌ها
    try:
        files = [os.path.join(DOWNLOAD_FOLDER, f) for f in os.listdir(DOWNLOAD_FOLDER) 
                 if os.path.isfile(os.path.join(DOWNLOAD_FOLDER, f))]
    except Exception as e:
        await message.reply_text(f"❌ خطا در خواندن پوشه: {e}")
        return
    
    if not files:
        await message.reply_text(f"⚠️ پوشه {DOWNLOAD_FOLDER} خالی است!\nلطفاً فایل‌هایی در آن قرار دهید.")
        return
    
    # ارسال همه فایل‌ها
    success_count = 0
    fail_count = 0
    
    for file_path in files:
        file_type = get_file_type(file_path)
        file_name = os.path.basename(file_path)
        
        try:
            with open(file_path, 'rb') as f:
                if file_type == "Image":
                    await bot.send_image(chat_id=message.chat_id, image=f, caption=file_name)
                elif file_type == "Video":
                    await bot.send_video(chat_id=message.chat_id, video=f, caption=file_name)
                elif file_type == "Audio":
                    await bot.send_audio(chat_id=message.chat_id, audio=f, caption=file_name)
                else:
                    await bot.send_document(chat_id=message.chat_id, document=f, caption=file_name)
                
                success_count += 1
                time.sleep(0.5)  # کمی تاخیر بین ارسال‌ها
                
        except Exception as e:
            fail_count += 1
            await message.reply_text(f"❌ خطا در ارسال {file_name}: {e}")
    
    await message.reply_text(f"✅ ارسال کامل شد!\n📤 موفق: {success_count}\n❌ ناموفق: {fail_count}")

@bot.on_message()
async def handle_other(bot: Robot, message: Message):
    # پیام‌های غیر از # رو نادیده بگیر
    pass

if __name__ == "__main__":
    print("🤖 ربات روشن شد...")
    print(f"📁 پوشه دانلود: {os.path.abspath(DOWNLOAD_FOLDER)}")
    print("📩 برای ارسال فایل‌ها، پیام # را بفرستید")
    print("=" * 50)
    bot.run()
