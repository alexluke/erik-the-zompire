import pygame, os
import resource
import random
import isogroup
import numpy
from vectors import *

class Character(pygame.sprite.Sprite):
    def __init__(self, name, worldRect, position):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.action = 'stopped'
        self.idle = 'stopped'
        self.dir = random.choice(('n','ne','e','se','s','sw','w','nw'))
        self.worldRect = worldRect
        self.images = resource.get_action(self.name, self.action, self.dir)
        self.nframes = len(self.images)
        self.rect = self.images[0].get_rect()
        self.rect.center = position
        self.frame = 0 #random.randint(0,self.nframes)
        self.image = self.images[self.frame]
        self.fspeed = 8
        self.alive = 1
        self.animated = 1
        self.deadtime = 5 #seconds
        self.cRect = self.rect
        self.attackRect = self.rect
        self.health = 100
        self.eatable = 0
        self.actionCounter = 0.0
        self.actionDelay = 2 #seconds
        self.hasBrains = 0
        
    def walk(self, direction):
        self.dir = direction
        self.action = 'walking'
        
    def run(self, direction):
        self.dir = direction
        self.action = 'running'

    def attack(self, enemy, osd):
        if self.actionCounter <= 0:
            self.actionCounter = self.actionDelay
            self.action = 'attack'
            self.frame = 0
            victim = isogroup.findVictim(self, enemy)
            if victim and victim.alive:
                sound = random.choice(resource.get_action_sound(self.name, 'hit'))
                sound.play()
                hit = random.randint(self.atk-self.atkRange, self.atk)
                if victim.getHit(hit):
                    msg = self.niceName+' has slain '+victim.niceName+'!'
                else:
                    msg = self.niceName+' hits '+victim.niceName+' for '+str(hit)+' damage.'
                osd.addMessage(msg)
                return victim.health
                
    def getHit(self, attack):
        self.health -= attack
        self.wounded()
        if self.health <= 0:
            return 1
        else:
            return 0

    def wounded(self):
        self.action = 'been hit'
        self.frame = 0

    def stop(self):
        self.action = self.idle

    def die(self):
        self.action = 'tipping over'
        self.frame = 0
        self.alive = 0
        self.deadtime
        self.eatable = 1
        
    def collide(self):
        self.rect.center = self.oldpos
        self.cRect.center = self.cOldpos
        
    def update(self, *args):
        time = args[0]
        osd = args[1]
        
        if not self.alive and self.frame+self.fspeed*time >= self.nframes:
            self.animated = 0
        if not self.alive:
            self.deadtime -= time
            if self.deadtime <= 0 and not self.animated:
                self.kill()
                
        self.actionCounter -= time        
        if self.animated:
            oldrect = self.rect
            self.frame += self.fspeed * time
            try:
                self.images = resource.get_action(self.name, self.action, self.dir)
            except:
                pass
            self.nframes = len(self.images)
            self.rect = self.images[0].get_rect()
            self.rect.center = oldrect.center
            self.nframes = len(self.images)
            
            if self.action != 'walking' and self.action != 'running':
                if self.frame + self.fspeed*time >= self.nframes:
                    self.stop()
            
            while self.frame >= self.nframes:
                self.frame -= self.nframes
            self.image = self.images[int(self.frame)]
            
        if self.health <= 0 and self.alive:
            self.die()
        

