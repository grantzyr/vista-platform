from typing import Optional
from datetime import datetime, timezone

from sqlmodel import Session

from app.core.config import settings
from app.utils import setup_logger
from app.models.game import GameUpdate, GamePublic
from app.games.registry import game_registry
from app.services.game_service import GameService

logger = setup_logger("GameManager", settings.LOG_LEVEL)

class GameManager:
    """game manager service"""
    
    def sync_games_to_database(self, session: Session) -> None:
        """sync games to database"""
        game_service = GameService(session)

        registered_games = game_registry.list_game_metadata()
        
        for game_create_model in registered_games:
            existing_game = game_service.get_game_by_name(game_create_model.game_name)
            if existing_game:
                # update existing game
                game_update_model = GameUpdate(**existing_game.model_dump())
                game_update_model.display_name = game_create_model.display_name
                game_update_model.description = game_create_model.description
                game_update_model.icon_url = game_create_model.icon_url
                game_update_model.updated_at = datetime.now(timezone.utc)
                game_service.update_game(existing_game.id, game_update_model)
            else:
                game_service.create_game(game_create_model)
        
        logger.info(f"Synced {len(registered_games)} games to database")
                
    
    def sync_game_setups_to_database(self, db_session: Session) -> None:
        """sync game setups to database"""
        game_service = GameService(db_session)

        registered_games = game_registry.get_all_games()
        for game_name, game_class in registered_games.items():
            if game_class.check_game_setup_exists(db_session):
                logger.info(f"Game {game_name} setup already exists")
                continue
            logger.info(f"Game {game_name} setup does not exist, saving...")
            game_class.save_game_setups(db_session)
            logger.info(f"Game {game_name} setup saved")
        
        logger.info(f"Synced setups for {len(registered_games)} game to database")

    def get_game_metadata(self, session: Session, game_name: str) -> Optional[GamePublic]:
        """get single game metadata"""
        game_service = GameService(session)
        return game_service.get_game_public_by_name(game_name)
    
# global game manager
game_manager = GameManager()