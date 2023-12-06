import simpleGE, pygame, random


class Player(simpleGE.SuperSprite):
    def __init__(self, scene):
        simpleGE.SuperSprite.__init__(self, scene)
        self.setImage("platypus.png")
        self.setSize(50, 50)
        self.setBoundAction(self.STOP)
        position = (320, 400)
        self.setPosition(position)

    def checkEvents(self):
        speed = 7
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y -= speed
        if keys[pygame.K_s]:
            self.y += speed
        if keys[pygame.K_d]:
            self.x += speed
        if keys[pygame.K_a]:
            self.x -= speed
        self.x = max(25, min(self.x, 640 - 25))
        self.y = max(250, min(self.y, 480 - 25))


class Shot(simpleGE.SuperSprite):
    def __init__(self, scene, parent):
        super().__init__(scene)
        self.parent = parent
        self.setImage("spear.png")
        self.setSize(20, 35)
        self.setBoundAction(self.HIDE)
        self.setAngle(90)
        self.setImageAngle(360)
        self.visible = True

    def fire(self):
        self.setPosition(self.parent.rect.center)
        self.setSpeed(20)

    def hide(self):
        self.visible = False
        self.setPosition((-100, -100))
        print("Shot hidden")  # debugging

    def isVisible(self):
        return self.visible


