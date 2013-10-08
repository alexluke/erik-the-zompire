import pygame
import math

class ISOGroup(pygame.sprite.Group):
    def compare(self, a, b):
        if a.cRect.bottom < b.cRect.bottom:
            return -1
        elif a.cRect.bottom > b.cRect.bottom:
            return 1
        else:
            return 0
        
    def draw(self, surface):
        sprites = self.sprites()
        sprites.sort(self.compare)
        surface_blit = surface.blit
        for spr in sprites:
            self.spritedict[spr] = surface_blit(spr.image, spr.rect)
        self.lostsprites = []
        
def spritecollideany(sprite, group):
    spritecollide = sprite.cRect.colliderect
    for s in group:
        if spritecollide(s.cRect):
            return s
    return None

def findVictim(sprite, group):
    spritecollide = sprite.attackRect.colliderect
    if isinstance(group, ISOGroup):
        for s in group:
            if spritecollide(s.hitRect):
                return s
    else:
        return group
    return None

def distance(first, second):
    xd = abs(first[0]-second[0])
    yd = abs(first[1]-second[1])
    dist = math.sqrt(xd*xd + yd*yd)
        
    return dist
