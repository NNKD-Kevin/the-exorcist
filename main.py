import pygame
import random
import math
import os
import pytmx
from pytmx.util_pygame import load_pygame

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
#Font
game_title=pygame.font.Font('assets//Font//bloodfont.ttf',175)
chat_font=pygame.font.Font('assets/Font/gothic.ttf', 50)
small_font=pygame.font.Font('assets/Font/gothic.ttf', 20)


#Functions
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


#DIALOGUE
dialogue_2=[
    ('main','This house, I finally found it.')
    #('main',"I heard this house is cursed by some evil spirits."),
    #('main',"Let's see if I can help them.")
]
dialogue_3=[
    ('main','Hello lil boy'),
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
        self.y=600
        self.direction='right'
        self.show=True
        self.speed=3
        self.health=100
        self.direction='right'
        self.x_direction='right'
        self.is_moving=False
        idle_path="assets/characters/priest_idling"
        walk_path="assets/characters/priest_walking"
        self.idles=[pygame.transform.scale(pygame.image.load(f"{idle_path}/{f}").convert_alpha(), (23*4,27*4 )) for f in os.listdir(idle_path) if f.endswith(".png")]
        self.walks=[pygame.transform.scale(pygame.image.load(f"{walk_path}/{f}").convert_alpha(), (23*4, 27*4)) for f in os.listdir(walk_path) if f.endswith(".png")]
        self.idle_index=0
        self.walk_index=0
        self.img=self.idles[self.idle_index]
        self.animation_timer=0
        self.animation_speed=0.1
        self.rect=pygame.Rect(self.x,self.y,23*4,27*4)
    def draw(self,screen):
        if self.show:
            screen.blit(self.img, (self.x, self.y))
    def update(self):
        self.rect=pygame.Rect(self.x,self.y,100,100)


class Character:
    def __init__(self,x,y,name):
        self.x=x
        self.y=y
        self.target_x=x
        self.target_y=y
        self.direction='right'
        if name=='maid':
            idle_path="assets/characters/maid_idling"
            walk_path="assets/characters/maid_walking"
            self.idles=[pygame.transform.scale(pygame.image.load(f"{idle_path}/{f}").convert_alpha(), (23*4,27*4 )) for f in os.listdir(idle_path) if f.endswith(".png")]
            self.walks=[pygame.transform.scale(pygame.image.load(f"{walk_path}/{f}").convert_alpha(), (23*4, 27*4)) for f in os.listdir(walk_path) if f.endswith(".png")]
            self.rect=pygame.Rect(self.x,self.y,23*4,27*4)
        elif name=='grandpa':
            self.img="assets/characters/grandpa.png"
        elif name=='child':
            idle_path="assets/characters/child_idling"
            walk_path="assets/characters/child_walking"
            self.idles=[pygame.transform.scale(pygame.image.load(f"{idle_path}/{f}").convert_alpha(), (13*4,20*4 )) for f in os.listdir(idle_path) if f.endswith(".png")]
            self.walks=[pygame.transform.scale(pygame.image.load(f"{walk_path}/{f}").convert_alpha(), (13*4, 20*4)) for f in os.listdir(walk_path) if f.endswith(".png")]
            self.rect=pygame.Rect(self.x,self.y,13*4,20*4)
        self.is_moving=False
        self.idle_index=0
        self.walk_index=0
        self.img=self.idles[self.idle_index]
        self.animation_timer=0
        self.animation_speed=0.1
        self.speed=50
        self.width=self.rect.width
        self.height=self.rect.height
    def draw(self,screen):
        screen.blit(self.img, (self.x, self.y))
    def update(self):
        self.rect=pygame.Rect(self.x+self.width/2,self.y+self.height/2,self.width/32,self.height/32)
    def move_towards(self,dt):
        dx=self.target_x-self.x
        self.direction='right' if dx>0 else 'left'
        dy=self.target_y-self.y
        distance=math.hypot(dx,dy)
        if distance<=self.speed*dt:
            self.x=self.target_x
            self.y=self.target_y
            self.is_moving=False
            return
        else:
            self.is_moving=True
            self.x+=dx/distance*self.speed*dt
            self.y+=dy/distance*self.speed*dt

        
class Chatbox:
    def __init__(self,character,content):
        img_path="assets/characters/priest-icon.png"
        if character=='maid':
            img_path="assets/characters/maid.png"
        elif character=='grandpa':
            img_path="assets/characters/grandpa.png"
        self.full_content=content
        self.displayed_content=""
        self.img = pygame.image.load(img_path).convert_alpha()
        self.img = pygame.transform.scale(self.img, (150, 150))
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
        screen.blit(self.img, (75,675))
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
class Door:
    def __init__(self,x,y,origin,goal):
        self.x=x
        self.y=y
        self.rect=pygame.Rect(x,y,10,100)
        self.origin=origin
        self.goal=goal
        self.paired_door=None
        if self.origin==living_room and self.goal==bathroom:
            self.rect=pygame.Rect(x,y,60,100)
        if self.origin==bathroom and self.goal==living_room:
            self.rect=pygame.Rect(x,y,100,10)
    def draw(self,screen):
        pygame.draw.rect(screen,(255,255,255),self.rect,0)
class Object:
    def __init__(self,x,y,location,item):
        self.x=x
        self.y=y
        self.item=item
        self.location=location
        if self.item=='tivi':
            self.rect=pygame.Rect(self.x,self.y,100,60)
    def draw(self,screen):
        pygame.draw.rect(screen,(255,0,0),self.rect,2)
class Interaction:
    def __init__(self,item):
        self.x=400
        self.y=100
        self.item=item
        self.rect=pygame.Rect(self.x,self.y,600,600)
    def draw(self,screen):
        pygame.draw.rect(screen,(0,128,128),self.rect)
#Dialogue Management system
active_dialogue_index=0
active_chat_index=0
active_chatbox=Chatbox(dialogues[active_dialogue_index][active_chat_index][0],dialogues[active_dialogue_index][active_chat_index][1])

#Background
cutscene_bg = pygame.image.load("assets/bg/background.png").convert_alpha()
cutscene_bg = pygame.transform.scale(cutscene_bg, (1530, 880))
cutscene_bg2 = pygame.image.load("assets/bg/background2.png").convert_alpha()
cutscene_bg2= pygame.transform.scale(cutscene_bg2, (1530, 880))
living_room=load_pygame('assets/bg/living_room_map.tmx')
bathroom=load_pygame('assets/bg/bathroom_map.tmx')
kitchen=load_pygame('assets/bg/kitchen_map.tmx')
bedroom1=load_pygame('assets/bg/bedroom_map.tmx')
bedroom2=load_pygame('assets/bg/bedroom2_map.tmx')
map_scale=2.5
black_screen=pygame.Rect(0,0,1530,880)
scaled_tile_cache={}
current_bg = cutscene_bg
location=living_room
current_collisions=[]
doors=[
    Door(225,400,living_room,bedroom1),Door(1295,350,living_room,kitchen),Door(400,220,living_room,bathroom), #Living Room
    Door(1175,600,bedroom1,living_room), #Bedroom 1
    Door(400,400,kitchen,living_room),Door(1115,550,kitchen,bedroom2), #Kitchen
    Door(455,400,bedroom2,kitchen), #Bedroom 2
    Door(500,670,bathroom,living_room) #Bathroom
       ]
for door1 in doors:
    for door2 in doors:
        if door1.origin==door2.goal and door1.goal==door2.origin:
            door1.paired_door=door2
            break
def get_map_collision(map,scale,offset_x,offset_y):
    rects=[]
    for layer in map.layers:
        if isinstance(layer,pytmx.TiledObjectGroup):
            for obj in layer:
                scaled_rect=pygame.Rect(obj.x*scale+offset_x,obj.y*scale+offset_y,obj.width*scale,obj.height*scale)
                rects.append(scaled_rect)
    return rects

objects=[Object(955,210,living_room,'tivi')]
candles=[Decor(100,600,250,'candle'),Decor(1200,600,250,'candle'),Decor(300,600,150,'candle'),Decor(1050,600,150,'candle'),Decor(475,600,75,'candle'), Decor(950,600,75,'candle')]
fires=[Decor(165,560,100,'fire'),Decor(1270,560,100,'fire'),Decor(345,585,50,'fire'),Decor(1095,585,50,'fire'),Decor(500,592,25,'fire'),Decor(975,592,25,'fire')]
playertest=Playertest()
player=Player()
cursed_child=Boss(700,400)
child=Character(700,400,'child')
maid=Character(900,400,'maid')
npcs=[child]
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
walking_reset_timer=0.5
teleport_timer=0.5
teleported=True
#GAME LOOP
running=True
interacting=False
interacting_object=None
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
                stage='house'
            if event.key == pygame.K_9:
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
            if stage=='house':
                child.target_x=event.pos[0]
                child.target_y=event.pos[1]
        if stage=='house' and active_chatbox==None and teleported==True:
            for object in objects:
                if object.location==location:
                    player.update()
                    dx=abs(object.x-player.x)
                    dy=abs(object.y-player.y)
                    distance=math.hypot(dx,dy)
                    if distance<100:
                        if keys[pygame.K_e]:
                            interacting_object=Interaction(object.item)
                            interacting=True
                    if interacting and event.type==pygame.MOUSEBUTTONDOWN:
                        if not interacting_object.rect.collidepoint(pygame.mouse.get_pos()):
                            interacting=False
                            interacting_object=None
    map_pixel_width=location.width*location.tilewidth*map_scale
    map_pixel_height=location.height*location.tileheight*map_scale

    offset_x=(1530-map_pixel_width)//2
    offset_y=(880-map_pixel_height)//2
    keys=pygame.key.get_pressed()
    if keys[pygame.K_LSHIFT]:
        player.speed=6
        player.animation_speed=0.05
    if not keys[pygame.K_LSHIFT]:
        player.speed=3
        player.animation_speed=0.1
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
    if stage=='house' and active_chatbox==None:
        if keys[pygame.K_1]:
            location=living_room
        if keys[pygame.K_2]:
            location=bedroom1
        if keys[pygame.K_3]:
            location=bedroom2
        if keys[pygame.K_4]:
            location=kitchen
        if keys[pygame.K_5]:
            location=bathroom
    #MOVEMENT
    if (stage=='house' or stage=='boss') and active_chatbox==None  and teleported==True and interacting==False:    
        dx=0
        dy=0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx-=1
            player.is_moving=True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx+=1
            player.is_moving=True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy-=1
            player.is_moving=True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy+=1
            player.is_moving=True
        if dx!=0 or dy!=0:
            length=math.hypot(dx,dy)
            player.x+=dx*player.speed/length
            player.update()
            for rect in current_collisions:
                if player.rect.colliderect(rect):
                    if dx>0:
                        player.rect.right=rect.left
                    elif dx<0:
                        player.rect.left=rect.right
                    player.x=player.rect.x
            for npc in npcs:
                npc.update()
                if player.rect.colliderect(npc.rect):
                    if dx>0:
                        player.rect.right=npc.rect.left
                    elif dx<0:
                        player.rect.left=npc.rect.right
                    player.x=player.rect.x
            player.y+=dy*player.speed/length
            player.update()
            for rect in current_collisions:
                if player.rect.colliderect(rect):
                    if dy>0:
                        player.rect.bottom=rect.top
                    elif dy<0:
                        player.rect.top=rect.bottom
                    player.y=player.rect.y
            for npc in npcs:
                npc.update()
                if player.rect.colliderect(npc.rect):
                    if dy>0:
                        player.rect.bottom=npc.rect.top
                    elif dy<0:
                        player.rect.top=npc.rect.bottom
                    player.y=player.rect.y
        if dx==1:player.direction,player.x_direction='right','right'
        if dx==-1:player.direction,player.x_direction='left','left'
        if dy==1:player.direction='down'
        if dy==-1:player.direction='up'
    
        

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
    elif stage=='house':
        child.move_towards(dt)
        if teleported:
            for door in doors:
                if door.origin==location and door.rect.colliderect(player.rect):
                    location=door.goal
                    x=door.paired_door.x
                    y=door.paired_door.y
                    if door.origin==bedroom1:x+=50 #Bedroom1
                    if door.origin==bedroom2:x-=100 #Bedroom2
                    if door.origin==bathroom:y+=100 #Bathroom
                    if door.origin==kitchen:
                        if door.goal==living_room:x-=100
                        elif door.goal==bedroom2:x+=50
                    if door.origin==living_room:
                        if door.goal==bedroom1:x-=100
                        elif door.goal==kitchen:x+=50
                        elif door.goal==bathroom:y-=100
                    player.x=x
                    player.y=y
                    player.update()
                    teleported=False
            
            
        else:
            teleport_timer-=dt
            if teleport_timer<0:
                teleport_timer=0.5
                teleported=True
            
        
        
        current_collisions=get_map_collision(location,map_scale,offset_x,offset_y)
        

        





    #Stage 7 Logic
    elif stage=='boss':
        #Boss logic

        #Mass Attack
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
        #Chase Attack
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
        #Bullet Spread Attack
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
        #brightness=150
        screen.fill((0,0,0))
        map_pixel_width=location.width*location.tilewidth*map_scale
        map_pixel_height=location.height*location.tileheight*map_scale

        offset_x=(1530-map_pixel_width)//2
        offset_y=(880-map_pixel_height)//2
        for layer in location.layers:
            if isinstance(layer,pytmx.TiledTileLayer):
                for x,y, gid in layer:
                    if gid==0:
                        continue
                    cache_key=(location.filename,gid)
                    #Create scale img
                    if cache_key not in scaled_tile_cache:
                        original_img=location.get_tile_image_by_gid(gid)
                        if original_img:
                            w,h=original_img.get_size()
                            #Scale
                            scaled_tile_cache[cache_key]=pygame.transform.scale(original_img,(w*map_scale,h*map_scale))
                    #Draw after scaling
                    tile_image=scaled_tile_cache[cache_key]
                    if tile_image:
                        pixel_x=x*location.tilewidth*map_scale+offset_x
                        pixel_y=y*location.tileheight*map_scale+offset_y
                        screen.blit(tile_image,(pixel_x,pixel_y))
        walking_reset_timer-=dt
        if walking_reset_timer<0:
            walking_reset_timer=0.5
            if player.is_moving:
                player.is_moving=False

        player.animation_timer+=dt
        if player.animation_timer>player.animation_speed:
            player.animation_timer=0
            if player.is_moving==False:
                player.idle_index+=1
                player.img=player.idles[player.idle_index%len(player.idles)]
                if player.x_direction!='right':
                    player.img=pygame.transform.flip(player.img,True,False)
            else:
                player.walk_index+=1
                player.img=player.walks[player.walk_index%len(player.walks)]
                if player.x_direction=='left':
                    player.img=pygame.transform.flip(player.img,True,False)
        for object in objects:
            if object.location==location:
                player.update()
                dx=abs(object.x-player.x)
                dy=abs(object.y-player.y)
                distance=math.hypot(dx,dy)
                if distance<100:
                    object.draw(screen)
                    draw_text(f'E',chat_font,(255,255,255),object.x+50,object.y-50)
        player.update()
        for npc in npcs:
            npc.animation_timer+=dt
            if npc.animation_timer>npc.animation_speed:
                npc.animation_timer=0
                if npc.is_moving==False:
                    npc.idle_index+=1
                    npc.img=npc.idles[npc.idle_index%len(npc.idles)]
                    if npc.direction=='left':
                        npc.img=pygame.transform.flip(npc.img,True,False)
                else:
                    npc.walk_index+=1
                    npc.img=npc.walks[npc.walk_index%len(npc.walks)]
                    if npc.direction=='left':
                        npc.img=pygame.transform.flip(npc.img,True,False)
            if npc.y<=player.y:
                npc.draw(screen)
                player.draw(screen)
            else:
                player.draw(screen)
                npc.draw(screen)
        



        for door in doors:
            if door.origin==location:
                door.draw(screen)
        if active_chatbox:
            active_chatbox.update()
            active_chatbox.draw(screen)
        
        map_pixel_width=location.width*location.tilewidth*map_scale
        map_pixel_height=location.height*location.tileheight*map_scale

        offset_x=(1530-map_pixel_width)//2
        offset_y=(880-map_pixel_height)//2
        
        if interacting:
            interacting_object.draw(screen)
    
        #for rect in current_collisions:
        #    debug_rect=pygame.Rect(rect.x,rect.y,rect.width,rect.height)
        #    pygame.draw.rect(screen,(255,0,0),debug_rect,2)
        if not teleported:
            pygame.draw.rect(screen,(0,0,0),black_screen)
    


    #Stage 7 Rendering
    elif stage=='boss':
        screen.fill((0,0,0))

        player.animation_timer+=dt
        if player.animation_timer>player.animation_speed:
            player.animation_timer=0
            if player.is_moving==False:
                player.idle_index+=1
                player.img=player.idles[player.idle_index%len(player.idles)]
                if player.x_direction=='left':
                    player.img=pygame.transform.flip(player.img,True,False)
            else:
                player.walk_index+=1
                player.img=player.walks[player.walk_index%len(player.walks)]
                if player.x_direction=='left':
                    player.img=pygame.transform.flip(player.img,True,False)
                
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