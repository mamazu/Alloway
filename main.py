# Import and start Pygame
import pygame

from Scenes import SceneManager
from tools.Sound import Sound
from tools.VecMath import Vec2D


class Game(SceneManager):

    def __init__(self, name, size=None):
        from mechanics.Ball import Ball, MovementMode
        from mechanics.Level import Level
        from mechanics.Player import Player
        from tools.Score import Score
        SceneManager.__init__(self, size)
        pygame.display.set_caption(name)

        # Creating objects
        # Ball
        self.ball = Ball(size=40)
        self.mode = MovementMode()
        self.mode.pos = (self.size - self.mode.size) * Vec2D(.5, 1) - Vec2D(0, 5)

        self.player = Player()
        self.effects = []
        self.level = Level()
        # Setting up the score
        self.points = Score(0)
        self.points.pos = Vec2D(self.size.x - self.points.size.x) + Vec2D(-10, 10)
        #Setting up the sound
        self.sound = Sound()
        self.sound.pos = self.size - self.sound.size - Vec2D(20, 5)
        print("LOADING COMPLETE")
        #Setting up the game loop and the first level
        self.running = True
        self.setup()
        self.keymap()

    def setup(self):
        from mechanics.Effect import Effect

        # self.effects.append(Effect("PlayerBooster", 5))
        # self.effects.append(Effect("BallSlower", 5))
        # Sets the level to 1
        self.level.switchLevel(1)
        # Centers the player
        playerRect = self.player.getRect()
        playerRect.center = (self.size.x / 2, self.size.y - self.player.offsetY)
        self.player.pos = Vec2D(playerRect.left, playerRect.top)
        # Relocates the ball to the middle of the player
        self.ball.movement = Vec2D(0, 0)
        self.ball.pos = self.player.pos + self.player.size * Vec2D(.5,0) - self.ball.size * Vec2D(.5, 1)
        # Reset score
        self.points.reset()

    def keymap(self):
        self.keymap = {
            pygame.K_ESCAPE:    self.stop,
            pygame.K_p:         self.pauseScreen,
            pygame.K_UP:        self.ball.moveRand,
            pygame.K_SPACE:     self.ball.moveRand,
            pygame.K_s:         self.sound.toggleSound,
            pygame.K_m:         self.mode.toggle,
            pygame.K_q:         self.gameOver,
        }

    def start(self):
        # Gameloop
        while self.running:
            for event in pygame.event.get():
                self.eventLoop(event)

            # Applying movement
            if self.ball.move():
                self.gameOver()
            self.player.move()

            # Applying effects
            for i, effect in enumerate(self.effects):
                effect.tick()
                effect.drawEffect(i)

            self.draw()
            self.clock.tick(self.level.time)

    def eventLoop(self, event):
        # todo: implement keymap
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.player.movement = 1
            elif event.key == pygame.K_LEFT:
                self.player.movement = -1
            try:
                self.keymap[event.key]()
            except KeyError:
                pass
        elif event.type == pygame.KEYUP:
            self.player.movement = 0
        elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
            self.click(pygame.mouse.get_pos())

    def click(self, mousepos):
        self.sound.click(mousepos)

    def draw(self):
        self.screen.fill(SceneManager.BACKGROUND_COLOR)
        drawing = [self.ball, self.player, self.points, self.sound, self.level, self.mode]
        for drawCall in drawing:
            drawCall.draw(self.screen)
        pygame.display.update()

    def stop(self):
        self.running = False

    def gameOver(self):
        self.sound.playSound("gameOver")
        if self.gameOverScreen() == SceneManager.RESTART:
            self.setup()

# todo: add debug class

g = Game('Alloway')
g.start()


pygame.quit()
quit()
