import pygame, os, sys
from pygame.locals import *
import resource
import player
from player import Player
import terrain
import isogroup
import character
import environment
import random
import types
from osd import OSD

def main():
    debug = 0
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        debug = 1
        
    pygame.init()
    screenSize = 800,600
    maxfps = 60
    screen = pygame.display.set_mode(screenSize)
    curLevel = 0
    maxLevel = 4
    brains = 100
    
    running = 1
    while running:
        if curLevel == 0:
            brains = 100
            menu = runMenu(screen)
            if menu == 0:
                curLevel = 1
            elif menu == 1:
                if help(screen) == -1:
                    break
            elif menu == 2:
                break
        else:
            if printStory(curLevel, screen) == -1:
                break
            if curLevel > maxLevel:
                curLevel = 0
                continue
            oldbrains = brains
            curLevel, brains = runLevel(curLevel, brains, screen, maxfps, debug)
            if brains == 0:
                answer = retry(screen)
                brains = oldbrains
                if not answer:
                    curLevel = 0
        
        if curLevel == -1:
            break
    pygame.quit()
    
def runMenu(screen):
    filename = os.path.join('data', 'sound', 'menu.ogg')
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(-1)
    screenSize = screen.get_size()
    selected = 0
    font = pygame.font.Font(None, 48)
    smallfont = pygame.font.Font(None, 20)
    bigfont = pygame.font.Font(None, 100)
    options = ("Play", "Help", "Quit")
    other = ("Alex Luke", "CSCI 321", "Instructor: Matthews", "Winter 2007")
    loc = {}
    spacing = font.get_linesize()*1.5
    
    menu = pygame.Surface(screenSize)
    data = pygame.Surface((150,70))
    title = bigfont.render("Erik the Zompire", 1, (0,255,0), (0,0,0))
    
    x = 0
    y = 300
    for opt in options:
        text = font.render(opt, 1, (255,0,0), (0,0,0))
        textWidth = text.get_width()
        loc[x] = screenSize[0]/2-textWidth/2 - 30
        menu.blit(text, (screenSize[0]/2-textWidth/2,y))
        x += 1
        y += spacing
    
    y = 0
    for o in other:
        text = smallfont.render(o, 1, (0,120,255), (0,0,0))
        data.blit(text, (0,y))
        y += smallfont.get_linesize()
    
    cGroup = pygame.sprite.Group()
        
    cursor = pygame.sprite.Sprite(cGroup)
    cursor.image = resource.get_image('cursor.bmp')
    cursor.rect = cursor.image.get_rect()
    cursor.rect.center = (20,20)
    y = 297
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return 2
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return 2
            elif event.type == KEYDOWN and event.key == K_DOWN:
                selected += 1
            elif event.type == KEYDOWN and event.key == K_UP:
                selected -= 1
            elif event.type == KEYDOWN and event.key == K_RETURN:
                return selected
                
        if selected >= len(options):
            selected = len(options) - 1
        elif selected < 0:
            selected = 0
                
        cursor.rect.topleft = (loc[selected], selected*spacing+y+.25*spacing)
        
        
        screen.blit(menu, (0,0))
        screen.blit(title, (screenSize[0]/2-title.get_width()/2,20))
        screen.blit(data, (650,520))
        cGroup.draw(screen)
        pygame.display.flip()    
    
    
def printStory(curLevel, screen):
    filename = os.path.join('data', 'sound', 'story.ogg')
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(-1)
    
    current = 0
    font = pygame.font.Font(None, 48)
    color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
    screenSize = screen.get_size()
    
    filename = os.path.join('data', 'story', 'level'+str(curLevel)+'.txt')
    file = open(filename, 'r')
    lines = file.readlines()
    total = len(lines)
    
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return -1
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN:
                current += 1
                color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
                
        if current >= total:
            return
        screen.fill((0,0,0))
        y = 0
        text = font.render(lines[current].strip(), 1, (255,0,0), (0,0,0))
        textWidth = text.get_width()
        screen.blit(text, (screenSize[0]/2-textWidth/2,screenSize[1]/2 - font.get_linesize()/2))
        pygame.display.flip()
        
def help(screen):
    current = 0
    font = pygame.font.Font(None, 48)
    color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
    screenSize = screen.get_size()
    image = resource.get_image('help.jpg')
    screen.blit(image, (0,0))
    pygame.display.flip()
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return -1
            elif event.type == KEYDOWN:
                return
            
def retry(screen):
    filename = os.path.join('data', 'sound', 'menu.ogg')
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(-1)
    screenSize = screen.get_size()
    selected = 0
    font = pygame.font.Font(None, 48)
    bigfont = pygame.font.Font(None, 100)
    options = ("Yes", "No")
    loc = {}
    spacing = font.get_linesize()*1.5
    
    menu = pygame.Surface(screenSize)
    data = pygame.Surface((150,70))
    title = bigfont.render("Retry?", 1, (0,255,0), (0,0,0))
    
    x = 0
    y = 300
    for opt in options:
        text = font.render(opt, 1, (255,0,0), (0,0,0))
        textWidth = text.get_width()
        loc[x] = screenSize[0]/2-textWidth/2 - 30
        menu.blit(text, (screenSize[0]/2-textWidth/2,y))
        x += 1
        y += spacing
    
    cGroup = pygame.sprite.Group()
        
    cursor = pygame.sprite.Sprite(cGroup)
    cursor.image = resource.get_image('cursor.bmp')
    cursor.rect = cursor.image.get_rect()
    cursor.rect.center = (20,20)
    y = 297
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return 2
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return 2
            elif event.type == KEYDOWN and event.key == K_DOWN:
                selected += 1
            elif event.type == KEYDOWN and event.key == K_UP:
                selected -= 1
            elif event.type == KEYDOWN and event.key == K_RETURN:
                return not selected
                
        if selected >= len(options):
            selected = len(options) - 1
        elif selected < 0:
            selected = 0
                
        cursor.rect.topleft = (loc[selected], selected*spacing+y+.25*spacing)
        
        screen.blit(menu, (0,0))
        screen.blit(title, (screenSize[0]/2-title.get_width()/2,20))
        cGroup.draw(screen)
        pygame.display.flip()   
        
