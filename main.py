import os
import random
import string
from dotenv import load_dotenv
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# .env dan token, admin id va proxy ni yuklash
load_dotenv()
BOT_TOKEN = os.getenv("TOKEN")
CHANNEL_ID = '@BATLEE1VS1Comunity'
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

if not BOT_TOKEN or not ADMIN_CHAT_ID:
    raise ValueError("Iltimos, .env faylini to'g'ri sozlang va TOKEN va ADMIN_CHAT_ID ni kiriting!")

USERS_FILE = "users.py"

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as file:
                return eval(file.read())
        except Exception as e:
            print(f"Xatolik: {e}")
            return {}
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as file:
        file.write(repr(users))

translations = {
    'uz': {
        'welcome': 'Tilni tanlang:',
        'subscribe_channels': 'Quyidagi kanallarga obuna bo\'ling:',
        'check_subscription': '✅ Obunani tekshirish',
        'subscription_success': '🎉 Tabriklaymiz! Botdan foydalanishga ruxsat berildi.',
        'subscription_failed': '❌ Siz quyidagi kanallarga obuna bo\'lmagansiz:',
        'error_message': 'Botda xatolik yuz berdi. Qayta urinib ko\'ring.',
        'my_score': '🌟 Sizning balingiz: {}\n👥 Taklif qilinganlar: {}',
        'invite_friends': '👥 Do\'stlaringizga havolani yuboring:\n{}',
        'contact_admin': '📞 Admin bilan bog\'lanish',
        'admin_contacted': 'Admin bilan bog\'lanish uchun quyidagi tugmani bosing:',
        'top_referrers_title': '🏆 Haftalik eng ko\'p taklif qilganlar:',
        'no_top_referrers': 'Hozirda hech kim taklif qilmagan.',
        'referral_subscribed': '🎉 Siz taklif qilgan foydalanuvchi to\'liq ro\'yxatdan o\'tdi va Batlga qatnashdi! Sizga 10 ball qo\'shildi.',
        'batl_username_request': "Iltimos, usernameni '@' bilan kiriting (masalan: @username)",
        'batl_participated': "🎉 Siz Batlga muvaffaqiyatli qatnashdingiz! Endi asosiy menyudan foydalanishingiz mumkin.",
        'username_invalid': "Username noto'g'ri kiritildi yoki sizda Telegram username yo'q.",
        'batl_button': "📣 Batlga qatnashish",
        'vote_button': "Kanalga Boost ovoz berish 30 ball",
        'statistika_button': "📊 Statistika",
        'statistika_text': "📊 Statistika:\n\n👥 Jami referallar soni: {total_referrals}\n🌟 Jami ballar yig'indisi: {total_score}\n🎯 Batlga qatnashganlar soni: {batl_count}"
    },
    'ru': {
        'welcome': 'Выберите язык:',
        'subscribe_channels': 'Подпишитесь на следующие каналы:',
        'check_subscription': '✅ Проверить подписку',
        'subscription_success': '🎉 Поздравляем! Вам разрешено использовать бота.',
        'subscription_failed': '❌ Вы не подписались на следующие каналы:',
        'error_message': 'Произошла ошибка. Попробуйте еще раз.',
        'my_score': '🌟 Ваш счет: {}\n👥 Приглашенные: {}',
        'invite_friends': '👥 Отправьте ссылку друзьям:\n{}',
        'contact_admin': '📞 Связаться с админом',
        'admin_contacted': 'Для связи с админом нажмите кнопку ниже:',
        'top_referrers_title': '🏆 Лучшие приглашающие за неделю:',
        'no_top_referrers': 'Пока никто не пригласил друзей.',
        'referral_subscribed': '🎉 Пользователь, которого вы пригласили, полностью зарегистрировался и участвует в батле! Вам начислено 10 баллов.',
        'batl_username_request': "Пожалуйста, введите username с '@' (например: @username)",
        'batl_participated': "🎉 Вы успешно участвуете в батле! Теперь вы можете пользоваться основным меню.",
        'username_invalid': "Username введён неверно или у вас нет username в Telegram.",
        'batl_button': "📣 Принять участие в батле",
        'vote_button': "Увеличить голосование за канал 30 баллов",
        'statistika_button': "📊 Статистика",
        'statistika_text': "📊 Статистика:\n\n👥 Общее количество рефералов: {total_referrals}\n🌟 Общая сумма баллов: {total_score}\n🎯 Участвующих в батле: {batl_count}"
    },
    'en': {
        'welcome': 'Choose a language:',
        'subscribe_channels': 'Subscribe to the following channels:',
        'check_subscription': '✅ Check Subscription',
        'subscription_success': '🎉 Congratulations! You can now use the bot.',
        'subscription_failed': '❌ You are not subscribed to the following channels:',
        'error_message': 'An error occurred. Try again later.',
        'my_score': '🌟 Your score: {}\n👥 Invited: {}',
        'invite_friends': '👥 Send this link to your friends:\n{}',
        'contact_admin': '📞 Contact admin',
        'admin_contacted': 'Click the button below to contact the admin:',
        'top_referrers_title': '🏆 Weekly top referrers:',
        'no_top_referrers': 'No one has invited anyone yet.',
        'referral_subscribed': '🎉 The user you invited fully registered and joined the battle! You have been awarded 10 points.',
        'batl_username_request': "Please enter your username with '@' (e.g.: @username)",
        'batl_participated': "🎉 You have successfully joined the battle! Now you can use the main menu.",
        'username_invalid': "Invalid username or you don't have a Telegram username.",
        'batl_button': "📣 Join the battle",
        'vote_button': "Boost voting for the channel 30 points",
        'statistika_button': "📊 Statistics",
        'statistika_text': "📊 Statistics:\n\n👥 Total referrals: {total_referrals}\n🌟 Total score: {total_score}\n🎯 Participants in battle: {batl_count}"
    }
}

