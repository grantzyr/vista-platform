from abc import ABC, abstractmethod

from sqlmodel import Session

from app.models.game import GameCreate

class GameMetadataBase(ABC):
    """Game metadata base class"""
    
    @property
    @abstractmethod
    def game_name(self) -> str:
        """get game name"""
        pass

    @property
    @abstractmethod
    def game_display_name(self) -> str:
        """get game display name"""
        pass
    
    @property
    @abstractmethod
    def game_description(self) -> str:
        """get game description"""
        pass
    
    @property
    @abstractmethod
    def game_icon_url(self) -> str:
        """get game icon url"""
        pass
    
    @property
    @abstractmethod
    def game_create_model(self) -> GameCreate:
        """get game create model"""
        pass

    @abstractmethod
    def check_game_setup_exists(self, session: Session) -> bool:
        """check if game setup exists"""
        pass

    @abstractmethod
    def save_game_setups(self, session: Session) -> None:
        """save game setups"""
        pass