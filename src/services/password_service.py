import hashlib

class PasswordsService:
    
    def create_hash(self, password: str) -> str:

        password_bytes = password.encode('utf-8')

        hash_object = hashlib.sha256(password_bytes)
        hex_dig = hash_object.hexdigest()

        return hex_dig

    def equale_hash(self, password: str, db_password:str) -> bool:
        return self.create_hash(password) == db_password