def get_translation(lang, key):
    return translations.get(lang, {}).get(key, 'Translation not found')

start_channels = [
    {"name": "Rasmiy Kanal", "link": "https://t.me/suxa_cyber", "channelId": "@suxa_cyber"},
    {"name": "BATLEE 1 VS 1 Stars | Premium Community ", "link": "https://t.me/BATLEE1VS1Comunity", "channelId": "@BATLEE1VS1Comunity"},
]

def generate_referral_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def init_user(chat_id, username, users, referral_code=None):
    if str(chat_id) not in users:
        referral_code_generated = generate_referral_code()
        users[str(chat_id)] = {
            "username": username or "Noma'lum",
            "score": 0,
            "referralCode": referral_code_generated,
            "invitedBy": referral_code,
            "invitedUsers": 0,
            "language": "uz",
            "batl_participated": False,
            "referal_rewarded": False
        }
        save_users(users)

def can_show_main_menu(user_id):
    users = load_users()
    user = users.get(str(user_id), {})
    return user.get("batl_participated", False)

def get_form_text(username, lang):
    if lang == "uz":
        return (f"🏆 {username}\n"
                "⭐️ Stars 5 ball\n"
                "👍 Reaksiya 1 ball\n"
                "📝 Comment 30 ball\n"
                "👥Oʻyinga referal 10 ball\n\n"
                "💸 Ton, Payeer rubl, USDT, Stars, NFT, Telegram akaunt sotib olish va sotish uchun qoʻshimcha ball olish mumkin."
                )
    if lang == "ru":
        return (f"🏆 {username}\n"
                "⭐️ Stars 5 баллов\n"
                "👍 Реакция 1 балл\n"
                "📝 Комментарий 30 баллов\n"
                "👥За реферала в игру 10 баллов\n\n"
                "💸 Можно получить дополнительные баллы за покупку/продажу Ton, Payeer рублей, USDT, Stars, NFT, аккаунтов Telegram."
                )
    return (f"🏆 {username}\n"
            "⭐️ Stars 5 points\n"
            "👍 Reaction 1 point\n"
            "📝 Comment 30 points\n"
            "👥Referral to game 10 points\n\n"
            "💸 Extra points available for buying/selling Ton, Payeer rubles, USDT, Stars, NFT, Telegram accounts."
            )

def get_contact_admin_and_boost_inline_buttons(lang):
    admin_url = "https://t.me/suxacyber"
    boost_url = "https://t.me/boost/MamurZokirovv"
    texts = {
        "uz": ("📝 Murojaat uchun admin", "Kanalga Boost ovoz berish 30 ball"),
        "ru": ("📝 Связаться с админом", "Увеличить голосование за канал 30 баллов"),
        "en": ("📝 Contact admin", "Boost voting for the channel 30 points")
    }
    admin_text, boost_text = texts.get(lang, texts["uz"])
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(admin_text, url=admin_url)],
        [InlineKeyboardButton(boost_text, url=boost_url)]
    ])


