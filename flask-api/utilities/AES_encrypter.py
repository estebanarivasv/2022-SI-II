import os

from Crypto.Cipher import AES


class AESEncryption:
    def __init__(self, ):
        self.key = os.getenv('AES_KEY').encode('utf-8')

    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)

        return cipher.nonce + tag + ciphertext

    def decrypt(self, data):
        nonce = data[:AES.block_size]
        tag = data[AES.block_size:AES.block_size * 2]
        ciphertext = data[AES.block_size * 2:]

        cipher = AES.new(self.key, AES.MODE_EAX, nonce)

        return cipher.decrypt_and_verify(ciphertext, tag)


