from game_controller import TopLevelController
from enemies import SewerGauntlet

game = TopLevelController()
game.gauntlet = SewerGauntlet()
game.play_gauntlet()
