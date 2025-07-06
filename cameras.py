import pygame
import random
import sys
import pathlib
from tkinter import *
from tkinter import ttk
from screeninfo import get_monitors
from math import sin
from os import walk
from csv import reader
from debug import debug


def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter =',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(path):
    surface_list = []
    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = str(path) + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list


monitor_pars = []
for monitor in get_monitors():
    monitor_pars.append(monitor.width)
    monitor_pars.append(monitor.height)


WHITE = [255, 255, 255]
BROWN = [25, 11, 1]
GREY = [67, 67, 79]
WIDTH = 64*13
HEIGTH = 64*8
FPS = 60
TILESIZE = 64
GREEN = (0, 255, 0)
BLUE = '#0000FF'

# colors
BAR_HEIGHT = 20   # ui
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = '../graphics/font/joystix.ttf'
# UI_FONT = pygame.font.Font("graphics/font/joystix.ttf", 40)
UI_FONT_SIZE = 18

WATER_COLOR = '#71ddee'  # general colors
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

HEALTH_COLOR = 'red'  # ui colors
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# enemy
night_king = pathlib.Path(__file__).parent/'graphics'/'enemy'/'skeleton.png'
zombie = pathlib.Path(__file__).parent/'graphics'/'zombie'/'skeleton.png'

# pet
wolf = pathlib.Path(__file__).parent/'graphics'/'wolf'/'wolf.png'
wolf_left = pathlib.Path(__file__).parent/'graphics'/'wolf'/'wolf_left.png'
wolf_right = pathlib.Path(__file__).parent/'graphics'/'wolf'/'wolf_right.png'

# objects
black_image = pathlib.Path(
    __file__).parent/'graphics'/'objects'/'black.png'
grey_image = pathlib.Path(
    __file__).parent/'graphics'/'objects'/'grey.png'
brown_image = pathlib.Path(
    __file__).parent/'graphics'/'objects'/'brown.png'
exit_image = pathlib.Path(
    __file__).parent/'graphics'/'objects'/'exit.png'
wall_down_image = pathlib.Path(
    __file__).parent/'graphics'/'objects'/'wall_down.png'
wall_down_left_image = pathlib.Path(
    __file__).parent/'graphics'/'objects'/'wall_down_left.png'
wall_down_right_image = pathlib.Path(
    __file__).parent/'graphics'/'objects'/'wall_down_right.png'
wall_left_image = pathlib.Path(
    __file__).parent/'graphics'/'objects'/'wall_left.png'
wall_right_image = pathlib.Path(
    __file__).parent/'graphics'/'objects'/'wall_right.png'
wall_up_image = pathlib.Path(
    __file__).parent/'graphics'/'objects'/'wall_up.png'
tree_image = pathlib.Path(
    __file__).parent/'graphics'/'objects'/'tree.png'
cave_image = pathlib.Path(
    __file__).parent/'graphics'/'objects'/'cave.png'
cold_fireplace_image = pathlib.Path(
    __file__).parent/'graphics'/'cold_fireplace'/'cold_fireplace_0.png'
fireplace_image = pathlib.Path(
    __file__).parent/'graphics'/'fireplace'/'fireplace_0.png'
magic_tree = pathlib.Path(
    __file__).parent/'graphics'/'objects'/'magic_tree.png'
canvas = pathlib.Path(
    __file__).parent/'graphics'/'items_of_the_wild'/'canvas.png'
path_to_obstacle = pathlib.Path(
    __file__).parent/'graphics'/'objects'/'rock.png'
rock = pathlib.Path(
    __file__).parent/'graphics'/'objects'/'rock.png'
grass = pathlib.Path(
    __file__).parent/'graphics'/'objects'/'grass.png'
mushrooms = pathlib.Path(
    __file__).parent/'graphics'/'objects'/'mushrooms.png'
stone = pathlib.Path(
    __file__).parent/'graphics'/'objects'/'stone.png'

path_to_image = pathlib.Path(__file__).parent/'graphics'/'player'/'down.png'
path_to_image_Act = pathlib.Path(__file__).parent/'graphics'/'player'

# weapon
weapon_data = {
    'sword': {'cooldown': 100,
              'damage': 15,
              'graphic': '../graphics/weapons/sword/full.png'},
}


weapon_data = {
    'sword': {'cooldown': 100,
              'damage': 15,
              'graphic': '../graphics/weapons/sword/full.png'},
    'fireball': {'cooldown': 100,
                   'damage': 15,
                   'graphic': '../graphics/weapons/fireball/down.png'},
}

player_health = 100
number_of_arrows = 10
number_of_elixirs = 0
number_of_grass = 0
number_of_mushrooms = 0
number_of_enemies = 0
is_active = 0
is_finished = 0
is_active_1 = 0
is_finished_1 = 0
is_active_2 = 0
is_finished_2 = 0

snow_list = []
# Пройдемся 50 раз циклом и добавьм снежинки в рандомную позицию x,y
for i in range(350):
    x = random.randrange(0, WIDTH)
    y = random.randrange(0, HEIGTH)
    snow_list.append([x, y])

coords = [0]


