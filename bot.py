import re
from pyrogram import Client, filters

API_ID = 12345678  # ضع الـ API_ID الخاص بك
API_HASH = "your_api_hash_here"  # ضع الـ API_HASH هنا
BOT_TOKEN = "8704455695:AAF2lpZ_Jx5UghGIBKnz4YBM6f5SwJZk_A"  # توكن البوت

app = Client("Alokimibot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# معرفات المجموعتين (مجموعة التجارب وقناة صفقات ماجد)
TARGET_CHAT_IDS = [
    -"-100xxxxxxxxxx",  
    -"-100yyyyyyyyyy",  
]

# متغير لحفظ حالة البوت (مغلق افتراضياً)
bot_active = False


# أمر التشغيل من محادثتك الخاصة
@app.on_message(filters.command("start_bot") & filters.private)
async def start_bot(client, message):
  global bot_active
  bot_active = True
  await message.reply(
      "🟢 تم تفعيل البوت! بدأ المراقبة الفعالة للمجموعتين معاً."
  )


# أمر الإيقاف من محادثتك الخاصة
@app.on_message(filters.command("stop_bot") & filters.private)
async def stop_bot(client, message):
  global bot_active
  bot_active = False
  await message.reply("🔴 تم إيقاف البوت مؤقتاً بناءً على طلبك.")


# مراقبة المجموعتين معاً
@app.on_message(filters.chat(TARGET_CHAT_IDS))
async def extract_signal_pair(client, message):
  global bot_active
  if not bot_active:
    return  # البوت متوقف، لا يراقب شيئاً

  text = message.text or message.caption
  if not text:
    return

  # تصفية الرسائل واستهداف التوصيات فقط
  if "سعر الدخول:" in text or "التوصية:" in text or "المدة: 5 دقائق" in text:
    pattern = r"\b([A-Z]{3}[\/\-][A-Z]{3})\b"
    pairs = re.findall(pattern, text)

    if pairs:
      target_pair = pairs[0]
      await client.send_message(
          message.from_user.id if message.from_user else "me",
          f"🎯 تم التقاط زوج جديد:\n{target_pair}",
      )


print("البوت جاهز ويعمل بكامل إعدادات التحكم والربط.")
app.run()
