import os
import random
import asyncio
from telegram import Update, ReactionTypeEmoji
from telegram.ext import Application, ContextTypes, MessageHandler, filters

# Configuration
RENDER_URL = "https://test-bot-1-1c5g.onrender.com"  # Your Render URL
PORT = 10000  # Render's required port
REACTION_EMOJIS = ["👍", "❤️", "🔥", "🥰", "👏", "😄", "🎉", "🤩"]

# List of bot tokens
BOT_TOKENS = [
    "8084840411:AAHTa2dD5n_3EGP7_B5AVp-OXXCnfZBAoI0",
"7218699799:AAFnNOtlyfqcGuBHydCI6q5UoRR63xFwjnc",
"8175165766:AAH4YgCdqpuiYO6gtZhihper-52Afds8OYo",
"7053167093:AAEBXtxWFVms_ymSc-8V3z6gX6ex-qq7iU4",
"7973249393:AAFacmwJSaWsBcuV0wKfTCyFybl6E9i3CtI",
"7869923971:AAFk2KiR_xvDyOhiV21zj1z6Te-FISQ5x4M",
"7982174990:AAEi9guKRFgXFk2B5Dz6Tev9AmxK69w5SGM",
"7358756678:AAH69NvK7u_kl_TnqtHYzunQ09AwejWNjHg",
"8029878430:AAETgO3KgOYSlxcRh8RewxEJ-pOJp048C20",
"8027380950:AAGI8M_cwaw38iF6p9IxBKIHC1I8X2smjrk",
"8013008477:AAGP5RSekk-ZVxyFo1oRLh5cxcMtV6e7X6E",
"8108660905:AAGf6vEB75olB6NWoDTjxo8e-JHx82-nxU8",
"7826951523:AAEl7FjI8Nd43GyFmrYIefuts5KzXTCpl9c",
"7916551884:AAGAl_rX9WGgDZq2NTUSy0mzxt7V2qpdBcE",
"7769596189:AAEIwjKIvF7r6uflSFkzr5R7kfhRrKwr5XA",
"7123067873:AAGPDpzQvIDyNDjMNhBMqS-ADISyDCGig_M",
"7881204841:AAHUHbpLoA_f7V9h4bObb_dGUPHDnkYvhS8",
"7695761547:AAFq2NQlwESTTn9o0j83MaG9MHszze2scWs",
"8050489504:AAHT9EuVjJey3aGLmcw5TneLuT9MXf1ih7Q",
"8149603943:AAHhAO9_t1CH5B-WPuZcqXB51yLaecf1HXg"
    # Add more tokens as needed...
]



async def auto_react(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        post = update.message or update.channel_post
        if post and post.chat.type in ["channel", "supergroup", "group"]:
            emoji = random.choice(REACTION_EMOJIS)
            await post.set_reaction([ReactionTypeEmoji(emoji)])
    except:
        pass

async def setup_bot(bot_token: str):
    app = Application.builder().token(bot_token).build()
    app.add_handler(MessageHandler(
        filters.ChatType.CHANNEL | filters.ChatType.GROUPS,
        auto_react
    ))
    
    if os.getenv('RENDER'):
        # Webhook configuration for the primary bot only
        if bot_token == BOT_TOKENS[0]:  # First bot handles webhook
            await app.bot.set_webhook(
                f"{RENDER_URL}/{bot_token}",
                allowed_updates=["message", "channel_post"]
            )
            await app.run_webhook(
                listen="0.0.0.0",
                port=PORT,
                url_path=bot_token,
                webhook_url=f"{RENDER_URL}/{bot_token}"
            )
        else:
            # Secondary bots use polling
            await app.initialize()
            await app.start()
            await app.updater.start_polling()
    else:
        # Local development - all bots poll
        await app.initialize()
        await app.start()
        await app.updater.start_polling()

async def main():
    await asyncio.gather(*[setup_bot(token) for token in BOT_TOKENS])

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
