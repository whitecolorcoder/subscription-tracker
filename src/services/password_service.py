import hashlib

class PasswordsService:
    'Класс создания хэш ключа для использования JWT'
    def create_hash(self, password: str) -> str:
        'Генерация хэш-значения'

        password_bytes = password.encode('utf-8')

        hash_object = hashlib.sha256(password_bytes)
        hex_dig = hash_object.hexdigest()

        return hex_dig

    def equale_hash(self, password: str, db_password:str) -> bool:
        'Проверка хэш-значения'
        return self.create_hash(password) == db_password