def get_language_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🇺🇿 Uzbek", callback_data="lang_uz")],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")]
    ])

def get_main_menu(lang):
    menu_translations = {
        'uz': [
            ["🌟 Mening balim", "👥 Do'stlarni taklif qilish"],
            ["🏆 Eng ko'p taklif qilganlar (haftalik)", "📊 Statistika"],
            ["📞 Admin bilan bog'lanish"]
        ],
        'ru': [
            ["🌟 Мой балл", "👥 Пригласить друзей"],
            ["🏆 Лучшие приглашающие (неделя)", "📊 Статистика"],
            ["📞 Связаться с админом"]
        ],
        'en': [
            ["🌟 My score", "👥 Invite friends"],
            ["🏆 Weekly top referrers", "📊 Statistics"],
            ["📞 Contact admin"]
        ]
    }
    return ReplyKeyboardMarkup(menu_translations[lang], resize_keyboard=True)

async def check_subscription(user_id, context):
    failed_channels = []
    for channel in start_channels:
        try:
            member = await context.bot.get_chat_member(chat_id=channel["channelId"], user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                failed_channels.append(channel)
        except Exception as e:
            print(f"Xatolik: {e}")
            failed_channels.append(channel)
    return len(failed_channels) == 0, failed_channels

async def show_menu_or_join_batl(user_id, context, lang):
    users = load_users()
    user = users.get(str(user_id), {})
    if user.get("batl_participated", False):
        await context.bot.send_message(
            chat_id=user_id,
            text=get_translation(lang, 'batl_participated'),
            reply_markup=get_main_menu(lang)
        )
    else:
        join_batl_button = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                get_translation(lang, 'batl_button'), callback_data="join_batl")]
        ])
        await context.bot.send_message(
            chat_id=user_id,
            text=get_translation(lang, 'subscription_success'),
            reply_markup=join_batl_button
        )

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.from_user:
        return
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    args = context.args
    users = load_users()
    referral_code = args[0] if args else None
    init_user(user_id, username, users, referral_code)
    await update.message.reply_text(
        "Tilni tanlang / Choose a language / Выберите язык:",
        reply_markup=get_language_keyboard()
    )

# /lang komandasi
async def lang_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    await update.message.reply_text(
        "Tilni tanlang / Choose a language / Выберите язык:",
        reply_markup=get_language_keyboard()
    )

async def handle_language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query or not query.from_user:
        return
    await query.answer()
    lang = query.data.split('_')[1]
    user_id = query.from_user.id
    users = load_users()
    if str(user_id) in users:
        users[str(user_id)]["language"] = lang
        save_users(users)
    is_subscribed, failed_channels = await check_subscription(user_id, context)
    if not is_subscribed:
        message = get_translation(lang, 'subscribe_channels') + "\n"
        keyboard = []
        for channel in failed_channels:
            message += f"• {channel['name']}\n"
            keyboard.append([InlineKeyboardButton(channel["name"], url=channel["link"])])
        keyboard.append([InlineKeyboardButton(get_translation(lang, 'check_subscription'), callback_data="check_start")])
        await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await show_menu_or_join_batl(user_id, context, lang)

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query or not query.from_user:
        return
    user_id = query.from_user.id
    users = load_users()
    lang = users.get(str(user_id), {}).get("language", "uz")
    await query.answer()
    if query.data.startswith("lang_"):
        await handle_language_selection(update, context)
    elif query.data == "check_start":
        is_subscribed, failed_channels = await check_subscription(user_id, context)
        if is_subscribed:
            await show_menu_or_join_batl(user_id, context, lang)
        else:
            message = get_translation(lang, 'subscription_failed') + "\n"
            keyboard = []
            for channel in failed_channels:
                message += f"• {channel['name']}\n"
                keyboard.append([InlineKeyboardButton(channel["name"], url=channel["link"])])
            keyboard.append([InlineKeyboardButton(get_translation(lang, 'check_subscription'), callback_data="check_start")])
            await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == "join_batl":
        await context.bot.send_message(
            chat_id=user_id,
            text=get_translation(lang, 'batl_username_request')
        )