class Player(pygame.sprite.Sprite):
    '''Создаёт персонажа'''
    def __init__(self,
                 pos,
                 group,
                 obstacle_sprites,
                 create_attack,
                 destroy_attack,
                 take_bow,
                 put_off_bow,
                 heal,
                 remove_heal,
                #  start_quest,
                #  passage,
                 ):
        super().__init__(group)
        global player_health
        # image and rect
        self.image = pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'down'/'down_0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2()
        self.obstacle_sprites = obstacle_sprites
        self.hitbox = self.rect.inflate(-26, -26)
        # healing
        self.heal = heal
        self.remove_heal = remove_heal
        self.healing = False
        self.heal_cooldown = 1000
        self.heal_time = None
        # attacks
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        # shooting
        self.take_bow = take_bow
        self.put_off_bow = put_off_bow
        self.shooting = False
        self.shoot_cooldown = 1000
        self.shoot_time = None
        # quests
        # self.start_quest = start_quest
        # parametres
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.status = 'down_idle'
        self.index = 0
        self.animation_speed = 0.1
        self.animations = {'up': [pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'up'/'up_0.png').convert_alpha(),
                                  pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'up'/'up_1.png').convert_alpha(),
                                  pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'up'/'up_2.png').convert_alpha(),
                                  pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'up'/'up_3.png').convert_alpha()],
                           'down': [pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'down'/'down_0.png').convert_alpha(),
                                    pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'down'/'down_1.png').convert_alpha(),
                                    pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'down'/'down_2.png').convert_alpha(),
                                    pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'down'/'down_3.png').convert_alpha()],
                           'left': [pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'left'/'left_0.png').convert_alpha(),
                                    pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'left'/'left_1.png').convert_alpha(),
                                    pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'left'/'left_2.png').convert_alpha(),
                                    pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'left'/'left_3.png').convert_alpha()],
                           'right': [pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'right'/'right_0.png').convert_alpha(),
                                     pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'right'/'right_1.png').convert_alpha(),
                                     pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'right'/'right_2.png').convert_alpha(),
                                     pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'right'/'right_3.png').convert_alpha()],
                           'right_idle': [pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'right_idle'/'right_idle_0.png').convert_alpha(),
                                          pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'right_idle'/'right_idle_1.png').convert_alpha()],
                           'left_idle': [pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'left_idle'/'left_idle_0.png').convert_alpha(),
                                         pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'left_idle'/'left_idle_1.png').convert_alpha()],
                           'up_idle': [pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'up_idle'/'up_idle_0.png').convert_alpha(),
                                       pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'up_idle'/'up_idle_1.png').convert_alpha()],
                           'down_idle': [pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'down_idle'/'down_idle_0.png').convert_alpha(),
                                         pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'down_idle'/'down_idle_1.png').convert_alpha(),
                                         pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'down_idle'/'down_idle_2.png').convert_alpha(),
                                         pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'down_idle'/'down_idle_3.png').convert_alpha(),],
                           'right_attack': [pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'right_attack'/'right_attack_0.png').convert_alpha(),
                                            pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'right_attack'/'right_attack_1.png').convert_alpha(),
                                            pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'right_attack'/'right_attack_2.png').convert_alpha(),
                                            pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'right_attack'/'right_attack_3.png').convert_alpha(),],
                           'left_attack': [pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'left_attack'/'left_attack_0.png').convert_alpha(),
                                           pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'left_attack'/'left_attack_1.png').convert_alpha(),
                                           pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'left_attack'/'left_attack_2.png').convert_alpha(),
                                           pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'left_attack'/'left_attack_3.png').convert_alpha(),],
                           'up_attack': [pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'up_attack'/'up_attack_0.png').convert_alpha(),
                                         pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'up_attack'/'up_attack_1.png').convert_alpha(),
                                         pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'up_attack'/'up_attack_2.png').convert_alpha(),
                                         pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'up_attack'/'up_attack_3.png').convert_alpha(),],
                           'down_attack': [pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'down_attack'/'down_attack_0.png').convert_alpha(),
                                           pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'down_attack'/'down_attack_1.png').convert_alpha(),
                                           pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'down_attack'/'down_attack_2.png').convert_alpha(),
                                           pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'down_attack'/'down_attack_3.png').convert_alpha(),
                                           pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'down_attack'/'down_attack_4.png').convert_alpha(),
                                           pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'down_attack'/'down_attack_5.png').convert_alpha(),],
                            'right_shoot': [
                                            pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'right_shoot'/'right_shoot_2.png').convert_alpha(),],
                            'left_shoot': [
                                           pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'left_shoot'/'left_shoot_2.png').convert_alpha(),],
                            'down_shoot': [
                                           pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'down_shoot'/'down_shoot_1.png').convert_alpha(),],
                            'up_shoot': [
                                         pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'up_shoot'/'up_shoot_1.png').convert_alpha(),]}
        self.id = id
        self.stats = {'health': 100,
                      'energy': 60,
                      'attack': 10,
                      'speed': 4}
        # self.health = self.stats['health']
        self.health = None
        self.energy = self.stats['energy']
        self.speed = self.stats['speed']
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500
        # self.passage = passage
        self.set_health()

    def set_health(self):
        global player_health
        self.health = player_health

    def input(self):
        global coords
        global is_active
        global is_finished
        global number_of_mushrooms
        global number_of_elixirs

        global is_active_1
        global is_finished_1
        global number_of_grass
        global number_of_arrows

        global is_active_2
        global is_finished_2
        global number_of_enemies
        if not self.attacking and not self.shooting and not self.healing:
            keys = pygame.key.get_pressed()
            # Вертикальное направление
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0
            if keys[pygame.K_SPACE] and not self.attacking:
                self.create_attack()
                self.animation_speed = 0.001
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
            if keys[pygame.K_q] and not self.shooting and number_of_arrows != 0:
                self.direction.x = 0
                self.direction.y = 0
                self.shooting = True
                self.shoot_time = pygame.time.get_ticks()
                self.take_bow()
            if keys[pygame.K_1] and self.health < 100 and number_of_elixirs != 0:
                self.health += 20
                self.healing = True
                number_of_elixirs += -1
                self.direction.x = 0
                self.direction.y = 0
                if self.health > 100:
                    self.health = 100
                self.heal_time = pygame.time.get_ticks()
                self.heal()
            if keys[pygame.K_m]:
                coords.append(self.rect.center)

    def get_status(self):
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status and not 'shoot' in self.status:
                self.status = self.status + '_idle'
        # attacking
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')
        # shooting
        if self.shooting:
            self.direction.x = 0
            self.direction.y = 0
            if not 'shoot' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_shoot')
                elif 'attack' in self.status:
                    self.status = self.status.replace('_attack', '_shoot')
                else:
                    self.status = self.status + '_shoot'
        else:
            if 'shoot' in self.status:
                self.status = self.status.replace('_shoot', '')

    def collisions(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x*speed
        self.collisions('horizontal')
        self.hitbox.y += self.direction.y*speed
        self.collisions('vertical')
        self.rect.center = self.hitbox.center

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time-self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True
        if self.healing:
            if current_time-self.heal_time >= self.heal_cooldown:
                self.healing = False
                self.remove_heal()
        if self.shooting:
            if current_time-self.shoot_time >= self.shoot_cooldown:
                self.shooting = False
                self.put_off_bow()

    def animate(self):
        if '_idle' in self.status:
            self.animation_speed = 0.05
        if '_attack' in self.status:
            self.animation_speed = 0.3
        if '_shoot' in self.status:
            self.animation_speed = 0.1
        if '_idle' not in self.status and '_attack' not in self.status and '_shoot' not in self.status:
            if self.direction.x == 1 or self.direction.x == -1:
                self.animation_speed = 0.13
            else:
                self.animation_speed = 0.1
        animation = self.animations[self.status]
        self.index += self.animation_speed
        if self.index >= len(animation):
            self.index = 0
        self.image = animation[int(self.index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = 15 + base_damage
        return weapon_damage

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def restart(self):
        global player_health
        global number_of_enemies
        global number_of_grass
        global number_of_mushrooms
        global number_of_arrows
        global number_of_elixirs
        global is_active
        global is_active_1
        global is_active_2
        if self.health <= 0:
            player_health = 100
            number_of_arrows = 0
            number_of_elixirs = 0
            number_of_enemies = 0
            number_of_grass = 0
            number_of_mushrooms = 0
            number_of_arrows = 0
            number_of_elixirs = 0
            is_active = 0
            is_active_1 = 0
            is_active_2 = 0
            game = Game('layout_0')
            game.run()

    def update(self):
        self.get_status()
        self.input()
        self.cooldowns()
        self.animate()
        self.move(self.speed)
        self.restart()


class Wildlings(pygame.sprite.Sprite):
    def __init__(self, pos, type, group):
        super().__init__(group)
        self.type = type
        self.images_tormund = []
        self.images_karsi = []
        self.images_orell = []
        self.images_woodman = [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'tormund'/'Woodman'/'left_idle_0.png').convert_alpha(),
                               pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'tormund'/'Woodman'/'left_idle_1.png').convert_alpha(),
                               pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'tormund'/'Woodman'/'left_idle_2.png').convert_alpha(),
                               pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'tormund'/'Woodman'/'left_idle_3.png').convert_alpha(),
                               pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'tormund'/'Woodman'/'left_idle_4.png').convert_alpha(),
                               pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'tormund'/'Woodman'/'left_idle_5.png').convert_alpha(),
                               pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'tormund'/'Woodman'/'left_idle_5.png').convert_alpha(),]
        self.images_walker = [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'tormund'/'Walker'/'left_0.png').convert_alpha(),
                              pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'tormund'/'Walker'/'left_1.png').convert_alpha(),
                              pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'tormund'/'Walker'/'left_2.png').convert_alpha(),]
        self.index = 0
        self.images_tormund.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'tormund'/'tormund_0.png').convert_alpha())
        self.images_tormund.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'tormund'/'tormund_1.png').convert_alpha())
        self.images_karsi.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'tormund'/'karsi_0.png').convert_alpha())
        self.images_karsi.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'tormund'/'karsi_1.png').convert_alpha())
        self.images_orell.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'tormund'/'orell_0.png').convert_alpha())
        self.images_orell.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'tormund'/'orell_1.png').convert_alpha())
        self.animation_speed = 0.03
        if self.type == 'tormund':
            self.image = self.images_tormund[self.index]
        if self.type == 'karsi':
            self.image = self.images_karsi[self.index]
        if self.type == 'orell':
            self.image = self.images_orell[self.index]
        if self.type == 'woodman':
            self.image = self.images_woodman[self.index]
        if self.type == 'walker':
            self.image = self.images_walker[self.index]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -130)

    def animate(self):
        if self.type == 'tormund':
            self.index += self.animation_speed
            if self.index >= len(self.images_tormund):
                self.index = 0
            self.image = self.images_tormund[int(self.index)]
        elif self.type == 'karsi':
            self.index += self.animation_speed
            if self.index >= len(self.images_karsi):
                self.index = 0
            self.image = self.images_karsi[int(self.index)]
        elif self.type == 'orell':
            self.index += self.animation_speed
            if self.index >= len(self.images_orell):
                self.index = 0
            self.image = self.images_orell[int(self.index)]
        elif self.type == 'woodman':
            self.index += self.animation_speed
            if self.index > 2:
                self.animation_speed = 0.17
            if self.index <= 2:
                self.animation_speed = 0.02
            if self.index >= len(self.images_woodman):
                self.index = 0
            self.image = self.images_woodman[int(self.index)]
        elif self.type == 'walker':
            self.index += self.animation_speed
            if self.index >= len(self.images_walker):
                self.index = 0
            self.image = self.images_walker[int(self.index)]
            # if self.index > 2:
            #     self.animation_speed = 0.17
            # if self.index <= 2:
            #     self.animation_speed = 0.02
            # if self.index >= len(self.images_woodman):
            #     self.index = 0
            # self.image = self.images_woodman[int(self.index)]

    def update(self):
        self.animate()


class Archer(pygame.sprite.Sprite):
    def __init__(self, pos, group, shoot, put_off_shoot):
        super().__init__(group)
        self.image = pygame.image.load(pathlib.Path(__file__).parent/'player'/'Jon'/'down'/'down_0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.shoot = shoot
        self.put_off_shoot = put_off_shoot
        self.index = 0
        self.animations = [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'tormund'/'archer'/'left_idle'/'left_idle_0.png').convert_alpha(),
                           pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'tormund'/'archer'/'left_idle'/'left_idle_1.png').convert_alpha(),
                           pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'tormund'/'archer'/'left_idle'/'left_idle_2.png').convert_alpha(),
                           pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'tormund'/'archer'/'left_shoot'/'left_shoot_2.png').convert_alpha()]
        self.pos = pos
        self.animation_speed = 0.03
        self.image = self.animations[self.index]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -130)

    def animate(self):
        self.index += self.animation_speed
        if self.index == 2:
            self.animation_speed = 0.0001
        if self.index >= len(self.animations):
            self.index = 0
        self.image = self.animations[int(self.index)]
        if self.image == self.animations[3]:
            self.shoot()
        if self.image != self.animations[3]:
            self.put_off_shoot()

    def update(self):
        self.animate()


