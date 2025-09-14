from typing import Dict, List, Optional

from app.models.game import GameCreate
from app.games.base.main import GameMetadataBase

class GameRegistry:
    """game registry"""
    
    def __init__(self):
        self._games: Dict[str, GameMetadataBase] = {}
    
    def register(self, game_class: GameMetadataBase) -> None:
        """register game"""
        # create temp instance to get game name
        temp_instance = game_class()
        game_name = temp_instance.game_name
        self._games[game_name] = temp_instance
    
    def get_game(self, game_name: str) -> Optional[GameMetadataBase]:
        """get game class"""
        if game_name not in self._games:
            return None
        return self._games[game_name]
    
    def get_game_create_model(self, game_name: str) -> Optional[GameCreate]:
        """get game create model"""
        game = self.get_game(game_name)
        if game is None:
            return None
        return game.game_create_model
    
    def get_all_games(self) -> Dict[str, GameMetadataBase]:
        """get all registered games"""
        return self._games.copy()
    
    def list_game_names(self) -> list[str]:
        """list all game names"""
        return list(self._games.keys())
    
    def list_game_metadata(self) -> List[GameCreate]:
        """list all game metadata"""
        return [game.game_create_model for game in self._games.values()]

# global game registry
game_registry = GameRegistry()