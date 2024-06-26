# Nathaniel Pawluk
# Flappy Bird Clone
# May 31st 2024
# Things to fix/add: death animation, sounds, score, menu?


import pygame
import random
import sys

W = 1920
H = 1080
BIRD_W = 136
BIRD_H = 96
PIPE_W = 136
PIPE_H = 792

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Flappy Bird")
running = True
clock = pygame.time.Clock()
path = sys.argv[0].strip("flappybird.py")

class Bird:
    def __init__(self):
        self.frames = []
        self.x = W//4
        self.y = H//2
        self.frameNumber = 0
        self.v = 0
        self.loadSprites()
        self.rect = (self.x, self.y, BIRD_W, BIRD_H)
        self.red = 0
        self.green = 255
        
    def loadSprites(self):
        spriteCords = ((0, 0, BIRD_W, BIRD_H), (BIRD_W, 0, BIRD_W, BIRD_H), (2 * BIRD_W, 0, BIRD_W, BIRD_H))
        self.sheet = pygame.image.load(f"{path}/assets/bird.png").convert()

        for cord in spriteCords:
            rect = pygame.Rect(cord)
            image = pygame.Surface(rect.size).convert()
            image.blit(self.sheet, (0, 0), rect)
            image.set_colorkey(image.get_at((0,0)), pygame.RLEACCEL)
            self.frames.append(image)

    def currentFrame(self):
        return self.frames[self.frameNumber]
    
    def draw(self):
        image = self.currentFrame()
        image = pygame.transform.rotate(image, 0 - self.v//1.5)
        rect = image.get_rect(center = (self.x + (BIRD_W//2), self.y + (BIRD_H//2)))
        screen.blit(image, rect)
        self.red = self.red - 5 if self.red > 0 else 0
        self.green = self.green + 5 if self.green < 255 else 255

        #Hitbox
        self.hbColor = pygame.Color(self.red,self.green,0,75)
        self.rect = (self.x, self.y, BIRD_W, BIRD_H)
        self.hitBoxSurface = pygame.Surface((W, H), pygame.SRCALPHA)
        pygame.draw.rect(self.hitBoxSurface, self.hbColor, self.rect)
        screen.blit(self.hitBoxSurface, (0,0))

    def jump(self):
        self.v = -30

    def move(self):
        # Move bird
        self.y += self.v
        
        # Update sprite
        if self.v <= -25:
            self.frameNumber = 1
        elif self.v <= 0:
            self.frameNumber = 2
        else:
            self.frameNumber = 0

        # Cap downwards velocity
        if self.v < 45:
            self.v += 3
        else:
            self.v = 45

    def collide(self, hitboxes):
        rect = pygame.Rect(self.rect)
        for hb in hitboxes:
            if rect.colliderect(hb):
                self.red = 255
                self.green = 0
        if self.y < 0 or self.y > H - BIRD_H:
            self.red = 255
            self.green = 0


class Pipe:
    def __init__(self):
        self.x = W + 30
        self.top = pygame.image.load(f"{path}/assets/pipeTop.png")
        self.bottom = pygame.image.load(f"{path}/assets/pipeBottom.png")
        self.topY = 0 - random.randint(200, PIPE_H - 300)
        self.bottomY = self.topY + PIPE_H + 300
        self.v = -10
    
    def draw(self):
        self.hitboxes = []
        self.hitboxes.append((self.x, self.topY, PIPE_W, PIPE_H))
        screen.blit(self.top, (self.x, self.topY))
        self.hitboxes.append((self.x, self.bottomY, PIPE_W, PIPE_H))
        screen.blit(self.bottom, (self.x, self.bottomY))
        self.x += self.v

    def onscreen(self):
        if self.x + PIPE_W < 0:
            return False
        else:
            return True
        
    def drawHitbox(self):
        self.hitboxSurface = pygame.Surface((W, H), pygame.SRCALPHA)
        for hitbox in self.hitboxes:
            pygame.draw.rect(self.hitboxSurface, pygame.Color(255,0,0,75), hitbox)
            screen.blit(self.hitboxSurface, (0,0))

class Bushes:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = pygame.image.load(f"{path}/assets/bushes.png")
    
    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        screen.blit(self.image, (self.x + W, self.y))
        self.x -= 2
        if self.x + W < 0:
            self.x = 0

class Clouds:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = pygame.image.load(f"{path}/assets/clouds.png")
    
    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        screen.blit(self.image, (self.x + W, self.y))
        self.x -= 1
        if self.x + W < 0:
            self.x = 0

bird = Bird()
pipes = []
pipes.append(Pipe())
timer = 0
bushes = Bushes()
clouds = Clouds()

while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()
    
    bird.move()
    screen.fill("white")
    #screen.fill("cyan")
    #clouds.draw()
    #bushes.draw()
    for pipe in pipes:
        pipe.draw()
        #pipe.drawHitbox()
        bird.collide(pipe.hitboxes)

    bird.draw()
    pygame.display.flip()
    if timer == 60:
        pipes.append(Pipe())
        timer = 0
    else:
        timer += 1

    if not pipes[0].onscreen():
        pipes.pop(0)