class Quests(pygame.sprite.Sprite):
    def __init__(self, npc, groups, player_npc, quest_name):
        super().__init__(groups)
        self.npc = npc
        self.player_npc = player_npc
        self.quest_name = quest_name
        self.image = pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'symbols'/'take_quest.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=self.npc.rect.midtop+pygame.math.Vector2(0, 10))

    def statement(self):
        npc_vec = pygame.math.Vector2(self.npc.rect.center)
        player_vec = pygame.math.Vector2(self.player_npc.rect.center)
        distance = (npc_vec - player_vec).magnitude()
        if distance <= 100:
            debug('Нажмите Y, чтобы принять или завершить задание!')

    def quest(self):
        global is_active
        global is_finished
        global number_of_mushrooms
        global number_of_elixirs

        global is_active_1
        global is_finished_1
        global number_of_grass
        global number_of_arrows

        global is_active_2
        global is_finished_2
        global number_of_enemies
        npc_vec = pygame.math.Vector2(self.npc.rect.center)
        player_vec = pygame.math.Vector2(self.player_npc.rect.center)
        distance = (npc_vec - player_vec).magnitude()
        keys = pygame.key.get_pressed()
        if self.quest_name == 'grass':
            if is_active_1 == 0:
                if keys[pygame.K_y]:
                    is_active_1 = 1
            if is_active_1 == 1 and is_finished_1 == 0 and number_of_grass < 5:
                self.image = pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'symbols'/'text_2.png').convert_alpha()
            if is_active_1 == 1 and is_finished_1 == 0 and number_of_grass >= 5:
                if distance <= 100:
                    if keys[pygame.K_y]:
                        is_finished_1 = 1
                        number_of_arrows = 10
                        self.kill()
        if self.quest_name == 'mushrooms':
            if is_active == 0:
                if keys[pygame.K_y]:
                    is_active = 1
            if is_active == 1 and is_finished == 0 and number_of_mushrooms < 5:
                self.image = pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'symbols'/'text_1.png').convert_alpha()
            if is_active == 1 and is_finished == 0 and number_of_mushrooms >= 5:
                if distance <= 100:
                    if keys[pygame.K_y]:
                        is_finished = 1
                        number_of_elixirs = 10
                        self.kill()
        if self.quest_name == 'enemies':
            if is_active_2 == 0:
                if keys[pygame.K_y]:
                    is_active_2 = 1
            if is_active_2 == 1 and is_finished_2 == 0 and number_of_enemies < 5:
                self.image = pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'symbols'/'text_3.png').convert_alpha()
            if is_active_2 == 1 and is_finished_2 == 0 and number_of_enemies >= 1:
                if distance <= 100:
                    if keys[pygame.K_y]:
                        is_finished_2 = 1
                        self.kill()

    def update(self):
        self.statement()
        self.quest()


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect(center=player.rect.center)
        path_to_weapon = pathlib.Path(__file__).parent/'graphics'/'weapons'/'sword'/'full_empty.png'
        self.image = pygame.image.load(path_to_weapon).convert_alpha()


class Heal(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'heal'
        self.image = pygame.Surface((40, 40))
        self.images = []
        self.images.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'weapons'/'heal'/'heal_0.png').convert_alpha())
        self.images.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'weapons'/'heal'/'heal_1.png').convert_alpha())
        self.images.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'weapons'/'heal'/'heal_2.png').convert_alpha())
        self.images.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'weapons'/'heal'/'heal_3.png').convert_alpha())
        self.images.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'weapons'/'heal'/'heal_4.png').convert_alpha())
        self.images.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'weapons'/'heal'/'heal_5.png').convert_alpha())
        self.index = 0
        self.animation_speed = 0.1
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(midtop=player.rect.midtop+pygame.math.Vector2(0, -60))

    def animate(self):
        self.index += self.animation_speed
        if self.index >= len(self.images):
            self.index = 0
            self.kill()
        self.image = self.images[int(self.index)]

    def update(self):
        self.animate()


class WeaponBow(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'bow'
        self.image = pygame.Surface((40, 40))
        direction = player.status.split('_')[0]
        # bow
        path_to_weapon = pathlib.Path(__file__).parent/'graphics'/'weapons'/'bow'/f'bow_{direction}.png'
        self.image = pygame.image.load(path_to_weapon).convert_alpha()
        # arrow
        path_to_arrow = pathlib.Path(__file__).parent/'graphics'/'weapons'/'bow'/f'arrow_{direction}.png'
        self.image_arrow = pygame.image.load(path_to_arrow).convert_alpha()
        if direction == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright+pygame.math.Vector2(-40, 23))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft+pygame.math.Vector2(40, 23))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom+pygame.math.Vector2(-22, -40))
        else:
            self.rect = self.image.get_rect(midbottom=player.rect.midtop +pygame.math.Vector2(20, 60))


class Arrow(pygame.sprite.Sprite):
    def __init__(self, player, groups, obstacle_sprites):
        super().__init__(groups)
        self.sprite_type = 'arrow'
        self.display_surface = pygame.display.get_surface()
        self.image = pygame.Surface((40, 40))
        self.obstacle_sprites = obstacle_sprites
        self.status = player.status.split('_')[0]
        self.speed = 5
        path_to_arrow = pathlib.Path(__file__).parent/'graphics'/'weapons'/'bow'/f'arrow_{self.status}.png'
        self.image = pygame.image.load(path_to_arrow).convert_alpha()
        if self.status == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright+pygame.math.Vector2(-30, 0))
        elif self.status == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft+pygame.math.Vector2(30, 0))
        elif self.status == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom+pygame.math.Vector2(10, -20))
        else:
            self.rect = self.image.get_rect(midbottom=player.rect.midtop +pygame.math.Vector2(-10, 60))
        self.hitbox = self.rect

    def collisions(self, dir):
        allowed_sprites = ['boundary', 'tormund', 'fireplace', 'grass']
        if dir == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.type not in allowed_sprites:
                    if sprite.hitbox.colliderect(self.hitbox):
                        self.kill()
        if dir == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.type not in allowed_sprites:
                    if sprite.hitbox.colliderect(self.hitbox):
                        self.kill()

    def move(self, speed):
        if self.status == 'right':
            self.hitbox.x += 1*speed
            self.collisions('horizontal')
        elif self.status == 'left':
            self.hitbox.x += -1*speed
            self.collisions('horizontal')
        elif self.status == 'down':
            self.hitbox.y += 1*speed
            self.collisions('vertical')
        else:
            self.hitbox.y += -1*speed
            self.collisions('vertical')

    def update(self):
        self.move(self.speed)


class Arrow_2(pygame.sprite.Sprite):
    def __init__(self, npc, groups, obstacle_sprites):
        super().__init__(groups)
        self.sprite_type = 'arrow'
        self.display_surface = pygame.display.get_surface()
        self.image = pygame.Surface((40, 40))
        self.obstacle_sprites = obstacle_sprites
        self.status = 'left'
        self.speed = 5
        path_to_arrow = pathlib.Path(__file__).parent/'graphics'/'weapons'/'bow'/f'arrow_{self.status}.png'
        self.image = pygame.image.load(path_to_arrow).convert_alpha()
        self.rect = self.image.get_rect(midright=npc.rect.midleft+pygame.math.Vector2(30, 0))
        self.hitbox = self.rect

    def collisions(self, dir):
        allowed_sprites = ['boundary', 'tormund', 'fireplace', 'grass']
        if dir == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.type not in allowed_sprites:
                    if sprite.hitbox.colliderect(self.hitbox):
                        self.kill()
        # if dir == 'vertical':
        #     for sprite in self.obstacle_sprites:
        #         if sprite.type not in allowed_sprites:
        #             if sprite.hitbox.colliderect(self.hitbox):
        #                 self.kill()

    def move(self, speed):
        self.hitbox.x += -1*speed
        self.collisions('horizontal')

    def update(self):
        self.move(self.speed)


