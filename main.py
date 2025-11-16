import pygame
import threading
import time
import random
import heapq

# ==================== 變數 ====================
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
MAP_DATA = [[0 for i in range(96)] for i in range(54)]
mapdata = []
walls = []
bings = []

# ==================== 顏色 ====================
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# ==================== 遊戲初始化 ====================
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('小精靈')
FPS = 60
clock = pygame.time.Clock()
running = True

# ==================== 讀取圖片 ====================
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

# ==================== 讀取地圖 ====================
F = open('mapdata.txt', 'r')
maprawdata = F.read()
for i in range(len(maprawdata)):
    if maprawdata[i] == '0':
        mapdata.append(0)
    elif maprawdata[i] == '1':
        mapdata.append(1)
    elif maprawdata[i] == '2':
        mapdata.append(2)
    else:
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
            pygame.draw.rect(screen, BLACK, (x * tile_size, y * tile_size, tile_size, tile_size))
        elif MAP_DATA[y][x] == 1:
            pygame.draw.rect(screen, BLUE, (x * tile_size, y * tile_size, tile_size, tile_size))
            wall_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
            walls.append(wall_rect)
        else:
            screen.blit(BING, (x * tile_size, y * tile_size))
            bing_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
            bings.append(bing_rect)

# ==================== 敵人巡路機制 ====================

"""計算距離"""
def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star_search(start, goal, MAP_DATA, tile_size):
    MAP_COLS = len(MAP_DATA[0])
    MAP_ROWS = len(MAP_DATA)
    SPRITE_TILES = 3

    """檢查碰撞"""
    def is_valid(grid_x, grid_y):
        for offset_y in range(SPRITE_TILES):
            for offset_x in range(SPRITE_TILES):
                check_x = grid_x + offset_x
                check_y = grid_y + offset_y
                if not (0 <= check_x < MAP_COLS and 0 <= check_y < MAP_ROWS):
                    return False
                if MAP_DATA[check_y][check_x] == 1:
                    return False
        return True

    """獲取所有可走座標"""
    def get_neighbors(pos):
        x, y = pos
        neighbors = []
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_x, new_y = x + dx, y + dy
            if is_valid(new_x, new_y):
                neighbors.append((new_x, new_y))
        return neighbors

    """初始化"""
    options = []
    heapq.heappush(options, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    """主循環"""
    while options:
        _, current = heapq.heappop(options)

        if current == goal:
            break

        for next_pos in get_neighbors(current):
            new_cost = cost_so_far[current] + 1

            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                priority = new_cost + distance(next_pos, goal)
                heapq.heappush(options, (priority, next_pos))
                came_from[next_pos] = current

    """沒找到"""
    if goal not in came_from:
        return None

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]

    if not path:
        return None

    next_step = path[-1]
    dx = next_step[0] - start[0]
    dy = next_step[1] - start[1]

    return (dx, dy)


# ==================== 輔助函數 ====================

"""畫面刷新"""
def refresh():
    for y in range(len(MAP_DATA)):
        for x in range(len(MAP_DATA[0])):
            if MAP_DATA[y][x] == 0:
                pygame.draw.rect(screen, BLACK, (x * tile_size, y * tile_size, tile_size, tile_size))
            elif MAP_DATA[y][x] == 1:
                pygame.draw.rect(screen, BLUE, (x * tile_size, y * tile_size, tile_size, tile_size))
            else:
                screen.blit(BING, (x * tile_size, y * tile_size))

"""顯示分數"""
def show_score():
    score_text = 'score:' + str(score)
    font = pygame.font.Font(None, 25)
    score_surface = font.render(score_text, False, WHITE)
    score_rect = score_surface.get_rect()
    score_rect.x = 0
    score_rect.y = 0
    screen.blit(score_surface, score_rect)

"""遊戲失敗"""
def Game_Over():
    font = pygame.font.Font(None, 200)
    text = font.render("Game Over", True, RED)
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(3000)

"""遊戲獲勝"""
def Win():
    font = pygame.font.Font(None, 200)
    text = font.render("You Win", True, RED)
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(3000)

"""獲取可走方向"""
def get_directions(grid_x, grid_y):
    neighbors = []
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    MAP_COLS = len(MAP_DATA[0])
    MAP_ROWS = len(MAP_DATA)
    SPRITE_TILES = 3
    for dx, dy in directions:
        is_clear = True
        new_grid_x = grid_x + dx
        new_grid_y = grid_y + dy
        for offset_y in range(SPRITE_TILES):
            for offset_x in range(SPRITE_TILES):
                check_x = new_grid_x + offset_x
                check_y = new_grid_y + offset_y
                if not (0 <= check_x < MAP_COLS and 0 <= check_y < MAP_ROWS):
                    is_clear = False
                    break
                if MAP_DATA[check_y][check_x] == 1:
                    is_clear = False
                    break
            if not is_clear:
                break
        if is_clear:
            neighbors.append((dx, dy))
    return neighbors


