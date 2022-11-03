class ServerRSA:
    def __init__(self, new_key, user_private_key):
        self.new_key = new_key
        self.private_key_server = user_private_key
        self.cipher_decrypt = ""

    def decrypt_message(self, encrypted):
        return self.cipher_decrypt.decrypt(eval(encrypted)).decode('utf-8')
