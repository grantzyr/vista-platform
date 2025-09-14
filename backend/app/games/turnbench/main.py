import os

from sqlmodel import Session

from app.core.config import settings
from app.utils import load_json, setup_logger
from app.games.base.main import GameMetadataBase, GameCreate
from app.games.turnbench.config import GAME_NAME, GAME_DISPLAY_NAME, GAME_DESCRIPTION, GAME_ICON_URL
from app.games.turnbench.models.setup import GameSetupCreate
from app.games.turnbench.game_setup.setup_service import SetupService

logger = setup_logger("TurnbenchGameMetadata", settings.LOG_LEVEL)

class TurnbenchGameMetadata(GameMetadataBase):
    """Turnbench game metadata"""
    
    def __init__(self):
        self.name = GAME_NAME
        self.display_name = GAME_DISPLAY_NAME
        self.description = GAME_DESCRIPTION
        self.icon_url = GAME_ICON_URL
    
    @property
    def game_name(self) -> str:
        """get game name"""
        return self.name
    
    @property
    def game_display_name(self) -> str:
        """get game display name"""
        return self.display_name
    
    @property
    def game_description(self) -> str:
        """get game description"""
        return self.description
    
    @property
    def game_icon_url(self) -> str:
        """get game icon url"""
        return self.icon_url
    
    @property
    def game_create_model(self) -> GameCreate:
        """get game create model"""
        return GameCreate(
            game_name=self.name,
            display_name=self.display_name,
            description=self.description,
            icon_url=self.icon_url,
        )
    
    def check_game_setup_exists(self, session: Session) -> bool:
        """check if game setup exists"""
        setup_service = SetupService(session)
        filepath = "app/games/turnbench/data/setups.json"
        logger.info(f"Trying to load {filepath} to check game setups")
        all_setups = load_json(filepath)
        setups, total = setup_service.list_setups(page=1, page_size=len(all_setups))
        if total == len(all_setups):
            return True
        return False
    
    def save_game_setups(self, session: Session) -> None:
        """save game setups"""
        setup_service = SetupService(session)
        filepath = "app/games/turnbench/data/setups.json"
        logger.info(f"Trying to load {filepath} to save game setups")
        all_setups = load_json(filepath)
        setup_creates = [GameSetupCreate(**setup) for setup in all_setups.values()]
        setups = setup_service.create_setups(setup_creates=setup_creates)
        logger.info(f"Saved {len(setups)} game setups")