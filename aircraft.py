import pygame
from pygame.locals import *
import sys
import random
import time

class Obj:
    def __init__(self, mode, type, pos, index):
        self.mode  = mode
        self.type  = type
        self.pos   = pos
        self.index = index

    def __repr__(self):
        return "mode = %d, type=%s, pos=%s, index = %d".format(self.mode, self.type, self.pos, self.index)

class Display:
    def __init__(self, width, height):
        pygame.init()
        self._width  = width
        self._height = height
        self.buffer = [0] * width * height
        self.screen = pygame.display.set_mode((width , height))

    @property
    def width(self):
        return self._width
    @property
    def height(self):
        return self._height

    def point(self, point, color):
        self.screen.set_at(point, color)

    def draw8image(self, zero, buffer, mode=True):
        x0, y0 = zero
        width    =  buffer[0] + (buffer[1] << 8)
        height   =  buffer[2] + (buffer[3] << 8)

        for x in range(width):
            for y in range(height):
                c = buffer[x + y * width + 4]
                if c != 0:
                    color = self.getColor(c)
                    if mode:
                        self.point((x + x0, height - y - 1 + y0), color)
                    else:
                        self.point((x + x0,y + y0), color)
    def swap(self):
        pygame.display.flip()

    def clear(self):
        self.screen.fill((0, 0, 0))

    def getColor(self, bit8color):
        r = bit8color >> 5
        g = (bit8color & 0b00011100) >> 2
        b = bit8color & 0b00000011
        return (r * 32,g * 32, b * 64)