# ==================== Player  ====================

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = P2
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
        global Px, Py, PXb, PYb, WIDTH, HEIGHT, score, present_image2, present_image1

        # 取得嘗試移動前座標
        PXb = self.rect.x
        PYb = self.rect.y

        # 移動
        self.rect.x += Px
        self.rect.y += Py
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w]:
            Py = -SPEED
            Px = 0
            present_image2 = pygame.transform.rotate(P2, 90)
            present_image1 = pygame.transform.rotate(P1, 90)
        if key_pressed[pygame.K_s]:
            Py = SPEED
            Px = 0
            present_image2 = pygame.transform.rotate(P2, 270)
            present_image1 = pygame.transform.rotate(P1, 270)
        if key_pressed[pygame.K_a]:
            Px = -SPEED
            Py = 0
            present_image2 = pygame.transform.rotate(P2, 180)
            present_image1 = pygame.transform.rotate(P1, 180)
        if key_pressed[pygame.K_d]:
            Px = SPEED
            Py = 0
            present_image2 = P2
            present_image1 = P1

        # 牆壁碰撞
        player_rect = pygame.Rect(self.rect.x, self.rect.y, 30, 30)
        for wall_rect in walls:
            if player_rect.colliderect(wall_rect):
                self.rect.x = PXb
                self.rect.y = PYb

        # 邊界
        self.rect.x = min(self.rect.x, WIDTH - 30)
        self.rect.x = max(0, self.rect.x)
        self.rect.y = min(self.rect.y, HEIGHT - 30)
        self.rect.y = max(0, self.rect.y)

        # 吃豆子
        for bing_rect in bings:
            if player_rect.colliderect(bing_rect):
                pygame.draw.rect(screen, (BLACK), bing_rect)
                score += 1
                bings.remove(bing_rect)
                bing_x = int(bing_rect[0] / 10)
                bing_y = int(bing_rect[1] / 10)
                MAP_DATA[bing_y][bing_x] = 0


