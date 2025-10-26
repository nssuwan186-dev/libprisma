import os
import asyncio
import google.generativeai as genai
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- ตั้งค่าตรงนี้ ---
TELEGRAM_TOKEN = "8227507211:AAH7pkYGXSG8IFl9bd5qvaA9TLL8C8KcXhM"
ALLOWED_CHAT_ID = 8144545476
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- ตรวจสอบและตั้งค่า Gemini ---
if not GEMINI_API_KEY:
    print("!!! ไม่พบ GOOGLE_API_KEY ในระบบ !!!")
    print("กรุณาตั้งค่าด้วยคำสั่ง: export GOOGLE_API_KEY='Your_Key_Here'")
    exit()

try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("Gemini API ตั้งค่าเรียบร้อยแล้ว")
except Exception as e:
    print(f"เกิดข้อผิดพลาดในการตั้งค่า Gemini: {e}")
    exit()

def ask_gemini(prompt):
    """ฟังก์ชันสำหรับส่งคำถามไปให้ Gemini API"""
    print(f"Sending to Gemini: {prompt}")
    try:
        response = model.generate_content(prompt)
        result = response.text
        print(f"Received from Gemini: {result}")
        return result
    except Exception as e:
        print(f"An error occurred with Gemini API: {e}")
        return "ขออภัยค่ะ, เกิดข้อผิดพลาดในการเชื่อมต่อกับ Gemini"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ฟังก์ชันสำหรับคำสั่ง /start"""
    await update.message.reply_text('สวัสดีครับ! ผมพร้อมทำงานแล้ว ส่งข้อความมาได้เลย')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ฟังก์ชันสำหรับจัดการข้อความทั่วไป"""
    chat_id = update.message.chat_id
    user_message = update.message.text

    # ตรวจสอบว่ามาจากแชทที่อนุญาตหรือไม่
    if chat_id != ALLOWED_CHAT_ID:
        print(f"ข้อความจาก Chat ID ที่ไม่ได้รับอนุญาต: {chat_id}")
        return

    # แสดง "typing..." ใน Telegram
    await context.bot.send_chat_action(chat_id=chat_id, action='typing')

    # ส่งไปให้ Gemini และรับคำตอบ
    response_text = ask_gemini(user_message)
    
    # ตอบกลับใน Telegram
    await update.message.reply_text(response_text)

def main() -> None:
    """ฟังก์ชันหลักสำหรับรันบอท"""
    print("กำลังเริ่ม Telegram Bot...")
    
    # สร้าง Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # เพิ่ม Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # เริ่มการทำงานของบอท
    print("Bot กำลังทำงาน... (กด Ctrl+C เพื่อหยุด)")
    application.run_polling()

if __name__ == '__main__':
    main()
