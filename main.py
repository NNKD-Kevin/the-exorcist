import pygame
import random
import math
import os
#Setup
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1530, 880))
pygame.display.set_caption("The Exorcist")
stage='start'
clock=pygame.time.Clock()

#Color
light_wood=(199,153,82)
beige=(237,203,152)
#Asset
game_title=pygame.font.Font('assets//Font//bloodfont.ttf',175)
chat_font=pygame.font.Font('assets/Font/gothic.ttf', 50)
small_font=pygame.font.Font('assets/Font/gothic.ttf', 20)
#Background
cutscene_bg = pygame.image.load("assets/bg/background.png").convert_alpha()
cutscene_bg = pygame.transform.scale(cutscene_bg, (1530, 880))
cutscene_bg2 = pygame.image.load("assets/bg/background2.png").convert_alpha()
cutscene_bg2= pygame.transform.scale(cutscene_bg2, (1530, 880))
current_bg = cutscene_bg
#Functions
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


#DIALOGUE
dialogue_2=[
    ('main','This house, I finally found it.'),
    ('main',"I heard this house is cursed by some evil spirits."),
    ('main',"Let's see if I can help them.")
]
dialogue_3=[
    ('main','Boss Fight(I decided to work on this first)'),
]
dialogues=[dialogue_2,dialogue_3]




#Classes
class Decor:
    def __init__(self,x,y,size,type):
        self.x=x
        self.y=y 
        self.size=size
        if type=='candle':
            self.img="assets/stock/candle.png"
        elif type=='fire':
            self.img='assets/stock/fire.jpeg'
        self.img = pygame.image.load(self.img).convert_alpha()
        self.img = pygame.transform.scale(self.img, (size, size))
    def draw(self,screen):
         screen.blit(self.img, (self.x, self.y))
class Playertest:
    def __init__(self):
        self.x=100
        self.y=525
        self.direction='right'
        self.show=True
        self.img="assets/bg/mc.png"
        self.speed=5
        self.img = pygame.image.load(self.img).convert_alpha()
        self.img = pygame.transform.scale(self.img, (100, 100))
    def draw(self,screen):
        if self.show:
            screen.blit(self.img, (self.x, self.y))
class Player:
    def __init__(self):
        self.x=700
        self.y=800
        self.direction='right'
        self.show=True
        self.img="assets/characters/main_character.png"
        self.speed=6
        self.health=100
        self.img = pygame.image.load(self.img).convert_alpha()
        self.img = pygame.transform.scale(self.img, (100, 100))
        self.rect=pygame.Rect(self.x,self.y,100,100)
    def draw(self,screen):
        if self.show:
            screen.blit(self.img, (self.x, self.y))
    def update(self):
        self.rect=pygame.Rect(self.x,self.y,100,100)
class Character:
    def __init__(self,x,y,name):
        self.x=x
        self.y=y
        if name=='maid':
            self.img="assets/characters/maid.png"
        elif name=='grandpa':
            self.img="assets/characters/grandpa.png"
        elif name=='child':
            idle_path="assets/characters/child_idling"
            walk_path="assets/characters/child_walking"
            self.idles=[pygame.transform.scale(pygame.image.load(f"{idle_path}/{f}").convert_alpha(), (48,80 )) for f in os.listdir(idle_path) if f.endswith(".png")]
            self.walks=[pygame.transform.scale(pygame.image.load(f"{walk_path}/{f}").convert_alpha(), (48, 80)) for f in os.listdir(walk_path) if f.endswith(".png")]
        self.is_moving=False
        self.idle_index=0
        self.walk_index=0
        self.img=self.idles[self.idle_index]
        self.animation_timer=0
        self.animation_speed=0.1
    def draw(self,screen):
        screen.blit(self.img, (self.x, self.y))
