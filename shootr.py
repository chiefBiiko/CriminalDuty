# CriminalDuty - a mini pygame
# -----------------------------------------------------------------------------
import os, sys, random, math, pygame, string
from pygame import *
import time as sleepr

def main():
    """CriminalDuty - a mini pygame for goons"""
    black = 0, 0, 0
    white = 255, 255, 255
    screen_w, screen_h = 700, 400
    player_x, player_y = 0, 0
    move_player_x, move_player_y = 0, 0
    num_cops = 5
    score = 0
    done = False
    clock = pygame.time.Clock()
    SONGS = [os.path.join('snd\\songs', 'Bando.mp3'), os.path.join('snd\\songs', 'KarateChop.mp3')]
    KILLWAV = [os.path.join('snd\\kill', 'Gucci Mane Yeah (2).wav'), os.path.join('snd\\kill', 'Vox (Mafia-Hoe).wav')]
    HITWAV = os.path.join('snd\\hit', 'OJ Damn.wav')

    # HELPRS ----------------------------------------------------------------------
    def get_key():
        while 1:
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN:
                return event.key
            else:
                pass
    # -----------------------------------------------------------------------------
    def display_box(screen, message):
        """Print a message in a box in the middle of the screen"""
        fontobject = pygame.font.Font(None, 24)
        pygame.draw.rect(screen, (0, 0, 0),
                         ((screen.get_width() / 2) - 100,
                         (screen.get_height() / 2) - 10,
                         240, 20), 0)
        pygame.draw.rect(screen, (255, 255, 255),
                         ((screen.get_width() / 2) - 102,
                         (screen.get_height() / 2) - 12,
                         244, 24), 1)
        if len(message) != 0:
            screen.blit(fontobject.render(message, 1, (255, 255, 255)),
                        ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
        pygame.display.flip()
    # -----------------------------------------------------------------------------
    def ask(screen, question):
        """ask(screen, question) -> answer"""
        pygame.font.init()
        current_string = []
        display_box(screen, question + ': ' + string.join(current_string, ''))
        while 1:
            inkey = get_key()
            if inkey == K_BACKSPACE:
                current_string = current_string[0:-1]
            elif inkey == K_RETURN:
                break
            elif inkey == K_MINUS:
                current_string.append('_')
            elif inkey <= 127:
                current_string.append(chr(inkey))
            display_box(screen, question + ': ' + string.join(current_string, ''))
        return string.join(current_string, '')
    # -----------------------------------------------------------------------------
    def load_png(name):
        """Load image and return image object"""
        fullname = os.path.join('img', name)
        try:
            image = pygame.image.load(fullname)
            if image.get_alpha() is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
        except pygame.error, message:
            print 'Cannot load image:', fullname
            raise SystemExit, message
        return image, image.get_rect()

    # CLASSES ---------------------------------------------------------------------
    class Cop(pygame.sprite.Sprite):
        """This is the Cop class so far, cop by foot chasing player."""
        def __init__(self):
            """Give stoopid cop look"""
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = load_png('cop.png')
            self.rect.x = random.randrange(screen_w)
            self.rect.y = random.randrange(330)
        def update(self):
            """Cop movement: constantly chasing the player"""
            if player_x < self.rect.x:
                self.rect.x -= 1
            elif player_x > self.rect.x:
                self.rect.x += 1
            if player_y < self.rect.y:
                self.rect.y -= 1
            elif player_y > self.rect.y:
                self.rect.y += 1
    # -----------------------------------------------------------------------------
    class Tank(pygame.sprite.Sprite):
        """Tank doesnt chase player, adjusts y only and shoots player"""
        def __init__(self):
            """Assign pic later on"""
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = load_png('tank.png')
            self.health = 1000
        def update(self):
            """Tank movement: adjusting y rel 2 player"""
            if player_y < self.rect.y:
                self.rect.y -= 1
            elif player_y > self.rect.y:
                self.rect.y += 1
            elif player_y == self.rect.y:
                self.shoot()
        def shoot(self):
            """Tank shoots player"""
            canon = Bullet([player_x, player_y], [self.rect.x, self.rect.y])
            canon.rect.x = self.rect.x
            canon.rect.y = self.rect.y
            all_sprites_list.add(canon)
            canon_list.add(canon)
    # -----------------------------------------------------------------------------
    class Player(pygame.sprite.Sprite):
        """The Player class"""
        def __init__(self):
            """Load in avatar"""
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = load_png('goon.png')
            self.rect.x, self.rect.y = 2, 2
            self.health = 100   
        def update(self):
            """player_x,_y are the players new coords for every next frame"""
            self.rect.x = player_x
            self.rect.y = player_y
        def hit_vox(self):
            """Play this when player got hit"""
            pygame.mixer.Sound(HITWAV).play()    
        def kill_vox(self):
            """Play this when player just killed"""
            pygame.mixer.Sound(random.choice(KILLWAV)).play()
    # -----------------------------------------------------------------------------
    class Bullet(pygame.sprite.Sprite):
        """Class for bullets player and tank shoot"""
        speed = 4.
        def __init__(self, mouse, player):
            """Give look and provide coords at init"""
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface([8, 6])
            self.image.fill(black)
            self.mouse_x, self.mouse_y = mouse[0], mouse[1]
            self.player = player
            self.rect = self.image.get_rect()    
        def update(self):
            """Bullets flying their way"""
            distance = [self.mouse_x - self.player[0], self.mouse_y - self.player[1]]
            norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
            direction = [distance[0] / norm, distance[1] / norm]
            bullet_vector = [direction[0] * Bullet.speed, direction[1] * Bullet.speed]
            self.rect.x += bullet_vector[0]
            self.rect.y += bullet_vector[1]
    # -----------------------------------------------------------------------------
    class Footr(pygame.sprite.Sprite):
        """Basically a scoreboard, how2 raise its z-value, so that no overlap??"""
        def __init__(self):
            """Setting up the scoreboard"""
            pygame.sprite.Sprite.__init__(self)
            self.font = pygame.font.Font(None, 24)
            self.text = self.font.render('{}'.format(NAME) + '    health: {}'.format(player.health) + '    cops shot: {}'.format(score) + '    tank: {}'.format(tank.health), 1, white)
            self.image = pygame.Surface([700, 50])
            self.rect = self.image.get_rect()
            self.rect.left, self.rect.top = 0, 350
            self.image.blit(self.text, (10, 10))
        def update(self):
            """Updating health and score"""
            self.text = self.font.render('{}'.format(NAME) + '    health: {}'.format(player.health) + '    cops shot: {}'.format(score) + '    tank: {}'.format(tank.health), 1, white)
            self.image = pygame.Surface([700, 50])
            self.rect = self.image.get_rect()
            self.rect.left, self.rect.top = 0, 350
            self.image.blit(self.text, (10, 10))

    # INITIALIZATION --------------------------------------------------------------
    pygame.mixer.pre_init(frequency = 44100, size = -16, channels = 2, buffer = 4096)
    pygame.init(); print(pygame.mixer.get_init())
    pygame.mixer.music.load(random.choice(SONGS))
    pygame.mixer.music.play()
    screen = pygame.display.set_mode([screen_w, screen_h])
    pygame.display.set_caption('Criminal Duty')
    NAME = ask(screen, 'Name')
    # -----------------------------------------------------------------------------
    all_sprites_list = pygame.sprite.Group()
    player_list = pygame.sprite.Group()
    tank_list = pygame.sprite.Group()
    cop_list = pygame.sprite.Group()
    bullet_list = pygame.sprite.Group()
    canon_list = pygame.sprite.Group()
    # -----------------------------------------------------------------------------
    for i in range(num_cops):
        cop = Cop()
        cop_list.add(cop)
        all_sprites_list.add(cop)
    # -----------------------------------------------------------------------------
    player = Player()
    player_list.add(player)
    tank = Tank()
    tank.rect.x, tank.rect.y = 500, 200
    tank_list.add(tank)
    footr = Footr()
    all_sprites_list.add(player, footr, tank)

    # MAIN PROGRAM LOOP  ----------------------------------------------------------
    while not done:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display_box(screen, 'cops shot: {}'.format(score))
                sleepr.sleep(10)
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:  # player shooting bullets
                bullet = Bullet(pygame.mouse.get_pos(), [player.rect.x, player.rect.y])
                bullet.rect.x = player.rect.x
                bullet.rect.y = player.rect.y
                all_sprites_list.add(bullet)
                bullet_list.add(bullet)
            # player movement
            if event.type == pygame.KEYDOWN:    
                if event.key == K_a:
                    move_player_x=-4
                elif event.key == K_d:
                    move_player_x=+4
                elif event.key == K_w:
                    move_player_y=-4
                elif event.key == K_s:
                    move_player_y=+4
            if event.type == pygame.KEYUP:
                if event.key == K_a:
                    move_player_x=0
                elif event.key == K_d:
                    move_player_x=0
                elif event.key == K_w:
                    move_player_y=0
                elif event.key == K_s:
                    move_player_y=0
                elif event.key == K_ESCAPE:
                    display_box(screen, 'cops shot: {}'.format(score))
                    sleepr.sleep(10)
                    done = True
        # --- Game logic
        all_sprites_list.update()
        # new player position
        player_x += move_player_x
        player_y += move_player_y
        # Cop instances hitting player
        cop_hit_list = pygame.sprite.spritecollide(player, cop_list, True)
        for cop in cop_hit_list:
            player.hit_vox()
            player.health -= 5
        # Tank instance overlapping with player
        tank_hit_list = pygame.sprite.spritecollide(player, tank_list, False)
        for tank in tank_hit_list:
            player.hit_vox()
            player.health -= 10
        # Cop instances that player shot
        for bullet in bullet_list:
            cop_kill_list = pygame.sprite.spritecollide(bullet, cop_list, True)
            for cop in cop_kill_list:
                player.kill_vox()
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)
                score += 1
            # bullets hitting Tank instance
            tank_hit_list = pygame.sprite.spritecollide(bullet, tank_list, False)
            for hit in tank_hit_list:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)
                tank.health -= 10
            # bullets out of bounds get erased, u cant shoot when outta view
            if (bullet.rect.y < 0 or bullet.rect.y > screen_h - 50 or
                bullet.rect.x < -10 or bullet.rect.x > screen_w - 40):
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)
        # Tanks canons aimed at player
        """canons out of bounds r not removed, u cant hide outta view, Tank instance will still shoot ya"""
        for canon in canon_list:
            canon_hit_list = pygame.sprite.spritecollide(canon, player_list, False)
            for hit in canon_hit_list:
                player.hit_vox()
                canon_list.remove(canon)
                all_sprites_list.remove(canon)
                player.health -= 10
        # Revive cops++ when all got shot
        if len(cop_list) == 0:
            num_cops += 1
            for i in range(num_cops):
                cop = Cop()
                cop_list.add(cop)
                all_sprites_list.add(cop)
        # player dead
        if player.health <= 0:
            display_box(screen, 'dead.. total cops shot: {}'.format(score))
            sleepr.sleep(10) 
            done = True
        # A.C.A.B. player won
        if tank.health <= 0:
            score += 100
            display_box(screen, 'A.C.A.B! total cops shot: {}'.format(score))
            sleepr.sleep(10) 
            done = True
        # -----------------------------------------------------------------------------
        screen.fill(white)
        all_sprites_list.draw(screen)
        pygame.display.flip()
        clock.tick(30)
    # -----------------------------------------------------------------------------
    pygame.quit()
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
