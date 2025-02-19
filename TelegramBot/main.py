from typing import Final
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Cấu hình Google Gemini API
genai.configure(api_key="AIzaSyCEfm_x6S3iTScij5ZeUMJD1OWGS1cMpW4")

# Khởi tạo model AI
model = genai.GenerativeModel("gemini-1.5-flash")

TOKEN: Final = "8189182156:AAGb5yZ-2DMSHUQSzQLEpLnm4PRtaK-29N0"
BOT_USERNAME: Final = "@tusleebigdaddybot"

# Hàm gọi Google Gemini AI
def chat_with_gemini(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)  # Gửi yêu cầu đến Gemini AI
        return response.text  # Lấy nội dung phản hồi
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "Xin lỗi, tôi đang gặp sự cố. Vui lòng thử lại sau!"

# Xử lý tin nhắn từ user
async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    user_id = update.message.chat.id
    print(f'User({user_id}): "{text}"')

    response = chat_with_gemini(text)  # Gửi tin nhắn đến Gemini AI
    print(f'Bot: "{response}"')

    await update.message.reply_text(response)  # Trả lời user

# Lệnh start
async def start_command(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! Tôi là TusLee AI, sẵn sàng giúp bạn!")

# Lệnh help
async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text("Hãy hỏi tôi bất kỳ điều gì!")

# Lệnh custom
async def custom_command(update: Update, context: CallbackContext):
    await update.message.reply_text("TusLee AI luôn bên bạn!")

# Xử lý lỗi
async def error(update: Update, context: CallbackContext):
    print(f"Lỗi xảy ra: {context.error}")

# Khởi chạy bot
if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Thêm lệnh
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    # Xử lý tin nhắn
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Xử lý lỗi
    app.add_error_handler(error)

    # Chạy bot với Polling
    print("Polling...")
    app.run_polling(poll_interval=3)