class Chatbox:
    def __init__(self,character,content):
        img_path="assets/characters/main_character.png"
        if character=='maid':
            img_path="assets/characters/maid.png"
        elif character=='grandpa':
            img_path="assets/characters/grandpa.png"
        self.full_content=content
        self.displayed_content=""
        self.img = pygame.image.load(img_path).convert_alpha()
        self.img = pygame.transform.scale(self.img, (100, 100))
        self.rect=pygame.Rect(50,650,1400,200)

        self.typing_speed=2
        self.is_typing=True
        self.char_index=0

    def update(self):
        if self.is_typing:
            self.char_index+=self.typing_speed
            self.displayed_content=self.full_content[:int(self.char_index)]
            if self.char_index>=len(self.full_content):
                self.is_typing=False
                self.displayed_content=self.full_content
    def draw(self,screen):
        pygame.draw.rect(screen,light_wood,self.rect,0)
        pygame.draw.rect(screen,beige,(75,675,150,150))
        screen.blit(self.img, (100,725))
        draw_text(self.displayed_content,chat_font,(0,0,0),250,700)
        if not self.is_typing:
            draw_text("Click to continue",small_font,(0,0,0),1275,800)
    def is_ready_to_advance(self):
        return not self.is_typing
class Boss:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.img="assets/characters/cursed_child2.png"
        self.img = pygame.image.load(self.img).convert_alpha()
        self.img = pygame.transform.scale(self.img, (100, 100))
    def draw(self,screen):
        screen.blit(self.img, (self.x, self.y))
    def attack(self):
        pass
class Boss_Attack:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.img="assets/characters/cross1.png"
        self.img = pygame.image.load(self.img).convert_alpha()
        self.img = pygame.transform.scale(self.img, (150, 150))
        self.rect=pygame.Rect(x+20,y+20,110,110)
    def draw(self,screen):
        screen.blit(self.img, (self.x, self.y))
class Boss_Pattern:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.img="assets/characters/pentagon.png"
        self.img = pygame.image.load(self.img).convert_alpha()
        self.img = pygame.transform.scale(self.img, (150, 150))
        self.rect=pygame.Rect(x,y,150,150)
    def draw(self,screen):
        screen.blit(self.img, (self.x, self.y))
class Bullet:
    def __init__(self, angle):
        self.direction = angle
        self.x=cursed_child.x
        self.y=cursed_child.y
        self.img="assets/characters/cross2.png"
        self.img = pygame.image.load(self.img).convert_alpha()
        self.img = pygame.transform.scale(self.img, (100, 100))
        self.rect=pygame.Rect(self.x+15,self.y+15,70,70)
        self.speed=100
    def draw(self,screen):
        screen.blit(self.img, (self.x, self.y))
    def update(self):
        self.rect=pygame.Rect(self.x+15,self.y+15,70,70)
    def move(self,dt):
        self.x+=dt*self.speed*math.cos(self.direction/180*math.pi)
        self.y+=dt*self.speed*math.sin(self.direction/180*math.pi)
               

#Dialogue Management system
active_dialogue_index=0
active_chat_index=0
active_chatbox=Chatbox(dialogues[active_dialogue_index][active_chat_index][0],dialogues[active_dialogue_index][active_chat_index][1])


candles=[Decor(100,600,250,'candle'),Decor(1200,600,250,'candle'),Decor(300,600,150,'candle'),Decor(1050,600,150,'candle'),Decor(475,600,75,'candle'), Decor(950,600,75,'candle')]
fires=[Decor(165,560,100,'fire'),Decor(1270,560,100,'fire'),Decor(345,585,50,'fire'),Decor(1095,585,50,'fire'),Decor(500,592,25,'fire'),Decor(975,592,25,'fire')]
playertest=Playertest()
player=Player()
cursed_child=Boss(700,400)
child=Character(700,400,'child')
boss_attacks=[]
boss_patterns=[]
#Variables
candle_timer=0
attack_spawn_timer=5
attack_timer=2
blow_candle=False
brightness=45
attack_count=2
attack=False
attack_disappear_timer=2
attack_disappear=False
phase=0
stop_timer=6
n=0
bullets=[]
bullet_timer=15