class NPC(Character):
    def __init__(self, name, worldRect, position, speed, mass):
        Character.__init__(self, name, worldRect, position)
        self.rect.center = vector(position)
        self.maxspeed = speed
        self.velocity = vector(0, 0)
        self.force = vector(0, 0)
        self.heading = vector(0.0, 0.0)
        self.mass = mass
        self.wanderpoint = normalize(vector(random.random(), random.random()))
        self.ai = 'wait'
        self.target = None
        self.oldpos = self.rect.center
        self.cOldpos = self.cRect.center
        self.aiTime = 0.0
        
    def wander(self):
        self.ai = 'wander'
        self.action = 'walking'
    
    def die(self):
        Character.die(self)
        self.force = vector(0,0)
        self.velocity = vector(0,0)
        self.cRect = pygame.Rect(0,0,0,0)

    def collide(self):
        Character.collide(self)
        self.force = -self.force
        self.heading = -self.heading
        
    def newAction(self):
        action = random.randint(0,2)
        if self.target is not None:
            action = 9
        if action == 0: #idle
            self.ai = 'wait'
            self.action = self.idle
            self.aiTime = float(random.randint(0, 10))
        elif action == 1: #wander
            self.ai = 'wander'
            self.action = 'walking'
            self.aiTime = float(random.randint(0, 10))
        elif action == 9: #attack
            self.ai = 'attack'
            #self.target = target
            self.aiTime = -1
        
    def update(self, *args):
        time,osd,player = args
        
        #print self.aiTime
        #print self.force
        
        if self.alive:   
            if isogroup.distance(self.rect.center, player.rect.center) < self.aggro:
                self.target = player

            if self.aiTime <= 0 and self.aiTime != -1:
                self.newAction()
            
            if self.aiTime != -1:
                self.aiTime -= time
            
            if self.ai == 'wait':
                self.force = vector(0,0)
                self.velocity = vector(0,0)
            elif self.ai == 'wander':
                self.wanderpoint += (1000*(random.random()-0.5), \
                    1000*(random.random()-0.5))
                self.wanderpoint = 500*normalize(self.wanderpoint)
                self.wanderpoint += 500*self.heading
                self.force = self.wanderpoint
            elif self.ai == 'attack':
                if self.attackRect.colliderect(self.target.hitRect):
                    Character.attack(self, self.target, osd)
                else:
                    self.ai = 'seek'
                    self.aiTime = -1
                    self.action = 'walking'
            elif self.ai == 'seek':
                if self.attackRect.colliderect(self.target.hitRect):
                    self.action = self.idle
                    self.ai = 'attack'
                else:
                    desired_velocity = self.maxspeed * normalize(vector(self.target.rect.center) - self.rect.center)
                    self.force = desired_velocity - self.velocity
        
        if (self.action == 'walking' or self.action == 'running') and self.target is None:
            walld = 128
            screenw, screenh = self.worldRect.width, self.worldRect.height
            leftd = self.rect.left
            rightd = screenw - self.rect.right
            topd = self.rect.top
            bottomd = screenh - self.rect.bottom
            mind = min(leftd, rightd, topd, bottomd)
            # Add forces away from close walls
            if mind < walld:
                if leftd == mind:
                    self.force += vector(walld-leftd,0)
                if rightd == mind:
                    self.force += vector(-walld+rightd,0)
                if topd == mind:
                    self.force += vector(0,walld-topd)
                if bottomd == mind:
                    self.force += vector(0,-walld+bottomd)
        
        self.velocity = self.velocity + self.force/self.mass
        speed = vlen(self.velocity)
        if speed > 0.001:
            self.heading = normalize(self.velocity)
        if speed > self.maxspeed:
            self.velocity = self.maxspeed*self.heading
            
        self.oldpos = self.rect.center
        self.cOldpos = self.cRect.center
        self.rect.center += self.velocity * time
        self.cRect.center += self.velocity * time
        
        if speed >= 0.1 or self.target is not None:
            small = .382
            big = 0.923
            x,y = self.heading
            if y >= big:
                self.dir = 's'
            elif small <= y:
                if x > 0:
                    self.dir = 'se'
                else:
                    self.dir = 'sw'
            elif -small <= y:
                if x > 0:
                    self.dir = 'e'
                else:
                    self.dir = 'w'
            elif -big <= y:
                if x > 0:
                    self.dir = 'ne'
                else:
                    self.dir = 'nw'
            else:
                self.dir = 'n'
                
        Character.update(self, time, osd)

    