class FlyPrecursor(simpleGE.SuperSprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("red_square.png")
        self.setSize(900, 100)
        position = (320, 350)
        self.setPosition(position)


class Fly(simpleGE.SuperSprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("fly.png")
        self.setSize(125, 125)
        self.setSpeed(15)
        self.setMoveAngle(180)
        self.setBoundAction(self.CONTINUE)
        self.setPosition((-100, -100))


class BossAttack(simpleGE.SuperSprite):
    def __init__(self, scene, parent):
        super().__init__(scene)
        self.parent = parent
        self.setImage("redCoin.png")
        self.setSize(25, 45)
        self.setBoundAction(self.CONTINUE)
        self.visible = True

    def fire(self):
        offset = 75  #
        position = (self.parent.x, self.parent.y + offset)  #
        self.setPosition(position)
        self.setSpeed(5)
        self.setAngle(random.uniform(215, 320))

    def hide(self):
        self.visible = False
        self.setPosition((-100, -100))
        self.setSpeed(0)
        print("Boss attack hidden")  # debugging

    def isVisible(self):
        return self.visible


class Boss(simpleGE.SuperSprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("boss_fly.png")
        self.setSize(200, 200)
        position = (350, 175)
        self.setPosition(position)


class Game(simpleGE.Scene):
    def __init__(self):
        simpleGE.Scene.__init__(self)
        self.background = pygame.image.load("background.png")
        self.player = Player(self)
        self.playerMaxHealth = 5
        self.NUM_SHOTS = 15
        self.currentShot = 0

        self.shots = [Shot(self, self.player) for _ in range(self.NUM_SHOTS)]

        self.precursor = FlyPrecursor(self)
        self.lblTime = simpleGE.Label()
        self.lblTime.text = "Time:"
        self.lblTime.center = (590, 10)
        self.lblTime.size = (100, 25)
        self.timer = simpleGE.Timer()

        self.boss = Boss(self)
        self.bossMaxHealth = 100

        self.bossAttacks = [BossAttack(self, self.boss) for _ in range(15)]

        for attack in self.bossAttacks:
            attack.setPosition((-100, -100))
            attack.visible = True
            attack.fire()

        self.attackTimer = simpleGE.Timer()
        self.attackInterval = 0.8

        self.lblBossHealth = simpleGE.Label()
        self.lblBossHealth.text = f"Boss Health: {self.bossMaxHealth}"
        self.lblBossHealth.center = (85, 10)
        self.lblBossHealth.size = (220, 25)

        self.lblPlayerHealth = simpleGE.Label()
        self.lblPlayerHealth.text = f"Player Health: {self.playerMaxHealth}"
        self.lblPlayerHealth.center = (15, 465)
        self.lblPlayerHealth.size = (200, 25)

        self.fly = Fly(self)

        self.lblWinLose = simpleGE.Label()
        self.lblWinLose.text = None
        self.lblWinLose.center = (-200, -200)

        self.gameSprite = [
            self.player,
            self.shots,
            self.lblTime,
            self.lblBossHealth,
            self.lblPlayerHealth,
            self.boss,
            self.bossAttacks,
            self.lblWinLose,
        ]
        self.gameGroup = self.makeSpriteGroup(self.gameSprite)

        self.lblInstructions = simpleGE.Label()
        self.lblInstructions.text = "Move : WASD | Shoot: Space | Dodge and good luck"
        self.lblInstructions.center = (300, 200)
        self.lblInstructions.fgColor = (255, 255, 255)
        self.lblInstructions.bgColor = (0, 0, 0)
        self.lblInstructions.size = (500, 50)

        self.startButton = simpleGE.Button()
        self.startButton.text = "Start Game"
        self.startButton.center = (400, 350)
        self.startButton.bgColor = (255, 255, 255)
        self.startButton.clicked = False

        self.startSprite = [self.lblInstructions, self.startButton]
        self.startGroup = self.makeSpriteGroup(self.startSprite)

        self.quitButton = simpleGE.Button()
        self.quitButton.text = "Quit"
        self.quitButton.center = (400, 300)
        self.quitButton.bgColor = (255, 255, 255)
        self.quitButton.clicked = False

        self.bossHit = simpleGE.Sound("blip.ogg")

        self.playerHit = simpleGE.Sound("blop.ogg")

        self.resetButton = simpleGE.Button()
        self.resetButton.text = "Restart"
        self.resetButton.center = (400, 350)
        self.resetButton.bgColor = (255, 255, 255)
        self.resetButton.clicked = False

        self.buttonSprites = [self.quitButton, self.resetButton]
        self.buttonGroup = self.makeSpriteGroup(self.buttonSprites)

        self.addGroup(self.startGroup)

        self.sprites = []
        self.precursorReady = [10, 20, 30, 40, 50, 55, 60, 65]

        self.gameOver = True

        self.precursorAdded = False

        self.flyAdded = False

        self.precursorTimer = None

        self.bossFiredAttacks = 0

        self.timeSpent = 0

    def doEvents(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.currentShot += 1
                if self.currentShot >= self.NUM_SHOTS:
                    self.currentShot = 0
                self.shots[self.currentShot].fire()

    def update(self):
        for button in self.buttonSprites:
            button.update()
            if button.clicked:
                if button == self.quitButton:
                    self.stop()
                elif button == self.resetButton:
                    self.resetGame()
                if button == self.startButton:
                    self.resetGame()
                button.clicked = False
        self.timeSpent = 0 + self.timer.getElapsedTime()

        if int(self.timeSpent) >= 100:
            self.gameOver = True
        if not self.gameOver:
            self.lblTime.text = f"Time: {int(self.timeSpent)}"
            if int(self.timeSpent) in self.precursorReady and not self.precursorAdded:
                print("added to screen")  # debugging
                self.precursorGroup = self.makeSpriteGroup([self.precursor])
                self.addGroup(self.precursorGroup)
                self.precursorAdded = True
                self.precursorTimer = simpleGE.Timer()
                # self.precursorTimer.start()

            if self.precursorAdded and self.precursorTimer.getElapsedTime() >= 1:
                self.precursorGroup.empty()
                self.precursorAdded = False
                self.fly.setPosition((600, 350))
                self.flyGroup = self.makeSpriteGroup([self.fly])
                self.addGroup(self.flyGroup)
                self.flyAdded = True
                print(f"{self.flyGroup}")

            flyOffScreen = -60
            if self.fly.x < flyOffScreen and self.flyAdded:
                print("fly gone")
                self.flyGroup.empty()
                self.flyAdded = False

            if self.fly.collidesWith(self.player):
                print("fly collided")
                self.playerMaxHealth = 0
                self.lblPlayerHealth.text = f"Player Health: {self.playerMaxHealth}"

            for shot in self.shots:
                offScreen = not shot.isVisible() and (shot.x < 0)
                if offScreen:
                    shot.visible = True  # make shots visible again
                if shot.isVisible() and shot.collidesWith(self.boss):
                    print(
                        f"collision detected for shot {self.shots.index(shot)}"
                    )  # debugging
                    self.bossHit.play()
                    self.bossMaxHealth -= 1
                    self.lblBossHealth.text = f"Boss Health: {self.bossMaxHealth}"
                    shot.hide()

            for attack in self.bossAttacks:
                offScreen = not attack.isVisible() and (attack.x > 480)
                if offScreen:
                    attack.visible = True  # make bossAttack visible again
                else:
                    attack.update()
                    if attack.collidesWith(self.player):
                        print(f"player hit by {self.bossAttacks.index(attack)}")
                        self.playerHit.play()
                        self.playerMaxHealth -= 1
                        self.lblPlayerHealth.text = (
                            f"Player Health: {self.playerMaxHealth}"
                        )
                        attack.hide()
                if self.attackTimer.getElapsedTime() >= self.attackInterval:
                    attack.fire()
                    self.attackTimer.start()

            if self.attackTimer.getElapsedTime() >= self.attackInterval:
                for attack in self.bossAttacks:
                    if not attack.isVisible():
                        attack.fire()
                        break

                self.attackTimer.start()
            if self.playerMaxHealth <= 0:
                self.lblWinLose.text = "You Lost"
                self.gameOver = True
                self.lblWinLose.center = (200, 200)

                self.addGroup(self.buttonGroup)
            elif self.bossMaxHealth <= 0:
                self.lblWinLose.text = "You Win"
                self.gameOver = True
                self.lblWinLose.center = (200, 200)
                self.addGroup(self.buttonGroup)

        if self.gameOver:
            self.buttonGroup.add(self.buttonSprites)

    def resetGame(self):
        self.addGroup(self.gameGroup)
        self.startGroup.empty()
        self.gameOver = False
        self.buttonGroup.empty()
        self.quitButton.clicked = False
        self.resetButton.clicked = False

        self.lblWinLose.center = (-200, -200)

        # Reset player
        self.playerMaxHealth = 5
        self.lblPlayerHealth.text = f"Player Health: {self.playerMaxHealth}"
        self.player.speed = 0
        self.player.setPosition((320, 400))

        # Reset boss
        self.bossMaxHealth = 100
        self.lblBossHealth.text = f"Boss Health: {self.bossMaxHealth}"

        for attack in self.bossAttacks:
            attack.setSpeed(-5)

        # Reset timer and other game state variables
        self.timeSpent = 0
        self.timer.start()
        self.attackTimer.start()

        # Clear shots and boss attacks from the screen
        for shot in self.shots:
            shot.hide()
        for attack in self.bossAttacks:
            attack.hide()

        # Reset flags and timers
        self.precursorAdded = False
        self.flyAdded = False
        self.bossFiredAttacks = 0
        self.precursorTimer = None
        self.flyTimer = None


def main():
    game = Game()
    game.start()


if __name__ == "__main__":
    main()


# w, h = pygame.display.get_surface().get_size()
# print(w, h)


# if attack.isVisible() and attack.collidesWith(self.player):
#     print(
#         f"player hit by {self.bossAttacks.index(attack)}"
#     )  # debugging
#     attack.hide()