#GAME LOOP
running=True
while running:
    dt = clock.tick(60) / 1000
    #INPUT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #Start Game
        if stage=='start' and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                blow_candle=True
        if stage=='start' and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_8:
                stage='boss'
        #Next Dialogue
        if event.type==pygame.MOUSEBUTTONDOWN:
            if active_chatbox and active_chatbox.rect.collidepoint(pygame.mouse.get_pos()):
                if active_chatbox.is_ready_to_advance():
                    active_chat_index+=1
                    if active_chat_index<len(dialogues[active_dialogue_index]):
                        next_char,next_text=dialogues[active_dialogue_index][active_chat_index]
                        active_chatbox=Chatbox(next_char,next_text)
                    else:
                        active_chatbox=None
    keys=pygame.key.get_pressed()
    #Cutscene movement  
    if stage=='cutscene' and active_chatbox==None:
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and playertest.x>0:
            playertest.x-=playertest.speed
            if playertest.direction=='right':
                playertest.direction='left'
                playertest.img=pygame.transform.flip(playertest.img, True, False)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            playertest.x+=playertest.speed
            if playertest.direction=='left':
                playertest.direction='right'
                playertest.img=pygame.transform.flip(playertest.img, True, False)
    
    #MOVEMENT 
    if (stage=='house' or stage=='boss') and active_chatbox==None:    
        dx=0
        dy=0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:dx-=1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:dx+=1
        if keys[pygame.K_UP] or keys[pygame.K_w]:dy-=1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:dy+=1
        if dx!=0 or dy!=0:
            length=math.hypot(dx,dy)
            player.x+=dx*player.speed/length
            player.y+=dy*player.speed/length


    #LOGIC HANDLING
    #Stage 1 logic
    if stage=='start':
        if blow_candle:
            candle_timer-=dt
        if candle_timer<0:
            if fires:
                fires.pop()
                fires.pop()
                brightness+=70
                candle_timer=0.5
            else:
                stage='cutscene'
                blow_candle=False
                candle_timer=1

        
                            
        for candle in candles:
            candle.draw(screen)
        for fire in fires:
            fire.draw(screen)


    #Stage 2 Logic
    elif stage=='cutscene':
        brightness=50
        if blow_candle:
            candle_timer-=dt
        if candle_timer<0:
            stage='house'
            active_dialogue_index+=1
            active_chat_index=0
            active_chatbox=Chatbox(dialogues[active_dialogue_index][active_chat_index][0],dialogues[active_dialogue_index][active_chat_index][1])

        screen.blit(current_bg,(0,0))

        if playertest.x>1250 and not blow_candle:
            current_bg=cutscene_bg2
            candle_timer=1
            blow_candle=True
            playertest.show=False

    #Stage 3 Logic






    #Stage 7 Logic
    elif stage=='boss':
        if phase%3!=0 or phase==0:
            if not attack and not attack_disappear:
                attack_spawn_timer-=dt
                if attack_spawn_timer<0:
                    attack_spawn_timer=1
                    if attack_count<10:
                        attack_count+=1
                    for i in range(attack_count):
                        attack_x=random.randint(0,1430)
                        attack_y=random.randint(0,780)
                        boss_patterns.append(Boss_Pattern(attack_x,attack_y))
                    attack=True
                    attack_timer=1
            elif attack:
                attack_timer-=dt
                if attack_timer<0:
                    attack=False
                    attack_disappear=True
                    attack_disappear_timer=1
                    for pattern in boss_patterns:
                        boss_attacks.append(Boss_Attack(pattern.x,pattern.y))
                    boss_patterns=[]
                    
            if attack_disappear:
                attack_disappear_timer-=dt
                if attack_disappear_timer<0:
                    boss_attacks=[]
                    phase+=1
                    attack_disappear=False
        elif phase%3==0:
            stop_timer-=dt
            if stop_timer<0:
                stop_timer=6
                phase+=1
                boss_attacks=[]
            attack_spawn_timer-=dt
            if attack_spawn_timer<0:
                attack_spawn_timer=0.5
                boss_patterns.append(Boss_Pattern(player.x,player.y))
                attack=True
            if attack:
                attack_timer-=dt
            if attack_timer<0:
                attack_timer=0.5
                if boss_patterns:
                    boss_attacks.append(Boss_Attack(boss_patterns[0].x,boss_patterns[0].y))
                    boss_patterns.pop(0)
        bullet_timer-=dt
        if bullet_timer<0:
            bullet_timer=15
            for i in range(0,360,36):
                bullets.append(Bullet(i))
        for j in boss_attacks[:]:
            if j.rect.colliderect(player.rect):
                player.health-=1
                boss_attacks.remove(j)
        for bullet in bullets:
            bullet.move(dt)
            if bullet.rect.colliderect(player.rect):
                bullets.remove(bullet)
                player.health-=1

        


            
            
                 



    #RENDER HANDLING
    #Stage 1 Rendering
    if stage=='start':
        screen.fill((0, 0, 0))
        time_ms=pygame.time.get_ticks()
        cross_surf = pygame.Surface((300, 300), pygame.SRCALPHA)
        pygame.draw.rect(cross_surf,(77,48,27),(125,0,50,300),0)
        pygame.draw.rect(cross_surf,(77,48,27),(50,75,200,50),0)
        rotated_cross=pygame.transform.rotate(cross_surf,45)
        cross_rect=rotated_cross.get_rect(center=(1000, 200))
        screen.blit(rotated_cross,cross_rect)
        draw_text("The Exorcist",game_title,(255,0,0),350,200)

        dynamic_font=pygame.font.Font('assets//Font//bloodfont.ttf',30+int(math.sin(time_ms*0.002)*4))
        text_surf=dynamic_font.render("Press Enter to start",True,(255,0,0))
        text_surf1=pygame.transform.rotate(text_surf,10)
        text_rect=text_surf1.get_rect(center=(750, 500))
        screen.blit(text_surf1,text_rect)
        for candle in candles:
            candle.draw(screen)
        for fire in fires:
            fire.draw(screen)


    #Stage 2 Rendering
    elif stage=='cutscene':
        screen.blit(current_bg,(0,0))
        playertest.draw(screen)
        if active_chatbox:
            active_chatbox.update()
            active_chatbox.draw(screen)




    #Stage 3 Rendering
    elif stage=='house':
        screen.fill((0,128,128))
        player.draw(screen)
        child.animation_timer+=dt
        if child.animation_timer>child.animation_speed:
            child.animation_timer=0
            if child.is_moving==False:
                child.idle_index+=1
                child.img=child.idles[child.idle_index%len(child.idles)]
            else:
                child.walk_index+=1
                child.img=child.walks[child.walk_index%len(child.walks)]
        child.draw(screen)
        


    #Stage 7 Rendering
    elif stage=='boss':
        screen.fill((0,0,0))


        player.update()
        for bullet in bullets:
            bullet.update()
            bullet.draw(screen)
        if active_chatbox:
            active_chatbox.update()
            active_chatbox.draw(screen)

        for pattern in boss_patterns:
            pattern.draw(screen)
        player.draw(screen)
        for i in boss_attacks:
            i.draw(screen)
        cursed_child.draw(screen)
        draw_text("Health: "+str(player.health),chat_font,(255,0,0),50,50)

        


    #Global blur
    blur_surface=pygame.Surface((1530, 880), pygame.SRCALPHA)
    blur_surface.fill((0, 0, 0, brightness))
    screen.blit(blur_surface, (0, 0))

    pygame.display.flip()



pygame.quit()