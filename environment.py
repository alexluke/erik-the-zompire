import pygame, os
import resource

class Tree(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        filename = os.path.join('environment', 'fir.bmp')
        self.image = resource.get_image(filename, -1)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.cRect = self.rect.inflate(-110,-110)
        self.cRect.move_ip(0,45)
        
class Cactus(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        filename = os.path.join('environment', 'cactus.bmp')
        self.image = resource.get_image(filename, -1)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.cRect = self.rect.inflate(-110,-110)
        self.cRect.move_ip(-10,35)
        
class Rocks(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        filename = os.path.join('environment', 'rocks.bmp')
        self.image = resource.get_image(filename)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.cRect = self.rect
        
class House(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        filename = os.path.join('environment', 'house.bmp')
        self.image = resource.get_image(filename, -1)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.cRect = self.rect.inflate(-50,-70)
        self.cRect.move_ip(5,20)
        
class Door(pygame.sprite.Sprite):
    def __init__(self, position, orientation):
        pygame.sprite.Sprite.__init__(self)
        filename = os.path.join('environment', 'door '+orientation+'.bmp')
        self.image = resource.get_image(filename, pygame.Color('magenta'))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        
        
        if orientation == 'n':
            self.cRect = self.rect.inflate(0,-77)
            self.cRect.move_ip(0,-39)
        if orientation == 's':
            self.cRect = self.rect.inflate(0,-77)
            self.cRect.move_ip(0,39)
        if orientation == 'e':
            self.cRect = self.rect.inflate(-77,0)
            self.cRect.move_ip(39,0)
        if orientation == 'w':
            self.cRect = self.rect.inflate(-77,0)
            self.cRect.move_ip(-39,0)
        