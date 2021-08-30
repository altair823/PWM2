'''
# 사용자가 입력한 비밀번호를 검증하고
# 사용자의 정보를 암호화 하는 클래스.
'''
from os import urandom
from base64 import urlsafe_b64encode
from hashlib import sha3_512
from cryptography import exceptions
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Encryption:
    def __init__(self):
        self.salt = None
        self.key = None
        self.fernet = None

# 사용자가 입력한 비밀번호를 해시값으로 검증한다.
# salt 값은 데이터 파일에서 가져오거나
# 무작위로 생성된 bytes 타입의 난수여야 한다.
    def verifyPW(self, inputPW, hashedStr, salt, isCreateInitial=False):
        if type(salt) is not bytes and isCreateInitial is False:
            raise AttributeError
        # salt 는 이후에도 해당 파일을 암호화 할 때 사용할 키를 생성하는데 쓴다.
        if isCreateInitial is True:
            self.salt = urandom(1000)
        else:
            self.salt = salt
        # 비밀번호와 salt 로 해시값을 구하여 검증한다.
        # 만약 데이터 파일이 없다면 검증하지 않는다.
        if isCreateInitial is False and self.hashing(inputPW) != hashedStr:
            raise exceptions.InvalidKey
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA3_256(),
            length=32,
            salt=self.salt,
            iterations=1000000, )
        self.key = urlsafe_b64encode(kdf.derive(inputPW.encode()))
        self.fernet = Fernet(self.key)

    def decryptPW(self, encryptedText):
        return self.fernet.decrypt(encryptedText.encode()).decode()

    def encryptPW(self, rawText):
        return self.fernet.encrypt(rawText.encode()).decode()

    def hashing(self, text):
        return sha3_512(text.encode() + self.salt).hexdigest()