import random
import asyncio
import json
import edge_tts
import time
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8337495954"))
if not TOKEN:
    print("ERROR: Set BOT_TOKEN environment variable!")
    exit(1)

bot = Bot(TOKEN)
dp = Dispatcher()

DATA_FILE = "data.json"

# ================= DATA =================

def load():
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except:
        return {"users":{},"boss": {"hp":0, "active":False}, "couples":{},"tt_ranks":{}}

def save(data):
    with open(DATA_FILE,"w") as f:
        json.dump(data,f, indent=4)

data = load()

def get_user(uid):
    uid=str(uid)
    if uid not in data["users"]:
        data["users"][uid]={
            "xu":500,
            "bank":0,
            "daily_time":0,
            "couple":None,
            "tt_all":0, "tt_week":0, "tt_day":0,
            "cooldowns":{}
        }
    if "couples" not in data:
        data["couples"] = {}
    if "tt_ranks" not in data:
        data["tt_ranks"] = {}
    return data["users"][uid]

def can_claim_daily(uid):
    user = get_user(uid)
    return time.time() - user["daily_time"] > 86400

def set_daily_claimed(uid):
    get_user(uid)["daily_time"] = time.time()

def set_cooldown(uid, cd_type, duration):
    get_user(uid)["cooldowns"][cd_type] = time.time() + duration

def is_cooldown(uid, cd_type):
    user = get_user(uid)
    return time.time() < user["cooldowns"].get(cd_type, 0)

def get_couple(uid):
    return data["couples"].get(str(uid))

def set_couple(u1, u2):
    u1 = str(u1)
    u2 = str(u2)
    data["couples"][u1] = u2
    data["couples"][u2] = u1
    get_user(u1)["couple"] = u2
    get_user(u2)["couple"] = u1

def remove_couple(uid):
    partner = get_couple(uid)
    if partner:
        p = str(partner)
        data["couples"].pop(uid, None)
        data["couples"].pop(p, None)
        get_user(uid)["couple"] = None
        if p in data["users"]:
            get_user(p)["couple"] = None

# ================= START =================

@dp.message(Command("menu"), Command("help"), Command("danhsachlenh"))
async def menu(msg: types.Message):
    await msg.reply("""
🏆 **DANH SÁCH LỆNH HoQuocTEAM** 🏆

🎮 **GAME:**
/nohu [xu] 💎✨ — No hu jackpot
/taixiu [xu] 🎲⏳ — Tai xiu (chon sau)
/tx [tai|xiu] [xu] ⚡🎯 — Tai xiu nhanh
/baucua [xu] 🦀🦞🐟 — Bau cua tom ca
/chuoixu 🍌🌿 — Cay chuoi xu (1h)
/dauboss 🐉⚔️ — Danh boss ngau nhien
/cauca 🐟🎣 — Cau ca (5 phut)
/say [text] 🎤🔊 — Text to speech
/kbb [keo|bua|bao] [xu] ✂️🪨📜 — Keo bua bao

💕 **TINH YEU:**
/ghep 🌹💫 — Ghep doi ngau nhien
/ghep @user 💑❤️ — Ghep doi voi nguoi cu the
/ghep huy 💔🛑 — Huy cap doi
/ghep ds 📜💞 — Danh sach cap doi nhom
/hendo 🖼️🌅 — Hen ho voi cap doi (hinh nen ngau nhien)
[hendo [nen] 🎨🏞️ — Chon nen: cafe|bien|rung|thanh|vuon|tuyet|hoang|vu tru

🆘 **HO TRO:**
/nhanxu 🎁📅 — Nhan xu hang ngay (+500 xu)
/chuyenxu [xu] 💸➡️ — Chuyen xu (reply tin nhan hoac @user)
/rank 👤📊 — Xem rank cua ban
/rank @user 👥📈 — Xem rank nguoi khac
/bxh 🏆🔟 — Bang xep hang top 10
/checktt 📈⭐ — Tuong tac cua ban
/checktt all 🌐🏅 — Top tuong tac tong
/checktt week 📅🏅 — Top tuong tac tuan
/checktt day ☀️🏅 — Top tuong tac ngay
/tag @user [lan] 🏷️🔄 — Tag user (max 20, -1000 xu)
/bypass [url] 🔗🛡️ — Bypass link rut gon / quang cao

🔧 **QUAN LY (Admin):**
/addtien [xu] 💰🔧 — Cong/tru xu (reply tin nhan)
/romom 😂🤪 — Ro mom (cap 30+ hoac 10k xu)
/gocamchat 🧹💬 — Go cam chat
/taoanhnhom [size] [mau] [ten] 👥🎨 — Tao anh nhom

💡 **Tip:** Choi game de kiem xu! 🎮💰
   Moi ngay nhan 500 xu mien phi! 🎉
    """)

