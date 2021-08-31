from datetime import datetime

from pyotp import TOTP
from qrcode import make
from security.otp_key import TOTP_KEY


class OTP:
    def __init__(self, name=None):
        self.totp = None
        self.name = name

    def makeCredential(self):
        # 배포판마다 다른 키 값을 가져야함! 무조건!
        # 키 생성은 random_base32()를 사용할 것.
        self.totp = TOTP(TOTP_KEY)

    def generatorOTP(self):
        return self.totp.now()

    def saveCredentialIMG(self, fileName='Credential.png'):
        make(self.totp.provisioning_uri(name=self.name, issuer_name='Secure Password Manager')).save(fileName)
        # 생성한 QR코드 이미지는 사용 후 반드시 삭제되어야 함.

    def verifyOTP(self, inputOTP):
        now = datetime.now()
        # 바로 전 OTP 까지는 허용한다.
        if self.totp.verify(inputOTP) is False and self.totp.verify(inputOTP, (now.timestamp() - 15)) is False:
            raise KeyError
        else:
            return True

