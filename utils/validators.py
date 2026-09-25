import re

class Validators:
    @staticmethod
    def is_valid_transformice_username(username: str) -> bool:
        """
        Valida se o username do Transformice é válido.
        Transformice usernames: 1-20 caracteres, letras, números, underscores
        """
        if not username or len(username) > 20 or len(username) < 1:
            return False
        
        pattern = r'^[a-zA-Z0-9_]+$'
        return bool(re.match(pattern, username))
    
    @staticmethod
    def is_valid_discord_id(user_id: int) -> bool:
        """
        Valida se o Discord ID é válido.
        """
        return isinstance(user_id, int) and user_id > 0
    
    @staticmethod
    def sanitize_username(username: str) -> str:
        """
        Remove espaços e caracteres especiais do username.
        """
        return username.strip().replace(' ', '_')