@dp.message(Command("start"))
async def start(msg: types.Message):
    await menu(msg)

# ================= PROFILE =================

@dp.message(Command("profile"))
async def profile(msg: types.Message):
    user=get_user(msg.from_user.id)
    await msg.reply(f"""
👤 **THÔNG TIN NGƯỜI CHƠI**

💰 Xu: **{user["xu"]}**
🏦 Ngân hàng: **{user["bank"]}**
""")

# ================= SLOT =================

@dp.message(Command("slot"))
async def slot(msg: types.Message):
    user=get_user(msg.from_user.id)
    if user["xu"] < 100:
        await msg.reply("❌ Không đủ xu! Cần 100xu")
        return
    icons=["🍒","🍋","🍉","⭐","💎"]
    a=random.choice(icons)
    b=random.choice(icons)
    c=random.choice(icons)
    user["xu"] -= 100
    if a==b==c:
        win=500
        user["xu"] += win
        text=f"💎 **JACKPOT!** +{win} xu"
    else:
        text="💀 **Trượt rồi!** -100xu"
    save(data)
    await msg.reply(f"""
🎰 SLOT MACHINE

┃ {a} │ {b} │ {c} ┃

{text}
""")

# ================= BLACKJACK =================

@dp.message(Command("blackjack"))
async def blackjack(msg: types.Message):
    user=get_user(msg.from_user.id)
    if user["xu"] < 150:
        await msg.reply("❌ Không đủ xu! Cần 150xu")
        return
    user["xu"] -= 150
    player=random.randint(15,21)
    botp=random.randint(15,21)
    if player>botp:
        user["xu"]+=300
        result="🏆 **BẠN THẮNG!** +300"
    else:
        result="💀 **BẠN THUA!** -150"
    save(data)
    await msg.reply(f"""
🃏 BLACKJACK

👤 Bạn: {player}
🤖 Bot: {botp}

{result}
""")

# ================= POKER =================

@dp.message(Command("poker"))
async def poker(msg: types.Message):
    user=get_user(msg.from_user.id)
    if user["xu"] < 100:
        await msg.reply("❌ Không đủ xu! Cần 100xu")
        return
    user["xu"] -= 100
    p=random.randint(1,13)
    b=random.randint(1,13)
    if p>b:
        user["xu"]+=200
        text="🏆 Thắng! +200"
    else:
        text="💀 Thua! -100"
    save(data)
    await msg.reply(f"""
♠️ POKER

🃏 Bạn: {p}
🎴 Bot: {b}

{text}
""")

# ================= TAIXIU =================

@dp.message(Command("taixiu"))
async def taixiu(msg: types.Message):
    user = get_user(msg.from_user.id)
    try:
        parts = msg.text.split()
        if len(parts) < 3:
            await msg.reply("❌ /taixiu [tài/xỉu] <amount>")
            return
        bet_type = parts[1].lower()
        amount = int(parts[2])
        if amount < 50 or amount > user["xu"]:
            await msg.reply("❌ Cược 50- max xu!")
            return
        user["xu"] -= amount
        result = random.choice(["tài", "xỉu"])
        if bet_type == result:
            user["xu"] += amount * 2
            await msg.reply(f"🎲 **{result.upper()}** - THẮNG! +{amount}")
        else:
            await msg.reply(f"🎲 **{result.upper()}** - THUA!")
        save(data)
    except:
        await msg.reply("❌ Lỗi! /taixiu tài 100")

# ================= FISH =================

fish_list=[
("🐟 Cá nhỏ",50),
("🐠 Cá vàng",120),
("🦈 Cá mập",400),
("🐙 Bạch tuộc hiếm",600)
]

@dp.message(Command("fish"))
async def fish(msg: types.Message):
    user=get_user(msg.from_user.id)
    name,price=random.choice(fish_list)
    user["xu"]+=price
    save(data)
    await msg.reply(f"""
🎣 CÂU CÁ

Bạn bắt được:
{name}

💰 +{price} xu
""")

# ================= BOSS =================