# ==================== Enemy  ====================

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, img, territory=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction_x = SPEED
        self.direction_y = 0
        self.exit1 = (54, 33)
        self.exit2 = (57, 33)
        self.path_update_counter = 0
        self.path_update_interval = 10
        self.territory = territory  # 設定行動範圍
        self.set_territory_bounds()  # 計算範圍邊界
    
    """設定邊界"""
    def set_territory_bounds(self):
        if self.territory == "left_top":
            # 左上區域
            self.min_x = 0
            self.max_x = 48
            self.min_y = 0
            self.max_y = 27
        elif self.territory == "right_top":
            # 右上區域
            self.min_x = 48
            self.max_x = 96
            self.min_y = 0
            self.max_y = 27
        elif self.territory == "left_bottom":
            # 左下區域
            self.min_x = 0
            self.max_x = 48
            self.min_y = 27
            self.max_y = 54
        elif self.territory == "right_bottom":
            # 右下區域
            self.min_x = 48
            self.max_x = 96
            self.min_y = 27
            self.max_y = 54
        else:
            # 無限制 (全地圖)
            self.min_x = 0
            self.max_x = 96
            self.min_y = 0
            self.max_y = 54
    
    """檢查行動範圍"""
    def is_in_territory(self, grid_x, grid_y):
       
        if self.territory is None:
            return True  # 無限制
        
        # 檢查精靈的3x3範圍是否都在領地內
        for offset_y in range(3):
            for offset_x in range(3):
                check_x = grid_x + offset_x
                check_y = grid_y + offset_y
                if not (self.min_x <= check_x < self.max_x and 
                        self.min_y <= check_y < self.max_y):
                    return False
        return True

    """離開出身點"""
    def leave_home(self):
        current_grid_x = self.rect.x // tile_size
        current_grid_y = self.rect.y // tile_size
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

    """追玩家"""
    def chase(self):
        current_grid_x = self.rect.x // tile_size
        current_grid_y = self.rect.y // tile_size
        player_grid_x = PXb // tile_size
        player_grid_y = PYb // tile_size
        
        if not self.is_in_territory(player_grid_x, player_grid_y):
            self.patrol_territory(current_grid_x, current_grid_y)
            return

        direction = a_star_search(
            (current_grid_x, current_grid_y),
            (player_grid_x, player_grid_y),
            MAP_DATA,
            tile_size
        )

        if direction:
            dx, dy = direction
            new_grid_x = current_grid_x + dx
            new_grid_y = current_grid_y + dy
            if self.is_in_territory(new_grid_x, new_grid_y):
                self.direction_x = dx * SPEED
                self.direction_y = dy * SPEED
            else:
                self.patrol_territory(current_grid_x, current_grid_y)
        else:
            self.patrol_territory(current_grid_x, current_grid_y)
    
    """領地巡邏"""
    def patrol_territory(self, current_grid_x, current_grid_y):
        available_directions = get_directions(current_grid_x, current_grid_y)
        
        # 過濾出在領地內的方向
        valid_directions = []
        for dx, dy in available_directions:
            new_grid_x = current_grid_x + dx
            new_grid_y = current_grid_y + dy
            if self.is_in_territory(new_grid_x, new_grid_y):
                valid_directions.append((dx, dy))
        
        if valid_directions:
            # 隨機選一個方向
            dx, dy = random.choice(valid_directions)
            self.direction_x = dx * SPEED
            self.direction_y = dy * SPEED
        else:
            # 沒有可走的方向，嘗試反向
            available_directions = get_directions(current_grid_x, current_grid_y)
            if available_directions:
                dx, dy = random.choice(available_directions)
                self.direction_x = dx * SPEED
                self.direction_y = dy * SPEED

    def mode_choose(self):
        current_grid_x = self.rect.x // tile_size
        current_grid_y = self.rect.y // tile_size
        if 36 <= current_grid_y <= 44 and 50 <= current_grid_x <= 63:
            self.leave_home()
        else:
            self.chase()

    def update(self):
        global tile_size
        EXb = self.rect.x
        EYb = self.rect.y
        current_grid_x = EXb // tile_size
        current_grid_y = EYb // tile_size

        # 走完一格時更新路徑
        if EXb % tile_size == 0 and EYb % tile_size == 0:
            self.path_update_counter += 1
            if self.path_update_counter >= self.path_update_interval:
                self.mode_choose()
                self.path_update_counter = 0
            else:
                available_directions = get_directions(current_grid_x, current_grid_y)
                if len(available_directions) > 2:
                    self.mode_choose()

        # 移動
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
            self.rect.x = EXb
            self.rect.y = EYb
            available_directions = get_directions(current_grid_x, current_grid_y)
            if available_directions:
                filtered = [d for d in available_directions
                            if d != (self.direction_x // SPEED, self.direction_y // SPEED)]
                if filtered:
                    dx, dy = random.choice(filtered)
                else:
                    dx, dy = random.choice(available_directions)
                self.direction_x = dx * SPEED
                self.direction_y = dy * SPEED

        # 邊界檢查
        self.rect.x = max(0, min(self.rect.x, WIDTH - 30))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - 30))


# ==================== 切換玩家圖片 ====================

def change_picture():
    global present_image2, present_image1
    while running:
        for i in range(0, 4):
            player.image = present_image1
            time.sleep(0.05)
        for i in range(0, 4):
            player.image = present_image2
            time.sleep(0.05)


# ==================== 初始化精靈 ====================

enemies = [
    Enemy(510, 430, E1, "left_top"),     
    Enemy(540, 430, E2, "right_top"),    
    Enemy(570, 430, E3, "left_bottom"),  
    Enemy(600, 430, E4, "right_bottom")  
]

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for enemy in enemies:
    all_sprites.add(enemy)

enemy_group = pygame.sprite.Group()
for enemy in enemies:
    enemy_group.add(enemy)

# ==================== 多線程 ====================

change_picture_thread = threading.Thread(target=change_picture)
change_picture_thread.start()

# ==================== 遊戲主迴圈 ====================

while running:
    clock.tick(FPS)

    # 事件處理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 碰撞偵測
    if pygame.sprite.spritecollide(player, enemy_group, False):
        Game_Over()
        running = False

    # 獲勝偵測
    if score == 695:
        Win()
        running = False

    # 更新畫面
    screen.fill(BLACK)
    refresh()

    # 更新角色
    all_sprites.update()

    # 畫面顯示
    pygame.draw.rect(screen, BLACK, pygame.Rect(50, 0, 30, 20))
    all_sprites.draw(screen)

    # 分數顯示
    show_score()
    pygame.display.update()

pygame.quit()