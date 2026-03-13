import random
import asyncio
import json
import edge_tts
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID","8337495954"))

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

DATA_FILE="data.json"

# ================= DATA =================

def load():
    try:
        with open(DATA_FILE,encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"users":{}, "boss":{"hp":0,"active":False}}

def save(data):
    with open(DATA_FILE,"w",encoding="utf-8") as f:
        json.dump(data,f,indent=2)

data=load()

def get_user(uid):
    uid=str(uid)
    if uid not in data["users"]:
        data["users"][uid]={"xu":1000,"bank":0}
    return data["users"][uid]

# ================= START =================

@dp.message(Command("start",ignore_mention=True))
async def start(msg: types.Message):

    await msg.reply("""
🎮 <b>CASINO GAME BOT</b>

🎲 /taixiu tài 100
🎰 /slot
🃏 /blackjack
♠️ /poker

🐟 /fish
🐉 /boss

🏦 /bank
🏦 /gui 100
🏧 /rut 50

💸 reply /chuyentien 100
👑 reply /addtien 500

🏆 /top
👤 /profile

🎤 /say Xin chào
""")

# ================= PROFILE =================

@dp.message(Command("profile",ignore_mention=True))
async def profile(msg: types.Message):

    user=get_user(msg.from_user.id)

    await msg.reply(f"""
👤 PROFILE

💰 Xu: {user["xu"]}
🏦 Bank: {user["bank"]}
""")

# ================= SLOT =================

@dp.message(Command("slot",ignore_mention=True))
async def slot(msg: types.Message):

    user=get_user(msg.from_user.id)

    if user["xu"]<100:
        await msg.reply("❌ cần 100 xu")
        return

    icons=["🍒","🍋","🍉","⭐","💎"]

    a=random.choice(icons)
    b=random.choice(icons)
    c=random.choice(icons)

    user["xu"]-=100

    if a==b==c:
        win=500
        user["xu"]+=win
        text=f"💎 JACKPOT +{win}"
    else:
        text="💀 thua"

    save(data)

    await msg.reply(f"""
🎰 SLOT

┃ {a} │ {b} │ {c} ┃

{text}
""")

# ================= BLACKJACK =================

@dp.message(Command("blackjack",ignore_mention=True))
async def blackjack(msg: types.Message):

    user=get_user(msg.from_user.id)

    if user["xu"]<150:
        await msg.reply("❌ cần 150 xu")
        return

    user["xu"]-=150

    p=random.randint(15,21)
    b=random.randint(15,21)

    if p>b:
        user["xu"]+=300
        text="🏆 thắng +300"
    else:
        text="💀 thua"

    save(data)

    await msg.reply(f"""
🃏 BLACKJACK

👤 {p}
🤖 {b}

{text}
""")

# ================= POKER =================

@dp.message(Command("poker",ignore_mention=True))
async def poker(msg: types.Message):

    user=get_user(msg.from_user.id)

    if user["xu"]<100:
        await msg.reply("❌ cần 100 xu")
        return

    user["xu"]-=100

    p=random.randint(1,13)
    b=random.randint(1,13)

    if p>b:
        user["xu"]+=200
        text="🏆 thắng"
    else:
        text="💀 thua"

    save(data)

    await msg.reply(f"""
♠️ POKER

🃏 {p}
🎴 {b}

{text}
""")

# ================= TAIXIU =================

@dp.message(Command("taixiu",ignore_mention=True))
async def taixiu(msg: types.Message):

    user=get_user(msg.from_user.id)

    try:

        parts=msg.text.split()

        bet=parts[1].lower()
        amount=int(parts[2])

        if bet not in ["tài","xỉu"]:
            await msg.reply("❌ chọn tài hoặc xỉu")
            return

        if amount<50 or amount>user["xu"]:
            await msg.reply("❌ cược >=50")
            return

        user["xu"]-=amount

        result=random.choice(["tài","xỉu"])

        multiplier=random.randint(2,7)

        if bet==result:

            win=amount*multiplier

            user["xu"]+=win

            text=f"""
🎲 TÀI XỈU

Kết quả: {result}

🏆 THẮNG

💰 x{multiplier}
+{win}
"""

        else:

            text=f"""
🎲 TÀI XỈU

Kết quả: {result}

💀 THUA
-{amount}
"""

        save(data)

        await msg.reply(text)

    except:
        await msg.reply("❌ /taixiu tài 100")

# ================= FISH =================