@dp.message(Command("boss"))
async def boss_cmd(msg: types.Message):
    user=get_user(msg.from_user.id)
    boss_data = data.get("boss", {"hp":0, "active":False})
    if not boss_data["active"]:
        data["boss"] = {"hp":2000, "active":True}
        save(data)
        await msg.reply("""
🐉 **BOSS XUẤT HIỆN**

❤️ HP: 2000

⚔️ Dùng /boss để tấn công!
""")
        return
    dmg=random.randint(50,200)
    boss_data["hp"] -= dmg
    data["boss"] = boss_data
    save(data)
    if boss_data["hp"] <= 0:
        user["xu"] += 500
        data["boss"] = {"hp":0, "active":False}
        save(data)
        await msg.reply("""
💀 BOSS ĐÃ BỊ TIÊU DIỆT!

🏆 +500 xu
""")
    else:
        await msg.reply(f"""
⚔️ Bạn gây **{dmg}** sát thương

❤️ Boss còn: **{boss_data["hp"]}** HP
""")

# ================= BANK =================

@dp.message(Command("bank"))
async def bank(msg: types.Message):
    user = get_user(msg.from_user.id)
    await msg.reply(f"""
🏦 **NGÂN HÀNG**

💰 Ví: {user["xu"]}
🏦 Bank: {user["bank"]}
➕ /gui <amount>
➖ /rut <amount>
""")

@dp.message(Command("gui"))
async def gui(msg: types.Message):
    user = get_user(msg.from_user.id)
    try:
        amount = int(msg.text.split()[1])
        if amount < 1 or amount > user["xu"]:
            await msg.reply("❌ Không hợp lệ!")
            return
        user["xu"] -= amount
        user["bank"] += amount
        save(data)
        await msg.reply(f"✅ Gửi **{amount}** → bank")
    except:
        await msg.reply("❌ /gui <amount>")

@dp.message(Command("rut"))
async def rut(msg: types.Message):
    user = get_user(msg.from_user.id)
    try:
        amount = int(msg.text.split()[1])
        if amount < 1 or amount > user["bank"]:
            await msg.reply("❌ Không hợp lệ!")
            return
        user["bank"] -= amount
        user["xu"] += amount
        save(data)
        await msg.reply(f"✅ Rút **{amount}** ← bank")
    except:
        await msg.reply("❌ /rut <amount>")

# ================= TRANSFER =================

@dp.message(Command("chuyentien"))
async def chuyentien(msg: types.Message):

    user = get_user(msg.from_user.id)

    if not msg.reply_to_message:
        await msg.reply("❌ Reply người cần chuyển tiền\nVí dụ: reply /chuyentien 100")
        return

    try:
        amount = int(msg.text.split()[1])
    except:
        await msg.reply("❌ /chuyentien <amount>")
        return

    if amount <= 0 or amount > user["xu"]:
        await msg.reply("❌ Không đủ xu!")
        return

    target_id = msg.reply_to_message.from_user.id
    target_user = get_user(target_id)

    user["xu"] -= amount
    target_user["xu"] += amount

    save(data)

    await msg.reply(f"""
💸 **CHUYỂN TIỀN**

👤 {msg.from_user.id} ➜ {target_id}

💰 {amount} xu
""")

# ================= ADMIN =================

@dp.message(Command("addtien"))
async def addtien(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return
    try:
        parts = msg.text.split()
        target_id = parts[1].lstrip('@')
        amount = int(parts[2])
        target_user = get_user(target_id)
        target_user["xu"] += amount
        save(data)
        await msg.reply(f"✅ Admin add **{amount}** xu cho `{target_id}`")
    except:
        await msg.reply("❌ /addtien @user <amount>")

# ================= SAY =================

@dp.message(Command("say"))
async def say(msg: types.Message):
    text=msg.text.replace("/say ","").strip()
    if not text:
        await msg.reply("❌ /say <text>")
        return
    try:
        file="voice.mp3"
        voice="vi-VN-HoaiMyNeural"
        tts=edge_tts.Communicate(text,voice)
        await tts.save(file)
        audio=types.FSInputFile(file)
        await msg.answer_voice(audio)
        os.remove(file)
    except Exception as e:
        await msg.reply("❌ Lỗi TTS!")

# ================= TOP =================

@dp.message(Command("top"))
async def top(msg: types.Message):
    ranking=sorted(data["users"].items(),
                   key=lambda x:x[1]["xu"],
                   reverse=True)
    text="🏆 **TOP 10 NGƯỜI GIÀU NHẤT**\n\n"
    for i, (uid,user) in enumerate(ranking[:10],1):
        text+=f"{i}. 👤 `{uid}` — 💰 **{user['xu']}** xu\n"
    await msg.reply(text)

# ================= RUN =================

async def main():
    print("Bot started!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


