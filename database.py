from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import config

engine = create_engine(config.DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class VerifiedUser(Base):
    __tablename__ = 'verified_users'
    
    id = Column(Integer, primary_key=True)
    discord_id = Column(String(20), unique=True, nullable=False)
    transformice_username = Column(String(20), nullable=False)
    verified_at = Column(DateTime, default=datetime.now)
    verification_ip = Column(String(45), nullable=True)

class VerificationCode(Base):
    __tablename__ = 'verification_codes'
    
    code = Column(String(20), primary_key=True)
    discord_id = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)

class VerificationLog(Base):
    __tablename__ = 'verification_logs'
    
    id = Column(Integer, primary_key=True)
    discord_id = Column(String(20), nullable=False)
    action = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False)  # 'success', 'failed', 'expired'
    timestamp = Column(DateTime, default=datetime.now)
    notes = Column(String(255), nullable=True)

# Criar tabelas
Base.metadata.create_all(engine)

def get_session():
    """Retorna uma nova sessão do banco de dados."""
    return Session()

def add_verified_user(discord_id: str, transformice_username: str, ip: str = None) -> bool:
    """Adiciona um usuário verificado ao banco."""
    session = get_session()
    try:
        user = VerifiedUser(
            discord_id=str(discord_id),
            transformice_username=transformice_username,
            verification_ip=ip
        )
        session.add(user)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"Erro ao adicionar usuário verificado: {e}")
        return False
    finally:
        session.close()

def get_verified_user(discord_id: str) -> VerifiedUser:
    """Busca um usuário verificado pelo Discord ID."""
    session = get_session()
    try:
        user = session.query(VerifiedUser).filter_by(discord_id=str(discord_id)).first()
        return user
    finally:
        session.close()

def remove_verification(discord_id: str) -> bool:
    """Remove a verificação de um usuário."""
    session = get_session()
    try:
        user = session.query(VerifiedUser).filter_by(discord_id=str(discord_id)).first()
        if user:
            session.delete(user)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Erro ao remover verificação: {e}")
        return False
    finally:
        session.close()
