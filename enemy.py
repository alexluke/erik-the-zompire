import pygame, os
import character
import random

class Deer(character.NPC):
    def __init__(self, worldRect, position):
        character.NPC.__init__(self, 'deer', worldRect, position, 70, 2)
        self.niceName = 'Deer'
        self.health = 20
        #set collision rect
        self.cRect = self.rect.inflate(-60,-60)
        self.hitRect = self.cRect
        self.attackRect = self.cRect.move(30,0)
        self.idle = 'eating'
        self.atk = 5
        self.atkRange = 5
        self.aggro = 100
        
    def getCRectSize():
        return 36,36
                
    def update(self, *args):
        character.NPC.update(self, *args)
        if self.dir == 'w':
            self.attackRect = self.cRect.move(-30,0)
        if self.dir == 'e':
            self.attackRect = self.cRect.move(30,0)
        if self.dir == 'n':
            self.attackRect = self.cRect.move(0,-20)
        if self.dir == 's':
            self.attackRect = self.cRect.move(0,20)
        if self.dir == 'ne':
            self.attackRect = self.cRect.move(20,-20)
        if self.dir == 'nw':
            self.attackRect = self.cRect.move(-20,-20)
        if self.dir == 'sw':
            self.attackRect = self.cRect.move(-20,20)
        if self.dir == 'se':
            self.attackRect = self.cRect.move(20,20)
        
        
class Spider(character.NPC):
    def __init__(self, worldRect, position):
        character.NPC.__init__(self, 'spider', worldRect, position, 130, 1)
        self.niceName = 'Spider'
        self.health = 20
        #set collision rect
        self.cRect = self.rect.inflate(-60,-60)
        self.hitRect = self.cRect
        self.atk = 4
        self.atkRange = 4
        self.aggro = 300
        
    def update(self, *args):
        character.NPC.update(self, *args)
        if self.dir == 'w':
            self.attackRect = self.cRect.move(-10,0)
        if self.dir == 'e':
            self.attackRect = self.cRect.move(10,0)
        if self.dir == 'n':
            self.attackRect = self.cRect.move(0,-10)
        if self.dir == 's':
            self.attackRect = self.cRect.move(0,10)
        if self.dir == 'ne':
            self.attackRect = self.cRect.move(10,-10)
        if self.dir == 'nw':
            self.attackRect = self.cRect.move(-10,-10)
        if self.dir == 'sw':
            self.attackRect = self.cRect.move(-10,10)
        if self.dir == 'se':
            self.attackRect = self.cRect.move(10,10)
            
class Troll(character.NPC):
    def __init__(self, worldRect, position):
        character.NPC.__init__(self, 'troll', worldRect, position, 130, 4)
        self.niceName = 'Troll'
        self.health = 60
        #set collision rect
        self.cRect = self.rect.inflate(-60,-60)
        self.hitRect = self.cRect
        self.atk = 12
        self.atkRange = 5
        self.aggro = 250
        
    def update(self, *args):
        character.NPC.update(self, *args)
        if self.dir == 'w':
            self.attackRect = self.cRect.move(-10,0)
        if self.dir == 'e':
            self.attackRect = self.cRect.move(10,0)
        if self.dir == 'n':
            self.attackRect = self.cRect.move(0,-10)
        if self.dir == 's':
            self.attackRect = self.cRect.move(0,10)
        if self.dir == 'ne':
            self.attackRect = self.cRect.move(10,-10)
        if self.dir == 'nw':
            self.attackRect = self.cRect.move(-10,-10)
        if self.dir == 'sw':
            self.attackRect = self.cRect.move(-10,10)
        if self.dir == 'se':
            self.attackRect = self.cRect.move(10,10)
            
class Skeleton(character.NPC):
    def __init__(self, worldRect, position):
        character.NPC.__init__(self, 'skeleton', worldRect, position, 100, 1)
        self.niceName = 'Skeleton'
        self.health = 60
        #set collision rect
        self.cRect = self.rect.inflate(-60,-60)
        self.hitRect = self.cRect
        self.atk = 30
        self.atkRange = 5
        self.aggro = 350
        
    def update(self, *args):
        character.NPC.update(self, *args)
        if self.dir == 'w':
            self.attackRect = self.cRect.move(-10,0)
        if self.dir == 'e':
            self.attackRect = self.cRect.move(10,0)
        if self.dir == 'n':
            self.attackRect = self.cRect.move(0,-10)
        if self.dir == 's':
            self.attackRect = self.cRect.move(0,10)
        if self.dir == 'ne':
            self.attackRect = self.cRect.move(10,-10)
        if self.dir == 'nw':
            self.attackRect = self.cRect.move(-10,-10)
        if self.dir == 'sw':
            self.attackRect = self.cRect.move(-10,10)
        if self.dir == 'se':
            self.attackRect = self.cRect.move(10,10)
            
class Professor(character.NPC):
    def __init__(self, worldRect, position):
        character.NPC.__init__(self, 'professor', worldRect, position, 80, 1)
        self.niceName = 'Professor'
        self.health = 60
        #set collision rect
        self.cRect = self.rect.inflate(-60,-60)
        self.hitRect = self.cRect
        self.atk = 30
        self.atkRange = 5
        self.aggro = 100
        self.hasBrains = 1
        self.idle = 'experimenting'
        
    def update(self, *args):
        character.NPC.update(self, *args)
        if self.dir == 'w':
            self.attackRect = self.cRect.move(-10,0)
        if self.dir == 'e':
            self.attackRect = self.cRect.move(10,0)
        if self.dir == 'n':
            self.attackRect = self.cRect.move(0,-10)
        if self.dir == 's':
            self.attackRect = self.cRect.move(0,10)
        if self.dir == 'ne':
            self.attackRect = self.cRect.move(10,-10)
        if self.dir == 'nw':
            self.attackRect = self.cRect.move(-10,-10)
        if self.dir == 'sw':
            self.attackRect = self.cRect.move(-10,10)
        if self.dir == 'se':
            self.attackRect = self.cRect.move(10,10)
            
class Zombie(character.NPC):
    def __init__(self, worldRect, position):
        kind = random.choice(('red', 'green'))
        name = ' '.join((kind, 'zombie'))
        character.NPC.__init__(self, name, worldRect, position, 100, 2)
        self.niceName = 'Zombie'
        self.health = 110
        #set collision rect
        self.cRect = self.rect.inflate(-60,-60)
        self.hitRect = self.cRect
        self.atk = 30
        self.atkRange = 5
        self.aggro = 300
        
    def update(self, *args):
        character.NPC.update(self, *args)
        if self.dir == 'w':
            self.attackRect = self.cRect.move(-10,0)
        if self.dir == 'e':
            self.attackRect = self.cRect.move(10,0)
        if self.dir == 'n':
            self.attackRect = self.cRect.move(0,-10)
        if self.dir == 's':
            self.attackRect = self.cRect.move(0,10)
        if self.dir == 'ne':
            self.attackRect = self.cRect.move(10,-10)
        if self.dir == 'nw':
            self.attackRect = self.cRect.move(-10,-10)
        if self.dir == 'sw':
            self.attackRect = self.cRect.move(-10,10)
        if self.dir == 'se':
            self.attackRect = self.cRect.move(10,10)
