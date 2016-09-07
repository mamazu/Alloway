import pygame

from tools.Score import Highscore
from tools.utils import TextPane
from tools.VecMath import Pane, Vec2D


class SceneManager:
    BACKGROUND_COLOR = (66, 180, 255)
    QUIT = 0
    CONTINUE = 1
    RESTART = 2

    def __init__(self, size):
        pygame.init()
        self.size = size if Vec2D.isVec(size) else Vec2D(500, 500)
        self.screen = pygame.display.set_mode(self.size.getTuple())
        self.clock = pygame.time.Clock()

    # Shows a pause screen
    def pauseScreen(self):
        pauseText = TextPane("Pause", 100)
        pauseText.pos = (self.size - pauseText.size) / 2
        pauseText.draw(self.screen)
        pygame.display.update()
        while True:
            for pauseEvent in pygame.event.get():
                if pauseEvent.type == pygame.QUIT:
                    return SceneManager.QUIT
                elif pauseEvent.type == pygame.KEYDOWN and pauseEvent.key in (pygame.K_p, pygame.K_ESCAPE):
                    return SceneManager.QUIT
            self.clock.tick(100)

    # Gameover Screen
    def gameOverScreen(self):
        playerName = ''
        blocked = True
        # Creating text panes
        gameOverText = TextPane("Game Over", 60)
        gameOverText.pos = (self.size - gameOverText.size) / 2
        gameOverText.draw(self.screen)
        # The text below
        restartText = TextPane("Q to quit or C to play again or H for highscore", 45)
        restartText.pos = (self.size - restartText.size) / 2 + Vec2D(0, 10)
        restartText.draw(self.screen)
        # Playername
        playerNameText = TextPane(playerName, 100)
        
        # Updating the screen and doing the event loop
        while True:
            for gameOverEvent in pygame.event.get():
                if gameOverEvent.type == pygame.QUIT:
                    return SceneManager.QUIT
                elif gameOverEvent.type == pygame.KEYDOWN:
                    if gameOverEvent.key == pygame.K_q and not blocked:
                        return SceneManager.QUIT
                    elif gameOverEvent.key == pygame.K_c and not blocked:
                        return SceneManager.RESTART
                    elif 97 <= gameOverEvent.key <= 122 and len(playerName) < 51:
                        playerName += chr(gameOverEvent.key)
                    elif gameOverEvent.key == pygame.K_BACKSPACE:
                        playerName = playerName[:-1]
                    elif gameOverEvent.key == pygame.K_RETURN:
                        blocked = False
                        print(playerName)
                        Highscore.saveToFile(playerName, player.points.score, level.levelid)
            fillPane = Pane(Vec2D(0, restartText.pos.y+restartText.size.y), Vec2D(self.size))
            self.screen.fill(SceneManager.BACKGROUND_COLOR, fillPane)
            # Playername
            if blocked:
                playerNameText.pos = self.size - playerNameText.size
                playerNameText.draw(self.screen)
                pygame.display.update()
            self.clock.tick(100)
