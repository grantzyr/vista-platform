from sqlmodel import Session, create_engine

# from app import crud
from app.core.config import settings
from app.services.game_manager import game_manager

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

def init_db(session: Session) -> None:
    game_manager.sync_games_to_database(session)
    game_manager.sync_game_setups_to_database(session)