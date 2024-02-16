# File untuk menyimpan constant
import pytz
import bcrypt
import base64

WA_ENGINE = "https://wa-engine.site:2053/send-message-bot"
lokasi = 'Asia/Jakarta'
zona_waktu = pytz.timezone(lokasi)

SECRET_KEY = "AbC"
SALT_KEY = bcrypt.gensalt()

ROT_KEY = "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ@#$_-&%:0123456789"
ROT_NUM = 15
