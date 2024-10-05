from cryptography.fernet import Fernet
class Encrypter:
    @staticmethod
    def encryptText(plain_text:str):
        key = Fernet.generate_key()
        encryptedText = Fernet(key).encrypt(plain_text.encode())+key
        return encryptedText.decode()
    @staticmethod
    def decryptText(encryptedText:str):
        text_key = encryptedText.split("==")
        text = text_key[0]+"=="
        key = text_key[1]
        decryptedText = Fernet(key.encode()).decrypt(text.encode())
        return decryptedText.decode()
