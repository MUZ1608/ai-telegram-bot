import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram import F
import asyncio
import subprocess
import os

# TOKENINGNI BU YERGA QO‘Y
API_TOKEN = "7834723423:AAForTjvHGVp42V3K0QXOFqbInkiz9BWwq0"

# Bot va dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# /start komandasi
@dp.message(CommandStart())
async def handle_start(message: types.Message):
    await message.answer("👋 Salom, botga hush kelibsan!\nMenga YouTube yoki Instagram havolasi yubor — men senga video bilan birga post yozuvini ham chiqarib beraman!")

# YouTube + Instagram media yuklovchi va caption chiqaruvchi
@dp.message(F.text)
async def download_media(message: types.Message):
    url = message.text.strip()

    if "youtu" in url or "instagram.com" in url:
        await message.reply("⏬ Yuklab olinmoqda...qo'toq sozib turing ,tezroq bo'ladi!...")

        try:
            # 1. CAPTION ajratib olish
            caption_result = subprocess.run(
                ["yt-dlp", "--print", "%(description)s", url],
                capture_output=True, text=True
            )
            caption_text = caption_result.stdout.strip()

            # 2. VIDEO yuklab olish
            filename = "media.mp4"
            subprocess.run(
                ["yt-dlp", "-f", "best[ext=mp4]", "-o", filename, url],
                check=True
            )

            # 3. Yuborish
            video = FSInputFile(path=filename)
            if caption_text:
                await bot.send_video(message.chat.id, video, caption=f"📄 {caption_text[:1020]}")
            else:
                await bot.send_video(message.chat.id, video)

            os.remove(filename)

        except Exception as e:
            await message.reply(f"❌ Xatolik:\n<code>{str(e)}</code>", parse_mode=ParseMode.HTML)

    else:
        await message.reply("⛔ Faqat YouTube yoki Instagram havolasini yuboring.")

# Botni ishga tushurish
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
