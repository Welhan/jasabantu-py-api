# File untuk menyimpan constant
import pytz
import bcrypt
import base64

API_VERSION = "1.0.0"
WA_ENGINE = "https://wa-engine.site:2053/"
lokasi = 'Asia/Jakarta'
zona_waktu = pytz.timezone(lokasi)

SECRET_KEY = "AbC"
SALT_KEY = bcrypt.gensalt()

ROT_KEY = "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ@#$_-&%:.0123456789"
ROT_NUM = 15
NEW_KEY = "kdyPe6QxOKHW923ngfb8-X7TLoS5ZU_ECvFR@DqV4whBruazMtp%l0$Y.iJ#s1jINcA:&Gm"
PREFIX_KEY = "$2y$" + str(ROT_NUM) +"$"

path_auth = "config/credential.json"