fish_list=[
("🐟 Cá nhỏ",50),
("🐠 Cá vàng",120),
("🦈 Cá mập",400),
("🐙 Bạch tuộc hiếm",600)
]

@dp.message(Command("fish",ignore_mention=True))
async def fish(msg: types.Message):

    user=get_user(msg.from_user.id)

    name,price=random.choice(fish_list)

    user["xu"]+=price

    save(data)

    await msg.reply(f"""
🎣 CÂU CÁ

{name}

💰 +{price}
""")

# ================= BOSS =================

@dp.message(Command("boss",ignore_mention=True))
async def boss(msg: types.Message):

    user=get_user(msg.from_user.id)

    boss=data["boss"]

    if not boss["active"]:

        data["boss"]={"hp":2000,"active":True}

        save(data)

        await msg.reply("""
🐉 BOSS XUẤT HIỆN

❤️ 2000 HP
⚔️ /boss đánh
""")
        return

    dmg=random.randint(50,200)

    boss["hp"]-=dmg

    if boss["hp"]<=0:

        user["xu"]+=500

        data["boss"]={"hp":0,"active":False}

        save(data)

        await msg.reply("💀 boss chết +500")

    else:

        save(data)

        await msg.reply(f"""
⚔️ damage {dmg}

❤️ boss còn {boss["hp"]}
""")

# ================= BANK =================

@dp.message(Command("bank",ignore_mention=True))
async def bank(msg: types.Message):

    user=get_user(msg.from_user.id)

    await msg.reply(f"""
🏦 BANK

💰 ví: {user["xu"]}
🏦 bank: {user["bank"]}
""")

@dp.message(Command("gui",ignore_mention=True))
async def gui(msg: types.Message):

    user=get_user(msg.from_user.id)

    try:
        amount=int(msg.text.split()[1])

        if amount>user["xu"]:
            return

        user["xu"]-=amount
        user["bank"]+=amount

        save(data)

        await msg.reply(f"🏦 gửi {amount}")

    except:
        await msg.reply("❌ /gui 100")

@dp.message(Command("rut",ignore_mention=True))
async def rut(msg: types.Message):

    user=get_user(msg.from_user.id)

    try:
        amount=int(msg.text.split()[1])

        if amount>user["bank"]:
            return

        user["bank"]-=amount
        user["xu"]+=amount

        save(data)

        await msg.reply(f"🏧 rút {amount}")

    except:
        await msg.reply("❌ /rut 50")

# ================= TRANSFER =================

@dp.message(Command("chuyentien",ignore_mention=True))
async def chuyentien(msg: types.Message):

    if not msg.reply_to_message:
        await msg.reply("❌ reply người cần chuyển")
        return

    user=get_user(msg.from_user.id)

    try:
        amount=int(msg.text.split()[1])
    except:
        return

    if amount>user["xu"]:
        await msg.reply("❌ không đủ xu")
        return

    target=msg.reply_to_message.from_user.id

    target_user=get_user(target)

    user["xu"]-=amount
    target_user["xu"]+=amount

    save(data)

    await msg.reply(f"💸 chuyển {amount}")

# ================= ADMIN =================

@dp.message(Command("addtien",ignore_mention=True))
async def addtien(msg: types.Message):

    if msg.from_user.id!=ADMIN_ID:
        return

    if not msg.reply_to_message:
        return

    amount=int(msg.text.split()[1])

    target=msg.reply_to_message.from_user.id

    target_user=get_user(target)

    target_user["xu"]+=amount

    save(data)

    await msg.reply(f"👑 add {amount}")

# ================= SAY VOICE =================

@dp.message(Command("say",ignore_mention=True))
async def say(msg: types.Message):

    text=msg.text.replace("/say","").strip()

    if not text:
        return

    voice="vi-VN-HoaiMyNeural"

    file="voice.mp3"

    tts=edge_tts.Communicate(text,voice)

    await tts.save(file)

    audio=types.FSInputFile(file)

    await msg.answer_voice(audio)

    os.remove(file)

# ================= TOP =================

@dp.message(Command("top",ignore_mention=True))
async def top(msg: types.Message):

    ranking=sorted(data["users"].items(),
                   key=lambda x:x[1]["xu"],
                   reverse=True)

    text="🏆 TOP 10\n\n"

    for i,(uid,user) in enumerate(ranking[:10],1):
        text+=f"{i}. {uid} — {user['xu']}\n"

    await msg.reply(text)

# ================= RUN =================

async def main():

    print("Bot started!")

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())