async def handle_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.from_user:
        return
    user_id = update.message.from_user.id
    users = load_users()
    user = users.get(str(user_id), {})
    lang = user.get('language', 'uz')
    if user.get('batl_participated', False):
        return
    input_username = update.message.text.strip()
    actual_username = update.message.from_user.username
    if actual_username is None or not input_username.startswith('@') or input_username != f"@{actual_username}":
        await update.message.reply_text(get_translation(lang, 'username_invalid'))
        return
    form_text = get_form_text(input_username, lang)
    try:
        sent = await context.bot.send_message(
            CHANNEL_ID,
            form_text,
            reply_markup=get_contact_admin_and_boost_inline_buttons(lang)
        )
        await context.bot.forward_message(chat_id=user_id, from_chat_id=CHANNEL_ID, message_id=sent.message_id)
        users[str(user_id)]["batl_participated"] = True
        save_users(users)
        await handle_referal_reward(user_id, context)
        await update.message.reply_text(get_translation(lang, 'batl_participated'), reply_markup=get_main_menu(lang))
    except Exception as e:
        print(f"Kanalga form xabar yuborishda xato: {e}")

async def handle_referal_reward(user_id, context):
    users = load_users()
    user = users.get(str(user_id))
    if not user or user.get("referal_rewarded", False):
        return
    invited_by = user.get("invitedBy")
    if invited_by:
        for ref_id, ref_data in users.items():
            if ref_data.get("referralCode") == invited_by:
                ref_data["score"] += 10
                ref_data["invitedUsers"] += 1
                user["referal_rewarded"] = True
                save_users(users)
                lang = ref_data.get("language", "uz")
                await context.bot.send_message(
                    chat_id=ref_id,
                    text=get_translation(lang, 'referral_subscribed')
                )
                break

async def my_score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.from_user:
        return
    user_id = update.message.from_user.id
    if not can_show_main_menu(user_id):
        return
    users = load_users()
    score = users.get(str(user_id), {}).get("score", 0)
    invited_users = users.get(str(user_id), {}).get("invitedUsers", 0)
    lang = users.get(str(user_id), {}).get("language", "uz")
    await update.message.reply_text(get_translation(lang, 'my_score').format(score, invited_users))

async def refer_friend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.from_user:
        return
    user_id = update.message.from_user.id
    if not can_show_main_menu(user_id):
        return
    users = load_users()
    referral_code = users.get(str(user_id), {}).get("referralCode", "")
    lang = users.get(str(user_id), {}).get("language", "uz")
    referral_link = f"https://t.me/BATLEE1VS1Stars_bot?start={referral_code}"
    if lang == "uz":
        message = (
            "👥BATTLga do'stlaringizni taklif qilish orqali tezroq va ko'proq ballar to'plang\n\n"
            "⚠️Diqqat! Siz taklif qilgan do'stingiz botdan to'liq ro'yxatdan o'tib, BATTLga qatnashganidan so'ng sizga qo'shimcha ballar  beriladi.\n\n"
            f"Sizning referal havolangiz:\n{referral_link}"
        )
        share_text = (
            "Sizning referal havolangiz ☝️:\n"
            "👥BATTLga do'stlaringizni taklif qilish orqali tezroq va ko'proq ballar to'plang\n\n"
            "⚠️Diqqat! Siz taklif qilgan do'stingiz botdan to'liq ro'yxatdan o'tib, BATTLga qatnashganidan so'ng sizga qo'shimcha ballar beriladi.\n\n"
        )
    elif lang == "ru":
        message = (
            "👥Приглашайте друзей в BATTL, чтобы быстрее зарабатывать баллы\n\n"
            "⚠️Внимание! Вы получите дополнительные баллы только после полной регистрации вашего друга в боте и участия в BATTL.\n\n"
            f"Ваша реферальная ссылка:\n{referral_link}"
        )
        share_text = (
            "Ваша реферальная ссылка ☝️:\n"
            "👥Приглашайте друзей в BATTL, чтобы быстрее зарабатывать баллы\n\n"
            "⚠️Внимание! Вы получите дополнительные баллы только после полной регистрации вашего друга в боте и участия в BATTL.\n\n"
        )
    else:
        message = (
            "👥Invite friends to BATTL to earn points faster\n\n"
            "⚠️Note: You'll get bonus points only after your friend completes registration in the bot and participates in BATTL.\n\n"
            f"Your referral link:\n{referral_link}"
        )
        share_text = (
            "Your referral link ☝️:\n"
            "👥Invite friends to BATTL to earn points faster\n\n"
            "⚠️Note: You'll get bonus points only after your friend completes registration in the bot and participates in BATTL.\n\n"
        )
    await update.message.reply_text(
        text=message,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(
                "📤 Ulashish" if lang == "uz" else "📤 Поделиться" if lang == "ru" else "📤 Share",
                url=f"https://t.me/share/url?url={referral_link}&text={share_text}"
            )]
        ])
    )

