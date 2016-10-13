# Import and start Pygame
import pygame
import timeit
from Scenes import SceneManager
from tools.VecMath import Vec2D
from timeit import default_timer
from tools.Debug import Debug

class Game(SceneManager):
    def __init__(self, name, size=None):
        SceneManager.__init__(self, size)
        pygame.display.set_caption(name)
        self.menuScreen()
        self.init()
        self.setup()

    def init(self):
        self.createObjects()
        self.running = True
        self.keymap = {
            pygame.K_ESCAPE:    self.stop,
            pygame.K_p:         self.pauseScreen,
            pygame.K_UP:        self.ball.moveRand,
            pygame.K_SPACE:     self.ball.moveRand,
            pygame.K_s:         self.sound.toggleSound,
            pygame.K_q:         self.gameOver,
        }

    def createObjects(self):
        from mechanics.Ball import Ball
        from mechanics.Level import Level
        from mechanics.Player import Player
        from tools.Sound import Sound
        from tools.Score import Score
        from gui.Text import TextPane

        self.ball = Ball(size=40)
        self.player = Player()
        self.effects = []
        self.level = Level()
        self.level.text.fs = 50
        self.level.text.update()
        self.score = Score(0)
        self.score.fs = 50
        self.score.update()
        self.sound = Sound()
        self.time = default_timer()

        Debug.printMessage("LOADING COMPLETE")
        #Setting GUI position
        self.score.pos = Vec2D(self.size.x - self.score.size.x) + Vec2D(-10, 10)
        self.sound.pos = self.size - self.sound.size - Vec2D(20, 10)
        self.sound.fs = 15
        self.sound.update()
        self.level.text.pos = Vec2D(10, 10)
        #Debug features
        if Debug.DEBUGGING:
            self.fpsCounter = TextPane('0 fps', 15)
            self.fpsCounter.pos = Vec2D(20, self.size.y - 10 - self.fpsCounter.size.y)

    def setup(self):
        # Setting the effects
        # from mechanics.Effect import Effect
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
        # Moving level Down
        self.level.setOffset(Vec2D(0, self.score.pos.y + self.score.size.y *.75))

        # Reset score
        self.score.reset()
        self.level.pos = Vec2D(0, self.score.pos.y + self.score.size.y)

    def start(self):
        # Gameloop
        while self.running:
            for event in pygame.event.get():
                self.eventLoop(event)

            self.player.move(self.size.x)
            # Applying movement to th ball
            self.ball.move()
            ballMovement = self.ball.constrain(self.size)
            if ballMovement == self.ball.FAIL:
                self.gameOver()
            elif ballMovement == self.ball.BOUNCE:
                self.sound.play("wall")
            if self.ball.collides(self.player):
                self.sound.play("player")
            # Checking for level collisions
            if self.level.collides(self.ball):
                self.ball.bounceY()
                self.score = self.score + 50
                if self.level.levelCheck() == 0:
                    #TODO: add wining screen
                    print("You win")

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
                self.player.movement.x = 1
            elif event.key == pygame.K_LEFT:
                self.player.movement.x = -1
            try:
                self.keymap[event.key]()
            except KeyError:
                pass
        elif event.type == pygame.KEYUP:
            self.player.movement = Vec2D(0, 0)
        elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
            self.click(pygame.mouse.get_pos())

    def click(self, mousepos):
        self.sound.click(mousepos)

    def draw(self):
        self.fps()
        self.screen.fill(SceneManager.BACKGROUND_COLOR)
        drawing = [self.ball, self.player, self.score, self.sound, self.level]
        if Debug.DEBUGGING:
            drawing.append(self.fpsCounter)
        for drawCall in drawing:
            drawCall.draw(self.screen)
        pygame.display.update()

    def fps(self):
        if not Debug.DEBUGGING:
            return
        time = default_timer()
        deltaTime = time - self.time
        self.fpsCounter.setText('%i fps' % (1 / deltaTime))
        self.time = time

    def stop(self):
        self.running = False

    def gameOver(self):
        self.sound.play("gameOver")
        gameOver = self.gameOverScreen()
        if gameOver == SceneManager.RESTART:
            self.setup()
        elif gameOver == SceneManager.QUIT:
            self.stop()

g = Game('Alloway')
g.start()

pygame.quit()
quit()
