# CriminalDuty - a mini pygame
# -----------------------------------------------------------------------------
import os, random, math, string, pygame
from pygame import *
from time import sleep as sleepr

def main():
    """CriminalDuty - a mini pygame for goons"""
    # SETUP -----------------------------------------------------------------------
    black = 0, 0, 0
    white = 255, 255, 255
    screen_w, screen_h = 700, 400
    player_x, player_y = 50, 100
    move_player_x, move_player_y = 0, 0
    num_cops = 5
    score = 0
    done = False
    clock = pygame.time.Clock()
    SONGS = [os.path.join('snd\\songs', 'SD.mp3'), os.path.join('snd\\songs', 'BRICKZ.mp3')]
    KILLWAV = [os.path.join('snd\\kill', 'Gucci Mane Yeah (2).wav'), os.path.join('snd\\kill', 'Vox (Mafia-Hoe).wav')]
    HITWAV = os.path.join('snd\\hit', 'OJ Damn.wav')
    all_sprites_list, player_list, cop_list, tank_list, heli_list, bullet_list, canon_list, rocket_list = (pygame.sprite.Group() for i in range(8))
    cop_hit_list, tank_hit_list, heli_hit_list, cop_kill_list, tank_kill_list, heli_kill_list, canon_hit_list, rocket_hit_list = ([] for i in range(8))
    
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
        pygame.draw.rect(screen, black,
                         ((screen.get_width() / 2) - 100,
                         (screen.get_height() / 2) - 10,
                         240, 20), 0)
        pygame.draw.rect(screen, white,
                         ((screen.get_width() / 2) - 102,
                         (screen.get_height() / 2) - 12,
                         244, 24), 1)
        if len(message) != 0:
            screen.blit(fontobject.render(message, 1, white),
                        ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
        pygame.display.flip()
    # -----------------------------------------------------------------------------
    def ask(screen, question):
        """ask(screen, question) returns answer"""
        pygame.font.init()
        current_string = []
        display_box(screen, question + ': ' + string.join(current_string, ''))
        while 1:
            inkey = get_key()
            if inkey == K_BACKSPACE:
                current_string = current_string[0:-1]
            elif inkey == K_RETURN:
                break
            elif inkey == K_ESCAPE:
                pygame.quit()
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
        """Cop by foot chasing player"""
        def __init__(self):
            """stoopid cop; init with random coords"""
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = load_png('cop.png')
            self.rect.x = random.randrange(screen_w)
            self.rect.y = random.randrange(330)
        def update(self):
            """cop movement: constantly chasing the player"""
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
        """Tank doesnt chase player, adjusts y only and shoots player, level 1"""
        def __init__(self):
            """first endgegner"""
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = load_png('tank.png')
            self.rect.x, self.rect.y = 500, 200
            self.health = 1000
        def update(self):
            """tank movement: adjusting y rel 2 player"""
            if player_y < self.rect.y:
                self.rect.y -= 1
            elif player_y > self.rect.y:
                self.rect.y += 1
            elif player_y == self.rect.y:
                self.shoot()
        def shoot(self):
            """tank shoots player"""
            canon = Bullet([player_x, player_y], [self.rect.x, self.rect.y])
            canon.rect.x = self.rect.x
            canon.rect.y = self.rect.y
            all_sprites_list.add(canon)
            canon_list.add(canon)
    # -----------------------------------------------------------------------------
    class Heli(pygame.sprite.Sprite):
        """Heli flys, adjusts x only, appears when tank dead, level 2"""
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = load_png('heli.png')
            self.rect.x, self.rect.y = 500, 0
            self.health = 1500
        def update(self):
            """heli movement: adjusting x rel 2 player"""
            if player_x < self.rect.x:
                self.rect.x -= 2
            elif player_x > self.rect.x:
                self.rect.x += 2
            elif player_x == self.rect.x:
                self.shoot()
        def shoot(self):
            """heli shoots player"""
            rocket = Bullet([player_x, player_y], [self.rect.x, self.rect.y])
            rocket.rect.x = self.rect.x
            rocket.rect.y = self.rect.y
            all_sprites_list.add(rocket)
            rocket_list.add(rocket)
    # -----------------------------------------------------------------------------
    class Player(pygame.sprite.Sprite):
        """The Player class"""
        def __init__(self):
            """load in avatar; could add feature to load in custom pic?"""
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = load_png('goon.png')
            self.rect.x, self.rect.y = player_x, player_y
            self.health = 100   
        def update(self):
            """player_x,_y are the players new coords for every next frame"""
            self.rect.x = player_x
            self.rect.y = player_y
        def shoot(self):
            bullet = Bullet(pygame.mouse.get_pos(), [player.rect.x, player.rect.y])
            bullet.rect.x = player.rect.x
            bullet.rect.y = player.rect.y
            all_sprites_list.add(bullet)
            bullet_list.add(bullet)
        def hit_vox(self):
            """play this when player got hit"""
            pygame.mixer.Sound(HITWAV).play()    
        def kill_vox(self):
            """play this when player just killed"""
            pygame.mixer.Sound(random.choice(KILLWAV)).play()
    # -----------------------------------------------------------------------------
    class Bullet(pygame.sprite.Sprite):
        """Class for bullets player, heli, tank.. shoot"""
        speed = 4.
        def __init__(self, target, instance):
            """target r x n y coords of well target; instance, well, the instnce shooting the bullet"""
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface([8, 6])
            self.image.fill(black)
            self.target_x, self.target_y = target[0], target[1]
            self.instance = instance
            self.rect = self.image.get_rect()    
        def update(self):
            """bullets flying their way"""
            distance = [self.target_x - self.instance[0], self.target_y - self.instance[1]]
            norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
            direction = [distance[0] / norm, distance[1] / norm]
            bullet_vector = [direction[0] * Bullet.speed, direction[1] * Bullet.speed]
            self.rect.x += bullet_vector[0]
            self.rect.y += bullet_vector[1]
    # -----------------------------------------------------------------------------
    class Footr(pygame.sprite.Sprite):
        """Basically a scoreboard, how2 raise its z-value, so that no overlap??"""
        def __init__(self):
            """setting up the scoreboard"""
            pygame.sprite.Sprite.__init__(self)
            self.font = pygame.font.Font(None, 24)
            self.text = self.font.render('{}'.format(NAME) + '    health: {}'.format(player.health) + '    cops shot: {}'.format(score) + '    tank: {}'.format(tank.health), 1, white)
            self.image = pygame.Surface([700, 50])
            self.rect = self.image.get_rect()
            self.rect.left, self.rect.top = 0, 350
            self.image.blit(self.text, (10, 10))
        def update(self):
            """updating health and score"""
            if len(tank_list) == 1:
                self.text = self.font.render('{}'.format(NAME) + '    health: {}'.format(player.health) + '    cops shot: {}'.format(score) + '    tank: {}'.format(tank.health), 1, white)
            elif len(heli_list) == 1:
                self.text = self.font.render('{}'.format(NAME) + '    health: {}'.format(player.health) + '    cops shot: {}'.format(score) + '    heli: {}'.format(heli.health), 1, white)
            self.image = pygame.Surface([700, 50])
            self.rect = self.image.get_rect()
            self.rect.left, self.rect.top = 0, 350
            self.image.blit(self.text, (10, 10))

    # INITIALIZATION --------------------------------------------------------------
    pygame.mixer.pre_init(frequency = 44100, size = -16, channels = 2, buffer = 4096)
    pygame.init(); print(pygame.mixer.get_init())
    pygame.mixer.music.load(random.choice(SONGS))
    sleepr(1)
    pygame.mixer.music.play()
    screen = pygame.display.set_mode([screen_w, screen_h])
    pygame.display.set_caption('CriminalDuty')
    NAME = ask(screen, 'Name')
    # Level 1 ---------------------------------------------------------------------
    screen.fill(black)
    screen.blit(pygame.font.Font(None, 96).render('Level 1', 1, white), (250, 150))
    pygame.display.flip()
    sleepr(5)
    # -----------------------------------------------------------------------------
    for i in range(num_cops):
        cop = Cop()
        cop_list.add(cop)
        all_sprites_list.add(cop)
    player = Player()
    player_list.add(player)
    tank = Tank()
    tank_list.add(tank)
    footr = Footr()
    all_sprites_list.add(player, tank, footr)

    # MAIN PROGRAM LOOP  ----------------------------------------------------------
    while not done:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display_box(screen, 'cops shot: {}'.format(score))
                sleepr(10)
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                player.shoot()
            # player movement
            if event.type == pygame.KEYDOWN:    
                if event.key == K_a:
                    move_player_x = -4
                elif event.key == K_d:
                    move_player_x = +4
                elif event.key == K_w:
                    move_player_y = -4
                elif event.key == K_s:
                    move_player_y = +4
            if event.type == pygame.KEYUP:
                if event.key == K_a:
                    move_player_x = 0
                elif event.key == K_d:
                    move_player_x = 0
                elif event.key == K_w:
                    move_player_y = 0
                elif event.key == K_s:
                    move_player_y = 0
                elif event.key == K_ESCAPE:
                    display_box(screen, 'cops shot: {}'.format(score))
                    sleepr(10)
                    done = True
        # --- Game logic
        all_sprites_list.update()
        # new player position
        player_x += move_player_x
        player_y += move_player_y
        # cops hitting player
        cop_hit_list = pygame.sprite.spritecollide(player, cop_list, True)
        for cop in cop_hit_list:
            player.hit_vox()
            player.health -= 5
        # tank overlapping with player
        tank_hit_list = pygame.sprite.spritecollide(player, tank_list, False)
        for tank in tank_hit_list:
            player.hit_vox()
            player.health -= 10
        # heli overlapping with player
        heli_hit_list = pygame.sprite.spritecollide(player, heli_list, False)
        for heli in heli_hit_list:
            player.hit_vox()
            player.health -= 10
        # cops that player shot
        for bullet in bullet_list:
            cop_kill_list = pygame.sprite.spritecollide(bullet, cop_list, True)
            for cop in cop_kill_list:
                player.kill_vox()
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)
                score += 1
            # bullets hitting tank
            tank_kill_list = pygame.sprite.spritecollide(bullet, tank_list, False)
            for hit in tank_kill_list:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)
                tank.health -= 10
            # bullets hitting heli
            heli_kill_list = pygame.sprite.spritecollide(bullet, heli_list, False)
            for hit in heli_kill_list:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)
                heli.health -= 10
            # bullets out of bounds get erased, u cant shoot when outta view
            if (bullet.rect.y < 0 or bullet.rect.y > screen_h - 50 or
                bullet.rect.x < -10 or bullet.rect.x > screen_w - 40):
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)
        # tanks canons aimed at player
        """canons out of bounds r not removed, u cant hide outta view, tank will still shoot ya"""
        for canon in canon_list:
            canon_hit_list = pygame.sprite.spritecollide(canon, player_list, False)
            for hit in canon_hit_list:
                player.hit_vox()
                canon_list.remove(canon)
                all_sprites_list.remove(canon)
                player.health -= 10
        # helis rockets aimed at player
        """rockets out of bounds r not removed, u cant hide outta view, heli will still shoot ya"""
        for rocket in rocket_list:
            rocket_hit_list = pygame.sprite.spritecollide(rocket, player_list, False)
            for hit in rocket_hit_list:
                player.hit_vox()
                rocket_list.remove(rocket)
                all_sprites_list.remove(rocket)
                player.health -= 15
        # revive cops++ when all got shot 
        if len(cop_list) == 0:
            num_cops += 1
            for i in range(num_cops):
                cop = Cop()
                cop_list.add(cop)
                all_sprites_list.add(cop)
        # player dead
        if player.health <= 0:
            display_box(screen, 'dead.. total cops shot: {}'.format(score))
            sleepr(10) 
            done = True
        # A.C.A.B. first endgegner dead
        if tank.health <= 0:
            if len(heli_list) == 0:
                score += 100
                tank_list.remove(tank)
                all_sprites_list.remove(tank)
                # Level 2 ---------------------------------------------------------------------
                screen.fill(black)
                screen.blit(pygame.font.Font(None, 96).render('Level 2', 1, white), (250, 150))
                pygame.display.flip()
                sleepr(5)
                # -----------------------------------------------------------------------------
                heli = Heli()
                heli_list.add(heli)
                all_sprites_list.add(heli)
            # A.C.A.B. player won
            if heli.health <= 0:
                score += 150
                display_box(screen, 'A.C.A.B! total cops shot: {}'.format(score))
                sleepr(10) 
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
