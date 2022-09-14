from pyrogram import Client, filters, idle, __version__
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

bot_me = [] # buraya dokunma
acc_me = [] # buraya dokunma

OWNER_ID = 5068551877 # Senin Telegram hesap id'in
BOT_TOKEN = "5589221614:AAE6EiLIq14G-xZxkYpByhX7SQ2Fyt7hIFk" # @BotFather'dan oluşturduğun botun tokeni
API_HASH = "5db0fc2e7d0062fc1a58954f0e13dde5" # buraya dokunma
API_ID = 10929531 # buraya dokunma
SESSION = "" # Asistan hesabın Pyrogram String Sessionu


###* GERİ KALAN HİÇBİR ŞEYE DOKUNMA ###

app = Client("ApproveAll", api_hash=API_HASH, api_id=API_ID, bot_token=BOT_TOKEN)
account = Client("ApproveAllAccount", api_hash=API_HASH, api_id=API_ID, session_string=SESSION)

@app.on_message(filters.command('start'))
async def start(bot, msg):
    text = f"""
    **Merhaba, ben {bot_me[0].mention}!**

__Kanallarda tüm istekleri onaylayabilmen için yaratıldım.__

--Bunu için asistanı kanalda yönetici yapman gerekir.--

**Asistan:**
__İsim:__ {acc_me[0].mention}
__ID:__ {acc_me[0].id}
__Kullanıcı Adı:__ {"@"+acc_me[0].username if acc_me[0].username else "Yok"}
"""
    await msg.reply(text)

@app.on_message(filters.command("approve"))
async def approveall(bot: Client, message: Message):
    user = message.from_user
    chat = message.from_user
    if len(message.text.split()) < 2:
        text = f"""**Yanlış Kullanım**\n\n__Kullanımı:__ `/approve [Kanal ID]`\n\n__Örnek:__ `/approve -1008376543672`"""
        return await message.reply(text)
    else:
        channel = message.command[1]
        try:
            get_chat = await account.get_chat(int(channel))
        except Exception as e:
            return await message.reply(
                f"**Sohbet Bulanamadı.**\n__Görünüşe göre sohbet alınamadı, hata aşağıda verilmiştir.__\n\n**--HATA:--** `{str(e)}`"
            )
        text = f"""
    **Sohbet Bulundu**

__Başlık:__ {get_chat.title}
__ID:__ `{get_chat.id}`
__Kullanıcı Adı:__ {"@"+get_chat.username if get_chat.username else "Gizli Sohbet"}

--Bu kanalda bulunan tüm istekleri kabul etmek ister misiniz?--
"""
        await message.reply(
            text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Evet", callback_data="set 1"),
                        InlineKeyboardButton("Hayır", callback_data="set 2"),
                    ],
                    [
                        InlineKeyboardButton("Sil", callback_data="set 0"),
                    ],
                ],
            ),
        )

@app.on_callback_query(filters.regex(r"set") & filters.user(OWNER_ID))
async def approve_(bot: Client, query: CallbackQuery):
    user = query.from_user
    data = query.data
    mod = int(data.split()[1])
    msg = query.message
    id = int((msg.text.split("ID: ")[1]).split("\nKullanıcı")[0])
    if mod == 1:
        await msg.edit(f"__Lütfen bekleyin__")
        try:
            await account.approve_all_chat_join_requests(id)
        except Exception as e:
            return await msg.edit(f"**Bir Hata Oluştu!**\n__İşlem sırasında bilinmeyen bir hata oluştu! Hata aşağıda verilmiştir.__\n\n--Hata:-- `{str(e)}`")
        await msg.edit(f"**İşlem başarıyla tamamlandı!**")
        return
    elif mod == 2:
        await msg.edit(f"__İşlem iptal edildi__")
        return
    elif mod == 0:
        await msg.delete()
        
app.start()
account.start()

me = app.get_me()
bot_me.clear()
bot_me.append(me)

account_me = account.get_me()
acc_me.clear()
acc_me.append(account_me)

text = f"""

    \033[32m Bot Started Successfully\033[0m

    \033[33m Bot Name:\033[0m {me.first_name}\033[0m
    \033[33m Bot ID:\033[0m {me.id}\033[0m
    \033[33m Bot Username:\033[0m @{me.username}\033[0m

    \033[33m Assistant Account:\033[0m {account_me.first_name}
    \033[33m Assistant Account ID:\033[0m {account_me.id}\033[0m
    \033[33m Assistant Account Username:\033[0m @{account_me.username}\033[0m
    
    \033[33m Pyrogram Version: \033[0m {__version__}\033[0m
    """
print(text)
idle()

