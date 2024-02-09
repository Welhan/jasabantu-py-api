# File untuk menyimpan constant
import pytz
import bcrypt

WA_ENGINE = "https://wa-engine.site:2053/send-message-bot"
lokasi = 'Asia/Jakarta'
zona_waktu = pytz.timezone(lokasi)

SECRET_KEY = "AbC"
SALT_KEY = bcrypt.gensalt()
