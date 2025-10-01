import pygame
import threading
import time
import random


#變數
Px = 0
Py = 0
PXb = 0
PYb = 0
WIDTH = 960
HEIGHT = 540
SPEED = 2
score = 0
score_text = 'score:' + str(score)
tile_size = 10
cols = 0
rows = 0
MAP_DATA = [[0 for _ in range(96)] for _ in range(54)]
mapdata = []
walls = []
bings = []

#顏色
YELLOW = (255, 255, 0)
BLACK = (0,0,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
RED = (255, 0, 0)

#遊戲初始化 和 創建視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('小精靈')
FPS = 60
clock = pygame.time.Clock()
running = True

#讀取圖片
BING = pygame.image.load('bing.png') 
BING = pygame.transform.scale(BING, (tile_size, tile_size))
P1 = pygame.image.load('player1.png') 
P1 = pygame.transform.scale(P1, (30, 30))
P2 = pygame.image.load('player2.png') 
P2 = pygame.transform.scale(P2, (30, 30))
E1 = pygame.image.load('enemy1.png') 
E1 = pygame.transform.scale(E1, (30, 30))
E2 = pygame.image.load('enemy2.png') 
E2 = pygame.transform.scale(E2, (30, 30))
E3 = pygame.image.load('enemy3.png') 
E3 = pygame.transform.scale(E3, (30, 30))
E4 = pygame.image.load('enemy4.png') 
E4 = pygame.transform.scale(E4, (30, 30))
present_image2 = P2
present_image1 = P1




#讀取地圖
F = open('mapdata.txt','r')
maprawdata = F.read()
for i in range(len(maprawdata)):
     if maprawdata[i] == '0':
         mapdata.append(0)
     elif maprawdata[i] == '1':
         mapdata.append(1)
     elif maprawdata[i] == '2':
         mapdata.append(2)
     else :
         continue
for i in range(len(mapdata)):
     MAP_DATA[rows][cols] = mapdata[i]
     cols += 1
     if cols == 96:
         rows += 1
         cols = 0
for y in range(len(MAP_DATA)):
    for x in range(len(MAP_DATA[0])):
        if MAP_DATA[y][x] == 0:
            pygame.draw.rect(screen,BLACK,(x * tile_size, y * tile_size, tile_size, tile_size))
        elif MAP_DATA[y][x] == 1:
            pygame.draw.rect(screen,BLUE,(x * tile_size, y * tile_size, tile_size, tile_size))
            wall_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
            walls.append(wall_rect)
        else:
            screen.blit(BING, (x * tile_size, y * tile_size))
            bing_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
            bings.append(bing_rect) 

#重整畫面
def refresh(): 
    for y in range(len(MAP_DATA)):
            for x in range(len(MAP_DATA[0])):
                if MAP_DATA[y][x] == 0:
                    pygame.draw.rect(screen,BLACK,(x * tile_size, y * tile_size, tile_size, tile_size))
                elif MAP_DATA[y][x] == 1:
                    pygame.draw.rect(screen,BLUE,(x * tile_size, y * tile_size, tile_size, tile_size))
                else:
                    screen.blit(BING, (x * tile_size, y * tile_size))
     
 #分數
def show_score():
    score_text = 'score:' + str(score)
    #文字渲染
    font = pygame.font.Font(None, 25)
    score_surface = font.render(score_text, False, WHITE)
        
    #文字位置
    score_rect = score_surface.get_rect()
    score_rect.x = 0
    score_rect.y = 0
    screen.blit(score_surface, score_rect)

def Game_Over():
    font = pygame.font.Font(None, 200) 
    text = font.render("Game Over", True, RED) 
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2)) 
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(3000)