class UI:
    def __init__(self, layout_name):
        self.layout_name = layout_name
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.SysFont(UI_FONT,
                                        UI_FONT_SIZE)
        self.health_bar_rect = pygame.Rect(10,
                                           10,
                                           HEALTH_BAR_WIDTH,
                                           BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10,
                                           34,
                                           ENERGY_BAR_WIDTH,
                                           BAR_HEIGHT)

    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        ratio = current/max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_symbols(self):
        bg_rect = pygame.Rect(10, 30, 50, 50)
        bg = pygame.draw.rect(self.display_surface, '#95500C', bg_rect)
        frame = pygame.draw.rect(self.display_surface, '#853B0A', bg_rect, 5)
        char_img = pygame.image.load(pathlib.Path(__file__).parent/'avatars'/'avatar_1.png').convert_alpha()
        char_img_small = pygame.transform.scale(char_img, (50, 50))
        char_rect = char_img_small.get_rect(topleft=(bg.topleft))
        self.display_surface.blit(char_img_small, char_rect)

        bg_rect_1 = pygame.Rect(40, 70, 30, 30)
        bg_1 = pygame.draw.rect(self.display_surface, '#95500C', bg_rect_1)
        frame = pygame.draw.rect(self.display_surface, '#853B0A', bg_rect_1, 5)
        wolf_img = pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'wolf'/'wolf_symbol.png').convert_alpha()
        wolf_img_small = pygame.transform.scale(wolf_img, (30, 30))
        wolf_rect = char_img_small.get_rect(topleft=(bg_1.topleft))
        self.display_surface.blit(wolf_img_small, wolf_rect)

    def show_sword(self):
        bg_rect = pygame.Rect(20, HEIGTH-100, 64, 64)
        bg = pygame.draw.rect(self.display_surface, '#95500C', bg_rect)
        frame = pygame.draw.rect(self.display_surface, '#853B0A', bg_rect, 5)
        weapon_img = pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'weapons'/'sword'/'full_0.png').convert_alpha()
        weapon_img_small = pygame.transform.scale(weapon_img, (64, 64))
        weapon_rect = weapon_img_small.get_rect(center=(bg.center))
        self.display_surface.blit(weapon_img, weapon_rect)

        text_surf = self.font.render(('Space'), False, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=(20+32, HEIGTH-84+64))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)
        self.display_surface.blit(text_surf, text_rect)

    def show_bow(self):
        global number_of_arrows
        bg_rect = pygame.Rect(84, HEIGTH-100, 64, 64)
        bg = pygame.draw.rect(self.display_surface, '#95500C', bg_rect)
        frame = pygame.draw.rect(self.display_surface, '#853B0A', bg_rect, 5)
        weapon_img = pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'weapons'/'bow'/'full.png').convert_alpha()
        weapon_img_small = pygame.transform.scale(weapon_img, (64, 64))
        weapon_rect = weapon_img_small.get_rect(center=(bg.center))
        self.display_surface.blit(weapon_img, weapon_rect)

        text_surf = self.font.render(('Q'), False, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=(20+32+64, HEIGTH-84+64))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)
        self.display_surface.blit(text_surf, text_rect)
        text_surf_1 = self.font.render((f'{number_of_arrows}/10'), False, TEXT_COLOR)
        text_rect_1 = text_surf_1.get_rect(center=(20+32+64+12, HEIGTH-84+64-20-5))
        self.display_surface.blit(text_surf_1, text_rect_1)

    def show_elixir(self):
        global number_of_elixirs
        bg_rect = pygame.Rect(84+64, HEIGTH-100, 64, 64)
        bg = pygame.draw.rect(self.display_surface, '#95500C', bg_rect)
        frame = pygame.draw.rect(self.display_surface, '#853B0A', bg_rect, 5)
        el_img = pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'objects'/'elixir.png').convert_alpha()
        el_img_small = pygame.transform.scale(el_img, (50, 50))
        el_rect = el_img_small.get_rect(center=(bg.center))
        self.display_surface.blit(el_img_small, el_rect)

        text_surf = self.font.render(('1'), False, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=(20+32+64+64, HEIGTH-84+64))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)
        self.display_surface.blit(text_surf, text_rect)
        text_surf_1 = self.font.render((f'{number_of_elixirs}/5'), False, TEXT_COLOR)
        text_rect_1 = text_surf_1.get_rect(center=(20+32+64+64+12, HEIGTH-84+64-20-5))
        self.display_surface.blit(text_surf_1, text_rect_1)

    def show_journal(self):
        bg_rect = pygame.Rect(212, HEIGTH-100, 64, 64)
        bg = pygame.draw.rect(self.display_surface, '#95500C', bg_rect)
        frame = pygame.draw.rect(self.display_surface, '#853B0A', bg_rect, 5)
        journal_img = pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'objects'/'quests.png').convert_alpha()
        journal_img_small = pygame.transform.scale(journal_img, (64, 37))
        weapon_rect = journal_img_small.get_rect(center=(bg.center))
        self.display_surface.blit(journal_img_small, weapon_rect)

        text_surf = self.font.render(('j'), False, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=(84+64+64+32, HEIGTH-84+64))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)
        self.display_surface.blit(text_surf, text_rect)

    def open_journal(self):
        global is_active
        global is_active_1
        global is_active_2
        global number_of_mushrooms
        global number_of_grass
        bg_rect = pygame.Rect(WIDTH-300, HEIGTH-300, 300, 300)
        bg = pygame.draw.rect(self.display_surface, '#95500C', bg_rect)
        frame = pygame.draw.rect(self.display_surface, '#853B0A', bg_rect, 5)
        line_1 = pygame.draw.line(self.display_surface, '#853B0A', (WIDTH-300+150, HEIGTH-300+30), (WIDTH-300+150, HEIGTH), 5)
        line_2 = pygame.draw.line(self.display_surface, '#853B0A', (WIDTH-300, HEIGTH-300+30), (WIDTH, HEIGTH-300+30), 5)
        text_1_surf = self.font.render(('Список задач'), False, TEXT_COLOR)
        text_1_rect = text_1_surf.get_rect(center=(WIDTH-150, HEIGTH-300+15))
        self.display_surface.blit(text_1_surf, text_1_rect)
        line_3 = pygame.draw.line(self.display_surface, '#853B0A', (WIDTH-300, HEIGTH-300+30+90), (WIDTH, HEIGTH-300+30+90), 5)
        line_3 = pygame.draw.line(self.display_surface, '#853B0A', (WIDTH-300, HEIGTH-300+30+90+90), (WIDTH, HEIGTH-300+30+90+90), 5)
        if is_active == 1:
            rect_1 = pygame.Rect(WIDTH-300, HEIGTH-300+30, 150, 90)
            mushrooms_bg = pygame.draw.rect(self.display_surface, '#95500C', rect_1)
            mushrooms_frame = pygame.draw.rect(self.display_surface, '#853B0A', rect_1, 3)
            mushrooms_img = pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'objects'/'mushrooms.png').convert_alpha()
            mushrooms_img_small = pygame.transform.scale(mushrooms_img, (64, 64))
            mushrooms_rect = mushrooms_img_small.get_rect(center=(mushrooms_bg.center))
            self.display_surface.blit(mushrooms_img, mushrooms_rect)
            text_surf_mushrooms = self.font.render((f'{number_of_mushrooms}/5'), False, TEXT_COLOR)
            text_rect_mushrooms = text_surf_mushrooms.get_rect(center=(WIDTH-300+120, HEIGTH-300+30+75))
            self.display_surface.blit(text_surf_mushrooms, text_rect_mushrooms)
            if is_finished == 1:
                mushrooms_fin_text_surf = self.font.render(('Задача выполнена'), False, TEXT_COLOR)
                mushrooms_fin_text_rect = mushrooms_fin_text_surf.get_rect(center=(WIDTH-75, HEIGTH-300+30+45))
                self.display_surface.blit(mushrooms_fin_text_surf, mushrooms_fin_text_rect)
        if is_active_1 == 1:
            rect_2 = pygame.Rect(WIDTH-300, HEIGTH-300+30+90, 150, 90)
            grass_bg = pygame.draw.rect(self.display_surface, '#95500C', rect_2)
            grass_frame = pygame.draw.rect(self.display_surface, '#853B0A', rect_2, 3)
            grass_img = pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'objects'/'grass.png').convert_alpha()
            grass_img_small = pygame.transform.scale(grass_img, (64, 64))
            grass_rect = grass_img_small.get_rect(center=(grass_bg.center))
            self.display_surface.blit(grass_img, grass_rect)
            text_surf_grass = self.font.render((f'{number_of_grass}/5'), False, TEXT_COLOR)
            text_rect_grass = text_surf_grass.get_rect(center=(WIDTH-300+120, HEIGTH-300+30+75+90))
            self.display_surface.blit(text_surf_grass, text_rect_grass)
            if is_finished_1 == 1:
                grass_fin_text_surf = self.font.render(('Задача выполнена'), False, TEXT_COLOR)
                grass_fin_text_rect = grass_fin_text_surf.get_rect(center=(WIDTH-75, HEIGTH-300+30+45+90))
                self.display_surface.blit(grass_fin_text_surf, grass_fin_text_rect)
        if is_active_2 == 1:
            rect_3 = pygame.Rect(WIDTH-300, HEIGTH-300+30+90+90, 150, 90)
            en_bg = pygame.draw.rect(self.display_surface, '#95500C', rect_3)
            en_frame = pygame.draw.rect(self.display_surface, '#853B0A', rect_3, 3)
            en_img = pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'enemy'/'down.png').convert_alpha()
            en_img_small = pygame.transform.scale(en_img, (64, 64))
            en_rect = en_img_small.get_rect(center=(en_bg.center))
            self.display_surface.blit(en_img, en_rect)
            text_surf_en = self.font.render((f'{number_of_enemies}/1'), False, TEXT_COLOR)
            text_rect_en = text_surf_en.get_rect(center=(WIDTH-300+120, HEIGTH-300+30+75+90+90))
            self.display_surface.blit(text_surf_en, text_rect_en)
            if is_finished_2 == 1:
                en_fin_text_surf = self.font.render(('Задача выполнена'), False, TEXT_COLOR)
                en_fin_text_rect = en_fin_text_surf.get_rect(center=(WIDTH-75, HEIGTH-300+30+45+90+90))
                self.display_surface.blit(en_fin_text_surf, en_fin_text_rect)

    def show_map(self):
        bg_rect = pygame.Rect(212+64, HEIGTH-100, 64, 64)
        bg = pygame.draw.rect(self.display_surface, '#95500C', bg_rect)
        frame = pygame.draw.rect(self.display_surface, '#853B0A', bg_rect, 5)
        map_img = pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'objects'/'map.png').convert_alpha()
        map_img_small = pygame.transform.scale(map_img, (53, 45))
        map_rect = map_img_small.get_rect(center=(bg.center))
        self.display_surface.blit(map_img_small, map_rect)

        text_surf = self.font.render(('m'), False, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=(84+64+64+32+64, HEIGTH-84+64))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)
        self.display_surface.blit(text_surf, text_rect)

    def open_map(self):
        global coords
        bg_rect = pygame.Rect(WIDTH-300, HEIGTH-300, 300, 300)
        bg = pygame.draw.rect(self.display_surface, '#95500C', bg_rect)
        frame = pygame.draw.rect(self.display_surface, '#853B0A', bg_rect, 5)
        text_surf = self.font.render(('Карта'), False, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=(WIDTH-150, HEIGTH-300+15))
        self.display_surface.blit(text_surf, text_rect)

        rect_1 = pygame.Rect(WIDTH-300, HEIGTH-300, 150, 90)
        if self.layout_name == 'layout_0':
            map_img = pygame.image.load(pathlib.Path(__file__).parent/'levels'/'level_0'/'map_big.png').convert_alpha()
        elif self.layout_name == 'layout_1':
            map_img = pygame.image.load(pathlib.Path(__file__).parent/'levels'/'level_1'/'map_big.png').convert_alpha()
        elif self.layout_name == 'layout_2':
            map_img = pygame.image.load(pathlib.Path(__file__).parent/'levels'/'level_2'/'map_big.png').convert_alpha()
        elif self.layout_name == 'layout_3':
            map_img = pygame.image.load(pathlib.Path(__file__).parent/'levels'/'level_3'/'map_big.png').convert_alpha()
        elif self.layout_name == 'cave':
            map_img = pygame.image.load(pathlib.Path(__file__).parent/'levels'/'cave'/'cave.png').convert_alpha()
        map_img_small = pygame.transform.scale(map_img, (240, 240))
        map_rect = map_img_small.get_rect(center=(bg.center))
        self.display_surface.blit(map_img_small, map_rect)
        if self.layout_name != 'cave':
            coordinates = coords[-1]
            coord_x = coordinates[0]-288
            coord_y = coordinates[1]-288
            pygame.draw.circle(self.display_surface,
                               BLUE,
                               (WIDTH-270+(coord_x)/4.3,
                                HEIGTH-270+(coord_y)/4),
                               4)
        else:
            coordinates = coords[-1]
            coord_x = coordinates[0]-288
            coord_y = coordinates[1]-288
            pygame.draw.circle(self.display_surface,
                               BLUE,
                               (WIDTH-270+(coord_x)/4.3,
                                HEIGTH-460+(coord_y)/4),
                               4)

    def display(self, player):
        global number_of_mushrooms
        global player_health
        self.show_bar(player.health,
                      player.stats['health'],
                      self.health_bar_rect,
                      HEALTH_COLOR)
        self.show_sword()
        self.show_bow()
        self.show_elixir()
        self.show_symbols()
        self.show_journal()
        self.show_map()
        if pygame.key.get_pressed()[pygame.K_j]:
            self.open_journal()
        if pygame.key.get_pressed()[pygame.K_m]:
            self.open_map()


