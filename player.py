import pygame, os
import resource
import character
import random
import isogroup

class Player(character.Character):
    def __init__(self, worldRect, position, level):
        character.Character.__init__(self, 'zombie', worldRect, position)
        self.niceName = 'Erik'
        self.level = level
        self.xp = 0
        self.maxBlood = 100*level
        self.maxBrains = 100
        self.blood = self.maxBlood
        self.brains = self.maxBrains
        self.bloodtick = 30
        self.braintick = 100
        self.walkspeed = 2 #pixels per second
        self.runspeed = 200 #pixels per second
        self.dir = 'e'
        self.atk = 10*level
        self.atkRange = 10
        self.idle = 'looking'
        self.oldpos = self.rect.center
        self.actionDelay = 2 #seconds
        
        #set collision rect
        self.cRect = self.rect.inflate(-80,-80)
        self.cRect.move_ip(0,25)
        
        self.cOldpos = self.cRect.center
        
        self.attackRect = pygame.Rect(self.rect.topleft, (60,40))
        self.attackRect.move_ip(45, 20)
        
        self.hitRect = self.rect.inflate(-40,-40)

    def talk(self):
        if self.name == 'zombie':
            self.action = 'talking'
            self.frame = 0
            
    def attack(self, enemy, osd):
        health = character.Character.attack(self, enemy, osd)
        if health is not None and health <= 0:
            self.xp += 100

    def morph(self):
        self.rect.move_ip((-16, -16))
        self.name = 'bat'
        self.action = 'stopped'
        self.frame = 0
        
    def getHit(self, attack):
        self.blood -= attack
        self.wounded()

    def bite(self, enemy):
        if self.name == 'zombie' and self.action == 'looking':
            self.action = 'biting'
            self.frame = 0
            victim = isogroup.findVictim(self, enemy)
            if victim:
                if victim.hasBrains:
                    self.brains = self.maxBrains
                if victim.eatable:
                    self.blood += 20*self.level
                    if self.blood > self.maxBlood:
                        self.blood = self.maxBlood
                    victim.eatable = 0

    def update(self, *args):
        time = args[0]
        osd = args[1]
        
        if self.alive:
            if self.action == 'walking' or self.action == 'running':
                if self.action == 'walking':
                    speed = self.walkspeed
                else:
                    speed = self.runspeed
                speed *= time
                self.oldpos = self.rect.center
                self.cOldpos = self.cRect.center
                if self.dir == 'n':
                    moved = (0, -speed)
                    self.attackRect = pygame.Rect(0,0,40,60)
                    self.attackRect.center = self.rect.center
                    self.attackRect.move_ip(0, -20)
                elif self.dir == 's':
                    moved = (0, speed)
                    self.attackRect = pygame.Rect(0,0,40,40)
                    self.attackRect.center = self.rect.center
                    self.attackRect.move_ip(0, 20)
                elif self.dir == 'e':
                    moved = (speed, 0)
                    self.attackRect = pygame.Rect(self.rect.topleft, (60,40))
                    self.attackRect.move_ip(45, 20)
                elif self.dir == 'w':
                    moved = (-speed, 0)
                    self.attackRect = pygame.Rect(self.rect.topleft, (60,40))
                    self.attackRect.move_ip(-8, 20)
                    
                newspot = self.cRect.move(moved)

                if self.worldRect.contains(newspot):
                    self.rect.move_ip(moved)
                    self.cRect.move_ip(moved)
                    self.attackRect.move_ip(moved)
                    self.hitRect = self.rect.inflate(-40,-40)
            
            if self.blood <= 0 or self.brains <= 0:
                self.die()
                
            if self.xp >= 1000:
                self.level += 1
                osd.addMessage('Erik is now level '+str(self.level)+'. It\'s time to leave this area.')
                self.xp = 0
                
        character.Character.update(self, *args)