def Win():  
    font = pygame.font.Font(None, 200) 
    text = font.render("You Win", True, RED) 
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2)) 
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(3000)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = P2
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        
    def update(self):
        global Px, Py, PXb, PYb, WIDTH, HEIGHT, score, present_image2, present_image1
        
        #取得嘗試移動前座標
        PXb = self.rect.x
        PYb = self.rect.y
                
        #移動
        self.rect.x += Px
        self.rect.y += Py
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w]:
            Py = -SPEED
            Px = 0
            present_image2 = pygame.transform.rotate(P2,90)
            present_image1 = pygame.transform.rotate(P1,90)
        if key_pressed[pygame.K_s]:
            Py = SPEED
            Px = 0
            present_image2 = pygame.transform.rotate(P2,270)
            present_image1 = pygame.transform.rotate(P1,270)
        if key_pressed[pygame.K_a]:
            Px = -SPEED
            Py = 0
            present_image2 = pygame.transform.rotate(P2,180)
            present_image1 = pygame.transform.rotate(P1,180)
        if key_pressed[pygame.K_d]:
            Px = SPEED
            Py = 0
            present_image2 = P2
            present_image1 = P1
              
        #牆壁
        player_rect = pygame.Rect(self.rect.x, self.rect.y, 30, 30)
        for wall_rect in walls:
            if player_rect.colliderect(wall_rect):
                self.rect.x = PXb
                self.rect.y = PYb
                
        #邊界
        self.rect.x = min(self.rect.x, WIDTH-30)
        self.rect.x = max(0, self.rect.x)
        self.rect.y = min(self.rect.y, HEIGHT-30)
        self.rect.y = max(0, self.rect.y)
        
        #豆子
        for bing_rect in bings:
            if player_rect.colliderect(bing_rect):
                pygame.draw.rect(screen, (BLACK), bing_rect)
                score += 1
                bings.remove(bing_rect)
                bing_x = int(bing_rect[0]/10)
                bing_y = int(bing_rect[1]/10)
                MAP_DATA[bing_y][bing_x] = 0
               
#切換玩家圖片
def change_picture():
    global present_image2, present_image1
    while running:
        for i in range(0,4):
            player.image = present_image1
            time.sleep(0.05)
        for i in range(0,4):
            player.image = present_image2
            time.sleep(0.05)

#獲取可走方向
def get_directions(grid_x, grid_y):
    neighbors = []
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    MAP_COLS = len(MAP_DATA[0])
    MAP_ROWS = len(MAP_DATA)
    SPRITE_TILES = 3 
    for dx, dy in directions:
        is_clear = True
        # 精靈移動後的左上角網格座標
        new_grid_x = grid_x + dx
        new_grid_y = grid_y + dy
        # 檢查精靈移動後所佔據的 3x3 所有格子
        for offset_y in range(SPRITE_TILES):
            for offset_x in range(SPRITE_TILES):
                check_x = new_grid_x + offset_x
                check_y = new_grid_y + offset_y
                # 檢查邊界
                if not (0 <= check_x < MAP_COLS and 0 <= check_y < MAP_ROWS):
                    is_clear = False
                    break 
                # 檢查牆壁
                if MAP_DATA[check_y][check_x] == 1:
                    is_clear = False
                    break 
            if not is_clear:
                break 
        if is_clear:
            neighbors.append((dx, dy))
    return neighbors
#獲取可走座標
def get_neighbor(grid_x, grid_y):
    neighbors = []
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    MAP_COLS = len(MAP_DATA[0])
    MAP_ROWS = len(MAP_DATA)
    SPRITE_TILES = 3 
    for dx, dy in directions:
        is_clear = True
        # 精靈移動後的左上角網格座標
        new_grid_x = grid_x + dx
        new_grid_y = grid_y + dy
        # 檢查精靈移動後所佔據的 3x3 所有格子
        for offset_y in range(SPRITE_TILES):
            for offset_x in range(SPRITE_TILES):
                check_x = new_grid_x + offset_x
                check_y = new_grid_y + offset_y
                # 檢查邊界
                if not (0 <= check_x < MAP_COLS and 0 <= check_y < MAP_ROWS):
                    is_clear = False
                    break 
                # 檢查牆壁
                if MAP_DATA[check_y][check_x] == 1:
                    is_clear = False
                    break 
            if not is_clear:
                break 
        if is_clear:
            neighbors.append((new_grid_x, new_grid_y))
    return neighbors