class Game:
    aircraft = aircraft = [
        16,0,16,0,0,0,0,29,25,0,0,0,0,25,29,196,0,0,0,0,0,0,0,25,25,0,0,0,0,25,0,196,0,
        0,0,0,112,112,0,25,196,40,40,29,112,112,40,112,0,112,112,112,40,40,112,112,40,40,
        25,25,112,40,40,112,112,112,112,112,112,40,112,25,40,40,112,112,112,40,40,25,
        40,112,112,0,0,112,112,25,40,40,40,112,40,40,40,25,40,112,0,0,0,0,112,25,40,
        112,40,112,112,112,40,25,112,0,0,0,0,0,0,29,112,0,40,0,112,0,112,29,0,0,0,0,
        0,0,0,29,112,0,40,54,112,0,112,29,0,0,0,0,0,0,0,29,0,0,40,54,112,0,0,29,0,0,
        0,0,0,0,0,0,0,40,112,25,112,112,0,0,0,0,0,0,0,0,0,0,0,40,112,25,112,112,0,0,
        0,0,0,0,0,0,0,0,0,40,112,112,112,112,0,0,0,0,0,0,0,0,0,0,0,0,40,112,112,0,0,
        0,0,0,0,0,0,0,0,0,0,0,40,25,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,112,0,0,0,0,0,0,0,
        0
    ]

    stars = [0] * 100
    objs  = [Obj(0, 0, (0,0), 0) for i in range(30)]
    keys  = {
        K_LCTRL: False,
        K_LEFT: False,
        K_UP: False,
        K_RIGHT: False,
        K_DOWN: False
    }
    
    fireInterval = 0
    isRun = True

    def __init__(self, display):
        self.x = 100
        self.y = 100
        self.display = display
        display.clear()
        display.swap()
        self.starInit()

    def starInit(self):
        for i, _ in enumerate(Game.stars):
            point = (random.randint(0, self.display.width), random.randint(0, self.display.width))
            v = random.randint(1, 3) * 10
            color = (255, 0, 0)
            Game.stars[i] = (point, v, color)

    def control(self, event):
        self.aircraftControl(event)

    def tick(self, t):
        self.aircraftControl(t)
        self.starControl(t)
        self.objControl(t)

    def check(self, p1, p2, r):
        x1, y1 = p1
        x2, y2 = p2
        if abs(x1 - x2) < r and abs(y1 -y2) < r:
            return True
        else:
            return False
            
    def objControl(self, t):
        self.enemyInit(t)

        for obj in Game.objs:
            if obj.mode == 1:
                x, y = obj.pos
                if y < 0:
                    obj.mode = 0
                obj.pos = (x, int(y - t * 150))
                for o in Game.objs:
                    if o.mode == 2:
                        if self.check(obj.pos, o.pos, 15):
                            o.mode = 0
                            obj.mode = 0
            elif obj.mode == 2:
                x, y = obj.pos
                if y > self.display.height:
                    obj.mode = 0
                obj.pos = (x, int(y + t * 50))
                if self.check(obj.pos, (self.x, self.y), 15):
                    Game.isRun = False
                    

    def enemyInit(self, t):
        if int(random.random() * 30) == 0:
            self.newEnemy()
            

    def starControl(self, t):
        for i, _ in enumerate(self.stars):
            star = self.stars[i]
            point, v, color = star
            x, y = point
            y += t * v

            if y > self.display.height:
                v = random.randint(1, 3) * 10
                x, y = random.randint(0, self.display.width), random.randint(-60, 0)

            self.stars[i] = ((x,y), v, color)
            

    def newObj(self, mode):
        """type == 0 is null obj, type == 1 is fire, type == 2 is Enemy"""
        for obj in Game.objs:
            if obj.mode == 0:
                obj.mode = mode
                return obj
                


    def newFire(self):
        x, y = self.x, self.y
        obj  = self.newObj(1)
        obj.pos = (x,y)


    def newEnemy(self):
        x       = random.randint(0, self.display.width)
        y       = random.randint(-60, -30)
        obj     = self.newObj(2)
        obj.pos = (x,y)
        return obj

    def key(self, event):
        if event.type == KEYDOWN or event.type == KEYUP:
            if event.key not in [K_LCTRL, K_LEFT, K_UP, K_RIGHT, K_DOWN]:
                return
                
        if event.type == KEYDOWN:
            Game.keys[event.key] = True
        elif event.type == KEYUP:
            Game.keys[event.key] = False
        else:
            pass
            
            
    def aircraftControl(self, t):
        x, y = self.x, self.y
        _x, _y = x, y
        
        speed = 5
        if self.keys[K_LEFT]:
            _x = x - speed
            
        if self.keys[K_UP]:
            _y = y - speed
            
        if self.keys[K_RIGHT]:
            _x = x + speed
            
        if self.keys[K_DOWN]:
            _y = y + speed
            
        if self.keys[K_LCTRL]:
            Game.fireInterval += 1
            Game.fireInterval %= 7
            if Game.fireInterval == 0:
                self.newFire()
        else:
            pass

        if (_x > 0 and _x < self.display.width):
            self.x = _x
        if (_y > 0 and _y < self.display.height):
            self.y = _y
            

    def drawMe(self):
        self.display.draw8image((self.x, self.y), Game.aircraft)

    def drawStar(self):
        for star in Game.stars:
            point, v, color = star
            x, y = point
            x, y = int(x), int(y)
            self.display.point((x,y), color)

    def drawFire(self, point):
        x, y = point
        color = (255,255,255)
        for i in range(-6, 6):
            self.display.point((x+3, y+i), color)
            self.display.point((x+2, y+i), color)
            self.display.point((x+12, y+i), color)
            self.display.point((x+13, y+i), color)

    def drawEnemy(self, point):
        self.display.draw8image(point, Game.aircraft, False)

    def drawObjs(self):
        for obj in Game.objs:
            if obj.mode == 1:
                self.drawFire(obj.pos)
            elif obj.mode == 2:
                self.drawEnemy(obj.pos)
            else:
                pass

    def show(self):
        self.display.clear()
        self.drawStar()
        self.drawObjs()
        self.drawMe()
        self.display.swap()

    @classmethod
    def loop(cls):
        display = Display(300, 300)
        game = Game(display)
        clock = pygame.time.Clock()
        while Game.isRun:
            t = clock.tick(30)
            for event in pygame.event.get():
                game.key(event)
                    
            game.tick(1.0 / t)
            game.show()

if __name__ == "__main__":
    Game.loop()
