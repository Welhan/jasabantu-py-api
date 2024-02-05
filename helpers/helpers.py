from models.userModels import User
from models.otpModels import Otp
import random



user_model = User()
otp_model = Otp()

def generate_otp():
    return str(random.randint(1000,9999))
    


def checkOtp(otp):
    checkOtp = otp_model.checkOtp(otp)
    if checkOtp is None:
        return False
    else:
        return True






def checkPin(pin):
    checkPin = user_model.checkPin(pin)
    if checkPin is None:
        return False
    else:
        return True
    