#選擇最佳方向
def choose_option(options, grid_x, grid_y):
    global PXb, PYb, SPEED
    distance = []
    player_grid_x = PXb // tile_size
    player_grid_y = PYb // tile_size
    for new_x, new_y in options:
        dist = abs(new_x - player_grid_x) + abs(new_y - player_grid_y)
        distance.append(dist)
    best_option = options[distance.index(min(distance))]
    dx = best_option[0] - grid_x
    dy = best_option[1] - grid_y
    direction_x = dx * SPEED
    direction_y = dy * SPEED
    return (direction_x, direction_y)
        


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction_x = SPEED    # 初始向右移動
        self.direction_y = 0
        self.exit1 = (54, 33)
        self.exit2 = (57, 33)
    def leave_home(self):
        current_grid_x = self.rect.x // tile_size
        current_grid_y = self.rect.y // tile_size   
        # 朝出口移動
        self.house_exit = random.choice([self.exit1, self.exit2])
        if current_grid_x < self.house_exit[0]:
            self.direction_x = SPEED
            self.direction_y = 0
        elif current_grid_x > self.house_exit[0]:
            self.direction_x = -SPEED
            self.direction_y = 0
        elif current_grid_y < self.house_exit[1]:
            self.direction_x = 0
            self.direction_y = SPEED
        elif current_grid_y > self.house_exit[1]:
            self.direction_x = 0
            self.direction_y = -SPEED

    def chase(self):
        current_grid_x = self.rect.x // tile_size
        current_grid_y = self.rect.y // tile_size
        #追逐
        options = get_neighbor(current_grid_x, current_grid_y)
        if len(options) > 2: #若是轉角就選擇路線
            self.direction_x, self.direction_y = choose_option(options, current_grid_x, current_grid_y)
        
    def mode_choose(self):
        current_grid_x = self.rect.x // tile_size
        current_grid_y = self.rect.y // tile_size
        if 36 <= current_grid_y <= 44 and 50 <= current_grid_x <= 63:
            self.leave_home()
        else:
            self.chase()

    def update(self):
        global tile_size
        #取得嘗試移動前座標
        EXb = self.rect.x
        EYb = self.rect.y
        current_grid_x = EXb // tile_size
        current_grid_y = EYb // tile_size
        current_dir = [self.direction_x, self.direction_y]
        #走完一格 判斷模式
        if EXb % tile_size == 0 and EYb % tile_size == 0: 
            self.mode_choose()
        #移動
        self.rect.x += self.direction_x
        self.rect.y += self.direction_y

         # 撞牆處理
        enemy_rect = pygame.Rect(self.rect.x, self.rect.y, 30, 30)
        collision = False
        for wall_rect in walls:
            if enemy_rect.colliderect(wall_rect):
                collision = True
                break
                
        if collision:
            # 恢復位置
            self.rect.x = EXb
            self.rect.y = EYb
            
            # 修正：撞牆後重新選擇方向，但不立即移動
            available_directions = get_directions(current_grid_x, current_grid_y)
            if available_directions:
                # 排除當前方向
                filtered = [d for d in available_directions 
                           if d != (self.direction_x, self.direction_y)]
                if filtered:
                    self.direction_x, self.direction_y = random.choice(filtered)
                else:
                    self.direction_x, self.direction_y = random.choice(available_directions)
        
        # 邊界檢查
        self.rect.x = max(0, min(self.rect.x, WIDTH-30))
        self.rect.y = max(0, min(self.rect.y, HEIGHT-30))
        
        
        
enemies = [Enemy(510, 430, E1), Enemy(540, 430, E2), Enemy(570, 430, E3), Enemy(600, 430, E4)]




#分組
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for enemy in enemies:
    all_sprites.add(enemy)
enemy_group = pygame.sprite.Group()
for enemy in enemies:
    enemy_group.add(enemy)

#多線程
change_picture_thread = threading.Thread(target = change_picture)
change_picture_thread.start() 

#遊戲迴圈
while running:
    clock.tick(FPS)

    #結束偵測
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if pygame.sprite.spritecollide(player, enemy_group, False):
        Game_Over()
        running = False
    #獲勝偵測
    if score == 695:
        Win()
        running = False
    #更新畫面
    screen.fill(BLACK)
    refresh()

    #更新角色
    all_sprites.update()

    #畫面顯示
    pygame.draw.rect(screen, BLACK, pygame.Rect(50, 0, 30, 20))
    all_sprites.draw(screen)
    
    #分數顯示
    show_score()
    pygame.display.update()

pygame.quit()