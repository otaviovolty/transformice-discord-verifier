import secrets
import string
from datetime import datetime, timedelta

class CodeGenerator:
    @staticmethod
    def generate_code(length: int = 12) -> str:
        """
        Gera um código de verificação aleatório e seguro.
        Formato: TM-XXXXXX (Transformice)
        """
        characters = string.ascii_uppercase + string.digits
        code = ''.join(secrets.choice(characters) for _ in range(length))
        return f"TM-{code}"
    
    @staticmethod
    def is_code_valid(code: str, created_at: datetime, expiration_minutes: int = 60) -> bool:
        """
        Verifica se o código ainda é válido (não expirou).
        """
        expiration_time = created_at + timedelta(minutes=expiration_minutes)
        return datetime.now() < expiration_time
    
    @staticmethod
    def get_remaining_time(created_at: datetime, expiration_minutes: int = 60) -> int:
        """
        Retorna o tempo restante em minutos.
        """
        expiration_time = created_at + timedelta(minutes=expiration_minutes)
        remaining = expiration_time - datetime.now()
        return max(0, int(remaining.total_seconds() / 60))
