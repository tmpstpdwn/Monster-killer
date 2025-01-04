### MODULE IMPORTS ###

from random import choice
from settings import *
from pytmx.util_pygame import load_pygame
from player_enemy import *
from gun_bullet import *
from extra_sprites import *
from os.path import join, basename 
from os import walk

### Game CLASS ###

class Game:
    # Init necessary game variables.
    def __init__(self):

        # Pygame setup.
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags=pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False

        # Assets.
        self.load_frames()
        self.font = pygame.font.Font(join('..', 'fonts', 'pix.ttf'), 20)

        # Enemy spawn points.
        self.enemy_spawn_points = []

        # Sprites, groups and map.
        self.all_sprites = AllSprites()
        self.collition_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.setup()

        # Event and timers.
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 2000)

        # Music and sounds.
        music = pygame.mixer.Sound(join('..', 'audio', 'music.wav'))
        music.set_volume(0.1)
        music.play(loops = -1)
        self.impact = pygame.mixer.Sound(join('..', 'audio', 'impact.ogg'))
        self.impact.set_volume(0.2)

        # Other
        self.hit_count = 0

    # Preload images for frequently created and destroyed objects.
    def load_frames(self):
        self.bullet_surf = pygame.image.load(join('..', 'images', 'gun', 'bullet.png')).convert_alpha()
        self.enemy_frames = {'bat': [], 'blob': [], 'skeleton': []}
        for folder_path, sub_folders, files in walk(join('..', 'images', 'enemies')):
            if files:
                for file in sorted(files, key=lambda x: int(x.split('.')[0])):
                    file_path = join(folder_path, file)
                    surf = pygame.image.load(file_path).convert_alpha()
                    key = basename(folder_path)
                    self.enemy_frames[key].append(surf)

    # Load the map.
    def setup(self):
        map = load_pygame(join('..', 'data', 'maps', 'world.tmx'))
        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Ground((x*TILE_SIZE, y*TILE_SIZE), image, self.all_sprites)
        for obj in map.get_layer_by_name('Objects'):
            CollitionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collition_sprites))
        for obj in map.get_layer_by_name('Collisions'):
            CollitionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collition_sprites)
        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collition_sprites)
                self.gun = Gun(self.player, (self.all_sprites, self.bullet_sprites))
            else:
                self.enemy_spawn_points.append((obj.x, obj.y))

    # Event loop to look for events.
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == self.enemy_event and not self.game_over:
                enemy = choice(['bat', 'blob', 'skeleton'])
                pos = choice(self.enemy_spawn_points)
                Enemy(self.enemy_frames[enemy], pos, self.player, (self.all_sprites, self.enemy_sprites),\
                        self.collition_sprites)

    # Detect bullet collition with enemy.
    def bullet_collitions(self):
        for bullet in self.bullet_sprites:
            shot_enemies = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False)
            if shot_enemies:
                bullet.kill()
                for enemy in shot_enemies:
                    enemy.end()
                    self.impact.play()
                    self.hit_count += 1
                break

    # Detect player collision with enemy.
    def enemy_collitions(self):
        hit_enemies = pygame.sprite.spritecollide(self.player, self.enemy_sprites, False,\
                pygame.sprite.collide_mask)
        if hit_enemies:           
            self.impact.play()
            self.game_over = True

    # Detect collisions.
    def collitions(self):
        self.bullet_collitions()
        self.enemy_collitions()

    # Refresh screen and update objects.
    def update(self, dt):
        self.screen.fill('black')
        self.all_sprites.update(dt)

    # Display score.
    def score(self):
        score_text = self.font.render("Score: " + str(self.hit_count), False, 'black')
        if self.game_over:
            score_rect = score_text.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT - 50))
        else:
            score_rect = score_text.get_frect(topleft = (40, 40))
        self.screen.blit(score_text, score_rect)
        pygame.draw.rect(self.screen, 'black', score_rect.inflate(20, 20).move(0, -5), 2, 5)

    # Display "GAME OVER" when it does.
    def gameo(self):
        gameo_text = self.font.render("GAME OVER", False, 'red')
        gameo_text = pygame.transform.scale2x(gameo_text)
        gameo_rect = gameo_text.get_frect(center = (WINDOW_WIDTH/2, 100))
        self.screen.blit(gameo_text, gameo_rect)
        pygame.draw.rect(self.screen, 'black', gameo_rect.inflate(20, 20).move(0, -5), 3, 5)

    # Draw things on to, and update the screen
    def draw(self):
        self.all_sprites.draw(self.screen, self.player.rect.topleft)
        if self.game_over:
            self.gameo()
        self.score()
        pygame.display.update()

    # Run the game
    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            self.event_loop()
            if not self.game_over:
                self.update(dt)
                self.collitions()
            self.draw()

### END ###
