import pygame
from const import *
from Background_class import *
from Player_class import *
from Enemy_class import *
import datetime
import json
from Control_class import *
import random
from Bonus_class import Bonus
from Enemy_class import Enemy
from Explosion_class import Explosion
from Menu import Menu

class Game():

    apparition_rate = datetime.datetime.now() + datetime.timedelta(seconds=randint(0, 7))

    def __init__(self):
        super().__init__() 
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((1080, 1920), pygame.FULLSCREEN | pygame.SCALED)
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        if len(self.joysticks) > 1:
            print("too many joysticks, plug only one. Bouffon va")
            exit
        self.clock = pygame.time.Clock()

        with open("attributes.json", "r") as f:
            data = json.loads(f.read())
            self.playerAttributes = data["player"]
            self.enemiesAttributes = data["enemies"]
            self.bonusAttributes = data["bonus"]   
        
        with open("score_board.json", "r") as f:
            self.score_board = json.loads(f.read())
        self.reset()

        self.score_max = 0
        for item in self.score_board:
            if len(self.score_board[item]) > 0:
                if max(self.score_board[item]) > self.score_max:
                    self.score_max = max(self.score_board[item])
                    self.school_score_max = item


        #Setting up Fonts
        self.font = pygame.font.SysFont("Verdana", 30)
        self.font_small = pygame.font.SysFont("Verdana", 20)
        self.waiting_verre = [self.font.render("Placer un verre", True, BLACK),
                              self.font.render("pour demarrer", True, BLACK)]
        self.font_score = pygame.font.Font("src/fonts/" + SCORE_FONT, SCORE_SIZE)
        self.menu = Menu()

        self.reset()

    def reset(self):
        self.state = GAME_STATE.MENU
        self.running = False
        self.score = 0
        self.ended = False

        if len(self.joysticks) > 0:
            self.player = Player(self.playerAttributes,self.joysticks[0])
            self.control = Control(self.joysticks[0])
        else:
            self.player = Player(self.playerAttributes,None)
            self.control = Control(None)
        SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_window_size()
        self.background = Background(SCREEN_WIDTH)
        self.playerBullets = pygame.sprite.Group()
        self.enemyBullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()



    def check_exit(self):
        if not pygame.get_init():
            return False
        if self.control.escape():
            pygame.quit()
            return True

        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
        return False

    def display_waiting(self):
        self.screen.blit(self.waiting_verre[0], 
                         ((SCREEN_WIDTH - self.waiting_verre[0].get_rect().width) / 2,
                         SCREEN_HEIGHT / 2 + 15))
        self.screen.blit(self.waiting_verre[1], 
                         ((SCREEN_WIDTH - self.waiting_verre[0].get_rect().width) / 2,
                         SCREEN_HEIGHT / 2 - 15))

    def render(self):
        self.background.render(self.screen)

        self.menu.render(self.screen)

        self.player.blit(self.screen)
            
        if not self.running:
            self.player.blit(self.screen)
            self.display_waiting()
            return

        for enemy in self.enemies:
            enemy.render(self.screen)

        for bullet in self.playerBullets:
            bullet.render(self.screen)

        for bullet in self.enemyBullets:
            bullet.render(self.screen)

        self.player.render_health_bar(self.screen)
        self.display_score = self.font_score.render("SCORE: " + str(self.score), True, BLACK)
        self.screen.blit(self.display_score, ((SCREEN_WIDTH / 2) - (self.display_score.get_rect().width / 2), 20))

        self.player.render(self.screen)
        return

    def exit_requested(self):
        return not pygame.get_init()

    def update(self):
        if not self.running:
            if self.control.shoot():
                self.running = True

        if self.state == GAME_STATE.MENU:
            if self.control.shoot():
                self.player.set_player_school(self.menu.chose_school("SHOOT"))
                self.state = GAME_STATE.IDLE
            if self.control.up():
                self.menu.chose_school("UP")
            if self.control.down():
                self.menu.chose_school("DOWN")
            if self.control.left():
                self.menu.chose_school("LEFT")
            if self.control.right():
                self.menu.chose_school("RIGHT")

        self.background.animate(self.state != GAME_STATE.IDLE)
        self.background.update()

        if self.running:
            for bullet in self.playerBullets:
                bullet.update()

            for bullet in self.enemyBullets:
                bullet.update()

            for enemy in self.enemies:
                enemy.update(self.enemyBullets)

            self.player.update(self.playerBullets)
            self.player.render_health_bar(self.screen)

            for hit in pygame.sprite.spritecollide(self.player, self.enemyBullets, False):
                self.player.hit(hit.damage)
                hit.kill()

            if self.player.is_alive() and len(pygame.sprite.spritecollide(self.player, self.enemies, False)) > 0:
                self.player.explode()

            for enemy in self.enemies:
                for hit in pygame.sprite.spritecollide(enemy, self.playerBullets, False):
                    self.score += enemy.hit()
                    hit.kill()
                if enemy.passed:
                    self.player.hit(10)
                    enemy.reset()

            if Game.apparition_rate <= datetime.datetime.now():
                self.enemies.add(Enemy())
                Game.apparition_rate += datetime.timedelta(seconds=randint(0, 7))

            if(len(self.enemies) == 0):
                self.enemies.add(Enemy())

        if not self.player.is_alive():
            for enemy in self.enemies:
                enemy.kill()
            for bullet in self.enemyBullets:
                bullet.kill()
            for bullet in self.playerBullets:
                bullet.kill()
            self.score_board[self.player.school].append(self.score)
            self.store_score()
            self.player.alive = True
            self.ended = True
            #self.store_score()
            self.state = GAME_STATE.ENDED
            self.menu.reset()
            return

    def loop(self):
        if self.check_exit():
            return

        # fill the screen with a color to wipe away anything from last frame
        self.update()
        # RENDER YOUR GAME HERE
        self.render()

        # flip() the display to put your work on screen
        pygame.display.flip()
    
        self.clock.tick(FPS)  # limits FPS to 60

    def store_score(self):
        if self.score_max < self.score:
            self.score_max = self.score
            self.school_score_max = self.player.school
        with open("score_board.json", "w") as f:
            f.write(json.dumps(self.score_board))

    def spawn(self):
        if self.state==GAME_STATE.ENDED or self.state==GAME_STATE.ENDING:
            return                    
 #           if Game.apparition_rate <= datetime.datetime.now():
 #               self.enemies.add(Enemy(random.choice(list(self.enemiesAttributes.values()))))
 #               Game.apparition_rate += datetime.timedelta(seconds=randint(0, 7))
        if(len(self.enemies) == 0 and self.player.is_alive()):
            self.enemies.add(Enemy(random.choice(list(self.enemiesAttributes.values()))))

        if Game.apparition_rate_bonus <= datetime.datetime.now():
            bonus = random.choices(list(self.bonusAttributes.values()), [val["weight"] for val in self.bonusAttributes.values()], k=1)[0]                
            self.bonus.add(Bonus(bonus))
            Game.apparition_rate_bonus += datetime.timedelta(seconds=random.randint(0, 7))

    def collisions(self):
        for bonus in self.bonus:
            bonus.update()
        for hit in pygame.sprite.spritecollide(self.player, self.enemyBullets, False, pygame.sprite.collide_mask): # type: ignore
            self.player.hit(hit)

        for bonus in pygame.sprite.spritecollide(self.player, self.bonus, False, pygame.sprite.collide_mask): # type: ignore
            self.player.add_bonus(bonus)
            bonus.kill()

        if not self.player.is_dead():
            for enemy in pygame.sprite.spritecollide(self.player, self.enemies, False, pygame.sprite.collide_mask): # type: ignore
                self.explosions.add(Explosion(self.player.pos))
                self.player.receive_damage(self.player.health)
                enemy.kill()
                break                    

        for enemy in self.enemies:
            for hit in pygame.sprite.spritecollide(enemy, self.playerBullets, False,  pygame.sprite.collide_mask): # type: ignore
                enemy.hit(hit)
            if enemy.passed():
                self.player.receive_damage(10)
                enemy.kill()
            if enemy.is_dead():
                self.explosions.add(Explosion(enemy.pos))
                enemy.kill()
                self.score += enemy.points