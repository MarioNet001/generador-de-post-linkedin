import os
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from dotenv import load_dotenv

from src.youtube_transcript import get_yt_transcript
from src.ai_engine import generate_linkedin_post, generate_infographic_content, generate_infographic_svg
from src.excel_storage import save_to_local_excel
from src.utils import setup_logger, convert_svg_to_png

load_dotenv()
logger = setup_logger("telegram_bot")

async def process_video_logic(update: Update, context: ContextTypes.DEFAULT_TYPE, video_url: str):
    """Lógica central: Transcripción -> Post -> Excel -> Infografía."""
    context.user_data['last_video_url'] = video_url
    
    if update.callback_query:
        await update.callback_query.answer()
        status_msg = await update.callback_query.message.reply_text("🔄 Procesando...")
    else:
        status_msg = await update.message.reply_text("👀 Procesando video...")

    try:
        transcript = get_yt_transcript(video_url)
        post = generate_linkedin_post(transcript)
        
        try:
            save_to_local_excel(f"Post: {video_url}", post)
        except PermissionError:
            await status_msg.edit_text("⚠️ El archivo Excel está abierto. Cerralo.")
            raise

        await status_msg.delete()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"🚀 **¡Post Generado!**\n\n{post}", parse_mode='Markdown')

        keyboard = [[InlineKeyboardButton("✅ Sí, crear infografía", callback_data='gen_info_yes'),
                     InlineKeyboardButton("❌ No, gracias", callback_data='gen_info_no')]]
        context.user_data['last_transcript'] = transcript
        await send_safe_message(context.bot, update.effective_chat.id, "¿Deseas crear una infografía?", reply_markup=InlineKeyboardMarkup(keyboard))

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        keyboard = [[InlineKeyboardButton("🔄 Reintentar", callback_data='retry_video_process')]]
        await send_safe_message(context.bot, update.effective_chat.id, f"❌ Error: {str(e)}", reply_markup=InlineKeyboardMarkup(keyboard))

async def send_safe_message(bot, chat_id, text, reply_markup=None):
    try:
        await bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown', reply_markup=reply_markup)
    except Exception:
        await bot.send_message(chat_id=chat_id, text=text, parse_mode=None, reply_markup=reply_markup)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hola! Soy tu asistente de LinkedIn. Mandame una URL de YouTube.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "youtube.com" in update.message.text or "youtu.be" in update.message.text:
        await process_video_logic(update, context, update.message.text)
    else:
        await update.message.reply_text("❌ URL inválida.")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'retry_video_process':
        url = context.user_data.get('last_video_url')
        if url: await process_video_logic(update, context, url)
    elif query.data == 'gen_info_yes':
        transcript = context.user_data.get('last_transcript')
        if not transcript: return
        await query.edit_message_text(text="🎨 Diseñando infografía...")
        try:
            svg_code = generate_infographic_svg(transcript)
            temp_dir = ".tmp"
            if not os.path.exists(temp_dir): os.makedirs(temp_dir)
            
            svg_path = os.path.join(temp_dir, f"inf_@{update.effective_chat.id}.svg")
            png_path = os.path.join(temp_dir, f"inf_@{update.effective_chat.id}.png")
            
            with open(svg_path, "w", encoding="utf-8") as f: f.write(svg_code)

            if convert_svg_to_png(svg_path, png_path):
                with open(png_path, "rb") as p:
                    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=p, caption="✨ Tu infografía!")
            
            with open(svg_path, "rb") as d:
                await context.bot.send_document(chat_id=update.effective_chat.id, document=d, filename="vector.svg")
        except Exception as e:
            await query.message.reply_text(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if token:
        app = ApplicationBuilder().token(token).build()
        app.add_handler(CommandHandler('start', start))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        app.add_handler(CallbackQueryHandler(button_callback))
        print("🤖 Bot iniciado...")
        app.run_polling()