class Wolf(pygame.sprite.Sprite):
    def __init__(self, pos, group, obstacle_sprites):
        super().__init__(group)
        self.image = pygame.image.load(str(wolf)).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.index = 0
        self.animation_speed = 0.2
        self.speed = 2
        self.obstacle_sprites = obstacle_sprites
        self.hitbox = self.rect.inflate(-30, -30)
        self.direction = pygame.math.Vector2()
        self.sprite_type = 'wolf'
        self.images_1 = []
        self.images_1.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'wolf'/'wolf_right_0.png').convert_alpha())
        self.images_1.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'wolf'/'wolf_right_1.png').convert_alpha())
        self.images_1.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'wolf'/'wolf_right_2.png').convert_alpha())
        self.images_1.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'wolf'/'wolf_right_3.png').convert_alpha())
        self.images_2 = []
        self.images_2.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'wolf'/'wolf_left_0.png').convert_alpha())
        self.images_2.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'wolf'/'wolf_left_1.png').convert_alpha())
        self.images_2.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'wolf'/'wolf_left_2.png').convert_alpha())
        self.images_2.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'wolf'/'wolf_left_3.png').convert_alpha())

    def get_player_distance_direction(self, player):
        wolf_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - wolf_vec).magnitude()
        if distance > 20:
            direction = (player_vec - wolf_vec).normalize()
        else:
            direction = pygame.math.Vector2()
        return (distance, direction)

    def actions(self, player):
        self.direction = self.get_player_distance_direction(player)[1]
        return self.direction

    def collisions(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def animate(self):
        if self.direction.x > 0:
            self.index += self.animation_speed
            if self.index >= len(self.images_1):
                self.index = 0
            self.image = self.images_1[int(self.index)]
        if self.direction.x < 0:
            self.index += self.animation_speed
            if self.index >= len(self.images_2):
                self.index = 0
            self.image = self.images_2[int(self.index)]

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x*speed
        self.collisions('horizontal')
        self.hitbox.y += self.direction.y*speed
        self.collisions('vertical')
        self.rect.center = self.hitbox.center

    def update(self):
        self.animate()
        self.move(self.speed)

    def wolf_update(self, player):
        self.actions(player)


class Enemy(pygame.sprite.Sprite):
    def __init__(self,
                 pos,
                 group,
                 obstacle_sprites,
                 damage_player,
                 type):
        super().__init__(group)
        self.image = pygame.image.load(str(night_king)).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.obstacle_sprites = obstacle_sprites
        self.hitbox = self.rect.inflate(-26, -26)
        self.direction = pygame.math.Vector2()
        self.sprite_type = 'enemy'
        self.type = type
        self.status = 'down_idle'
        self.status_1 = None
        self.index = 0
        if self.type == 'night_king':
            self.animations = {'up': [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'up'/'up_0.png').convert_alpha(),
                                      pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'up'/'up_1.png').convert_alpha(),
                                      pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'up'/'up_2.png').convert_alpha(),
                                      pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'up'/'up_3.png').convert_alpha()],
                               'down': [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'down'/'down_0.png').convert_alpha(),
                                        pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'down'/'down_1.png').convert_alpha(),
                                        pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'down'/'down_2.png').convert_alpha(),
                                        pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'down'/'down_3.png').convert_alpha()],
                               'left': [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'left'/'left_0.png').convert_alpha(),
                                        pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'left'/'left_1.png').convert_alpha(),
                                        pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'left'/'left_2.png').convert_alpha(),
                                        pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'left'/'left_3.png').convert_alpha()],
                               'right': [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'right'/'right_0.png').convert_alpha(),
                                         pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'right'/'right_1.png').convert_alpha(),
                                         pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'right'/'right_2.png').convert_alpha(),
                                         pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'right'/'right_3.png').convert_alpha()],
                               'right_idle': [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'right_idle'/'right_idle_0.png').convert_alpha(),
                                              pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'right_idle'/'right_idle_1.png').convert_alpha()],
                               'left_idle': [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'left_idle'/'left_idle_0.png').convert_alpha(),
                                             pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'left_idle'/'left_idle_1.png').convert_alpha()],
                               'up_idle': [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'up_idle'/'up_idle_0.png').convert_alpha(),
                                           pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'up_idle'/'up_idle_1.png').convert_alpha()],
                               'down_idle': [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'down_idle'/'down_idle_0.png').convert_alpha(),
                                             pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'down_idle'/'down_idle_1.png').convert_alpha(),],
                               'right_attack': [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'right_attack'/'right_attack_0.png').convert_alpha(),
                                                pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'right_attack'/'right_attack_1.png').convert_alpha(),],
                               'left_attack': [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'left_attack'/'left_attack_0.png').convert_alpha(),
                                               pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'left_attack'/'left_attack_1.png').convert_alpha(),],
                               'up_attack': [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'up_attack'/'up_attack_0.png').convert_alpha(),
                                             pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'up_attack'/'up_attack_1.png').convert_alpha()],
                               'down_attack': [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'down_attack'/'down_attack_0.png').convert_alpha(),
                                               pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'night_king'/'down_attack'/'down_attack_1.png').convert_alpha(),]}
            self.health = 100
            self.speed = 1
            self.attack_damage = 20
            self.resistance = 3
        if self.type == 'zombie':
            self.animations = {'up': [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'up'/'up_0.png').convert_alpha(),
                                      pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'up'/'up_1.png').convert_alpha(),
                                      pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'up'/'up_2.png').convert_alpha(),
                                      pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'up'/'up_3.png').convert_alpha()],
                               'down': [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'down'/'down_0.png').convert_alpha(),
                                        pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'down'/'down_1.png').convert_alpha(),
                                        pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'down'/'down_2.png').convert_alpha(),
                                        pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'down'/'down_3.png').convert_alpha()],
                               'left': [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'left'/'left_0.png').convert_alpha(),
                                        pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'left'/'left_1.png').convert_alpha(),
                                        pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'left'/'left_2.png').convert_alpha(),
                                        pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'left'/'left_3.png').convert_alpha()],
                               'right': [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'right'/'right_0.png').convert_alpha(),
                                         pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'right'/'right_1.png').convert_alpha(),
                                         pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'right'/'right_2.png').convert_alpha(),
                                         pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'right'/'right_3.png').convert_alpha()],
                               'right_idle': [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'right_idle'/'right_idle_0.png').convert_alpha(),
                                              pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'right_idle'/'right_idle_1.png').convert_alpha()],
                               'left_idle': [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'left_idle'/'left_idle_0.png').convert_alpha(),
                                             pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'left_idle'/'left_idle_1.png').convert_alpha()],
                               'up_idle': [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'up_idle'/'up_idle_0.png').convert_alpha(),
                                           pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'up_idle'/'up_idle_1.png').convert_alpha()],
                               'down_idle': [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'down_idle'/'down_idle_0.png').convert_alpha(),
                                             pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'down_idle'/'down_idle_1.png').convert_alpha(),],
                               'right_attack': [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'right_attack'/'right_attack_0.png').convert_alpha(),
                                                pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'right_attack'/'right_attack_1.png').convert_alpha(),],
                               'left_attack': [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'left_attack'/'left_attack_0.png').convert_alpha(),
                                               pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'left_attack'/'left_attack_1.png').convert_alpha(),],
                               'up_attack': [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'up_attack'/'up_attack_0.png').convert_alpha(),
                                             pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'up_attack'/'up_attack_1.png').convert_alpha()],
                               'down_attack': [pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'down_attack'/'down_attack_0.png').convert_alpha(),
                                               pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'zombie'/'down_attack'/'down_attack_1.png').convert_alpha(),]}
            self.health = 40
            self.speed = 1
            self.attack_damage = 5
            self.resistance = 3
        self.notice_radius = 400
        self.attack_radius = 80
        self.attacking = False
        self.attack_type = 'weapon'
        self.attack_time = None
        self.attack_cooldown = 200
        self.damage_player = damage_player
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300
        self.killed = False
        self.can_attack = True
        self.ressurect_time = 10000

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0 and distance < 400:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()
        return (distance, direction)

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        if self.attacking is True:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def actions(self, player):
        self.direction = self.get_player_distance_direction(player)[1]
        distance = self.get_player_distance_direction(player)[0]
        if distance <= self.notice_radius:
            if self.direction.y > 0 and (self.direction.x <= 0.8 and self.direction.x >= -0.8):
                self.status = 'down'
            if self.direction.y < 0 and (self.direction.x <= 0.8 and self.direction.x >= -0.8):
                self.status = 'up'
            if self.direction.x < -0.5:
                self.status = 'left'
            if self.direction.x > 0.5:
                self.status = 'right'
        if distance <= self.attack_radius and not self.attacking and self.can_attack == True:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage,
                               self.attack_type)

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if self.attacking is True:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.status = self.status = self.status.replace('_attack', '')
                # self.destroy_attack()
        if not self.vulnerable:
            if current_time - self.hit_time > self.invincibility_duration:
                self.vulnerable = True

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def animate(self):
        if '_idle' in self.status:
            self.animation_speed = 0.05
        if '_attack' in self.status:
            self.animation_speed = 0.3
        if '_idle' not in self.status and '_attack' not in self.status:
            self.animation_speed = 0.1
        animation = self.animations[self.status]
        self.index += self.animation_speed
        if self.index >= len(animation):
            self.index = 0
        self.image = animation[int(self.index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
        if self.killed == True:
            self.image = pygame.Surface((0.1, 0.1))
            # self.image.fill((255, 255, 255))
            self.can_attack = False
            death_time = pygame.time.get_ticks()
            if death_time % 1000 == 0:
                self.killed = False
                self.health = 100
                self.can_attack = True

    def collisions(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x*speed
        self.collisions('horizontal')
        self.hitbox.y += self.direction.y*speed
        self.collisions('vertical')
        self.rect.center = self.hitbox.center

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= 15
                print(self.health)
            elif attack_type == 'arrow':
                self.health -= 2
                print(self.health)
            elif attack_type == 'bow':
                self.health -= 1
                print(self.health)
            else:
                pass
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        global number_of_enemies
        if self.type == 'night_king':
            if self.health <= 0:
                self.kill()
                self.killed = True
                number_of_enemies += 1
        elif self.type == 'zombie':
            if self.health <= 0:
                self.killed = True

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.get_status()
        self.cooldown()
        self.check_death()
        self.animate()

    def enemy_update(self, player):
        self.actions(player)


class AnimatedObj(pygame.sprite.Sprite):
    def __init__(self, pos, groups, type):
        super().__init__(groups)
        self.type = type
        self.images_raven = []
        self.images_rabbit = []
        self.images_fireplace = []
        self.images_cold_fireplace = []
        self.images_passage = []
        self.index = 0
        # raven
        self.images_raven.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'raven'/'raven_0.png').convert_alpha())
        self.images_raven.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'raven'/'raven_1.png').convert_alpha())
        self.images_raven.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'raven'/'raven_2.png').convert_alpha())
        self.images_raven.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'raven'/'raven_3.png').convert_alpha())
        self.images_raven.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'raven'/'raven_4.png').convert_alpha())
        self.images_raven.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'raven'/'raven_5.png').convert_alpha())
        self.images_raven.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'raven'/'raven_6.png').convert_alpha())
        self.images_raven.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'raven'/'raven_7.png').convert_alpha())
        self.images_raven.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'raven'/'raven_8.png').convert_alpha())
        self.images_raven.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'raven'/'raven_9.png').convert_alpha())
        self.images_raven.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'raven'/'raven_10.png').convert_alpha())
        self.images_raven.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'raven'/'raven_11.png').convert_alpha())
        self.images_raven.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'raven'/'raven_12.png').convert_alpha())
        self.images_raven.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'raven'/'raven_13.png').convert_alpha())
        # rabbit
        self.images_rabbit.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'rabbit'/'rabbit_0.png').convert_alpha())
        self.images_rabbit.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'rabbit'/'rabbit_1.png').convert_alpha())
        self.images_rabbit.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'rabbit'/'rabbit_2.png').convert_alpha())
        self.images_rabbit.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'rabbit'/'rabbit_3.png').convert_alpha())
        self.images_rabbit.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'rabbit'/'rabbit_4.png').convert_alpha())
        self.images_rabbit.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'rabbit'/'rabbit_5.png').convert_alpha())
        self.images_rabbit.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'rabbit'/'rabbit_6.png').convert_alpha())
        self.images_rabbit.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'rabbit'/'rabbit_7.png').convert_alpha())
        self.images_rabbit.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'rabbit'/'rabbit_8.png').convert_alpha())
        self.images_rabbit.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'rabbit'/'rabbit_9.png').convert_alpha())

        # fireplace
        self.images_fireplace.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'fireplace'/'fireplace_0.png').convert_alpha())
        self.images_fireplace.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'fireplace'/'fireplace_1.png').convert_alpha())
        self.images_fireplace.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'fireplace'/'fireplace_2.png').convert_alpha())
        self.images_fireplace.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'fireplace'/'fireplace_3.png').convert_alpha())
        
        # cold_fireplace
        self.images_cold_fireplace.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'cold_fireplace'/'cold_fireplace_0.png').convert_alpha())
        self.images_cold_fireplace.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'cold_fireplace'/'cold_fireplace_1.png').convert_alpha())
        self.images_cold_fireplace.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'cold_fireplace'/'cold_fireplace_2.png').convert_alpha())
        self.images_cold_fireplace.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'cold_fireplace'/'cold_fireplace_3.png').convert_alpha())
        
        # passage
        self.images_passage.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'passage'/'passage_0.png').convert_alpha())
        self.images_passage.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'passage'/'passage_1.png').convert_alpha())
        self.images_passage.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'passage'/'passage_2.png').convert_alpha())
        self.images_passage.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'passage'/'passage_3.png').convert_alpha())
        self.images_passage.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'passage'/'passage_4.png').convert_alpha())
        self.images_passage.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'passage'/'passage_5.png').convert_alpha())
        self.images_passage.append(pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'passage'/'passage_6.png').convert_alpha())
        if self.type == 'Raven':
            self.animation_speed = 0.2
            self.image = self.images_raven[self.index]
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -130)
        if self.type == 'Rabbit':
            self.animation_speed = 0.16
            self.image = self.images_rabbit[self.index]
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -130)
        if self.type == 'Fireplace':
            self.animation_speed = 0.15
            self.image = self.images_fireplace[self.index]
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, 0)
        if self.type == 'Cold_fireplace':
            self.animation_speed = 0.15
            self.image = self.images_cold_fireplace[self.index]
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, 0)
        if self.type == 'Passage':
            self.animation_speed = 0.15
            self.image = self.images_passage[self.index]
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, 0)

    def animate(self):
        if self.type == 'Raven':
            self.index += self.animation_speed
            if self.index >= len(self.images_raven):
                self.index = 0
            self.image = self.images_raven[int(self.index)]
        if self.type == 'Rabbit':
            self.index += self.animation_speed
            if self.index >= len(self.images_rabbit):
                self.index = 0
            self.image = self.images_rabbit[int(self.index)]
        if self.type == 'Fireplace':
            self.index += self.animation_speed
            if self.index >= len(self.images_fireplace):
                self.index = 0
            self.image = self.images_fireplace[int(self.index)]
        if self.type == 'Cold_fireplace':
            self.index += self.animation_speed
            if self.index >= len(self.images_cold_fireplace):
                self.index = 0
            self.image = self.images_cold_fireplace[int(self.index)]
        if self.type == 'Passage':
            self.index += self.animation_speed
            if self.index >= len(self.images_passage):
                self.index = 0
            self.image = self.images_passage[int(self.index)]

    def action(self):
        if self.type == 'Passage':
            self.vector = pygame.math.Vector2()


    def update(self):
        self.animate()


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, group, type):
        super().__init__(group)
        self.type = type
        if self.type == 'tile':
            self.image = pygame.image.load(str(rock)).convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -10)
        elif self.type == 'boundary':
            self.image = pygame.image.load(str(grass)).convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, 0)
        elif self.type == 'tree':
            self.image = pygame.image.load(str(tree_image)).convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -110)
        elif self.type == 'cave':
            self.image = pygame.image.load(str(cave_image)).convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -110)
        elif self.type == 'black':
            self.image = pygame.image.load(str(black_image)).convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, 0)
        elif self.type == 'grey':
            self.image = pygame.image.load(str(grey_image)).convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, 0)
        elif self.type == 'brown':
            self.image = pygame.image.load(str(brown_image)).convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, 0)
        elif self.type == 'exit':
            self.image = pygame.image.load(str(exit_image)).convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, 0)
        elif self.type == 'wall_down':
            self.image = pygame.image.load(str(wall_down_image)).convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, 0)
        elif self.type == 'wall_down_left':
            self.image = pygame.image.load(str(wall_down_left_image)).convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, 0)
        elif self.type == 'wall_down_right':
            self.image = pygame.image.load(str(wall_down_right_image)).convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, 0)
        elif self.type == 'wall_left':
            self.image = pygame.image.load(str(wall_left_image)).convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, 0)
        elif self.type == 'wall_right':
            self.image = pygame.image.load(str(wall_right_image)).convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, 0)
        elif self.type == 'wall_up':
            self.image = pygame.image.load(str(wall_up_image)).convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, 0)
        elif self.type == 'grass':
            self.image = pygame.image.load(str(grass)).convert_alpha()
            self.rect = self.image.get_rect(topleft=(pos))
            self.hitbox = self.rect.inflate(0, -10)
        elif self.type == 'mushrooms':
            self.image = pygame.image.load(str(mushrooms)).convert_alpha()
            self.rect = self.image.get_rect(topleft=(pos))
            self.hitbox = self.rect.inflate(0, -10)
        elif self.type == 'canvas':
            self.image = pygame.image.load(str(canvas)).convert_alpha()
            self.rect = self.image.get_rect(topleft=(pos))
            self.hitbox = self.rect.inflate(0, -110)
        elif self.type == 'magic_tree':
            self.image = pygame.image.load(str(magic_tree)).convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -110)
        elif self.type == 'column':
            self.image = pygame.image.load(str(stone)).convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -110)
        if self.type == 'night_king':
            self.image = pygame.image.load(str(night_king)).convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-26, -26)
        if self.type == 'zombie':
            self.image = pygame.image.load(str(zombie)).convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-26, -26)
        self.resistance = 3
        self.health = 100
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300
        self.killed = False

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def animate(self):
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
        if self.killed == True:
            self.kill()
            # self.image = pygame.Surface((0.1, 0.1))
            # # self.image.fill((255, 255, 255))
            # death_time = pygame.time.get_ticks()
            # if death_time % 500 == 0:
            #     self.killed = False
            #     self.health = 100
            #     if self.type == 'grass':
            #         self.image = pygame.image.load(str(grass)).convert_alpha()
            #     elif self.type == 'mushrooms':
            #         self.image = pygame.image.load(str(mushrooms)).convert_alpha()

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.vulnerable:
            if current_time - self.hit_time > self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            if attack_type == 'weapon':
                self.health -= 90
                print(self.health)
            elif attack_type == 'bow':
                self.health -= 50
                print(self.health)
            elif attack_type == 'arrow':
                self.health -= 90
                print(self.health)
            else:
                pass
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        global number_of_grass
        global number_of_mushrooms
        current_time = pygame.time.get_ticks()
        if self.health <= 0:
            if self.type == 'grass':
                self.killed = True
                number_of_grass += 1
            if self.type == 'mushrooms':
                self.killed = True
                number_of_mushrooms += 1

    def update(self):
        self.cooldown()
        self.check_death()
        self.animate()


