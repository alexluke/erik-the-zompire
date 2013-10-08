import pygame, os
import resource
import environment
import isogroup
import enemy
import player
import random

class Terrain:
    def __init__(self, level):
        levelName = 'level'+str(level)
        try:
            filename = os.path.join('data', 'sound', levelName+'.ogg')
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play(-1)
        except:
            pass
        
        filename = os.path.join('data', 'levels', levelName + '.txt')
        levelFile = open(filename, 'r')
        lines = levelFile.readlines()
        self.height = len(lines)
        self.width = len(lines[0]) - 1 # for newline
        grass = resource.get_image('grass.jpg')
        height = grass.get_height()
        width = grass.get_width()
        self.background = pygame.Surface((self.width*width, self.height*height))
        self.background.convert()
        self.tileSize = (width, height)
        
        y = 0
        for line in lines:
            x = 0
            for char in line:
                if char == 'g':
                    tile = resource.get_image('grass.jpg')
                elif char == 'p':
                    tile = resource.get_image('path.jpg')
                elif char == 'b':
                    tile = resource.get_image('brown_path.jpg')
                elif char == 's':
                    tile = resource.get_image('sand.jpg')
                elif char == 't':
                    tile = resource.get_image('sand_path.jpg')
                else:
                    x += 1
                    continue
                self.background.blit(tile, (x*width, y*height))
                #pygame.draw.rect(self.background, pygame.Color('red'), pygame.Rect(x*width, y*height, width, height), 1)
                
                #print x*width, y* height
                x += 1
            y += 1
            
        

def groups(worldRect, level, tileSize):
    levelName = 'level'+str(level)
    filename = os.path.join('data', 'levels', levelName + '_o.txt')
    levelFile = open(filename, 'r')
    lines = levelFile.readlines()
    all = isogroup.ISOGroup()
    enviroG = isogroup.ISOGroup()
    playerG = isogroup.ISOGroup()
    enemyG = isogroup.ISOGroup()
    doorG = isogroup.ISOGroup()
    width = tileSize[0]
    height = tileSize[1]
    numLines = len(lines[0]) - 1, len(lines)

    y = 0
    for line in lines:
        x = 0
        for char in line:
            
            if char == 't':
                tmp = environment.Tree((0,0))
                dist = isogroup.distance(tmp.rect.center, tmp.cRect.center)
                spot = x*width+width*random.random(), y*height+height*random.random()-dist
                environment.Tree(spot).add(enviroG)
                spot = x*width+width*random.random(), y*height+height*random.random()-dist
                environment.Tree(spot).add(enviroG)
                spot = x*width+width*random.random(), y*height+height*random.random()-dist
                environment.Tree(spot).add(enviroG)
            if char == 'c':
                tmp = environment.Cactus((0,0))
                dist = isogroup.distance(tmp.rect.center, tmp.cRect.center)
                spot = x*width+width*random.random(), y*height+height*random.random()-dist
                environment.Cactus(spot).add(enviroG)
            elif char == 'l':
                if y == 0:
                    dir = 'n'
                if y == numLines[1] - 1:
                    dir = 's'
                if x == 0:
                    dir = 'w'
                if x == numLines[0] - 1:
                    dir = 'e'
                environment.Door((x*width, y*height),dir).add(enviroG, doorG)
            if char == 'r':
                environment.Rocks((x*width, y*height)).add(enviroG)
            if char == 'h':
                spot = x*width+width*.5, y*height+height*.5
                environment.House(spot).add(enviroG)
            elif char == 'p':
                tmp = player.Player(worldRect,(0,0),level)
                dist = isogroup.distance(tmp.rect.center, tmp.cRect.center)
                spot = x*width+width*random.random(), y*height+height*random.random()-dist
                player.Player(worldRect, spot, level).add(playerG, all)
            elif char == 'd':
                tmp = enemy.Deer(worldRect,(0,0))
                dist = isogroup.distance(tmp.rect.center, tmp.cRect.center)
                spot = x*width+width*random.random(), y*height+height*random.random()-dist
                enemy.Deer(worldRect, spot).add(enemyG, all)
            elif char == 's':
                tmp = enemy.Spider(worldRect,(0,0))
                dist = isogroup.distance(tmp.rect.center, tmp.cRect.center)
                spot = x*width+width*random.random(), y*height+height*random.random()-dist
                enemy.Spider(worldRect, spot).add(enemyG, all)
            elif char == 'f':
                tmp = enemy.Troll(worldRect,(0,0))
                dist = isogroup.distance(tmp.rect.center, tmp.cRect.center)
                spot = x*width+width*random.random(), y*height+height*random.random()-dist
                enemy.Troll(worldRect, spot).add(enemyG, all)
            elif char == 'u':
                tmp = enemy.Skeleton(worldRect,(0,0))
                dist = isogroup.distance(tmp.rect.center, tmp.cRect.center)
                spot = x*width+width*random.random(), y*height+height*random.random()-dist
                enemy.Skeleton(worldRect, spot).add(enemyG, all)
            elif char == 'b':
                tmp = enemy.Professor(worldRect,(0,0))
                dist = isogroup.distance(tmp.rect.center, tmp.cRect.center)
                spot = x*width+width*random.random(), y*height+height*random.random()-dist
                enemy.Professor(worldRect, spot).add(enemyG, all)
            elif char == 'z':
                tmp = enemy.Zombie(worldRect,(0,0))
                dist = isogroup.distance(tmp.rect.center, tmp.cRect.center)
                spot = x*width+width*random.random(), y*height+height*random.random()-dist
                enemy.Zombie(worldRect, spot).add(enemyG, all)
            x += 1
        y += 1
        
    return all, playerG, enviroG, enemyG, doorG