import pygame, os

class OSD:
    def __init__(self, screensize):
        self.osd = pygame.Surface(screensize)
        key = pygame.Color('magenta')
        self.osd.fill(key)
        self.osd.set_colorkey(key)
        self.bloodbar = pygame.Surface((100,20))
        self.brainbar = pygame.Surface((100,20))
        self.messageBox = pygame.Surface((300,100))
        self.fpsFont = pygame.font.Font(None, 36)
        self.messageFont = pygame.font.Font(None, 20)
        self.list = []
        self.listLen = 6
        
    def update(self, player, fps):
        self.bloodbar.fill((0,0,0))
        self.brainbar.fill((0,0,0))
        self.bloodbar.fill((255,0,0), pygame.Rect(0,0,int(float(player.blood)/player.maxBlood*100),20))
        self.brainbar.fill((0,0,255), pygame.Rect(0,0,int(float(player.brains)/player.maxBrains*100),20))
        self.osd.blit(self.bloodbar, (20,520))
        self.osd.blit(self.brainbar, (20,550))
        text = self.fpsFont.render(str(int(fps)), 1, (255,0,0), (0,0,0))
        self.osd.blit(text, (20,20))
        
        self.messageBox.fill((0,0,0))
        y = 0
        for message in self.list:
            text = self.messageFont.render(message, 1, (255,0,0), (0,0,0))
            self.messageBox.blit(text, (0,y))
            y += self.messageFont.get_linesize()
        self.osd.blit(self.messageBox, (490, 490))
        
    def addMessage(self, message):
        if len(self.list) == self.listLen:
            self.list.pop(0)
        
        if (len(self.list) == 0 or message != self.list[len(self.list) - 1]) and message is not '':
            self.list.append(message)