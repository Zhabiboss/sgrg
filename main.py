import pygame
import sys
import random
import json

with open("UserData/scores.json", "r") as score:
    scores = json.load(score)

pygame.init()

res = width, height = 1080, 820
screen = pygame.display.set_mode(res)
clock = pygame.time.Clock()
fps = 60
font = pygame.font.Font("freesansbold.ttf", 16)
scorefont = pygame.font.Font("freesansbold.ttf", 32)
lastgamescore = None
tile = 60
splashes = []
with open("Resources/splashes.txt", "r") as s:
    splashes = s.readlines()
pygame.display.set_caption(f"Super Great Rythm Game ({random.choice(splashes)})")
icon = pygame.image.load("Resources/icon.png")
pygame.display.set_icon(icon)
pygame.mouse.set_visible(False)
cursor = pygame.image.load("Resources/cursor.png")

class Node:
    def __init__(self, x, y, duration):
        self.x, self.y = x, y
        self.duration = duration
        self.lifespan = 0
        self.active = True
        self.indicator = pygame.image.load("Resources/indicator.png")
        #self.indicator = pygame.transform.scale(self.indicator, (60, 70))
        self.originalindicator = pygame.image.load("Resources/indicator.png")
        #self.originalindicator = pygame.transform.scale(self.originalindicator, (60, 70))
        self.angleincr = 360 / self.duration
        self.currentincr = -self.angleincr + 1
        self.passed = []

    def update(self):
        if self.active:
            self.lifespan += 1
            if self.lifespan >= self.duration:
                self.active = False

    def clickevent(self):
        if pygame.Rect(self.x - tile // 2, self.y - tile // 2, tile, tile).collidepoint(*pygame.mouse.get_pos()):
            self.active = False

    def draw(self):
        if self.active:
            if self.lifespan > 1 and self.lifespan <= 4:
                pygame.draw.circle(screen, (10, 10, 10), (self.x, self.y), tile // 2)
            if self.lifespan > 4 and self.lifespan <= 8:
                pygame.draw.circle(screen, (20, 20, 20), (self.x, self.y), tile // 2)
            if self.lifespan > 8 and self.lifespan <= 12:
                pygame.draw.circle(screen, (50, 50, 50), (self.x, self.y), tile // 2)
            if self.lifespan > 12 and self.lifespan <= 16:
                pygame.draw.circle(screen, (100, 100, 100), (self.x, self.y), tile // 2)
            if self.lifespan > 16 and self.lifespan <= 20:
                pygame.draw.circle(screen, (200, 200, 200), (self.x, self.y), tile // 2)
            if self.lifespan > 20:
                pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), tile // 2)
            #text = font.render(str(self.duration - self.lifespan), True, "black")
            #screen.blit(text, (self.x - text.get_rect().width // 2, self.y - text.get_rect().height // 2))

            #self.indicator = pygame.transform.rotate(self.indicator, self.angleincr)
            #rot_img = pygame.transform.rotate(self.indicator, self.angleincr)
            #new_rect = rot_img.get_rect(center = self.indicator.get_rect(x = self.x - tile // 2, y = self.y - tile // 2).center)
            #screen.blit(rot_img, new_rect)
            
            rotated_img, rect = self.blitRotateCenter(self.indicator, (self.x - tile // 2 - 7, self.y - tile // 2 - 7), -self.currentincr)
            self.passed.append((rotated_img, rect))
            for img, rect in self.passed:
                screen.blit(img, rect)
            self.currentincr += self.angleincr

    def blitRotateCenter(self, image, topleft, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

        screen.blit(rotated_image, new_rect)
        return rotated_image, new_rect

class Level:
    def __init__(self):
        self.nodes = []
        self.ticks_passed = 0
        self.duration = 240
        self.song = None
        self.score = 0

    def update(self):
        self.ticks_passed += 1
        if self.ticks_passed == 60:
            self.nodes.append(Node(100, 500, 120))
        if self.ticks_passed == 120:
            self.nodes.append(Node(10, 56, 120))

        for node in self.nodes:
            node.update()
            if node.lifespan <= node.duration and node.active == False:
                self.score += 1
                self.nodes.remove(node)
                if scores["level1"] < self.score:
                    scores["level1"] = self.score
                    with open("UserData/scores.json", "w") as score:
                        json.dump(scores, score)

    def draw(self):
        text = scorefont.render(f"Score: {self.score}", True, "blue")
        screen.blit(text, (0, 0))
        for node in self.nodes:
            node.draw()

    def clickevent(self):
        for node in self.nodes:
            node.clickevent()

class Level2:
    def __init__(self):
        self.nodes = []
        self.ticks_passed = 0
        self.duration = 180
        self.score = 0
        self.song = "Resources/lvl2.mp3"

    def update(self):
        self.ticks_passed += 1
        if self.ticks_passed == 60:
            self.nodes.append(Node(600, 600, 60))
        if self.ticks_passed == 90:
            self.nodes.append(Node(100, 100, 60))
        if self.ticks_passed == 130:
            self.nodes.append(Node(100, 200, 60))

        for node in self.nodes:
            node.update()
            if node.lifespan <= node.duration and node.active == False and pygame.Rect(node.x - tile // 2, node.y - tile // 2, tile, tile).collidepoint(*pygame.mouse.get_pos()):
                self.score += 1
                self.nodes.remove(node)
                if scores["level2"] < self.score:
                    scores["level2"] = self.score
                    with open("UserData/scores.json", "w") as score:
                        json.dump(scores, score)

    def draw(self):
        text = scorefont.render(f"Score: {self.score}", True, "blue")
        screen.blit(text, (0, 0))
        for node in self.nodes:
            node.draw()

    def clickevent(self):
        for node in self.nodes:
            node.clickevent()


class Game:
    def __init__(self, level):
        self.level = level
        self.esc = False

    def start(self):
        global lastgamescore

        if self.level.song:
            pygame.mixer.music.load(self.level.song)
            pygame.mixer.music.play()
        while True:
            screen.fill((0, 0, 0))

            self.level.update()
            self.level.draw()

            screen.blit(cursor, pygame.mouse.get_pos())

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    self.level.clickevent()

                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    print("ESC")
                    lastgamescore = self.level.score
                    pygame.mixer.music.stop()
                    self.esc = True

            if self.level.ticks_passed == self.level.duration:
                lastgamescore = self.level.score
                #print(lastgamescore)
                break

            if self.esc:
                break

            pygame.display.update()
            clock.tick(fps)


class Button:
    def __init__(self, image, x, y, func):
        self.image = pygame.image.load(image)
        self.func = func
        self.x, self.y = x, y

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def clickevent(self):
        if pygame.Rect(self.x, self.y, self.image.get_rect().width, self.image.get_rect().height).collidepoint(*pygame.mouse.get_pos()):
            self.func()


class CreditsMenu:
    def __init__(self):
        self.bg = pygame.image.load("Resources/creditsbg.png")
        self.exitbtn = Button("Resources/exitbtn.png", 780, 0, self.exit)
        self.exited = False
    
    def exit(self):
        self.exited = True

    def draw(self):
        self.exitbtn.draw()

    def start(self):
        while True:
            screen.fill((0, 0, 0))

            screen.blit(self.bg, (0, 0))
            self.draw()

            screen.blit(cursor, pygame.mouse.get_pos())

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    self.exitbtn.clickevent()

            if self.exited:
                break

            pygame.display.update()
            clock.tick(fps)


class AboutMenu:
    def __init__(self):
        self.bg = pygame.image.load("Resources/aboutbg.png")
        self.exitbtn = Button("Resources/exitbtn.png", 780, 0, self.exit)
        self.exited = False

    def exit(self):
        self.exited = True

    def draw(self):
        self.exitbtn.draw()

    def start(self):
        while True:
            screen.fill((0, 0, 0))

            screen.blit(self.bg, (0, 0))
            self.draw()

            screen.blit(cursor, pygame.mouse.get_pos())

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    self.exitbtn.clickevent()

            if self.exited:
                break

            pygame.display.update()
            clock.tick(fps)

class MainMenu:
    def __init__(self):
        self.playbtn = Button("Resources/playbtn.png", width // 2 - 150, height // 2 - 95, self.playfunc)
        self.logo = pygame.image.load("Resources/logo.png")
        #12deg y 7deg right
        self.aboutbtn = Button("Resources/aboutbtn.png", width // 2 - 150, height // 2 + 200, self.aboutfunc)
        self.creditsbtn = Button("Resources/creditsbtn.png", width - 190, height - 190, self.creditsfunc)

    def aboutfunc(self):
        aboutmenu = AboutMenu()
        aboutmenu.start()

    def creditsfunc(self):
        creditsmenu = CreditsMenu()
        creditsmenu.start()

    def draw(self):
        self.playbtn.draw()
        self.aboutbtn.draw()
        self.creditsbtn.draw()

    def playfunc(self):
        lvlmenu = LevelMenu()
        lvlmenu.start()
    
    def start(self):
        while True:
            screen.fill((0, 0, 0))

            self.draw()
            screen.blit(self.logo, (0, 0))

            screen.blit(cursor, pygame.mouse.get_pos())

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    self.playbtn.clickevent()
                    self.aboutbtn.clickevent()
                    self.creditsbtn.clickevent()

            pygame.display.update()
            clock.tick(fps)


class LevelMenu:
    def __init__(self):
        self.lvl1btn = Button("Resources/lvl1btn.png", 0, 0, self.lvl1func)
        self.lvl2btn = Button("Resources/lvl2btn.png", 0, 200, self.lvl2func)
        self.exitbtn = Button("Resources/exitbtn.png", 780, 0, self.exit)
        self.bg = pygame.image.load("Resources/levelmenubg.png")
        self.tickaftergame = 0
        self.tickshowingscore = 180
        self.counting = False
        self.exited = False

    def lvl1func(self):
        game = Game(Level())
        game.start()
        self.counting = True

    def lvl2func(self):
        game = Game(Level2())
        game.start()
        self.counting = True

    def exit(self):
        self.exited = True

    def draw(self):
        self.lvl1btn.draw()
        self.lvl2btn.draw()
        self.exitbtn.draw()

    def start(self):
        global lastgamescore, scores

        while True:
            screen.fill((0, 0, 0))

            screen.blit(self.bg, (0, 0))
            self.draw()

            screen.blit(cursor, pygame.mouse.get_pos())

            text = scorefont.render(f"Level 1: {scores['level1']}", True, "green")
            screen.blit(text, (width - text.get_rect().width, 0))
            text = scorefont.render(f"Level 2: {scores['level2']}", True, "green")
            screen.blit(text, (width - text.get_rect().width, text.get_rect().height))

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    self.lvl1btn.clickevent()
                    self.lvl2btn.clickevent()
                    self.exitbtn.clickevent()

            if self.exited:
                break

            if self.counting:
                text = scorefont.render(f"Game ended with the score of {lastgamescore}", True, "green")
                screen.blit(text, (width - text.get_rect().width, height - text.get_rect().height))

                self.tickaftergame += 1
                if self.tickaftergame > self.tickshowingscore:
                    self.counting = False
                    self.tickaftergame = 0
                    lastgamescore = None

            pygame.display.update()
            clock.tick(fps)

menu = MainMenu()
menu.start()