from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random

# توليد رقم بطاقة صالح بخوارزمية Luhn
def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10

def generate_card_number(prefix, length=16):
    number = prefix + ''.join(str(random.randint(0, 9)) for _ in range(length - len(prefix) - 1))
    checksum = luhn_checksum(number + '0')
    last_digit = (10 - checksum) % 10
    return number + str(last_digit)

# توليد تاريخ انتهاء عشوائي (سنة بين 2025 - 2030)
def generate_expiry_date():
    month = str(random.randint(1, 12)).zfill(2)
    year = str(random.randint(25, 30))
    return f"{month}/{year}"

# توليد CVV
def generate_cvv():
    return ''.join(str(random.randint(0, 9)) for _ in range(3))

# توليد اسم وهمي
def generate_name():
    first_names = ["John", "Ali", "Sara", "Lena", "Omar", "Anna"]
    last_names = ["Smith", "Hassan", "Brown", "Khan", "Lee", "Garcia"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

# توليد بطاقة كاملة
def generate_fake_card(card_type="Visa"):
    if card_type.lower() == "visa":
        prefix = "4"
    elif card_type.lower() == "mastercard":
        prefix = str(random.choice(["51", "52", "53", "54", "55"]))
    else:
        prefix = "4"  # default Visa

    card_number = generate_card_number(prefix)
    expiry = generate_expiry_date()
    cvv = generate_cvv()
    name = generate_name()

    return f"""نوع البطاقة: {card_type}
الرقم: {card_number}
الاسم: {name}
تاريخ الانتهاء: {expiry}
رمز الأمان: {cvv}"""

# أوامر التليجرام
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً! أرسل /visa أو /mastercard لتوليد بطاقة وهمية.")

async def visa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    card = generate_fake_card("Visa")
    await update.message.reply_text(card)

async def mastercard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    card = generate_fake_card("MasterCard")
    await update.message.reply_text(card)

# تشغيل البوت
app = ApplicationBuilder().token("8108488431:AAEXoYXGL2oNZN_doj0iB7FMxCe_w8_OkeE").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("visa", visa))
app.add_handler(CommandHandler("mastercard", mastercard))

print("Bot is running...")
app.run_polling()