async def top_referrers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.from_user:
        return
    user_id = update.message.from_user.id
    if not can_show_main_menu(user_id):
        return
    users = load_users()
    lang = users.get(str(user_id), {}).get("language", "uz")
    top_users = sorted(
        [(user_id, data["invitedUsers"]) for user_id, data in users.items() if data["invitedUsers"] > 0],
        key=lambda x: x[1],
        reverse=True
    )[:10]
    if not top_users:
        await update.message.reply_text(get_translation(lang, 'no_top_referrers'))
        return
    message = get_translation(lang, 'top_referrers_title') + "\n"
    for idx, (user_id, invited_count) in enumerate(top_users, 1):
        username = users[user_id].get("username", "Noma'lum")
        message += f"{idx}. @{username}: {invited_count} ta\n"
    await update.message.reply_text(message)

async def contact_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.from_user:
        return
    user_id = update.message.from_user.id
    if not can_show_main_menu(user_id):
        return
    username = update.message.from_user.username or "Noma'lum"
    lang = load_users().get(str(user_id), {}).get("language", "uz")
    admin_profile_url = "https://t.me/suxacyber"
    keyboard = [[InlineKeyboardButton("Admin profiliga o'tish" if lang == "uz" else "Перейти к админу" if lang == "ru" else "Go to admin", url=admin_profile_url)]]
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"Foydalanuvchi {username} siz bilan bog'lanmoq istayapti."
    )
    await update.message.reply_text(
        get_translation(lang, 'admin_contacted'),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.from_user:
        return
    user_id = update.message.from_user.id
    if not can_show_main_menu(user_id):
        return
    users = load_users()
    lang = users.get(str(user_id), {}).get("language", "uz")

    total_referrals = sum(data.get("invitedUsers", 0) for data in users.values())
    total_score = sum(data.get("score", 0) for data in users.values())
    batl_count = sum(1 for data in users.values() if data.get("batl_participated", False))

    stat_text = get_translation(lang, 'statistika_text').format(
        total_referrals=total_referrals,
        total_score=total_score,
        batl_count=batl_count
    )
    await update.message.reply_text(stat_text)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Xatolik yuz berdi: {context.error}")
    chat_id = None
    lang = "uz"
    if hasattr(update, "effective_chat") and update.effective_chat:
        chat_id = update.effective_chat.id
        lang = load_users().get(str(chat_id), {}).get("language", "uz")
    if chat_id:
        try:
            await context.bot.send_message(chat_id, get_translation(lang, 'error_message'))
        except Exception as e:
            print(f"Error sending error message: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("lang", lang_command))
    app.add_handler(MessageHandler(filters.Regex(r"^🌟 (Mening balim|Мой балл|My score)$"), my_score))
    app.add_handler(MessageHandler(filters.Regex(r"^👥 (Do'stlarni taklif qilish|Пригласить друзей|Invite friends)$"), refer_friend))
    app.add_handler(MessageHandler(filters.Regex(r"^🏆 (Eng ko'p taklif qilganlar \(haftalik\)|Лучшие приглашающие \(неделя\)|Weekly top referrers)$"), top_referrers))
    app.add_handler(MessageHandler(filters.Regex(r"^📊 (Statistika|Статистика|Statistics)$"), show_statistics))
    app.add_handler(MessageHandler(filters.Regex(r"^📞 (Admin bilan bog'lanish|Связаться с админом|Contact admin)$"), contact_admin))
    app.add_handler(CallbackQueryHandler(handle_callback_query))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_username))
    app.add_error_handler(error_handler)
    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == '__main__':
    main() 