class Level:
    '''Отвечает за создание уровня'''
    def __init__(self, layout_name, player_coords=None):
        self.layout_name = layout_name
        self.player_coords = player_coords
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCameraGRoup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.tormund = None
        self.orell = None
        self.karsi = None
        self.current_attack = None
        self.current_attack_bow = None
        self.current_attack_bow_2 = None
        self.current_arrow = None
        self.current_arrow_2 = None
        self.current_heal = None
        self.current_quest = None
        self.current_quest_1 = None
        self.current_quest_2 = None
        self.ui = UI(self.layout_name)
        self.create_map()

    def create_map(self):
        global is_active
        global is_finished
        global number_of_mushrooms
        global number_of_elixirs

        global is_active_1
        global is_finished_1
        global number_of_grass
        global number_of_arrows

        global is_active_2
        global is_finished_2
        global number_of_enemies
        if self.layout_name == 'layout_0':
            layouts = {'boundary': import_csv_layout(pathlib.Path(__file__).parent/'levels/level_0/level_0_boundary.csv'),
                       'grass_and_mushrooms': import_csv_layout(pathlib.Path(__file__).parent/'levels/level_0/level_0_grass_and_mushrooms.csv'),
                       'objects': import_csv_layout(pathlib.Path(__file__).parent/'levels/level_0/level_0_objects.csv'),
                       'animals': import_csv_layout(pathlib.Path(__file__).parent/'levels/level_0/level_0_animals.csv'),
                       'characters': import_csv_layout(pathlib.Path(__file__).parent/'levels/level_0/level_0_characters.csv')}
        if self.layout_name == 'layout_1':
            layouts = {'boundary': import_csv_layout(pathlib.Path(__file__).parent/'levels/level_1/level_1_boundary.csv'),
                       'grass_and_mushrooms': import_csv_layout(pathlib.Path(__file__).parent/'levels/level_1/level_1_grass_and_mushrooms.csv'),
                       'objects': import_csv_layout(pathlib.Path(__file__).parent/'levels/level_1/level_1_objects.csv'),
                       'animals': import_csv_layout(pathlib.Path(__file__).parent/'levels/level_1/level_1_animals.csv'),
                       'characters': import_csv_layout(pathlib.Path(__file__).parent/'levels/level_1/level_1_characters.csv')}
        if self.layout_name == 'layout_2':
            layouts = {'boundary': import_csv_layout(pathlib.Path(__file__).parent/'levels/level_2/level_2_boundary.csv'),
                       'grass_and_mushrooms': import_csv_layout(pathlib.Path(__file__).parent/'levels/level_2/level_2_grass_and_mushrooms.csv'),
                       'objects': import_csv_layout(pathlib.Path(__file__).parent/'levels/level_2/level_2_objects.csv'),
                       'animals': import_csv_layout(pathlib.Path(__file__).parent/'levels/level_2/level_2_animals.csv'),
                       'characters': import_csv_layout(pathlib.Path(__file__).parent/'levels/level_2/level_2_characters.csv')}
        if self.layout_name == 'layout_3':
            layouts = {'boundary': import_csv_layout(pathlib.Path(__file__).parent/'levels/level_3/level_3_boundary.csv'),
                       'grass_and_mushrooms': import_csv_layout(pathlib.Path(__file__).parent/'levels/level_3/level_3_grass_and_mushrooms.csv'),
                       'objects': import_csv_layout(pathlib.Path(__file__).parent/'levels/level_3/level_3_objects.csv'),
                       'animals': import_csv_layout(pathlib.Path(__file__).parent/'levels/level_3/level_3_animals.csv'),
                       'characters': import_csv_layout(pathlib.Path(__file__).parent/'levels/level_3/level_3_characters.csv')}
        if self.layout_name == 'cave':
            layouts = {'objects': import_csv_layout(pathlib.Path(__file__).parent/'levels/cave/cave_objects.csv'),
                       'animals': import_csv_layout(pathlib.Path(__file__).parent/'levels/cave/cave_animals.csv'),
                       'characters': import_csv_layout(pathlib.Path(__file__).parent/'levels/cave/cave_charecters.csv'),
                       'ground': import_csv_layout(pathlib.Path(__file__).parent/'levels/cave/cave_ground.csv')}
        current_time = pygame.time.get_ticks()

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '16':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if col == '18':
                            Tile((x, y), [self.obstacle_sprites], 'boundary')
                        if col == '7':
                            Tile((x, y),
                                    [self.visible_sprites,
                                    self.obstacle_sprites,
                                    self.attackable_sprites],
                                    'mushrooms')
                        if col == '4':
                            self.grass = Tile((x, y),
                                              [self.visible_sprites,
                                               self.obstacle_sprites,
                                               self.attackable_sprites],
                                               'grass')
                        if col == '14':
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'tree')
                        if col == '20':
                            self.cave = Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'cave')
                            print(self.cave.rect.center)
                        if col == '0':
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'canvas')
                        if col == '12':
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'column')
                        if col == '3':
                            AnimatedObj((x, y), [self.visible_sprites, self.obstacle_sprites], 'Fireplace')
                        if col == '6':
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'magic_tree')
                        if col == '10':
                            AnimatedObj((x, y), [self.visible_sprites], 'Raven')
                        if col == '9':
                            AnimatedObj((x, y), [self.visible_sprites], 'Rabbit')
                        if col == '2':
                            if self.player_coords is None:
                                self.player = Player((x, y),
                                                     [self.visible_sprites],
                                                     self.obstacle_sprites,
                                                     self.create_attack,
                                                     self.destroy_attack,
                                                     self.take_bow,
                                                     self.put_off_bow,
                                                     self.heal,
                                                     self.remove_heal)
                                self.player_vec = pygame.math.Vector2(self.player.rect.center)
                            elif self.player_coords is not None:
                                self.player = Player(self.player_coords,
                                                     [self.visible_sprites],
                                                     self.obstacle_sprites,
                                                     self.create_attack,
                                                     self.destroy_attack,
                                                     self.take_bow,
                                                     self.put_off_bow,
                                                     self.heal,
                                                     self.remove_heal,)
                                self.player_vec = pygame.math.Vector2(self.player.rect.center)
                        if col == '13':
                            if self.layout_name == 'layout_2':
                                self.tormund = Wildlings((x, y), 'tormund', [self.visible_sprites])
                                if is_finished == 0:
                                    Quests(self.tormund, [self.visible_sprites], self.player, 'mushrooms')
                                else:
                                    pass
                            else:
                                pass
                        if col == '5':
                            if self.layout_name == 'layout_0':
                                self.karsi = Wildlings((x, y), 'karsi', [self.visible_sprites])
                                if is_finished_1 == 0:
                                    Quests(self.karsi, [self.visible_sprites], self.player, 'grass')
                            else:
                                pass
                        if col == '8':
                            if self.layout_name == 'layout_1':
                                if self.player_coords is None:
                                    self.player = Player((x, y),
                                                        [self.visible_sprites],
                                                        self.obstacle_sprites,
                                                        self.create_attack,
                                                        self.destroy_attack,
                                                        self.take_bow,
                                                        self.put_off_bow,
                                                        self.heal,
                                                        self.remove_heal)
                                    self.player_vec = pygame.math.Vector2(self.player.rect.center)
                                elif self.player_coords is not None:
                                    self.player = Player(self.player_coords,
                                                        [self.visible_sprites],
                                                        self.obstacle_sprites,
                                                        self.create_attack,
                                                        self.destroy_attack,
                                                        self.take_bow,
                                                        self.put_off_bow,
                                                        self.heal,
                                                        self.remove_heal,)
                                self.player_vec = pygame.math.Vector2(self.player.rect.center)
                                self.orell = Wildlings((x, y), 'orell', [self.visible_sprites])
                                if is_finished_2 == 0:
                                    Quests(self.orell, [self.visible_sprites], self.player, 'enemies')
                        if col == '1':
                            self.enemy = Enemy((x, y),
                                                [self.visible_sprites,
                                                 self.attackable_sprites],
                                                 self.obstacle_sprites,
                                                 self.damage_player,
                                                 'night_king')
                        if col == '11':
                            self.zombie = Enemy((x, y),
                                                [self.visible_sprites,
                                                 self.attackable_sprites],
                                                self.obstacle_sprites,
                                                self.damage_player,
                                                'zombie')
                        if col == '15':
                            self.wolf = Wolf((x, y), [self.visible_sprites], self.obstacle_sprites)
                        if col == '19':
                            self.passage_coords = []
                            self.teleport = AnimatedObj((x, y), [self.visible_sprites], 'Passage')
                            self.passage_coords.append(self.teleport.rect.center)
                        if col == '21':
                            Tile((x, y),
                                 [self.visible_sprites],
                                 'black')
                        if col == '30':
                            Tile((x, y),
                                 [self.visible_sprites,
                                  self.obstacle_sprites,],
                                 'exit')
                        if col == '26':
                            Tile((x, y),
                                 [self.visible_sprites,
                                  self.obstacle_sprites,],
                                 'wall_down')
                        if col == '27':
                            Tile((x, y),
                                 [self.visible_sprites,
                                  self.obstacle_sprites,],
                                 'wall_down_left')
                        if col == '28':
                            Tile((x, y),
                                 [self.visible_sprites,
                                  self.obstacle_sprites,],
                                 'wall_down_right')
                        if col == '24':
                            Tile((x, y),
                                 [self.visible_sprites,
                                  self.obstacle_sprites,],
                                 'wall_left')
                        if col == '25':
                            Tile((x, y),
                                 [self.visible_sprites,
                                  self.obstacle_sprites,],
                                 'wall_right')
                        if col == '23':
                            Tile((x, y),
                                 [self.visible_sprites,
                                  self.obstacle_sprites,],
                                 'wall_up')
                        if col == '29':
                            AnimatedObj((x, y), [self.visible_sprites, self.obstacle_sprites], 'Cold_fireplace')
                        if col == '31':
                            if self.layout_name == 'layout_0':
                                self.archer = Archer((x, y), [self.visible_sprites], self.shoot, self.put_off_shoot)
                        if col == '32':
                            Wildlings((x, y), 'woodman', [self.visible_sprites])
                        if col == '34':
                            Wildlings((x-25, y+20), 'walker', [self.visible_sprites])

    def create_attack(self):
        self.current_attack = Weapon(self.player,
                                     [self.visible_sprites,
                                      self.attack_sprites],)

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def take_bow(self):
        global number_of_arrows
        number_of_arrows += -1
        # # cur.execute('''UPDATE params
        # #             SET number_of_arrows = number_of_arrows - 1
        # #             WHERE id = 1''')
        # # db.commit()
        # self.current_attack_bow = WeaponBow(self.player,
        #                                     [self.visible_sprites,
        #                                      self.attack_sprites],)
        self.current_arrow = Arrow(self.player, [self.visible_sprites,
                                                 self.attack_sprites],
                                                 self.obstacle_sprites)

    def shoot(self):
        if self.current_arrow_2 is None:
            self.current_arrow_2 = Arrow_2(self.archer, [self.visible_sprites, self.attack_sprites], self.obstacle_sprites)

    def put_off_shoot(self):
        # if self.current_arrow_2.hitbox.colliderect(self.enemy.hitbox):
        if self.current_arrow_2 is not None:
            self.current_arrow_2.kill()
            self.current_arrow_2 = None

    def put_off_bow(self):
        if self.current_attack_bow:
            if self.current_arrow.hitbox.colliderect(self.enemy.hitbox):
                self.current_arrow.kill()
            self.current_attack_bow.kill()
        self.current_attack_bow = None

    def heal(self):
        self.current_heal = Heal(self.player,
                                 [self.visible_sprites])

    def remove_heal(self):
        if self.current_heal:
            self.current_heal.kill()
        self.current_heal = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        target_sprite.get_damage(self.player,
                                                 attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        global player_health
        if self.player.vulnerable:
            self.player.health -= amount
            player_health = self.player.health
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

    def passage(self):
        keys = pygame.key.get_pressed()
        if self.layout_name == 'layout_0':
            if self.player.hitbox.center[0] in range(300, 400, 1) and self.player.hitbox.center[1] in range(800, 1000, 1):
                debug('Нажмите R для перехода!')
                if keys[pygame.K_r]:
                    game = Game('layout_1', (1220, 665))
                    game.run()
            if self.player.hitbox.center[0] in range(900, 1100, 1) and self.player.hitbox.center[1] in range(300, 400, 1):
                debug('Нажмите R для перехода!')
                if keys[pygame.K_r]:
                    game = Game('layout_3', (864, 1184))
                    game.run()
        if self.layout_name == 'layout_1':
            if self.player.hitbox.center[0] in range(1000, 1200, 1) and self.player.hitbox.center[1] in range(250, 450, 1):
                debug('Нажмите R для перехода!')
                if keys[pygame.K_r]:
                    game = Game('layout_2', (992, 1184))
                    game.run()
            if self.player.hitbox.center[0] in range(1150, 1300, 1) and self.player.hitbox.center[1] in range(550, 800, 1):
                debug('Нажмите R для перехода!')
                if keys[pygame.K_r]:
                    game = Game('layout_0', (352, 864))
                    game.run()
        if self.layout_name == 'layout_2':
            if self.player.hitbox.center[0] in range(1000, 1250, 1) and self.player.hitbox.center[1] in range(320, 600, 1):
                debug('Нажмите R для перехода!')
                if keys[pygame.K_r]:
                    game = Game('layout_3', (352, 672))
                    game.run()
            if self.player.hitbox.center[0] in range(800, 1100, 1) and self.player.hitbox.center[1] in range(1000, 1300, 1):
                debug('Нажмите R для перехода!')
                if keys[pygame.K_r]:
                    game = Game('layout_1', (1095, 352))
                    game.run()
        if self.layout_name == 'layout_3':
            if self.player.hitbox.center[0] in range(250, 500, 1) and self.player.hitbox.center[1] in range(550, 800, 1):
                debug('Нажмите R для перехода!')
                if keys[pygame.K_r]:
                    game = Game('layout_2', (1120, 480))
                    game.run()
            if self.player.hitbox.center[0] in range(720, 1000, 1) and self.player.hitbox.center[1] in range(1000, 1300, 1):
                debug('Нажмите R для перехода!')
                if keys[pygame.K_r]:
                    game = Game('layout_0', (1056, 352))
                    game.run()
            if self.player.hitbox.center[0] in range(1170, 1300, 1) and self.player.hitbox.center[1] in range(300, 450, 1):
                debug('Нажмите R для перехода!')
                if keys[pygame.K_r]:
                    game = Game('cave',)
                    game.run()
                    game.screen.fill(BROWN)
        if self.layout_name == 'cave':
            if self.player.hitbox.center[0] in range(700, 750, 1) and self.player.hitbox.center[1] in range(1080, 1180, 1):
                debug('Нажмите R для перехода!')
                if keys[pygame.K_r]:
                    game = Game('layout_3', (1200, 432))
                    game.run()

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.visible_sprites.wolf_update(self.player)
        self.ui.display(self.player)
        self.passage()


class YSortCameraGRoup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_w = self.display_surface.get_size()[0]//2
        self.half_h = self.display_surface.get_size()[1]//2
        self.offset = pygame.math.Vector2(self.half_w, self.half_h)
        # self.floor_surf = pygame.image.load(pathlib.Path(__file__).parent/'graphics'/'map'/'map.png').convert_alpha()
        self.floor_surf = pygame.image.load(pathlib.Path(__file__).parent/'levels'/'level_0'/'map_0.png').convert_alpha()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx-self.half_w
        self.offset.y = player.rect.centery-self.half_h
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)
        for sprite in sorted(self.sprites(),
                             key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft-self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

    def wolf_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'wolf']
        for enemy in enemy_sprites:
            enemy.wolf_update(player)


class Game:
    '''Запускает игру'''
    def __init__(self, layout_name, player_coords=None):
        self.layout_name = layout_name
        self.player_coords = player_coords
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('Adventures of Jon Snow')
        self.clock = pygame.time.Clock()
        self.level = Level(self.layout_name, self.player_coords)
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
            if self.layout_name != 'cave':
                self.screen.fill('WHITE')
                self.level.run()
                for i in range(len(snow_list)):
                    pygame.draw.circle(self.screen, WHITE, snow_list[i], 2)
                    snow_list[i][1] += 1
                    if snow_list[i][1] > HEIGTH:
                        y = random.randrange(-50, -10)
                        snow_list[i][1] = y
                        x = random.randrange(0, WIDTH)
                        snow_list[i][0] = x
                pygame.display.update()
                self.clock.tick(FPS)
            else:
                self.screen.fill(GREY)
                self.level.run()
                pygame.display.update()
                self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game('layout_0')
    game.run()
