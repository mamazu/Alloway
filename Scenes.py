import pygame

from tools.Score import Highscore
from gui.Text import TextPane
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
        toRender = []
        # Creating text panes
        gameOverText = TextPane("Game Over", 60)
        gameOverText.pos = (self.size - gameOverText.size) / 2
        toRender.append(gameOverText)
        # The text below
        restartText = TextPane("Q to quit or C to play again", 45)
        restartText2 = TextPane("H for highscore", 45)
        restartText.pos = (self.size - restartText.size) / 2 + Vec2D(0, 50)
        restartText2.pos = (self.size - restartText2.size) / 2 + Vec2D(0, 100)
        toRender.append(restartText)
        toRender.append(restartText2)
        # Playername
        playerNameText = TextPane(playerName, 90)
        playerNameText.pos.y = (self.size - playerNameText.size).y
        toRender.append(playerNameText)
        # Updating the screen and doing the event loop
        while True:
            for gameOverEvent in pygame.event.get():
                if gameOverEvent.type == pygame.QUIT:
                    return SceneManager.QUIT
                if gameOverEvent.type == pygame.KEYDOWN:
                    key = gameOverEvent.key
                    if key == pygame.K_ESCAPE:                return SceneManager.QUIT
                    if key == pygame.K_q and not blocked:     return SceneManager.QUIT
                    elif key == pygame.K_c and not blocked:   return SceneManager.RESTART
                    elif 97 <= key <= 122:                    playerName += chr(key)
                    elif key == pygame.K_SPACE:               playerName += ' '
                    elif key == pygame.K_BACKSPACE:           playerName = playerName[:-1]
                    elif key == pygame.K_RETURN and blocked:
                        blocked = False
                        print(playerName)
                        Highscore.saveToFile(playerName, player.points.score, level.levelid)
            #Drawing objects
            self.screen.fill(SceneManager.BACKGROUND_COLOR)
            playerNameText.setText("Enter your name" if playerName == '' else playerName)
            for obj in toRender: obj.draw(self.screen)
            pygame.display.update()

    def menuScreen(self):
        self.screen.fill(SceneManager.BACKGROUND_COLOR)
        buttons = [Button("Start", 30), Button("Highscore", 30)]
        #Drawing
        for button in buttons:
            button.size = Vec2D(200, 50)
            button.draw()
        while(True):
            for menuEvent in pygame.event.get():
                if menuEvent != pygame.MOUSEBUTTONDOWN or event.button != 1:
                    continue
                for button in buttons:
                    button.click(pygame.mouse.get_pos())