def runLevel(curLevel, brains, screen, maxfps, debug):
    screenSize = screen.get_size()
    
    #for darkening the screen
    darken=pygame.Surface(screen.get_size())
    darken.fill((20, 20, 30))
    darken.set_alpha(100)
    
    dark = 1
    
    #ids for timers
    bloodtimer = pygame.USEREVENT+1
    braintimer = bloodtimer + 1
    clock = pygame.time.Clock()
        
    level = terrain.Terrain(curLevel)
    world = pygame.Surface(level.background.get_size())
    osd = OSD(screenSize)

    screen.blit(level.background, (0, 0))
    pygame.display.flip()

    all, playerGroup, enviro, enemy, doors = terrain.groups(world.get_rect(), curLevel, level.tileSize)
    #enviro.draw(level.background)
    notPlayer = isogroup.ISOGroup()
    notPlayer.add(enviro, enemy)
    watchRect = pygame.rect.Rect((0,0), screenSize)
    player = playerGroup.sprites()[0]
    all.add(enviro)
    player.brains = brains

    onscreen = isogroup.ISOGroup()
    onscreenEnemy = isogroup.ISOGroup()
    
    pygame.time.set_timer(bloodtimer, player.bloodtick*maxfps)
    pygame.time.set_timer(braintimer, player.braintick*maxfps)
    
    while 1:
        clock.tick(maxfps)

        for event in pygame.event.get():
            if event.type == QUIT:
                return -1, player.brains
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return 0, player.brains
            elif event.type == KEYDOWN and event.key == K_q:
                return 0,player.brains
            elif event.type == KEYDOWN and event.key == K_F1:
                help(screen)
            elif event.type == KEYDOWN and event.key == K_UP:
                player.run('n')
            elif event.type == KEYDOWN and event.key == K_DOWN:
                player.run('s')
            elif event.type == KEYDOWN and event.key == K_LEFT:
                player.run('w')
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                player.run('e')
            elif event.type == KEYDOWN and event.key == K_LCTRL:
                player.attack(enemy, osd)
            elif event.type == KEYDOWN and event.key == K_a:
                player.wounded()
            elif event.type == KEYDOWN and event.key == K_s:
                player.talk()
            elif event.type == KEYDOWN and event.key == K_d:
                enemy.sprites()[0].health = 0
            elif event.type == KEYDOWN and event.key == K_f:
                player.bite(enemy)
            elif event.type == KEYDOWN and event.key == K_LALT:
                player.morph()
            elif event.type == KEYDOWN and event.key == K_t:
                dark = not dark
            elif event.type == KEYDOWN and event.key == K_p:
                return curLevel+1, player.brains
            elif event.type == KEYUP:
                if player.action == 'walking' or player.action == 'running':
                    player.stop()
            elif event.type == bloodtimer:
                player.blood -= 1
            elif event.type == braintimer:
                player.brains -= 1

        
        onscreen.empty()
        onscreenEnemy.empty()
        for s in all.sprites():
            if s.rect.colliderect(watchRect):
                if s in enemy:
                    onscreenEnemy.add(s)
                onscreen.add(s)
                
        #print clock.get_time()/1000.0
        onscreen.update(clock.get_time()/1000.0, osd, player)

        if isogroup.spritecollideany(player, doors):
            if player.level > curLevel:
                #warp level
                return curLevel + 1, player.brains
            else:
                osd.addMessage('You are not yet powerful enough to go there.')

        if isogroup.spritecollideany(player, notPlayer):
            player.collide()
            
        for s in onscreenEnemy:
            if isogroup.spritecollideany(s, enviro) or isogroup.spritecollideany(s, playerGroup):
                s.collide()
                
        osd.update(player, clock.get_fps())
        watchRect.center = player.rect.center
        sRect = world.get_rect()
        if not sRect.contains(watchRect):
            watchRect.clamp_ip(sRect)
        
        world.blit(level.background, watchRect, watchRect)
        
        onscreen.draw(world)
        if debug:
            for thing in onscreen:
                pygame.draw.rect(world, pygame.Color('red'), thing.cRect, 1)
                pygame.draw.rect(world, pygame.Color('blue'), thing.rect, 1)
                if hasattr(thing, "attackRect"):
                    pygame.draw.rect(world, pygame.Color('green'), thing.attackRect, 1)
                if hasattr(thing, "hitRect"):
                    pygame.draw.rect(world, pygame.Color('purple'), thing.hitRect, 1)
                if hasattr(thing, "velocity"):
                    pygame.draw.line(world, (50,75,222), thing.rect.center, thing.rect.center+(thing.velocity*30), 2)
                if hasattr(thing, "wanderpoint"):
                    pygame.draw.circle(world, (120,3,85), (int(thing.wanderpoint[0]), int(thing.wanderpoint[1])), 50)
            
        screen.fill((0,0,0))
        screen.blit(world, (0, 0), watchRect)
        if (dark):
            screen.blit(darken, (0, 0))
        screen.blit(osd.osd, (0, 0))
        pygame.display.flip()
        
        if not player.alive:
            return curLevel, 0

    

if __name__ == '__main__': 
    #psyco.profile()
    main()
