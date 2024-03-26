import pygame as pg
import random

with open('settings.txt', 'r') as f:
    settings = f.read().split()
    SCREEN_X = float(settings[0])
    SCREEN_Y = float(settings[1])
    FPS = int(settings[2])

pg.init()

class Pipe(pg.sprite.Sprite):
    def __init__(self, top, size):
        self.x = SCREEN_X
        self.top = top
        if (self.top):
            self.y = 0
            self.image = pg.transform.flip(pg.image.load("Sprites/Game_Objects/pipe-green.png").convert_alpha(), False, True)
            try:
                self.image = self.image.subsurface(0, 320 - size, 52, size)
            except:
                pass
            
        else:
            self.y = SCREEN_Y - size
            self.image = pg.image.load("Sprites/Game_Objects/pipe-green.png").convert_alpha()
            try:
                self.image = self.image.subsurface(0, 0, 52, size)
            except:
                pass
    
        self.width = 50
        self.height = size

    def update(self):
        self.x -= 2

class Bird(pg.sprite.Sprite):
    def __init__(self):
        self.vel = 0
        self.midFlap = pg.image.load("Sprites/Game_Objects/yellowbird-midflap.png").convert_alpha()
        self.image = self.midFlap
        self.dead = False
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = 100
        self.y = SCREEN_Y / 2 - self.height / 2

    def update(self):
        self.y += self.vel

        self.image = pg.transform.rotate(self.midFlap, self.vel * -2)

        if (self.y < 0 or self.y + self.height > SCREEN_Y):
            self.dead = True

    def jump(self):
        self.vel = -10

class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_X, SCREEN_Y), pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        pg.display.set_caption("Crappy Bird")
        self.background = pg.image.load("Sprites/Game_Objects/background-day.png").convert()
        self.base = pg.image.load("Sprites/Game_Objects/base.png").convert()
        self.score = 0
        self.freq = 200
        self.sprites = []
        self.pipes = []
        self.birds = []

    def spawnPipe(self):
        size = random.randint(50, int(SCREEN_Y / 1.5))
        size1 = SCREEN_Y - (size + 175)

        pipe = Pipe(True, size)
        pipe1 = Pipe(False, size1)

        self.pipes.append(pipe)
        self.pipes.append(pipe1)
        
        self.sprites.append(pipe)
        self.sprites.append(pipe1)

    def getClosestPipe(self):
        closestPipe = None
        for pipe in self.pipes:
            for bird in self.birds:
                if ((bird.x + bird.width) - pipe.x) > 0:
                    continue
                elif closestPipe == None:
                    closestPipe = pipe
                else:
                    return pipe
        return None

    def update(self):
        self.clock.tick(FPS + self.score * 2)
        pg.display.set_caption(f"Crappy Bird! FPS: {str(round(self.clock.get_fps(), 2))}")
        self.screen.blit(self.background, (0, 0))

        for bird in self.birds:
            if (bird.vel < 10):
                bird.vel += 0.5

        for sprite in self.sprites:
            sprite.update()
            self.screen.blit(sprite.image, (sprite.x, sprite.y))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.birds[0].jump()
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.birds[0].jump()

        if len(self.pipes) < 2:
            self.spawnPipe()

        for pipe in self.pipes:
            if (pipe.x < 0):
                self.pipes.remove(pipe)
                self.sprites.remove(pipe)
                self.score += 1

            for bird in self.birds:
                if (bird.x > pipe.x and bird.x + bird.width < pipe.x + pipe.width and bird.y > pipe.y and bird.y + bird.height < pipe.y + pipe.height) or (bird.x + bird.width > pipe.x and bird.x < pipe.x + pipe.width and bird.y + bird.height > pipe.y and bird.y < pipe.y + pipe.height):
                    bird.dead = True

        self.freq += 1

        self.screen.blit(self.base, (0, SCREEN_Y - 112/2))
        pg.display.flip()

    def run(self):
        while not self.birds[0].dead == True:
            self.update()

        return self.score

if __name__ == "__main__":
    while True:
        game = Game()
        game.birds.append(Bird())
        game.sprites.append(game.birds[0])
        game.run()